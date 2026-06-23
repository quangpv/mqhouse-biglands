import asyncio
import smtplib
from pathlib import Path

from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from src.platform.config import settings


_TEMPLATE_DIR = Path(__file__).parent / "email_templates"
_JINJA_ENV = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)))


class EmailService:
    async def send_password_reset(self, email: str, token: str) -> None:
        raise NotImplementedError

    async def send_welcome(self, email: str, username: str, password: str) -> None:
        raise NotImplementedError


class SmtpEmailService(EmailService):
    def _render(self, template_name: str, **kwargs) -> str:
        template = _JINJA_ENV.get_template(template_name)
        return template.render(**kwargs)

    async def send_password_reset(self, email: str, token: str) -> None:
        reset_link = f"{settings.frontend_url}/reset-password?token={token}"
        body = self._render(
            "password_reset.html",
            app_name=settings.app_name,
            reset_link=reset_link,
            expiry_minutes=15,
        )
        msg = MIMEText(body, "html")
        msg["Subject"] = "Password Reset"
        msg["From"] = settings.email_from
        msg["To"] = email

        await asyncio.to_thread(self._send_sync, msg)

    async def send_welcome(self, email: str, username: str, password: str) -> None:
        login_url = f"{settings.frontend_url}/login"
        body = self._render(
            "welcome.html",
            app_name=settings.app_name,
            username=username,
            password=password,
            login_url=login_url,
        )
        msg = MIMEText(body, "html")
        msg["Subject"] = "Welcome to Biglands"
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
