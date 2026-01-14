import json
from pathlib import Path
import sys

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
        product = service.create_product(
            name=event["name"],
            description=event["description"],
            category=event["category"],
            price_cents=int(event["price_cents"]),
            currency=event.get("currency", "USD"),
        )
    except ValidationError as exc:
        return {"statusCode": 400, "body": json.dumps({"error": str(exc)})}

    return {
        "statusCode": 200,
        "body": json.dumps({"product_id": str(product.id)}),
    }
