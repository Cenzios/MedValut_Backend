from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Union
from datetime import datetime
from enum import Enum


class OTPType(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    LOGIN = "login"


# Request schemas
class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password with at least 8 characters")
    confirm_password: str = Field(..., min_length=8, max_length=100, description="Confirm password (must match password)")
    full_name: str = Field(..., max_length=255, description="User's full name")
    nic: str = Field(..., max_length=20, description="User NIC / national ID")

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1)
    push_id: Optional[str] = Field(None, description="Push notification identifier")

    @validator("email")
    def validate_identifier(cls, v):
        if "@" not in v and not any(char.isdigit() for char in v):
            raise ValueError("Identifier must be a valid email or phone number")
        return v


class RequestOTPRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    otp_type: OTPType


class VerifyOTPRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    otp_code: str = Field(..., min_length=4, max_length=10)
    otp_reference: str = Field(..., min_length=6, max_length=6)
    otp_type: OTPType   


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)
    user_id: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)

    @validator("new_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)

    @validator("new_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


# Response schemas
class UserProfile(BaseModel):
    id: int
    email: str
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    gender_id: Optional[int]
    is_active: bool
    is_verified: bool
    email_verified: bool
    phone_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    profile_picture_url: Optional[str]
    bio: Optional[str]
    subscription_plan_id: Optional[int]
    subscription_start_date: Optional[datetime]
    subscription_end_date: Optional[datetime]
    height: Optional[float]
    weight: Optional[float]
    blood_type_id: Optional[int]
    smoking_level_id: Optional[int]
    alcohol_level_id: Optional[int]
    exercise_level_id: Optional[int]

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginResponse(BaseModel):
    user: UserProfile
    tokens: TokenResponse
    message: str = "Login successful"


class RegisterResponse(BaseModel):
    user_id: int
    email: str
    phone_number: Optional[str]
    message: str = "Registration successful. Please verify your email/phone."
    verification_required: bool = True


class OTPResponse(BaseModel):
    message: str
    expires_in_minutes: int = 5
    can_resend_after_seconds: int = 60


class VerifyOTPResponse(BaseModel):
    message: str
    is_verified: bool
    user_id: Optional[int] = None


class AuthDataResponse(BaseModel):
    user: UserProfile
    is_authenticated: bool
    token_valid: bool


class MessageResponse(BaseModel):
    message: str
    success: bool = True
