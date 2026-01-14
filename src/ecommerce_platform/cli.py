"""Command line utilities for local management."""

from __future__ import annotations

import argparse
from pathlib import Path

from .auth import hash_password
from .config import load_settings
from .db import init_db
from .services import EcommerceService

SAMPLE_PRODUCTS = [
    {
        "name": "Trail Backpack",
        "description": "Lightweight pack for day hikes and commutes.",
        "category": "outdoor",
        "price_cents": 7900,
        "currency": "USD",
    },
    {
        "name": "City Sneaker",
        "description": "Durable sneaker with breathable lining.",
        "category": "footwear",
        "price_cents": 12900,
        "currency": "USD",
    },
    {
        "name": "Travel Mug",
        "description": "Insulated mug that keeps drinks hot for hours.",
        "category": "kitchen",
        "price_cents": 2400,
        "currency": "USD",
    },
    {
        "name": "Mountain Jacket",
        "description": "Weatherproof shell with removable liner.",
        "category": "outdoor",
        "price_cents": 18400,
        "currency": "USD",
    },
]


def _seed_data(service: EcommerceService) -> None:
    password_hash, salt = hash_password("password123")
    service.create_user(
        email="demo@example.com",
        username="demo",
        password_hash=password_hash,
        password_salt=salt,
    )
    for product in SAMPLE_PRODUCTS:
        service.create_product(**product)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local e-commerce platform utilities")
    parser.add_argument(
        "command",
        choices=["init-db", "seed"],
        help="Action to run",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Optional path to .env file",
    )
    args = parser.parse_args()

    settings = load_settings(args.env_file)
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)

    if args.command == "init-db":
        print(f"Initialized database at {settings.sqlite_path}")
    elif args.command == "seed":
        _seed_data(service)
        print("Seeded demo user and products")


if __name__ == "__main__":
    main()
