import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import settings
from app.utils.logger import log_info, log_error
import asyncio
from concurrent.futures import ThreadPoolExecutor


class EmailUtils:
    @staticmethod
    def _create_smtp_connection():
        """
        Create SMTP connection with proper SSL/TLS configuration
        """
        if not all(
            [settings.SMTP_SERVER, settings.SMTP_USERNAME, settings.SMTP_PASSWORD]
        ):
            raise ValueError("SMTP configuration is incomplete")

        context = ssl.create_default_context()

        if settings.EMAIL_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls(context=context)
        else:
            server = smtplib.SMTP_SSL(
                settings.SMTP_SERVER, settings.SMTP_PORT, context=context
            )

        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        return server

    @staticmethod
    def _create_message(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> MIMEMultipart:
        """
        Create email message with HTML and optional text content
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = (
            f"{settings.EMAIL_FROM_NAME or settings.APP_NAME} <{settings.EMAIL_FROM_ADDRESS or settings.SMTP_USERNAME}>"
        )
        message["To"] = to_email

        # Add text content if provided
        if text_content:
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)

        # Add HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        return message

    @staticmethod
    def send_email_sync(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send email synchronously
        """
        try:
            server = EmailUtils._create_smtp_connection()
            message = EmailUtils._create_message(
                to_email, subject, html_content, text_content
            )

            server.send_message(message)
            server.quit()

            log_info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            log_error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    @staticmethod
    async def send_email_async(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send email asynchronously using thread pool
        """
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            try:
                result = await loop.run_in_executor(
                    executor,
                    EmailUtils.send_email_sync,
                    to_email,
                    subject,
                    html_content,
                    text_content,
                )
                return result
            except Exception as e:
                log_error(f"Failed to send async email to {to_email}: {str(e)}")
                return False

    @staticmethod
    async def send_otp_email(to_email: str, otp_code: str, otp_type: str) -> bool:
        """
        Send OTP verification email
        """
        subject_map = {
            "email_verification": "Verify Your Email - MedVault",
            "password_reset": "Reset Your Password - MedVault",
            "login": "Login Verification Code - MedVault",
        }

        subject = subject_map.get(otp_type, "Verification Code - MedVault")

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    background-color: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #007bff;
                    margin-bottom: 10px;
                }}
                .otp-code {{
                    background-color: #007bff;
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px;
                    margin: 30px 0;
                    letter-spacing: 5px;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🏥 MedVault</div>
                    <h2>Verification Code</h2>
                </div>

                <p>Hello,</p>

                <p>Your verification code is:</p>

                <div class="otp-code">{otp_code}</div>

                <div class="warning">
                    ⚠️ This code will expire in 5 minutes. Do not share this code with anyone.
                </div>

                <p>If you didn't request this code, please ignore this email or contact our support team.</p>

                <div class="footer">
                    <p>Best regards,<br>The MedVault Team</p>
                    <p><small>This is an automated email. Please do not reply to this email.</small></p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        MedVault - Verification Code

        Hello,

        Your verification code is: {otp_code}

        This code will expire in 5 minutes. Do not share this code with anyone.

        If you didn't request this code, please ignore this email or contact our support team.

        Best regards,
        The MedVault Team
        """

        return await EmailUtils.send_email_async(
            to_email, subject, html_content, text_content
        )

    @staticmethod
    async def send_welcome_email(to_email: str, first_name: str = "") -> bool:
        """
        Send welcome email after successful registration
        """
        subject = "Welcome to MedVault!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    background-color: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #007bff;
                    margin-bottom: 10px;
                }}
                .feature {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 4px solid #007bff;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🏥 MedVault</div>
                    <h2>Welcome to MedVault!</h2>
                </div>

                <p>Hello {first_name},</p>

                <p>Welcome to MedVault! We're excited to have you on board. Your account has been successfully created.</p>

                <h3>What you can do with MedVault:</h3>

                <div class="feature">
                    📋 <strong>Store Medical Records</strong><br>
                    Securely store and organize all your medical documents in one place.
                </div>

                <div class="feature">
                    👩‍⚕️ <strong>Track Health Data</strong><br>
                    Monitor your health metrics, medications, and appointments.
                </div>

                <div class="feature">
                    🔒 <strong>Privacy & Security</strong><br>
                    Your data is encrypted and protected with enterprise-grade security.
                </div>

                <div class="feature">
                    📱 <strong>Easy Access</strong><br>
                    Access your health information anytime, anywhere from any device.
                </div>

                <p>To get started, please verify your email address if you haven't already done so.</p>

                <p>If you have any questions or need assistance, don't hesitate to reach out to our support team.</p>

                <div class="footer">
                    <p>Best regards,<br>The MedVault Team</p>
                    <p><small>This is an automated email. Please do not reply to this email.</small></p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Welcome to MedVault!

        Hello {first_name},

        Welcome to MedVault! We're excited to have you on board. Your account has been successfully created.

        What you can do with MedVault:

        📋 Store Medical Records - Securely store and organize all your medical documents in one place.
        👩‍⚕️ Track Health Data - Monitor your health metrics, medications, and appointments.
        🔒 Privacy & Security - Your data is encrypted and protected with enterprise-grade security.
        📱 Easy Access - Access your health information anytime, anywhere from any device.

        To get started, please verify your email address if you haven't already done so.

        If you have any questions or need assistance, don't hesitate to reach out to our support team.

        Best regards,
        The MedVault Team
        """

        return await EmailUtils.send_email_async(
            to_email, subject, html_content, text_content
        )

    @staticmethod
    async def send_password_reset_email(to_email: str, reset_token: str) -> bool:
        """
        Send password reset email with reset link
        """
        subject = "Reset Your Password - MedVault"
        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password?token={reset_token}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    background-color: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #007bff;
                    margin-bottom: 10px;
                }}
                .reset-button {{
                    background-color: #007bff;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🏥 MedVault</div>
                    <h2>Reset Your Password</h2>
                </div>

                <p>Hello,</p>

                <p>You requested a password reset for your MedVault account. Click the button below to reset your password:</p>

                <div style="text-align: center;">
                    <a href="{reset_url}" class="reset-button">Reset Password</a>
                </div>

                <p>Or copy and paste this link in your browser:</p>
                <p style="word-break: break-all; color: #007bff;">{reset_url}</p>

                <div class="warning">
                    ⚠️ This link will expire in 24 hours. If you didn't request this reset, please ignore this email.
                </div>

                <div class="footer">
                    <p>Best regards,<br>The MedVault Team</p>
                    <p><small>This is an automated email. Please do not reply to this email.</small></p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        MedVault - Reset Your Password

        Hello,

        You requested a password reset for your MedVault account.

        Click this link to reset your password: {reset_url}

        This link will expire in 24 hours. If you didn't request this reset, please ignore this email.

        Best regards,
        The MedVault Team
        """

        return await EmailUtils.send_email_async(
            to_email, subject, html_content, text_content
        )
