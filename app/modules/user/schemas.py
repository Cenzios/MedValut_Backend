# from pydantic import BaseModel, EmailStr, Field, field_validator
# from typing import Optional
# from datetime import datetime
# from enum import Enum


# # ---------------------------
# # Enums
# # ---------------------------
# class OTPType(str, Enum):
#     EMAIL_VERIFICATION = "email_verification"
#     PASSWORD_RESET = "password_reset"
#     LOGIN = "login"


# # ---------------------------
# # Request Schemas
# # ---------------------------
# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str = Field(..., min_length=8, max_length=100)
#     confirm_password: str = Field(..., min_length=8, max_length=100)
#     full_name: str = Field(..., max_length=255)
#     nic: str = Field(..., max_length=20)

#     @field_validator("password")
#     def validate_password(cls, v: str) -> str:
#         if not any(char.isdigit() for char in v):
#             raise ValueError("Password must contain at least one digit")
#         if not any(char.isupper() for char in v):
#             raise ValueError("Password must contain at least one uppercase letter")
#         if not any(char.islower() for char in v):
#             raise ValueError("Password must contain at least one lowercase letter")
#         return v

#     @field_validator("confirm_password")
#     def passwords_match(cls, v: str, info) -> str:
#         if "password" in info.data and v != info.data["password"]:
#             raise ValueError("Passwords do not match")
#         return v


# class LoginRequest(BaseModel):
#     email: str = Field(..., min_length=3, max_length=255)
#     password: str = Field(..., min_length=1)
#     push_id: Optional[str] = None

#     @field_validator("email")
#     def validate_identifier(cls, v: str) -> str:
#         if "@" not in v and not any(char.isdigit() for char in v):
#             raise ValueError("Identifier must be a valid email or phone number")
#         return v


# class RequestOTPRequest(BaseModel):
#     email: str = Field(..., min_length=3, max_length=255)
#     otp_type: OTPType


# class VerifyOTPRequest(BaseModel):
#     email: str = Field(..., min_length=3, max_length=255)
#     otp_code: str = Field(..., min_length=4, max_length=10)
#     otp_reference: str = Field(..., min_length=6, max_length=6)


# class RefreshTokenRequest(BaseModel):
#     refresh_token: str = Field(..., min_length=1)


# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr


# class ResetPasswordRequest(BaseModel):
#     token: str = Field(..., min_length=1)
#     new_password: str = Field(..., min_length=8, max_length=100)

#     @field_validator("new_password")
#     def validate_password(cls, v: str) -> str:
#         if not any(char.isdigit() for char in v):
#             raise ValueError("Password must contain at least one digit")
#         if not any(char.isupper() for char in v):
#             raise ValueError("Password must contain at least one uppercase letter")
#         if not any(char.islower() for char in v):
#             raise ValueError("Password must contain at least one lowercase letter")
#         return v


# class ChangePasswordRequest(BaseModel):
#     current_password: str = Field(..., min_length=1)
#     new_password: str = Field(..., min_length=8, max_length=100)

#     @field_validator("new_password")
#     def validate_password(cls, v: str) -> str:
#         if not any(char.isdigit() for char in v):
#             raise ValueError("Password must contain at least one digit")
#         if not any(char.isupper() for char in v):
#             raise ValueError("Password must contain at least one uppercase letter")
#         if not any(char.islower() for char in v):
#             raise ValueError("Password must contain at least one lowercase letter")
#         return v


# # ---------------------------
# # Response Schemas
# # ---------------------------
# class UserProfile(BaseModel):
#     id: int
#     email: str
#     phone_number: Optional[str]
#     full_name: str
#     nic: str
#     is_active: bool
#     email_verified: bool
#     phone_verified: bool
#     last_login: Optional[datetime]
#     created_at: datetime
#     updated_at: datetime

#     model_config = {"from_attributes": True}


# class TokenResponse(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#     expires_in: int


# class LoginResponse(BaseModel):
#     user: UserProfile
#     tokens: TokenResponse
#     message: str = "Login successful"


# class RegisterResponse(BaseModel):
#     user_id: int
#     email: str
#     phone_number: Optional[str]
#     message: str = "Registration successful. Please verify your email/phone."
#     verification_required: bool = True


# class OTPResponse(BaseModel):
#     message: str
#     expires_in_minutes: int = 5
#     can_resend_after_seconds: int = 60


# class VerifyOTPResponse(BaseModel):
#     message: str
#     is_verified: bool
#     user_id: Optional[int] = None


# class AuthDataResponse(BaseModel):
#     user: UserProfile
#     is_authenticated: bool
#     token_valid: bool


# class MessageResponse(BaseModel):
#     message: str
#     success: bool = True