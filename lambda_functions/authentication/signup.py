import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.auth import hash_password
from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import EcommerceService, ValidationError


def lambda_handler(event, context):
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    username = event["username"]
    password = event["password"]
    email = event["email"]

    password_hash, salt = hash_password(password)
    try:
        user = service.create_user(
            email=email,
            username=username,
            password_hash=password_hash,
            password_salt=salt,
        )
    except ValidationError as exc:
        return {"statusCode": 400, "body": json.dumps({"error": str(exc)})}

    return {
        "statusCode": 200,
        "body": json.dumps({"user_id": str(user.id)}),
    }
