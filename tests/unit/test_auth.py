from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from ecommerce_platform.auth import hash_password, issue_token, verify_password


class AuthTests(unittest.TestCase):
    def test_hash_password_round_trip(self) -> None:
        digest, salt = hash_password("supersecret")
        self.assertTrue(digest)
        self.assertTrue(salt)
        self.assertTrue(verify_password("supersecret", digest, salt))
        self.assertFalse(verify_password("wrong", digest, salt))

    def test_issue_token_has_ttl(self) -> None:
        token = issue_token("user-1", "secret", 10)
        self.assertTrue(token.value)
        self.assertGreater(token.expires_at, datetime.utcnow())
        self.assertLessEqual(token.expires_at, datetime.utcnow() + timedelta(minutes=10, seconds=5))


if __name__ == "__main__":
    unittest.main()
