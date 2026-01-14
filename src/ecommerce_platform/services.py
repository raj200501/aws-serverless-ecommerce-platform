"""Business logic for the e-commerce platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from .auth import issue_token, verify_password
from .config import Settings
from .db import Database
from .repositories import (
    OrderItemRecord,
    OrderRecord,
    OrderRepository,
    ProductRecord,
    ProductRepository,
    UserRecord,
    UserRepository,
)


class EcommerceError(RuntimeError):
    """Base error for domain failures."""


class ValidationError(EcommerceError):
    """Raised for invalid input."""


class AuthenticationError(EcommerceError):
    """Raised for login failures."""


@dataclass
class EcommerceService:
    settings: Settings
    db: Database

    def __post_init__(self) -> None:
        self.users = UserRepository(self.db)
        self.products = ProductRepository(self.db)
        self.orders = OrderRepository(self.db)

    def create_user(self, email: str, username: str, password_hash: str, password_salt: str) -> UserRecord:
        if "@" not in email:
            raise ValidationError("email must contain '@'")
        if len(username) < 3:
            raise ValidationError("username must be at least 3 characters")
        if self.users.get_by_username(username):
            raise ValidationError("username already exists")
        if any(user.email == email for user in self.users.list_all()):
            raise ValidationError("email already exists")
        record = UserRecord(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=password_hash,
            password_salt=password_salt,
            created_at=datetime.utcnow(),
        )
        self.users.create(record)
        return record

    def login(self, username: str, password: str) -> tuple[UserRecord, str, int]:
        record = self.users.get_by_username(username)
        if record is None:
            raise AuthenticationError("Invalid username or password")
        if not verify_password(password, record.password_hash, record.password_salt):
            raise AuthenticationError("Invalid username or password")
        token = issue_token(str(record.id), self.settings.token_secret, self.settings.token_ttl_minutes)
        return record, token.value, self.settings.token_ttl_minutes

    def create_product(
        self,
        name: str,
        description: str,
        category: str,
        price_cents: int,
        currency: str,
    ) -> ProductRecord:
        if price_cents <= 0:
            raise ValidationError("price must be positive")
        record = ProductRecord(
            id=uuid4(),
            name=name,
            description=description,
            category=category,
            price_cents=price_cents,
            currency=currency,
            created_at=datetime.utcnow(),
        )
        self.products.create(record)
        return record

    def list_products(self) -> List[ProductRecord]:
        return self.products.list_all()

    def create_order(self, user_id: UUID, items: List[tuple[UUID, int]]) -> OrderRecord:
        if not items:
            raise ValidationError("order items cannot be empty")
        user = self.users.get_by_id(user_id)
        if user is None:
            raise ValidationError("user does not exist")
        total_cents = 0
        pending_items: List[OrderItemRecord] = []
        for product_id, quantity in items:
            product = self.products.get_by_id(product_id)
            if product is None:
                raise ValidationError(f"product {product_id} does not exist")
            total_cents += product.price_cents * quantity
            pending_items.append(
                OrderItemRecord(
                    id=uuid4(),
                    order_id=uuid4(),
                    product_id=product_id,
                    quantity=quantity,
                    price_cents=product.price_cents,
                )
            )
        order_id = uuid4()
        order_items = [
            OrderItemRecord(
                id=item.id,
                order_id=order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_cents=item.price_cents,
            )
            for item in pending_items
        ]
        order = OrderRecord(
            id=order_id,
            user_id=user_id,
            total_cents=total_cents,
            currency="USD",
            status="created",
            created_at=datetime.utcnow(),
        )
        self.orders.create(order, order_items)
        return order

    def list_orders(self, user_id: UUID) -> List[OrderRecord]:
        return self.orders.list_by_user(user_id)

    def list_order_items(self, order_id: UUID) -> List[OrderItemRecord]:
        return self.orders.list_items(order_id)

    def recommend_products(self, user_id: UUID) -> List[ProductRecord]:
        orders = self.list_orders(user_id)
        if not orders:
            products = self.products.list_all()
        else:
            categories = []
            for order in orders:
                for item in self.list_order_items(order.id):
                    product = self.products.get_by_id(item.product_id)
                    if product:
                        categories.append(product.category)
            category = max(categories, key=categories.count) if categories else None
            products = self.products.list_by_category(category) if category else self.products.list_all()
        return products[: self.settings.recommendations_per_user]
