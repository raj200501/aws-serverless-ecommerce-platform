import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import EcommerceService


def lambda_handler(event, context):
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    products = service.list_products()
    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "category": product.category,
                    "price_cents": product.price_cents,
                    "currency": product.currency,
                    "created_at": product.created_at.isoformat(),
                }
                for product in products
            ]
        ),
    }
