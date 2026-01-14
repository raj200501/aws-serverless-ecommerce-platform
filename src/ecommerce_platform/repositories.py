"""Repository layer for SQLite persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional
from uuid import UUID

from .db import Database, db_session


@dataclass(frozen=True)
class UserRecord:
    id: UUID
    email: str
    username: str
    password_hash: str
    password_salt: str
    created_at: datetime


@dataclass(frozen=True)
class ProductRecord:
    id: UUID
    name: str
    description: str
    category: str
    price_cents: int
    currency: str
    created_at: datetime


@dataclass(frozen=True)
class OrderItemRecord:
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price_cents: int


@dataclass(frozen=True)
class OrderRecord:
    id: UUID
    user_id: UUID
    total_cents: int
    currency: str
    status: str
    created_at: datetime


class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def create(self, record: UserRecord) -> None:
        with db_session(self._db) as conn:
            conn.execute(
                """
                INSERT INTO users (id, email, username, password_hash, password_salt, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.id),
                    record.email,
                    record.username,
                    record.password_hash,
                    record.password_salt,
                    record.created_at.isoformat(),
                ),
            )

    def get_by_username(self, username: str) -> Optional[UserRecord]:
        with db_session(self._db) as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
        return _row_to_user(row) if row else None

    def get_by_id(self, user_id: UUID) -> Optional[UserRecord]:
        with db_session(self._db) as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (str(user_id),)).fetchone()
        return _row_to_user(row) if row else None

    def list_all(self) -> List[UserRecord]:
        with db_session(self._db) as conn:
            rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
        return [_row_to_user(row) for row in rows]


class ProductRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def create(self, record: ProductRecord) -> None:
        with db_session(self._db) as conn:
            conn.execute(
                """
                INSERT INTO products (id, name, description, category, price_cents, currency, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.id),
                    record.name,
                    record.description,
                    record.category,
                    record.price_cents,
                    record.currency,
                    record.created_at.isoformat(),
                ),
            )

    def list_all(self) -> List[ProductRecord]:
        with db_session(self._db) as conn:
            rows = conn.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()
        return [_row_to_product(row) for row in rows]

    def get_by_id(self, product_id: UUID) -> Optional[ProductRecord]:
        with db_session(self._db) as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE id = ?", (str(product_id),)
            ).fetchone()
        return _row_to_product(row) if row else None

    def list_by_category(self, category: str) -> List[ProductRecord]:
        with db_session(self._db) as conn:
            rows = conn.execute(
                "SELECT * FROM products WHERE category = ? ORDER BY created_at DESC",
                (category,),
            ).fetchall()
        return [_row_to_product(row) for row in rows]


class OrderRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def create(self, order: OrderRecord, items: Iterable[OrderItemRecord]) -> None:
        with db_session(self._db) as conn:
            conn.execute(
                """
                INSERT INTO orders (id, user_id, total_cents, currency, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(order.id),
                    str(order.user_id),
                    order.total_cents,
                    order.currency,
                    order.status,
                    order.created_at.isoformat(),
                ),
            )
            conn.executemany(
                """
                INSERT INTO order_items (id, order_id, product_id, quantity, price_cents)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        str(item.id),
                        str(item.order_id),
                        str(item.product_id),
                        item.quantity,
                        item.price_cents,
                    )
                    for item in items
                ],
            )

    def list_by_user(self, user_id: UUID) -> List[OrderRecord]:
        with db_session(self._db) as conn:
            rows = conn.execute(
                "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (str(user_id),),
            ).fetchall()
        return [_row_to_order(row) for row in rows]

    def list_items(self, order_id: UUID) -> List[OrderItemRecord]:
        with db_session(self._db) as conn:
            rows = conn.execute(
                "SELECT * FROM order_items WHERE order_id = ?",
                (str(order_id),),
            ).fetchall()
        return [_row_to_order_item(row) for row in rows]



def _row_to_user(row) -> UserRecord:
    return UserRecord(
        id=UUID(row["id"]),
        email=row["email"],
        username=row["username"],
        password_hash=row["password_hash"],
        password_salt=row["password_salt"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_product(row) -> ProductRecord:
    return ProductRecord(
        id=UUID(row["id"]),
        name=row["name"],
        description=row["description"],
        category=row["category"],
        price_cents=row["price_cents"],
        currency=row["currency"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_order(row) -> OrderRecord:
    return OrderRecord(
        id=UUID(row["id"]),
        user_id=UUID(row["user_id"]),
        total_cents=row["total_cents"],
        currency=row["currency"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_order_item(row) -> OrderItemRecord:
    return OrderItemRecord(
        id=UUID(row["id"]),
        order_id=UUID(row["order_id"]),
        product_id=UUID(row["product_id"]),
        quantity=row["quantity"],
        price_cents=row["price_cents"],
    )
