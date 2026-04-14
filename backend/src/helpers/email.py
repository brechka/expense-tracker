import asyncio
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_SENDER_NAME
from src.helpers.logger import logger


class EmailService:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SMTP_USER
        self.sender_password = SMTP_PASSWORD
        self.sender_name = SMTP_SENDER_NAME

    def _send_smtp(self, message: MIMEMultipart) -> None:
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            if self.smtp_port != 1025:
                server.starttls(context=context)
            if self.sender_email and self.sender_password and self.smtp_port != 1025:
                server.login(self.sender_email, self.sender_password)
            server.send_message(message)

    async def send_email(self, to_email: str, subject: str, html_body: str, text_body: str | None = None) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.sender_name} <{self.sender_email}>"
            msg["To"] = to_email
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._send_smtp, msg)
            logger.info("Email sent to %s", to_email)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e)
            return False

    async def send_password_reset_email(self, to_email: str, reset_code: str, reset_link: str, user_name: str) -> bool:
        subject = "Password Reset - Expense Tracker"
        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;">
        <div style="max-width:600px;margin:0 auto;padding:20px;">
          <h2>Password Reset Request</h2>
          <p>Hello {user_name},</p>
          <p>We received a request to reset your password.</p>
          <div style="background:#e7f3ff;border:1px solid #b3d7ff;padding:15px;margin:20px 0;text-align:center;">
            <p>Your reset code is:</p>
            <div style="font-size:24px;font-weight:bold;color:#2c5aa0;letter-spacing:2px;">{reset_code}</div>
          </div>
          <p>Or click the link below:</p>
          <p style="text-align:center;"><a href="{reset_link}" style="display:inline-block;padding:12px 24px;background:#4338ca;color:white;text-decoration:none;border-radius:8px;">Reset Password</a></p>
          <p style="color:#d32f2f;font-weight:bold;">This code expires in 10 minutes.</p>
          <p>If you didn't request this, ignore this email.</p>
        </div></body></html>
        """
        text_body = f"Hello {user_name},\n\nYour password reset code is: {reset_code}\n\nOr use this link: {reset_link}\n\nThis code expires in 10 minutes."
        return await self.send_email(to_email, subject, html_body, text_body)


email_service = EmailService()
