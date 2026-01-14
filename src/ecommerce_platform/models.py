"""Dataclasses representing API payloads.

These models are intentionally lightweight to avoid external dependencies while
still documenting the expected shapes of payloads used by the API.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class UserCreateRequest:
    email: str
    username: str
    password: str


@dataclass
class UserResponse:
    id: UUID
    email: str
    username: str
    created_at: datetime


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class LoginResponse:
    user_id: UUID
    token: str
    expires_in_minutes: int


@dataclass
class ProductCreateRequest:
    name: str
    description: str
    category: str
    price_cents: int
    currency: str


@dataclass
class ProductResponse:
    id: UUID
    name: str
    description: str
    category: str
    price_cents: int
    currency: str
    created_at: datetime


@dataclass
class OrderItemCreate:
    product_id: UUID
    quantity: int


@dataclass
class OrderCreateRequest:
    user_id: UUID
    items: List[OrderItemCreate]


@dataclass
class OrderItemResponse:
    product_id: UUID
    quantity: int
    price_cents: int


@dataclass
class OrderResponse:
    id: UUID
    user_id: UUID
    status: str
    total_cents: int
    currency: str
    created_at: datetime
    items: List[OrderItemResponse]


@dataclass
class RecommendationResponse:
    user_id: UUID
    products: List[ProductResponse]
