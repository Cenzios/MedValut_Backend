import os
from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import List

class Settings(BaseSettings):
    # ---------------------------
    # Environment Settings
    # ---------------------------
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    APP_NAME: str = "MedVault"
    BACKEND_BASE_URL: str | None = None
    FRONTEND_BASE_URL: str | None = None
    CORS_ORIGINS: str = ""  # Will be split later
    RATE_LIMIT: int = 1000
    LOG_LEVEL: str = "INFO"

    # ---------------------------
    # Database Configuration
    # ---------------------------
    DATABASE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str

    # ---------------------------
    # JWT & Security Configuration
    # ---------------------------
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    PASSWORD_MIN_LENGTH: int = 8

    # ---------------------------
    # Email Configuration
    # ---------------------------
    EMAIL_FROM_ADDRESS: str | None = None
    EMAIL_FROM_NAME: str | None = None
    SMTP_SERVER: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_USE_TLS: bool = True
    EMAIL_TEMPLATES_DIR: str = "app/templates/email"

    # ---------------------------
    # SMS Configuration
    # ---------------------------
    SMS_PROVIDER: str = "dialog"
    DIALOG_BASE_URL: str | None = None
    DIALOG_USERNAME: str | None = None
    DIALOG_PASSWORD: str | None = None
    DIALOG_LOGIN_ENDPOINT: str | None = None
    DIALOG_SMS_ENDPOINT: str | None = None

    # ---------------------------
    # Firebase Configuration
    # ---------------------------
    FIREBASE_PROJECT_ID: str | None = None
    FIREBASE_PRIVATE_KEY_ID: str | None = None
    FIREBASE_PRIVATE_KEY: str | None = None
    FIREBASE_CLIENT_EMAIL: str | None = None
    FIREBASE_CLIENT_ID: str | None = None
    FIREBASE_DATABASE_URL: str | None = None

    # ---------------------------
    # File Storage Configuration
    # ---------------------------
    STORAGE_PROVIDER: str = "local"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = ""  # Will be split later
    UPLOAD_DIR: str = "uploads"

    # ---------------------------
    # Security Settings
    # ---------------------------
    BCRYPT_ROUNDS: int = 12
    SESSION_TIMEOUT_MINUTES: int = 30
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

    # ---------------------------
    # Rate Limiting
    # ---------------------------
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_PER_DAY: int = 10000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # This allows reading from environment variables directly
        extra = "ignore"

    # Helper properties
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        if not self.CORS_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Parse ALLOWED_FILE_TYPES string into list"""
        if not self.ALLOWED_FILE_TYPES:
            return []
        return [ft.strip() for ft in self.ALLOWED_FILE_TYPES.split(",") if ft.strip()]


settings = Settings()