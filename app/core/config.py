import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import AnyUrl

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    # ---------------------------
    # Environment Settings
    # ---------------------------
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    APP_NAME: str = os.getenv("APP_NAME", "MedVault")
    BACKEND_BASE_URL: AnyUrl = os.getenv("BACKEND_BASE_URL")
    FRONTEND_BASE_URL: AnyUrl = os.getenv("FRONTEND_BASE_URL")
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "").split(",")
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", "1000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ---------------------------
    # Database Configuration
    # ---------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_NAME")

    # ---------------------------
    # JWT & Security Configuration
    # ---------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 43200))
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", 8))

    # ---------------------------
    # Email Configuration
    # ---------------------------
    EMAIL_FROM_ADDRESS: str = os.getenv("EMAIL_FROM_ADDRESS")
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_TEMPLATES_DIR: str = os.getenv("EMAIL_TEMPLATES_DIR", "app/templates/email")

    # ---------------------------
    # SMS Configuration
    # ---------------------------
    SMS_PROVIDER: str = os.getenv("SMS_PROVIDER", "dialog")
    DIALOG_BASE_URL: str = os.getenv("DIALOG_BASE_URL")
    DIALOG_USERNAME: str = os.getenv("DIALOG_USERNAME")
    DIALOG_PASSWORD: str = os.getenv("DIALOG_PASSWORD")
    DIALOG_LOGIN_ENDPOINT: str = os.getenv("DIALOG_LOGIN_ENDPOINT")
    DIALOG_SMS_ENDPOINT: str = os.getenv("DIALOG_SMS_ENDPOINT")

    # ---------------------------
    # Firebase Configuration
    # ---------------------------
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL")

    # ---------------------------
    # File Storage Configuration
    # ---------------------------
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "local")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 10))
    ALLOWED_FILE_TYPES: list[str] = os.getenv("ALLOWED_FILE_TYPES", "").split(",")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    # ---------------------------
    # Security Settings
    # ---------------------------
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", 12))
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", 30))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", 5))
    LOCKOUT_DURATION_MINUTES: int = int(os.getenv("LOCKOUT_DURATION_MINUTES", 15))

    # ---------------------------
    # Rate Limiting
    # ---------------------------
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", 1000))
    RATE_LIMIT_PER_DAY: int = int(os.getenv("RATE_LIMIT_PER_DAY", 10000))


settings = Settings()