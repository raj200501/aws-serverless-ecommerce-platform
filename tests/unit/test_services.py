from __future__ import annotations

import unittest
from uuid import UUID

from ecommerce_platform.auth import hash_password
from ecommerce_platform.services import AuthenticationError, ValidationError
from tests.helpers import build_test_environment


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = build_test_environment()

    def tearDown(self) -> None:
        self.env.cleanup()

    def test_create_user(self) -> None:
        password_hash, salt = hash_password("password123")
        user = self.env.service.create_user(
            email="user@example.com",
            username="user",
            password_hash=password_hash,
            password_salt=salt,
        )
        self.assertEqual(user.email, "user@example.com")

    def test_create_user_duplicate_username(self) -> None:
        password_hash, salt = hash_password("password123")
        self.env.service.create_user(
            email="user@example.com",
            username="user",
            password_hash=password_hash,
            password_salt=salt,
        )
        with self.assertRaises(ValidationError):
            self.env.service.create_user(
                email="another@example.com",
                username="user",
                password_hash=password_hash,
                password_salt=salt,
            )

    def test_login(self) -> None:
        password_hash, salt = hash_password("password123")
        self.env.service.create_user(
            email="user@example.com",
            username="user",
            password_hash=password_hash,
            password_salt=salt,
        )
        user, token, ttl = self.env.service.login("user", "password123")
        self.assertEqual(user.username, "user")
        self.assertTrue(token)
        self.assertEqual(ttl, 15)

    def test_login_invalid(self) -> None:
        with self.assertRaises(AuthenticationError):
            self.env.service.login("missing", "password")

    def test_create_order_validation(self) -> None:
        with self.assertRaises(ValidationError):
            self.env.service.create_order(UUID(int=0), [])

    def test_recommendations_without_orders(self) -> None:
        password_hash, salt = hash_password("password123")
        user = self.env.service.create_user(
            email="user@example.com",
            username="user",
            password_hash=password_hash,
            password_salt=salt,
        )
        product = self.env.service.create_product(
            name="Bottle",
            description="Steel bottle",
            category="kitchen",
            price_cents=1200,
            currency="USD",
        )
        recommendations = self.env.service.recommend_products(user.id)
        self.assertTrue(recommendations)
        self.assertEqual(recommendations[0].id, product.id)


if __name__ == "__main__":
    unittest.main()
