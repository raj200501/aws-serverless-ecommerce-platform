from __future__ import annotations

import unittest

from tests.helpers import build_test_environment, json_request, run_test_server


class SmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = build_test_environment()

    def tearDown(self) -> None:
        self.env.cleanup()

    def test_smoke_flow(self) -> None:
        with run_test_server(self.env) as base_url:
            status, payload = json_request("GET", f"{base_url}/health")
            self.assertEqual(status, 200)
            self.assertEqual(payload["status"], "ok")

            status, payload = json_request(
                "POST",
                f"{base_url}/auth/signup",
                {
                    "email": "demo@example.com",
                    "username": "demo",
                    "password": "password123",
                },
            )
            self.assertEqual(status, 200)
            user_id = payload["id"]

            status, payload = json_request(
                "POST",
                f"{base_url}/auth/login",
                {"username": "demo", "password": "password123"},
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload["user_id"], user_id)

            status, payload = json_request(
                "POST",
                f"{base_url}/products",
                {
                    "name": "Trail Backpack",
                    "description": "Lightweight pack for day hikes.",
                    "category": "outdoor",
                    "price_cents": 7800,
                    "currency": "USD",
                },
            )
            self.assertEqual(status, 200)
            product_id = payload["id"]

            status, payload = json_request("GET", f"{base_url}/products")
            self.assertEqual(status, 200)
            self.assertTrue(any(item["id"] == product_id for item in payload))

            status, payload = json_request(
                "POST",
                f"{base_url}/orders",
                {
                    "user_id": user_id,
                    "items": [{"product_id": product_id, "quantity": 2}],
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload["total_cents"], 15600)

            status, payload = json_request("GET", f"{base_url}/orders/{user_id}")
            self.assertEqual(status, 200)
            self.assertTrue(payload)

            status, payload = json_request(
                "GET", f"{base_url}/recommendations/{user_id}"
            )
            self.assertEqual(status, 200)
            self.assertTrue(payload["products"])


if __name__ == "__main__":
    unittest.main()
