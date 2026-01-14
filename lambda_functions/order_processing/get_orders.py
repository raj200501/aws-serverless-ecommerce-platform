import json
from pathlib import Path
import sys
from uuid import UUID

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db
from ecommerce_platform.services import EcommerceService


def lambda_handler(event, context):
    settings = load_settings()
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    user_id = UUID(event["user_id"])
    orders = service.list_orders(user_id)
    response = []
    for order in orders:
        items = service.list_order_items(order.id)
        response.append(
            {
                "id": str(order.id),
                "user_id": str(order.user_id),
                "status": order.status,
                "total_cents": order.total_cents,
                "currency": order.currency,
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "product_id": str(item.product_id),
                        "quantity": item.quantity,
                        "price_cents": item.price_cents,
                    }
                    for item in items
                ],
            }
        )

    return {"statusCode": 200, "body": json.dumps(response)}
