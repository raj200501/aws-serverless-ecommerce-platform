"""HTTP-agnostic API layer.

This module provides a lightweight request handler that can be used by both the
HTTP server and unit tests without requiring third-party frameworks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import UUID

from .auth import hash_password
from .config import Settings, load_settings
from .db import init_db
from .services import AuthenticationError, EcommerceService, ValidationError


@dataclass
class ApiResponse:
    status_code: int
    body: bytes
    headers: Dict[str, str]


class EcommerceAPI:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or load_settings()
        self.db = init_db(self.settings)
        self.service = EcommerceService(settings=self.settings, db=self.db)

    def handle(self, method: str, path: str, body: Optional[str]) -> ApiResponse:
        try:
            return self._dispatch(method.upper(), path, body)
        except ValidationError as exc:
            return self._json_response(400, {"error": str(exc)})
        except AuthenticationError as exc:
            return self._json_response(401, {"error": str(exc)})
        except ValueError as exc:
            return self._json_response(400, {"error": str(exc)})
        except KeyError as exc:
            return self._json_response(400, {"error": f"missing field {exc}"})

    def _dispatch(self, method: str, path: str, body: Optional[str]) -> ApiResponse:
        if path == "/health" and method == "GET":
            return self._json_response(200, {"status": "ok", "environment": self.settings.env})

        if path == "/auth/signup" and method == "POST":
            payload = self._parse_json(body)
            password_hash, salt = hash_password(payload["password"])
            user = self.service.create_user(
                email=payload["email"],
                username=payload["username"],
                password_hash=password_hash,
                password_salt=salt,
            )
            return self._json_response(
                200,
                {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "created_at": user.created_at.isoformat(),
                },
            )

        if path == "/auth/login" and method == "POST":
            payload = self._parse_json(body)
            user, token, ttl = self.service.login(payload["username"], payload["password"])
            return self._json_response(
                200,
                {"user_id": str(user.id), "token": token, "expires_in_minutes": ttl},
            )

        if path == "/products" and method == "POST":
            payload = self._parse_json(body)
            product = self.service.create_product(
                name=payload["name"],
                description=payload["description"],
                category=payload["category"],
                price_cents=int(payload["price_cents"]),
                currency=payload.get("currency", "USD"),
            )
            return self._json_response(
                200,
                {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "category": product.category,
                    "price_cents": product.price_cents,
                    "currency": product.currency,
                    "created_at": product.created_at.isoformat(),
                },
            )

        if path == "/products" and method == "GET":
            products = self.service.list_products()
            return self._json_response(
                200,
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
                ],
            )

        if path == "/orders" and method == "POST":
            payload = self._parse_json(body)
            order = self.service.create_order(
                user_id=self._parse_uuid(payload["user_id"], "user_id"),
                items=[
                    (self._parse_uuid(item["product_id"], "product_id"), int(item["quantity"]))
                    for item in payload["items"]
                ],
            )
            items = self.service.list_order_items(order.id)
            return self._json_response(
                200,
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
                },
            )

        if path.startswith("/orders/") and method == "GET":
            user_id = self._parse_uuid(path.split("/", 2)[2], "user_id")
            orders = self.service.list_orders(user_id)
            response = []
            for order in orders:
                items = self.service.list_order_items(order.id)
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
            return self._json_response(200, response)

        if path.startswith("/recommendations/") and method == "GET":
            user_id = self._parse_uuid(path.split("/", 2)[2], "user_id")
            products = self.service.recommend_products(user_id)
            return self._json_response(
                200,
                {
                    "user_id": str(user_id),
                    "products": [
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
                    ],
                },
            )

        return self._json_response(404, {"error": "Not Found"})

    def _parse_uuid(self, value: str, field: str) -> UUID:
        try:
            return UUID(value)
        except ValueError as exc:
            raise ValueError(f"invalid {field}") from exc

    def _parse_json(self, body: Optional[str]) -> Dict[str, Any]:
        if not body:
            raise ValueError("request body is required")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError("invalid JSON payload") from exc
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
        return payload

    def _json_response(self, status_code: int, payload: Any) -> ApiResponse:
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(body)),
        }
        return ApiResponse(status_code=status_code, body=body, headers=headers)


def create_api(settings: Settings | None = None) -> EcommerceAPI:
    return EcommerceAPI(settings=settings)
