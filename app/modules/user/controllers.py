# from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional, List

# from app.core.database import get_db
# from app.modules.user.services import UserService
# from app.modules.user.schemas import (
#     UserUpdate,
#     UserProfileUpdate,
#     UserHealthUpdate,
#     UserContactUpdate,
#     ChangePasswordRequest,
#     UserResponse,
#     UserProfileResponse,
#     UserHealthResponse,
#     UserStatsResponse,
#     UserActivityResponse,
#     UserListResponse,
#     DeactivateAccountRequest,
# )
# from app.modules.auth.controllers import get_current_user_dependency
# from app.modules.user.models import User
# from app.utils.response import success_response, error_response, not_found
# from app.utils.logger import log_info, log_error

# router = APIRouter(prefix="/user", tags=["User Management"])


# # -------------------------------
# # Get Current User Profile
# # -------------------------------
# @router.get("/profile", summary="Get User Profile", response_model=dict)
# async def get_user_profile(
#     current_user: User = Depends(get_current_user_dependency),
# ):
#     """
#     Get current user's profile information
#     """
#     try:
#         user_profile = UserProfileResponse.model_validate(current_user)
#         return success_response(
#             message="Profile retrieved successfully", data=user_profile.dict()
#         )
#     except Exception as e:
#         log_error(f"Error getting user profile: {str(e)}")
#         return error_response("Failed to get profile", 500)


# # -------------------------------
# # Update User Profile
# # -------------------------------
# @router.put("/profile", summary="Update User Profile", response_model=dict)
# async def update_user_profile(
#     profile_data: UserProfileUpdate,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Update user profile information

#     - **first_name**: User's first name
#     - **last_name**: User's last name
#     - **bio**: User's bio/description
#     - **date_of_birth**: Date of birth
#     - **gender_id**: Gender ID reference
#     """
#     try:
#         user_service = UserService(db)
#         updated_user = await user_service.update_user_profile(
#             current_user.id, profile_data
#         )

#         user_profile = UserProfileResponse.model_validate(updated_user)
#         log_info(f"Profile updated for user: {current_user.email}")
#         return success_response(
#             message="Profile updated successfully", data=user_profile.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error updating user profile: {str(e)}")
#         return error_response("Failed to update profile", 500)


# # -------------------------------
# # Get User Health Data
# # -------------------------------
# @router.get("/health", summary="Get User Health Data", response_model=dict)
# async def get_user_health(
#     current_user: User = Depends(get_current_user_dependency),
# ):
#     """
#     Get current user's health information
#     """
#     try:
#         user_health = UserHealthResponse.model_validate(current_user)
#         return success_response(
#             message="Health data retrieved successfully", data=user_health.dict()
#         )
#     except Exception as e:
#         log_error(f"Error getting user health data: {str(e)}")
#         return error_response("Failed to get health data", 500)


# # -------------------------------
# # Update User Health Data
# # -------------------------------
# @router.put("/health", summary="Update User Health Data", response_model=dict)
# async def update_user_health(
#     health_data: UserHealthUpdate,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Update user health information

#     - **height**: Height in centimeters
#     - **weight**: Weight in kilograms
#     - **blood_type_id**: Blood type ID reference
#     - **smoking_level_id**: Smoking level ID reference
#     - **alcohol_level_id**: Alcohol consumption level ID reference
#     - **exercise_level_id**: Exercise level ID reference
#     """
#     try:
#         user_service = UserService(db)
#         updated_user = await user_service.update_user_health_data(
#             current_user.id, health_data
#         )

#         user_health = UserHealthResponse.model_validate(updated_user)
#         log_info(f"Health data updated for user: {current_user.email}")
#         return success_response(
#             message="Health data updated successfully", data=user_health.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error updating user health data: {str(e)}")
#         return error_response("Failed to update health data", 500)


# # -------------------------------
# # Update Contact Information
# # -------------------------------
# @router.put("/contact", summary="Update Contact Information", response_model=dict)
# async def update_user_contact(
#     contact_data: UserContactUpdate,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Update user contact information

#     - **phone_number**: Phone number
#     """
#     try:
#         user_service = UserService(db)
#         updated_user = await user_service.update_user_contact(
#             current_user.id, contact_data
#         )

#         user_profile = UserProfileResponse.model_validate(updated_user)
#         log_info(f"Contact information updated for user: {current_user.email}")
#         return success_response(
#             message="Contact information updated successfully", data=user_profile.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error updating user contact: {str(e)}")
#         return error_response("Failed to update contact information", 500)


# # -------------------------------
# # Change Password
# # -------------------------------
# @router.put("/password", summary="Change Password", response_model=dict)
# async def change_password(
#     password_data: ChangePasswordRequest,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Change user password

#     - **current_password**: Current password
#     - **new_password**: New password (must meet security requirements)
#     """
#     try:
#         user_service = UserService(db)
#         success = await user_service.change_password(current_user.id, password_data)

#         if success:
#             log_info(f"Password changed for user: {current_user.email}")
#             return success_response(
#                 message="Password changed successfully", data={"password_changed": True}
#             )
#         else:
#             return error_response("Failed to change password", 500)
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error changing password: {str(e)}")
#         return error_response("Failed to change password", 500)


# # -------------------------------
# # Update Profile Picture
# # -------------------------------
# @router.put("/profile-picture", summary="Update Profile Picture", response_model=dict)
# async def update_profile_picture(
#     picture_url: str,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Update user profile picture

#     - **picture_url**: URL of the uploaded profile picture
#     """
#     try:
#         user_service = UserService(db)
#         updated_user = await user_service.update_profile_picture(
#             current_user.id, picture_url
#         )

#         user_profile = UserProfileResponse.model_validate(updated_user)
#         log_info(f"Profile picture updated for user: {current_user.email}")
#         return success_response(
#             message="Profile picture updated successfully", data=user_profile.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error updating profile picture: {str(e)}")
#         return error_response("Failed to update profile picture", 500)


# # -------------------------------
# # Get User Statistics
# # -------------------------------
# @router.get("/stats", summary="Get User Statistics", response_model=dict)
# async def get_user_stats(
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Get user account statistics and information
#     """
#     try:
#         user_service = UserService(db)
#         stats = await user_service.get_user_stats(current_user.id)

#         return success_response(
#             message="User statistics retrieved successfully", data=stats.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error getting user statistics: {str(e)}")
#         return error_response("Failed to get user statistics", 500)


# # -------------------------------
# # Get User Activity
# # -------------------------------
# @router.get("/activity", summary="Get User Activity", response_model=dict)
# async def get_user_activity(
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Get user activity information
#     """
#     try:
#         user_service = UserService(db)
#         activity = await user_service.get_user_activity(current_user.id)

#         return success_response(
#             message="User activity retrieved successfully", data=activity.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error getting user activity: {str(e)}")
#         return error_response("Failed to get user activity", 500)


# # -------------------------------
# # Deactivate Account
# # -------------------------------
# @router.post("/deactivate", summary="Deactivate Account", response_model=dict)
# async def deactivate_account(
#     deactivate_data: DeactivateAccountRequest,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Deactivate user account

#     - **password**: Current password for verification
#     - **reason**: Reason for deactivation (optional)
#     - **feedback**: Feedback about the service (optional)
#     """
#     try:
#         # Verify password first
#         from app.utils.password_utils import PasswordUtils

#         if not PasswordUtils.verify_password(
#             deactivate_data.password, current_user.password_hash
#         ):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
#             )

#         user_service = UserService(db)
#         success = await user_service.deactivate_account(
#             current_user.id, deactivate_data.reason
#         )

#         if success:
#             log_info(f"Account deactivated for user: {current_user.email}")
#             return success_response(
#                 message="Account deactivated successfully",
#                 data={"account_deactivated": True},
#             )
#         else:
#             return error_response("Failed to deactivate account", 500)
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error deactivating account: {str(e)}")
#         return error_response("Failed to deactivate account", 500)


# # -------------------------------
# # Search Users (Admin/Public feature)
# # -------------------------------
# @router.get("/search", summary="Search Users", response_model=dict)
# async def search_users(
#     q: str = Query(..., min_length=2, description="Search query"),
#     limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
#     offset: int = Query(0, ge=0, description="Number of results to skip"),
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Search for users by name or email

#     - **q**: Search query (minimum 2 characters)
#     - **limit**: Number of results to return (1-50)
#     - **offset**: Number of results to skip for pagination
#     """
#     try:
#         user_service = UserService(db)
#         users, total = await user_service.search_users(q, limit, offset)

#         user_profiles = [UserProfileResponse.model_validate(user) for user in users]

#         result_data = {
#             "users": [profile.dict() for profile in user_profiles],
#             "total": total,
#             "query": q,
#             "limit": limit,
#             "offset": offset,
#         }

#         return success_response(message=f"Found {len(users)} users", data=result_data)
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error searching users: {str(e)}")
#         return error_response("Failed to search users", 500)


# # -------------------------------
# # Get User by ID (Admin feature)
# # -------------------------------
# @router.get("/{user_id}", summary="Get User by ID", response_model=dict)
# async def get_user_by_id(
#     user_id: int,
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Get user information by ID

#     Note: This endpoint might be restricted to admin users in a real application
#     """
#     try:
#         user_service = UserService(db)
#         user = await user_service.get_user_by_id(user_id)

#         if not user:
#             return not_found("User not found")

#         user_profile = UserProfileResponse.model_validate(user)
#         return success_response(
#             message="User retrieved successfully", data=user_profile.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error getting user by ID: {str(e)}")
#         return error_response("Failed to get user", 500)


# # -------------------------------
# # Get Users List (Admin feature)
# # -------------------------------
# @router.get("/", summary="Get Users List", response_model=dict)
# async def get_users_list(
#     page: int = Query(1, ge=1, description="Page number"),
#     size: int = Query(10, ge=1, le=100, description="Page size"),
#     active_only: bool = Query(True, description="Show only active users"),
#     current_user: User = Depends(get_current_user_dependency),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Get paginated list of users

#     Note: This endpoint might be restricted to admin users in a real application

#     - **page**: Page number (starts from 1)
#     - **size**: Number of users per page (1-100)
#     - **active_only**: Show only active users
#     """
#     try:
#         user_service = UserService(db)
#         users, total = await user_service.get_users_paginated(page, size, active_only)

#         user_profiles = [UserProfileResponse.model_validate(user) for user in users]

#         total_pages = (total + size - 1) // size  # Ceiling division

#         result_data = UserListResponse(
#             users=user_profiles, total=total, page=page, size=size, pages=total_pages
#         )

#         return success_response(
#             message=f"Retrieved {len(users)} users", data=result_data.dict()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         log_error(f"Error getting users list: {str(e)}")
#         return error_response("Failed to get users list", 500)
