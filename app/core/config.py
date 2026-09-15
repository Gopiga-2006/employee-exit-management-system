"""Application settings loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/employee_exit")
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_local_secret")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
JWT_ALGORITHM = "HS256"

if ENVIRONMENT.lower() == "production" and JWT_SECRET == "change_this_local_secret":
    raise RuntimeError("JWT_SECRET must be configured for production")
