import aiohttp
import asyncio
from typing import Optional, Dict, Any
from app.core.config import settings
from app.utils.logger import log_info, log_error
import json


class SMSUtils:
    """
    SMS utility class for sending SMS messages via Dialog provider
    """

    @staticmethod
    async def _get_dialog_auth_token() -> Optional[str]:
        """
        Get authentication token from Dialog API
        """
        if not all(
            [
                settings.DIALOG_BASE_URL,
                settings.DIALOG_USERNAME,
                settings.DIALOG_PASSWORD,
                settings.DIALOG_LOGIN_ENDPOINT,
            ]
        ):
            log_error("Dialog SMS configuration is incomplete")
            return None

        login_url = f"{settings.DIALOG_BASE_URL}{settings.DIALOG_LOGIN_ENDPOINT}"

        login_data = {
            "username": settings.DIALOG_USERNAME,
            "password": settings.DIALOG_PASSWORD,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    login_url,
                    json=login_data,
                    headers={"Content-Type": "application/json"},
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        token = result.get("access_token") or result.get("token")
                        log_info("Successfully obtained Dialog auth token")
                        return token
                    else:
                        log_error(
                            f"Failed to authenticate with Dialog API: {response.status}"
                        )
                        return None

        except Exception as e:
            log_error(f"Error authenticating with Dialog API: {str(e)}")
            return None

    @staticmethod
    async def send_sms_dialog(phone_number: str, message: str) -> bool:
        """
        Send SMS using Dialog provider
        """
        if not settings.DIALOG_SMS_ENDPOINT:
            log_error("Dialog SMS endpoint not configured")
            return False

        # Get authentication token
        auth_token = await SMSUtils._get_dialog_auth_token()
        if not auth_token:
            return False

        sms_url = f"{settings.DIALOG_BASE_URL}{settings.DIALOG_SMS_ENDPOINT}"

        # Normalize phone number (remove any non-digit characters except +)
        normalized_phone = "".join(
            char for char in phone_number if char.isdigit() or char == "+"
        )

        # Ensure phone number starts with country code
        if not normalized_phone.startswith("+"):
            if normalized_phone.startswith("0"):
                # Assume Sri Lankan number, replace 0 with +94
                normalized_phone = "+94" + normalized_phone[1:]
            else:
                # Add default country code
                normalized_phone = "+94" + normalized_phone

        sms_data = {
            "to": normalized_phone,
            "message": message,
            "from": "MedVault",  # Sender ID
        }

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    sms_url, json=sms_data, headers=headers
                ) as response:
                    if response.status in [200, 201, 202]:
                        log_info(f"SMS sent successfully to {phone_number}")
                        return True
                    else:
                        error_text = await response.text()
                        log_error(
                            f"Failed to send SMS to {phone_number}: {response.status} - {error_text}"
                        )
                        return False

        except Exception as e:
            log_error(f"Error sending SMS to {phone_number}: {str(e)}")
            return False

    @staticmethod
    async def send_otp_sms(
        phone_number: str, otp_code: str, otp_type: str = "verification"
    ) -> bool:
        """
        Send OTP via SMS
        """
        message_templates = {
            "verification": f"Your MedVault verification code is: {otp_code}. This code will expire in 5 minutes. Do not share this code with anyone.",
            "login": f"Your MedVault login verification code is: {otp_code}. This code will expire in 5 minutes.",
            "password_reset": f"Your MedVault password reset code is: {otp_code}. This code will expire in 5 minutes.",
            "phone_verification": f"Your MedVault phone verification code is: {otp_code}. This code will expire in 5 minutes.",
        }

        message = message_templates.get(otp_type, message_templates["verification"])

        return await SMSUtils.send_sms_dialog(phone_number, message)

    @staticmethod
    def validate_phone_number(phone_number: str) -> tuple[bool, str]:
        """
        Validate phone number format
        Returns (is_valid, normalized_number)
        """
        if not phone_number:
            return False, ""

        # Remove all non-digit characters except +
        normalized = "".join(
            char for char in phone_number if char.isdigit() or char == "+"
        )

        # Check if it's empty after normalization
        if not normalized:
            return False, ""

        # Remove + for digit counting
        digits_only = normalized.replace("+", "")

        # Must have at least 10 digits
        if len(digits_only) < 10:
            return False, ""

        # Normalize to international format
        if normalized.startswith("+"):
            # Already has country code
            if len(digits_only) >= 10:
                return True, normalized
        else:
            # Add country code
            if normalized.startswith("0"):
                # Assume Sri Lankan number
                normalized = "+94" + normalized[1:]
            elif len(digits_only) == 9:
                # 9 digits without leading 0, assume Sri Lankan
                normalized = "+94" + normalized
            elif len(digits_only) >= 10:
                # Already has country code without +
                normalized = "+" + normalized
            else:
                return False, ""

        return True, normalized

    @staticmethod
    async def send_welcome_sms(phone_number: str, first_name: str = "") -> bool:
        """
        Send welcome SMS after successful registration
        """
        name_part = f"{first_name}, " if first_name else ""
        message = f"Welcome to MedVault, {name_part}! Your account has been created successfully. Start managing your health records securely with us."

        return await SMSUtils.send_sms_dialog(phone_number, message)

    @staticmethod
    async def send_security_alert_sms(phone_number: str, action: str) -> bool:
        """
        Send security alert SMS for important account actions
        """
        message = f"MedVault Security Alert: {action} was performed on your account. If this wasn't you, please contact support immediately."

        return await SMSUtils.send_sms_dialog(phone_number, message)

    @staticmethod
    def is_sms_configured() -> bool:
        """
        Check if SMS is properly configured
        """
        required_settings = [
            settings.DIALOG_BASE_URL,
            settings.DIALOG_USERNAME,
            settings.DIALOG_PASSWORD,
            settings.DIALOG_LOGIN_ENDPOINT,
            settings.DIALOG_SMS_ENDPOINT,
        ]

        return all(setting is not None for setting in required_settings)
