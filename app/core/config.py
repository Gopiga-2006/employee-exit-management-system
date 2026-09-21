"""Application settings loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/employee_exit")
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_local_secret")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME)
OTP_DELIVERY = os.getenv("OTP_DELIVERY", "console")
JWT_ALGORITHM = "HS256"

if ENVIRONMENT.lower() == "production" and JWT_SECRET == "change_this_local_secret":
    raise RuntimeError("JWT_SECRET must be configured for production")
