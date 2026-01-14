import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import AuthenticationError, EcommerceService


def lambda_handler(event, context):
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    username = event["username"]
    password = event["password"]

    try:
        user, token, ttl = service.login(username, password)
    except AuthenticationError as exc:
        return {"statusCode": 401, "body": json.dumps({"error": str(exc)})}

    return {
        "statusCode": 200,
        "body": json.dumps({"user_id": str(user.id), "token": token, "expires_in_minutes": ttl}),
    }
