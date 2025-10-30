from passlib.context import CryptContext
from passlib.hash import bcrypt
from app.core.config import settings
import secrets
import string
from typing import Optional

# Create password context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """
        Generate a secure random password
        """
        # Include uppercase, lowercase, digits, and special characters
        characters = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + "!@#$%^&*()_+-="
        )

        # Ensure at least one character from each category
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*()_+-="),
        ]

        # Fill the rest randomly
        for _ in range(length - 4):
            password.append(secrets.choice(characters))

        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    @staticmethod
    def is_password_strong(password: str) -> tuple[bool, list[str]]:
        """
        Check if password meets strength requirements
        Returns (is_strong, list_of_issues)
        """
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

        # Check for common patterns
        if password.lower() in ["password", "123456", "qwerty", "admin", "letmein"]:
            issues.append("Password is too common")

        return len(issues) == 0, issues

    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """
        Check if password hash needs to be updated (e.g., due to changed rounds)
        """
        return pwd_context.needs_update(hashed_password)
