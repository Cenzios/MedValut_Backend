# app/modules/user/repositories.py
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_

from app.modules.user.models import User, OTPVerification, RefreshToken
from app.modules.auth.schemas import OTPType
from app.core.config import settings
from app.utils.logger import log_info, log_error


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # -------------------- User --------------------
    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            query = select(User).where(User.email == email, User.is_active == True)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except:
            log_error(f"Error getting user by email {email}")
            return None

    async def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            query = select(User).where(User.id == user_id, User.is_active == True )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except:
            log_error(f"Error getting user by id {user_id}")
            return None
        
        
    async def get_by_nic(self, nic: str) -> Optional[User]:
        try:
            query = select(User).where(User.nic == nic, User.is_active == True )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except:
            log_error(f"Error getting user by nic {nic}")
            return None

    async def create_user(self, user: User) -> Optional[User]:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            log_info(f"Error creating user: {e}")
            log_error(f"Error creating user with email {user.email}")
            return None
        
    # -------------------- OTP --------------------
    async def create_otp(
        self,
        email: str | None,
        otp_code: str,
        otp_type: OTPType,
        otp_reference: str,
        expires_minutes: int = 5,
    ) -> OTPVerification | None:
        try:
            # Deactivate existing OTPs for same identifier
            if email:
                query = (
                    update(OTPVerification)
                    .where(
                        and_(
                            OTPVerification.email == email,
                            OTPVerification.otp_type == otp_type.value,
                            OTPVerification.otp_reference == otp_reference,
                            OTPVerification.is_used == False,
                        )
                    )
                    .values(is_used=True)
                )
                await self.db.execute(query)

            otp_verification = OTPVerification(
                email=email,
                otp_code=otp_code,
                otp_reference=otp_reference,
                otp_type=otp_type.value,
                expires_at=datetime.utcnow() + timedelta(minutes=expires_minutes),
            )
            self.db.add(otp_verification)
            await self.db.commit()
            return otp_verification
        except:
            log_error(f"Error creating OTP for email {email}")
            return None

    async def get_active_otp(
        self, email: str, otp_type: OTPType
    ) -> Optional[OTPVerification]:
        try:
            
            if email:
                query = (
                    select(OTPVerification)
                    .where(
                        and_(
                            OTPVerification.email == email,
                            OTPVerification.otp_type == otp_type.value,
                            OTPVerification.is_used == False,
                            OTPVerification.expires_at > datetime.utcnow(),
                        )
                    )
                    .order_by(OTPVerification.created_at.desc())
                )
                result = await self.db.execute(query)
                return result.scalar_one_or_none()
            return None
        except:
            log_error(f"Error getting active OTP for email {email}")
            return None

    async def mark_otp_used(self, otp_id: int) -> bool:
        try:
            query = (
                update(OTPVerification)
                .where(OTPVerification.id == otp_id)
                .values(is_used=True, used_at=datetime.utcnow())
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error marking OTP {otp_id} as used")
            return False

    # -------------------- Verification flags --------------------
    async def mark_email_verified(self, email: str) -> bool:
        try:
            query = (
                update(User)
                .where(User.email == email)
                .values(is_email_verified=True, updated_at=datetime.utcnow())
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error marking email verified for user: {email}")
            return False

    # -------------------- Login attempts --------------------
    async def increment_login_attempts(self, user_id: int) -> bool:
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False

            new_attempts = user.login_attempts + 1
            locked_until = None
            if new_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                locked_until = datetime.utcnow() + timedelta(
                    minutes=settings.LOCKOUT_DURATION_MINUTES
                )

            query = (
                update(User)
                .where(User.id == user_id)
                .values(
                    login_attempts=new_attempts,
                    locked_until=locked_until,
                    updated_at=datetime.utcnow(),
                )
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error incrementing login attempts for user {user_id}")
            return False

    async def reset_login_attempts(self, user_id: int) -> bool:
        try:
            query = (
                update(User)
                .where(User.id == user_id)
                .values(login_attempts=0, locked_until=None, updated_at=datetime.utcnow())
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error resetting login attempts for user {user_id}")
            return False

    async def update_last_login(self, user_id: int) -> bool:
        try:
            query = (
                update(User)
                .where(User.id == user_id)
                .values(last_login=datetime.utcnow(), updated_at=datetime.utcnow())
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error updating last login for user {user_id}")
            return False

    # -------------------- Refresh tokens --------------------
    async def store_refresh_token(
        self,
        user_id: int,
        token: str,
        user_agent: str = None,
        ip_address: str = None,
        expires_delta=None,
    ) -> bool:
        try:
            if expires_delta is None:
                from datetime import timedelta
                from app.core.config import settings

                expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

            refresh_token_record = RefreshToken(
                user_id=user_id,
                token=token,
                expires_at=datetime.utcnow() + expires_delta,
                user_agent=user_agent,
                ip_address=ip_address,
            )
            self.db.add(refresh_token_record)
            await self.db.commit()
            return True
        except:
            log_error(f"Error storing refresh token for user {user_id}")
            return False

    async def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        try:
            query = select(RefreshToken).where(RefreshToken.token == token)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except:
            log_error(f"Error getting refresh token {token}")
            return None

    async def update_refresh_token_usage(self, token_id: int) -> bool:
        try:
            query = (
                update(RefreshToken)
                .where(RefreshToken.id == token_id)
                .values(last_used_at=datetime.utcnow())
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error updating usage for refresh token {token_id}")
            return False

    async def deactivate_refresh_token(self, token: str) -> bool:
        try:
            query = (
                update(RefreshToken)
                .where(RefreshToken.token == token)
                .values(is_active=False)
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error deactivating refresh token {token}")
            return False

    async def deactivate_all_refresh_tokens(self, user_id: int) -> bool:
        try:
            query = (
                update(RefreshToken)
                .where(RefreshToken.user_id == user_id)
                .values(is_active=False)
            )
            await self.db.execute(query)
            await self.db.commit()
            return True
        except:
            log_error(f"Error deactivating all refresh tokens for user {user_id}")
            return False