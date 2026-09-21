"""OTP email delivery helpers."""

import smtplib
from email.message import EmailMessage

from app.core.config import (
    ENVIRONMENT,
    OTP_DELIVERY,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)


def send_otp_email(recipient: str, otp: str) -> None:
    """Deliver a registration OTP using SMTP or local console delivery."""
    if OTP_DELIVERY.lower() == "console":
        print(f"Registration OTP for {recipient}: {otp}")
        return

    if not all((SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM)):
        if ENVIRONMENT.lower() == "production":
            raise RuntimeError("SMTP settings must be configured for OTP delivery")
        print(f"Registration OTP for {recipient}: {otp}")
        return

    message = EmailMessage()
    message["Subject"] = "Employee Exit Management System - Verification OTP"
    message["From"] = SMTP_FROM
    message["To"] = recipient
    message.set_content(
        f"Your verification OTP is {otp}. It expires in 10 minutes."
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
