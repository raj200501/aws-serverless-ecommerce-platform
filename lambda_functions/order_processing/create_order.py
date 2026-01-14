import json
from pathlib import Path
import sys
from uuid import UUID

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import EcommerceService, ValidationError


def lambda_handler(event, context):
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    try:
        order = service.create_order(
            user_id=UUID(event["user_id"]),
            items=[(UUID(item["product_id"]), int(item["quantity"])) for item in event["items"]],
        )
    except (ValidationError, KeyError, ValueError) as exc:
        return {"statusCode": 400, "body": json.dumps({"error": str(exc)})}

    return {
        "statusCode": 200,
        "body": json.dumps({"order_id": str(order.id), "total_cents": order.total_cents}),
    }
