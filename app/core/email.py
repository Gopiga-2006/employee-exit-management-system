"""OTP email delivery helpers."""

import json
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage

from app.core.config import (
    EMAIL_PROVIDER,
    ENVIRONMENT,
    RESEND_API_KEY,
    RESEND_FROM,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)


def _send_with_resend(recipient: str, otp: str) -> None:
    """Send an OTP through the Resend HTTPS email API."""
    payload = json.dumps(
        {
            "from": RESEND_FROM,
            "to": [recipient],
            "subject": "Employee Exit Management System - Verification OTP",
            "text": f"Your verification OTP is {otp}. It expires in 10 minutes.",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status < 200 or response.status >= 300:
                raise RuntimeError("Resend email delivery failed")
    except urllib.error.HTTPError as exc:
        raise RuntimeError("Resend email delivery failed") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("Unable to reach the email delivery service") from exc


def _send_with_smtp(recipient: str, otp: str) -> None:
    """Send an OTP through an SMTP server."""
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


def send_otp_email(recipient: str, otp: str) -> None:
    """Deliver a registration OTP using the configured email provider."""
    provider = EMAIL_PROVIDER.lower()

    if provider == "console":
        print(f"Registration OTP for {recipient}: {otp}")
        return

    if provider == "resend":
        if not RESEND_API_KEY or not RESEND_FROM:
            if ENVIRONMENT.lower() == "production":
                raise RuntimeError(
                    "Resend settings must be configured for OTP delivery"
                )
            print(f"Registration OTP for {recipient}: {otp}")
            return
        _send_with_resend(recipient, otp)
        return

    if provider == "smtp":
        if not all((SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM)):
            if ENVIRONMENT.lower() == "production":
                raise RuntimeError("SMTP settings must be configured for OTP delivery")
            print(f"Registration OTP for {recipient}: {otp}")
            return
        _send_with_smtp(recipient, otp)
        return

    raise RuntimeError("Unsupported OTP email provider")
