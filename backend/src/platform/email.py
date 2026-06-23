import smtplib
import asyncio
from email.mime.text import MIMEText

from src.platform.config import settings


class EmailService:
    async def send_password_reset(self, email: str, token: str) -> None:
        raise NotImplementedError


class SmtpEmailService(EmailService):
    async def send_password_reset(self, email: str, token: str) -> None:
        reset_link = f"{settings.frontend_url}/reset-password?token={token}"
        body = (
            f"You have requested a password reset.\n\n"
            f"Please click the link below to reset your password:\n{reset_link}\n\n"
            f"This link will expire in 15 minutes.\n"
            f"If you did not request this, please ignore this email."
        )
        msg = MIMEText(body)
        msg["Subject"] = "Password Reset - Biglands"
        msg["From"] = settings.email_from
        msg["To"] = email

        await asyncio.to_thread(self._send_sync, msg)

    def _send_sync(self, msg: MIMEText) -> None:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
