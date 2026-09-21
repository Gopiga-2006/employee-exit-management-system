"""OTP email delivery helpers."""

import base64
import json
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage
from email.mime.text import MIMEText

from app.core.config import (
    EMAIL_PROVIDER,
    ENVIRONMENT,
    GMAIL_CLIENT_ID,
    GMAIL_CLIENT_SECRET,
    GMAIL_FROM,
    GMAIL_REFRESH_TOKEN,
    RESEND_API_KEY,
    RESEND_FROM,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)


def _send_with_gmail(recipient: str, otp: str, subject: str) -> None:
    """Send an OTP through the Gmail API over HTTPS."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not all(
        (
            GMAIL_CLIENT_ID,
            GMAIL_CLIENT_SECRET,
            GMAIL_REFRESH_TOKEN,
            GMAIL_FROM,
        )
    ):
        raise RuntimeError("Gmail API settings must be configured for OTP delivery")

    credentials = Credentials(
        token=None,
        refresh_token=GMAIL_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GMAIL_CLIENT_ID,
        client_secret=GMAIL_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )
    credentials.refresh(Request())

    message = MIMEText(
        f"Your verification OTP is {otp}. It expires in 10 minutes.",
        "plain",
        "utf-8",
    )
    message["to"] = recipient
    message["from"] = GMAIL_FROM
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    service = build("gmail", "v1", credentials=credentials, cache_discovery=False)
    service.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()


def _send_with_resend(recipient: str, otp: str, subject: str) -> None:
    """Send an OTP through the Resend HTTPS email API."""
    payload = json.dumps(
        {
            "from": RESEND_FROM,
            "to": [recipient],
            "subject": subject,
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


def _send_with_smtp(recipient: str, otp: str, subject: str) -> None:
    """Send an OTP through an SMTP server."""
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = recipient
    message.set_content(
        f"Your verification OTP is {otp}. It expires in 10 minutes."
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


def send_otp_email(recipient: str, otp: str, subject: str) -> None:
    """Deliver an OTP using the configured email provider."""
    provider = EMAIL_PROVIDER.lower()

    if provider == "console":
        print(f"OTP for {recipient}: {otp}")
        return

    if provider == "gmail":
        _send_with_gmail(recipient, otp, subject)
        return

    if provider == "resend":
        if not RESEND_API_KEY or not RESEND_FROM:
            if ENVIRONMENT.lower() == "production":
                raise RuntimeError(
                    "Resend settings must be configured for OTP delivery"
                )
            print(f"Registration OTP for {recipient}: {otp}")
            return
        _send_with_resend(recipient, otp, subject)
        return

    if provider == "smtp":
        if not all((SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM)):
            if ENVIRONMENT.lower() == "production":
                raise RuntimeError("SMTP settings must be configured for OTP delivery")
            print(f"Registration OTP for {recipient}: {otp}")
            return
        _send_with_smtp(recipient, otp, subject)
        return

    raise RuntimeError("Unsupported OTP email provider")
