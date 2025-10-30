# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, update, delete, and_, or_, func
# from sqlalchemy.exc import IntegrityError
# from fastapi import HTTPException, status
# from datetime import datetime, timedelta
# from typing import Optional, List, Dict, Any, Tuple

# from app.modules.user.models import User, OTPVerification, RefreshToken
# from app.modules.user.schemas import (
#     UserProfileUpdate,
#     UserHealthUpdate,
#     UserContactUpdate,
#     ChangePasswordRequest,
#     UserResponse,
#     UserProfileResponse,
#     UserHealthResponse,
#     UserSubscriptionResponse,
#     UserStatsResponse,
#     UserActivityResponse,
#     UserPreferences,
#     UserPreferencesUpdate,
# )
# from app.utils.password_utils import PasswordUtils
# from app.utils.email_utils import EmailUtils
# from app.utils.sms_utils import SMSUtils
# from app.utils.logger import log_info, log_error
# from app.utils.action_logger import log_action
# from app.core.config import settings


# class UserService:
#     def __init__(self, db: AsyncSession):
#         self.db = db

#     async def get_user_by_id(self, user_id: int) -> Optional[User]:
#         """Get user by ID"""
#         try:
#             query = select(User).where(User.id == user_id)
#             result = await self.db.execute(query)
#             return result.scalar_one_or_none()
#         except Exception as e:
#             log_error(f"Error getting user by ID {user_id}: {e}")
#             return None

#     async def get_user_by_email(self, email: str) -> Optional[User]:
#         """Get user by email"""
#         try:
#             query = select(User).where(User.email == email)
#             result = await self.db.execute(query)
#             return result.scalar_one_or_none()
#         except Exception as e:
#             log_error(f"Error getting user by email {email}: {e}")
#             return None

#     async def get_user_by_phone(self, phone_number: str) -> Optional[User]:
#         """Get user by phone number"""
#         try:
#             query = select(User).where(User.phone_number == phone_number)
#             result = await self.db.execute(query)
#             return result.scalar_one_or_none()
#         except Exception as e:
#             log_error(f"Error getting user by phone {phone_number}: {e}")
#             return None

#     async def update_user_profile(
#         self, user_id: int, profile_data: UserProfileUpdate
#     ) -> User:
#         """Update user profile information"""
#         try:
#             # Get existing user
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Update fields that are provided
#             update_data = {}
#             for field, value in profile_data.dict(exclude_unset=True).items():
#                 update_data[field] = value

#             if update_data:
#                 update_data["updated_at"] = datetime.utcnow()

#                 query = update(User).where(User.id == user_id).values(**update_data)
#                 await self.db.execute(query)
#                 await self.db.commit()

#                 # Get updated user
#                 user = await self.get_user_by_id(user_id)

#                 # Log profile update
#                 await log_action(
#                     user_id, "profile_updated", {"fields": list(update_data.keys())}
#                 )

#             return user

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error updating user profile {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to update profile",
#             )

#     async def update_user_health_data(
#         self, user_id: int, health_data: UserHealthUpdate
#     ) -> User:
#         """Update user health information"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Update health fields
#             update_data = {}
#             for field, value in health_data.dict(exclude_unset=True).items():
#                 update_data[field] = value

#             if update_data:
#                 update_data["updated_at"] = datetime.utcnow()

#                 query = update(User).where(User.id == user_id).values(**update_data)
#                 await self.db.execute(query)
#                 await self.db.commit()

#                 # Get updated user
#                 user = await self.get_user_by_id(user_id)

#                 # Log health data update
#                 await log_action(
#                     user_id, "health_data_updated", {"fields": list(update_data.keys())}
#                 )

#             return user

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error updating user health data {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to update health data",
#             )

#     async def update_user_contact(
#         self, user_id: int, contact_data: UserContactUpdate
#     ) -> User:
#         """Update user contact information"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Check if phone number is already taken by another user
#             if contact_data.phone_number:
#                 existing_user = await self.get_user_by_phone(contact_data.phone_number)
#                 if existing_user and existing_user.id != user_id:
#                     raise HTTPException(
#                         status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="Phone number already in use",
#                     )

#             # Update contact fields
#             update_data = {}
#             for field, value in contact_data.dict(exclude_unset=True).items():
#                 update_data[field] = value

#             # If phone number is being updated, mark as unverified
#             if (
#                 "phone_number" in update_data
#                 and update_data["phone_number"] != user.phone_number
#             ):
#                 update_data["phone_verified"] = False

#             if update_data:
#                 update_data["updated_at"] = datetime.utcnow()

#                 query = update(User).where(User.id == user_id).values(**update_data)
#                 await self.db.execute(query)
#                 await self.db.commit()

#                 # Get updated user
#                 user = await self.get_user_by_id(user_id)

#                 # Log contact update
#                 await log_action(
#                     user_id, "contact_updated", {"fields": list(update_data.keys())}
#                 )

#             return user

#         except HTTPException:
#             raise
#         except IntegrityError:
#             await self.db.rollback()
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Phone number already in use",
#             )
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error updating user contact {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to update contact information",
#             )

#     async def change_password(
#         self, user_id: int, password_data: ChangePasswordRequest
#     ) -> bool:
#         """Change user password"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Verify current password
#             if not PasswordUtils.verify_password(
#                 password_data.current_password, user.password_hash
#             ):
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Current password is incorrect",
#                 )

#             # Hash new password
#             new_password_hash = PasswordUtils.hash_password(password_data.new_password)

#             # Update password
#             query = (
#                 update(User)
#                 .where(User.id == user_id)
#                 .values(password_hash=new_password_hash, updated_at=datetime.utcnow())
#             )
#             await self.db.execute(query)
#             await self.db.commit()

#             # Log password change
#             await log_action(user_id, "password_changed", {})

#             # Send security notification email
#             try:
#                 await EmailUtils.send_email_async(
#                     user.email,
#                     "Password Changed - MedVault",
#                     f"""
#                     <h2>Password Changed</h2>
#                     <p>Your password has been successfully changed.</p>
#                     <p>If you didn't make this change, please contact support immediately.</p>
#                     <p>Time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</p>
#                     """,
#                     f"Your MedVault password has been changed at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC. If you didn't make this change, please contact support.",
#                 )
#             except Exception as e:
#                 log_error(
#                     f"Failed to send password change notification to {user.email}: {e}"
#                 )

#             return True

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error changing password for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to change password",
#             )

#     async def update_profile_picture(self, user_id: int, picture_url: str) -> User:
#         """Update user profile picture"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             query = (
#                 update(User)
#                 .where(User.id == user_id)
#                 .values(profile_picture_url=picture_url, updated_at=datetime.utcnow())
#             )
#             await self.db.execute(query)
#             await self.db.commit()

#             # Get updated user
#             user = await self.get_user_by_id(user_id)

#             # Log profile picture update
#             await log_action(user_id, "profile_picture_updated", {"url": picture_url})

#             return user

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error updating profile picture for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to update profile picture",
#             )

#     async def deactivate_account(
#         self, user_id: int, reason: Optional[str] = None
#     ) -> bool:
#         """Deactivate user account"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Deactivate user account
#             query = (
#                 update(User)
#                 .where(User.id == user_id)
#                 .values(is_active=False, updated_at=datetime.utcnow())
#             )
#             await self.db.execute(query)

#             # Deactivate all refresh tokens
#             token_query = (
#                 update(RefreshToken)
#                 .where(RefreshToken.user_id == user_id)
#                 .values(is_active=False)
#             )
#             await self.db.execute(token_query)

#             await self.db.commit()

#             # Log account deactivation
#             await log_action(user_id, "account_deactivated", {"reason": reason})

#             # Send deactivation confirmation email
#             try:
#                 await EmailUtils.send_email_async(
#                     user.email,
#                     "Account Deactivated - MedVault",
#                     f"""
#                     <h2>Account Deactivated</h2>
#                     <p>Your MedVault account has been deactivated.</p>
#                     <p>You can reactivate your account at any time by logging in.</p>
#                     <p>Time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</p>
#                     """,
#                     f"Your MedVault account has been deactivated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC.",
#                 )
#             except Exception as e:
#                 log_error(
#                     f"Failed to send deactivation notification to {user.email}: {e}"
#                 )

#             return True

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error deactivating account for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to deactivate account",
#             )

#     async def reactivate_account(self, user_id: int) -> bool:
#         """Reactivate user account"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Reactivate user account
#             query = (
#                 update(User)
#                 .where(User.id == user_id)
#                 .values(
#                     is_active=True,
#                     login_attempts=0,  # Reset login attempts
#                     locked_until=None,  # Remove any locks
#                     updated_at=datetime.utcnow(),
#                 )
#             )
#             await self.db.execute(query)
#             await self.db.commit()

#             # Log account reactivation
#             await log_action(user_id, "account_reactivated", {})

#             # Send reactivation confirmation email
#             try:
#                 await EmailUtils.send_email_async(
#                     user.email,
#                     "Account Reactivated - MedVault",
#                     f"""
#                     <h2>Welcome Back!</h2>
#                     <p>Your MedVault account has been reactivated.</p>
#                     <p>You can now access all features of your account.</p>
#                     <p>Time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</p>
#                     """,
#                     f"Your MedVault account has been reactivated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC.",
#                 )
#             except Exception as e:
#                 log_error(
#                     f"Failed to send reactivation notification to {user.email}: {e}"
#                 )

#             return True

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error reactivating account for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to reactivate account",
#             )

#     async def get_user_stats(self, user_id: int) -> UserStatsResponse:
#         """Get user statistics"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Calculate account age
#             account_age = (datetime.utcnow() - user.created_at).days

#             # Verification status
#             verification_status = {
#                 "email_verified": user.email_verified,
#                 "phone_verified": user.phone_verified,
#                 "profile_complete": self._calculate_profile_completion(user),
#             }

#             stats = UserStatsResponse(
#                 total_documents=0,  # TODO: Implement when document module is ready
#                 storage_used_mb=0.0,  # TODO: Implement when document module is ready
#                 last_activity=user.last_login,
#                 account_age_days=account_age,
#                 verification_status=verification_status,
#             )

#             return stats

#         except HTTPException:
#             raise
#         except Exception as e:
#             log_error(f"Error getting user stats for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to get user statistics",
#             )

#     async def get_user_activity(self, user_id: int) -> UserActivityResponse:
#         """Get user activity information"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # TODO: Implement login count from action logs
#             login_count = 0

#             activity = UserActivityResponse(
#                 login_count=login_count,
#                 last_login=user.last_login,
#                 account_created=user.created_at,
#                 profile_completion=self._calculate_profile_completion(user),
#             )

#             return activity

#         except HTTPException:
#             raise
#         except Exception as e:
#             log_error(f"Error getting user activity for user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to get user activity",
#             )

#     async def search_users(
#         self, query: str, limit: int = 10, offset: int = 0
#     ) -> Tuple[List[User], int]:
#         """Search users by name or email"""
#         try:
#             # Build search query
#             search_query = (
#                 select(User)
#                 .where(
#                     and_(
#                         User.is_active == True,
#                         or_(
#                             User.first_name.ilike(f"%{query}%"),
#                             User.last_name.ilike(f"%{query}%"),
#                             User.email.ilike(f"%{query}%"),
#                         ),
#                     )
#                 )
#                 .offset(offset)
#                 .limit(limit)
#             )

#             # Count query
#             count_query = select(func.count(User.id)).where(
#                 and_(
#                     User.is_active == True,
#                     or_(
#                         User.first_name.ilike(f"%{query}%"),
#                         User.last_name.ilike(f"%{query}%"),
#                         User.email.ilike(f"%{query}%"),
#                     ),
#                 )
#             )

#             # Execute queries
#             result = await self.db.execute(search_query)
#             count_result = await self.db.execute(count_query)

#             users = result.scalars().all()
#             total = count_result.scalar()

#             return users, total

#         except Exception as e:
#             log_error(f"Error searching users with query '{query}': {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to search users",
#             )

#     async def get_users_paginated(
#         self, page: int = 1, size: int = 10, active_only: bool = True
#     ) -> Tuple[List[User], int]:
#         """Get users with pagination"""
#         try:
#             offset = (page - 1) * size

#             # Build query
#             base_filter = User.is_active == True if active_only else True

#             query = select(User).where(base_filter).offset(offset).limit(size)
#             count_query = select(func.count(User.id)).where(base_filter)

#             # Execute queries
#             result = await self.db.execute(query)
#             count_result = await self.db.execute(count_query)

#             users = result.scalars().all()
#             total = count_result.scalar()

#             return users, total

#         except Exception as e:
#             log_error(f"Error getting users paginated: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to get users",
#             )

#     def _calculate_profile_completion(self, user: User) -> float:
#         """Calculate profile completion percentage"""
#         total_fields = 12  # Total number of profile fields
#         completed_fields = 0

#         # Required fields
#         if user.email:
#             completed_fields += 1
#         if user.first_name:
#             completed_fields += 1
#         if user.last_name:
#             completed_fields += 1

#         # Optional but important fields
#         if user.phone_number:
#             completed_fields += 1
#         if user.date_of_birth:
#             completed_fields += 1
#         if user.gender_id:
#             completed_fields += 1
#         if user.bio:
#             completed_fields += 1
#         if user.profile_picture_url:
#             completed_fields += 1
#         if user.height:
#             completed_fields += 1
#         if user.weight:
#             completed_fields += 1
#         if user.blood_type_id:
#             completed_fields += 1
#         if user.email_verified:
#             completed_fields += 1

#         return round((completed_fields / total_fields) * 100, 1)

#     async def delete_user_permanently(self, user_id: int) -> bool:
#         """Permanently delete user and all associated data"""
#         try:
#             user = await self.get_user_by_id(user_id)
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#                 )

#             # Delete related data first
#             # Delete OTP verifications
#             await self.db.execute(
#                 delete(OTPVerification).where(OTPVerification.user_id == user_id)
#             )

#             # Delete refresh tokens
#             await self.db.execute(
#                 delete(RefreshToken).where(RefreshToken.user_id == user_id)
#             )

#             # Delete user
#             await self.db.execute(delete(User).where(User.id == user_id))

#             await self.db.commit()

#             # Log permanent deletion
#             log_info(f"User {user_id} ({user.email}) permanently deleted")

#             return True

#         except HTTPException:
#             raise
#         except Exception as e:
#             await self.db.rollback()
#             log_error(f"Error permanently deleting user {user_id}: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to delete user",
#             )
