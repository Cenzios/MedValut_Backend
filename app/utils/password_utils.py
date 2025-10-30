import bcrypt
from app.core.config import settings
import secrets
import string
from typing import Optional


class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        if not isinstance(password, str):
            raise TypeError(f"Expected str, got {type(password)}")

        print(f"[DEBUG] Password type: {type(password)}, value: {password}, length: {len(password)}")

        # Encode to bytes
        password_bytes = password.encode("utf-8")
        print(f"[DEBUG] Encoded length: {len(password_bytes)} bytes")

        # Bcrypt will automatically handle the 72-byte limit
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """Generate a secure random password"""
        characters = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + "!@#$%^&*()_+-="
        )

        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*()_+-="),
        ]

        for _ in range(length - 4):
            password.append(secrets.choice(characters))

        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    @staticmethod
    def is_password_strong(password: str) -> tuple[bool, list[str]]:
        """Check if password meets strength requirements"""
        issues = []

        if len(password) < settings.PASSWORD_MIN_LENGTH:
            issues.append(
                f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
            )

        if not any(char.isupper() for char in password):
            issues.append("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            issues.append("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            issues.append("Password must contain at least one digit")

        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
            issues.append("Password must contain at least one special character")

        if password.lower() in ["password", "123456", "qwerty", "admin", "letmein"]:
            issues.append("Password is too common")

        return len(issues) == 0, issues

    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """Check if password hash needs to be updated"""
        # With direct bcrypt, you could check the cost factor
        # For now, return False unless you implement version checking
        return False