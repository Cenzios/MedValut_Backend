from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

from app.core.database import get_db
from app.modules.auth.services import AuthService
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    RequestOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
)
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Dependency to get current authenticated user"""
    auth_service = AuthService(db)
    return await auth_service.get_current_user(credentials.credentials)


# -------------------------------
# User Registration
# -------------------------------
@router.post("/register", summary="User Registration", response_model=dict)
async def register_user(
    dto: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    response = await auth_service.register_user(dto)
    
    if response["success"]:
        return success_response(message=response["message"], data=response["data"])
    else:
        return error_response(response["message"], 500)


# -------------------------------
# User Login
# -------------------------------
@router.post("/login", summary="User Login", response_model=dict)
async def login_user(
    request: Request,
    dto: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user_agent = request.headers.get("user-agent", "Unknown")
    ip_address = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or getattr(request.client, "host", "Unknown")

    auth_service = AuthService(db)
    response = await auth_service.login_user(dto, user_agent, ip_address)

    if response["success"]:
        return success_response(message=response["message"], data=response["data"])
    else:
        return error_response(response["message"], 500)


# -------------------------------
# Request OTP
# -------------------------------
@router.post("/request-otp", summary="Request OTP", response_model=dict)
async def request_otp(dto: RequestOTPRequest, db: AsyncSession = Depends(get_db)):
    
    auth_service = AuthService(db)
    response = await auth_service.request_otp(dto)
    
    if response["success"]:
        return success_response(message=response["message"], data=response["data"])
    else:
        return error_response(response["message"], 500)


# -------------------------------
# Verify OTP
# -------------------------------
@router.post("/verify-otp", summary="Verify OTP", response_model=dict)
async def verify_otp(dto: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    
    auth_service = AuthService(db)
    response = await auth_service.verify_otp(dto)
    
    if response["success"]:
        return success_response(message=response["message"], data=response["data"])
    else:
        return error_response(response["message"], 400)


# -------------------------------
# Refresh Token
# -------------------------------
@router.post("/refresh", summary="Refresh Access Token", response_model=dict)
async def refresh_token(dto: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    
    auth_service = AuthService(db)
    response = await auth_service.refresh_access_token(dto.refresh_token)
    
    if response["success"]:
        return success_response(message=response["message"], data=response["data"])
    else:
        return error_response(response["message"], 401)


# -------------------------------
# Get User Data
# -------------------------------
@router.get("/me", summary="Get Auth User Data", response_model=dict)
async def get_auth_user_data(request: Request, db: AsyncSession = Depends(get_db)):
    
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return error_response("Authorization token missing", 401)

    auth_service = AuthService(db)
    response = await auth_service.get_current_user(token)
    
    if response["success"]:
        return success_response(message="User data retrieved successfully", data=response["data"].dict())
    else:
        return error_response(response["message"], 401)


# -------------------------------
# Logout
# -------------------------------
@router.post("/logout", summary="Logout", response_model=dict)
async def logout_user(
    dto: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    response = await auth_service.logout_user(dto)
    if response["success"]:
        return success_response(message=response["message"], data=None)
    else:
        return error_response(response["message"], 500)


# -------------------------------
# Logout from All Devices
# -------------------------------
@router.post("/logout-all", summary="Logout from All Devices", response_model=dict)
async def logout_all_devices(reqest: Request, db: AsyncSession = Depends(get_db)):
    
    current_user_id = reqest.state.user_id 
    
    auth_service = AuthService(db)
    response = await auth_service.logout_all_devices(current_user_id)
    if response["success"]:
        return success_response(message=response["message"], data=None)
    else:
        return error_response(response["message"], 500)


