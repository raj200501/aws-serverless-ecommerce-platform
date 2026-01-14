"""Authentication helpers for local mode."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple


def hash_password(password: str, salt: str | None = None) -> Tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return digest, salt


def verify_password(password: str, digest: str, salt: str) -> bool:
    expected, _ = hash_password(password, salt)
    return secrets.compare_digest(expected, digest)


@dataclass(frozen=True)
class Token:
    value: str
    expires_at: datetime


def issue_token(user_id: str, secret: str, ttl_minutes: int) -> Token:
    token_seed = f"{user_id}:{secret}:{secrets.token_hex(8)}"
    token = hashlib.sha256(token_seed.encode("utf-8")).hexdigest()
    return Token(value=token, expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes))
