"""Local auth setup (demo user)."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.auth import hash_password
from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import EcommerceService


if __name__ == "__main__":
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    password_hash, salt = hash_password("password123")
    try:
        service.create_user(
            email="demo@example.com",
            username="demo",
            password_hash=password_hash,
            password_salt=salt,
        )
    except Exception:
        print("Demo user already exists")
    else:
        print("Created demo user: demo / password123")
