from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Index

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    country_code = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    nic = Column(String(20), nullable=False)
    sign_up_method = Column(Integer, nullable=False)  # 1: 'email'/app, 2:'google', 3:'apple'
    social_id = Column(String(255), nullable=True)  # For social sign-ups

    # Profile information
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    gender_id = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    
    # Profile picture and bio
    profile_picture_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)

    # Account status
    is_profile_completed = Column(Boolean, default=False, nullable=False)
    is_email_verified = Column(Boolean, default=False, nullable=False)
    is_emergency_contact_added = Column(Boolean, default=False, nullable=False)

    # Authentication attempts
    login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)

    # Subscription
    subscription_plan_id = Column(
        Integer, nullable=True, default=1
    ) # Default plan is "Free"
    subscription_start_date = Column(DateTime, nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)

    # Health metrics
    height = Column(Float, nullable=True)  # in cm
    height_unit_id = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)  # in kg
    weight_unit_id = Column(Integer, nullable=True)
    blood_type_id = Column(Integer, nullable=True)
    smoking_level_id = Column(Integer, nullable=True)
    alcohol_level_id = Column(Integer, nullable=True)
    exercise_level_id = Column(Integer, nullable=True)
    pre_medical_conditions = Column(Text, nullable=True)
    chronical_diseases = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medicones_currently_taking = Column(Text, nullable=True)
    surgeries_history = Column(Text, nullable=True)
    
    # Family medical history
    has_heart_disease_family_history = Column(Boolean, default=False, nullable=False)
    has_diabetes_family_history = Column(Boolean, default=False, nullable=False)
    has_hypertension_family_history = Column(Boolean, default=False, nullable=False)
    has_cancer_family_history = Column(Boolean, default=False, nullable=False)
    has_asthma_family_history = Column(Boolean, default=False, nullable=False)
    has_other_family_history = Column(Text, nullable=True)
    other_family_medical_history = Column(Text, nullable=True)
    has_genetic_disorders_family_history = Column(Boolean, default=False, nullable=False)
    family_genetic_disorders_details = Column(Text, nullable=True)
    
    # Account Activation Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    
    __table_args__ = (
        Index('ix_users_email_is_active', 'email', 'is_active'),
        Index('ix_users_nic_is_active', 'nic', 'is_active'),
    )


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    otp_code = Column(String(10), nullable=False)
    otp_type = Column(
        Integer, default=1, nullable=False,
    )  # 1: 'email_verification', 2: 'phone_verification', 3: 'password_reset', 4: 'login'
    otp_reference = Column(String(100), nullable=True)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    used_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('ix_otp_verifications_email', 'email'),
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(500), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    __table_args__ = (
        Index('ix_refresh_tokens_user_id_is_active', 'user_id', 'is_active'),
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(500), nullable=False, unique=True)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    used_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('ix_password_reset_tokens_user_id', 'user_id'),
    )
