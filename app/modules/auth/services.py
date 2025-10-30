from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Dict, Any

from app.modules.user.models import User
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    RequestOTPRequest,
    VerifyOTPRequest,
    OTPType,
    RefreshTokenRequest,
)
from app.modules.user.repositories import UserRepository
from app.utils.jwt_utils import JWTUtils
from app.utils.password_utils import PasswordUtils
from app.utils.email_utils import EmailUtils
from app.utils.sms_utils import SMSUtils
from app.utils.action_logger import log_action
from app.core.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    # -------------------- Register --------------------
    async def register_user(self, dto: RegisterRequest) -> Dict[str, Any]:
        # Check if user exists
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # Hash password
        hashed_password = PasswordUtils.hash_password(dto.password)
        if not hashed_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to hash password",
            )

        # Create user
        new_user = User(
            email=dto.email,
            password_hash=hashed_password,
            full_name=dto.full_name,
            nic=dto.nic,
            is_active=True,
            email_verified=False,
            phone_verified=False,
        )

        new_user = await self.user_repo.create_user(new_user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )

        # Create OTP
        otp_code = JWTUtils.generate_otp(6)
        otp_reference = JWTUtils.generate_otp_reference(6)

        otp_record = await self.user_repo.create_otp(
            email=new_user.email,
            otp_code=otp_code,
            otp_type=OTPType.EMAIL_VERIFICATION,
            otp_reference=otp_reference,
            expires_minutes=5,
        )

        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create verification OTP",
            )

        # Send email
        is_sent = await EmailUtils.send_otp_email(new_user.email, otp_code, "email_verification")
        if not is_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email",
            )

        # Log action
        await log_action(new_user.id, "user_registered", {"email": new_user.email})

        new_user = User.from_orm(new_user)
        
        return {
            "success": True,
            "message": "Registration successful",
            "data": {"user": new_user},
        }

    # -------------------- Login --------------------
    async def login_user(self, dto: LoginRequest, user_agent: str = None, ip_address: str = None) -> Dict[str, Any]:
        # Verify user credentials
        user = await self.user_repo.get_by_email(dto.email)
        
        if not user or not PasswordUtils.verify_password(dto.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or account is deactivated",
            )

        # Reset login attempts and update last login
        await self.user_repo.reset_login_attempts(user.id)
        await self.user_repo.update_last_login(user.id)

        # Generate tokens
        token_data = {"sub": str(user.id), "email": user.email}
        expires_delta = timedelta(days=30) 
        access_token = JWTUtils.create_access_token(token_data)
        refresh_token = JWTUtils.create_refresh_token(token_data, expires_delta)
        await self.user_repo.store_refresh_token(user.id, refresh_token, user_agent, ip_address, expires_delta)

        tokens = {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}

        # Log action
        await log_action(user.id, "user_login", {"ip_address": ip_address, "user_agent": user_agent})
        
        user.tokens = tokens
        user = User.from_orm(user)
        
        return {"success": True, "message": "Login successful", "data": {"user": user}}

    # -------------------- Request OTP --------------------
    async def request_otp(self, dto: RequestOTPRequest) -> Dict[str, Any]:
        # Check if user exists
        user = await self.user_repo.get_by_email(dto.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if OTP is already sent recently
        existing_otp = await self.user_repo.get_active_otp(dto.email, dto.otp_type)
        if existing_otp and (datetime.utcnow() - existing_otp.created_at).total_seconds() < 60:
            raise HTTPException(status_code=429, detail="OTP already sent recently")

        # Create OTP
        otp_code = JWTUtils.generate_otp(6)
        otp_reference = JWTUtils.generate_otp_reference(6)
        
        # Create and save OTP record
        otp_record = await self.user_repo.create_otp(
            email=user.email,
            otp_code=otp_code,
            otp_type=dto.otp_type,
            otp_reference=otp_reference
        )
        if not otp_record:
            raise HTTPException(status_code=500, detail="Failed to create OTP")

        # Send OTP via email
        is_sent = await EmailUtils.send_otp_email(user.email, otp_code, dto.otp_type.value)
        if not is_sent:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
        
        # Log action
        await log_action(user.id, "user_request_otp", {"email": user.email, "otp_type": dto.otp_type.value})

        return {"success": True, "message": f"OTP sent to {user.email}", "data": {"otp_reference": otp_reference}}

    # -------------------- Verify OTP --------------------
    async def verify_otp(self, dto: VerifyOTPRequest) -> Dict[str, Any]:
        # Check if OTP is valid
        otp_record = await self.user_repo.get_active_otp(dto.email, dto.otp_type)
        if not otp_record or otp_record.otp_code != dto.otp_code or otp_record.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")

        await self.user_repo.mark_otp_used(otp_record.id)

        if dto.otp_type == OTPType.EMAIL_VERIFICATION and dto.email:
            await self.user_repo.mark_email_verified(dto.email)
        
        return {"success": True, "message": "OTP verified successfully", "data": None}

    # -------------------- Refresh token --------------------
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = JWTUtils.verify_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        stored_token = await self.user_repo.get_refresh_token(refresh_token)
        if not stored_token or not stored_token.is_active:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        await self.user_repo.update_refresh_token_usage(stored_token.id)
        new_access_token = JWTUtils.create_access_token({"sub": str(user.id), "email": user.email})
        await log_action(user.id, "token_refreshed", {})

        tokens = {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}
        
        return {"success": True, "message": "Token refreshed successfully", "data": tokens}

    # -------------------- Get current user --------------------
    async def get_current_user(self, token: str) -> Dict[str, Any]:
        payload = JWTUtils.verify_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        
        user = User.from_orm(user)

        return {"success": True, "message": "User retrieved successfully", "data": user}

    # -------------------- Logout --------------------
    async def logout_user(self, dto: RefreshTokenRequest) -> Dict[str, Any]:
        await self.user_repo.deactivate_refresh_token(dto.refresh_token)
        await log_action(dto.user_id, "user_logout", {})
        return {"success": True, "message": "Logged out successfully", "data": None}

    async def logout_all_devices(self, user_id: int) -> Dict[str, Any]:
        await self.user_repo.deactivate_all_refresh_tokens(user_id)
        await log_action(user_id, "logout_all_devices", {})
        return {"success": True, "message": "Logged out from all devices", "data": None}