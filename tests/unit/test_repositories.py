from __future__ import annotations

import unittest
from datetime import datetime
from uuid import uuid4

from ecommerce_platform.repositories import (
    OrderItemRecord,
    OrderRecord,
    OrderRepository,
    ProductRecord,
    ProductRepository,
    UserRecord,
    UserRepository,
)
from tests.helpers import build_test_environment


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = build_test_environment()

    def tearDown(self) -> None:
        self.env.cleanup()

    def test_user_repository_round_trip(self) -> None:
        repo = UserRepository(self.env.service.db)
        record = UserRecord(
            id=uuid4(),
            email="a@example.com",
            username="alpha",
            password_hash="hash",
            password_salt="salt",
            created_at=datetime.utcnow(),
        )
        repo.create(record)
        self.assertIsNotNone(repo.get_by_username("alpha"))
        self.assertIsNotNone(repo.get_by_id(record.id))
        self.assertTrue(repo.list_all())

    def test_product_repository_round_trip(self) -> None:
        repo = ProductRepository(self.env.service.db)
        record = ProductRecord(
            id=uuid4(),
            name="Pack",
            description="Travel pack",
            category="outdoor",
            price_cents=1999,
            currency="USD",
            created_at=datetime.utcnow(),
        )
        repo.create(record)
        self.assertIsNotNone(repo.get_by_id(record.id))
        self.assertTrue(repo.list_all())
        self.assertTrue(repo.list_by_category("outdoor"))

    def test_order_repository_round_trip(self) -> None:
        order_repo = OrderRepository(self.env.service.db)
        order = OrderRecord(
            id=uuid4(),
            user_id=uuid4(),
            total_cents=1000,
            currency="USD",
            status="created",
            created_at=datetime.utcnow(),
        )
        items = [
            OrderItemRecord(
                id=uuid4(),
                order_id=order.id,
                product_id=uuid4(),
                quantity=1,
                price_cents=1000,
            )
        ]
        order_repo.create(order, items)
        self.assertTrue(order_repo.list_by_user(order.user_id))
        self.assertTrue(order_repo.list_items(order.id))


if __name__ == "__main__":
    unittest.main()
