# API Reference

This API reference captures the local development contract for the e-commerce
platform. The endpoints mirror the AWS-style flows and are suitable for smoke
checks.

## Base URL

```
http://localhost:8000
```

## Authentication

The local platform issues a deterministic token when a user logs in. The token
is not currently required to call other endpoints, but it is returned so
clients can practice handling authentication.

## Health

### `GET /health`

Returns an `ok` status and the current environment.

Example:

```
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "environment": "local"
}
```

## Signup

### `POST /auth/signup`

Create a new user.

Request body:

```json
{
  "email": "demo@example.com",
  "username": "demo",
  "password": "password123"
}
```

Response:

```json
{
  "id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
  "email": "demo@example.com",
  "username": "demo",
  "created_at": "2024-01-01T10:00:00.000Z"
}
```

Errors:

- `400` when the username/email already exists.
- `400` when the email is missing `@`.

## Login

### `POST /auth/login`

Request body:

```json
{
  "username": "demo",
  "password": "password123"
}
```

Response:

```json
{
  "user_id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
  "token": "19f9939b3...",
  "expires_in_minutes": 60
}
```

Errors:

- `401` when credentials are invalid.

## Products

### `POST /products`

Request body:

```json
{
  "name": "Trail Backpack",
  "description": "Lightweight pack for day hikes and commutes.",
  "category": "outdoor",
  "price_cents": 7900,
  "currency": "USD"
}
```

Response:

```json
{
  "id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c",
  "name": "Trail Backpack",
  "description": "Lightweight pack for day hikes and commutes.",
  "category": "outdoor",
  "price_cents": 7900,
  "currency": "USD",
  "created_at": "2024-01-01T10:00:00.000Z"
}
```

### `GET /products`

Response:

```json
[
  {
    "id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c",
    "name": "Trail Backpack",
    "description": "Lightweight pack for day hikes and commutes.",
    "category": "outdoor",
    "price_cents": 7900,
    "currency": "USD",
    "created_at": "2024-01-01T10:00:00.000Z"
  }
]
```

## Orders

### `POST /orders`

Request body:

```json
{
  "user_id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
  "items": [
    { "product_id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c", "quantity": 2 }
  ]
}
```

Response:

```json
{
  "id": "f2a62ab2-1b29-44b5-8aa8-4dcf92a9c070",
  "user_id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
  "status": "created",
  "total_cents": 15800,
  "currency": "USD",
  "created_at": "2024-01-01T10:00:00.000Z",
  "items": [
    { "product_id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c", "quantity": 2, "price_cents": 7900 }
  ]
}
```

### `GET /orders/{user_id}`

Response:

```json
[
  {
    "id": "f2a62ab2-1b29-44b5-8aa8-4dcf92a9c070",
    "user_id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
    "status": "created",
    "total_cents": 15800,
    "currency": "USD",
    "created_at": "2024-01-01T10:00:00.000Z",
    "items": [
      { "product_id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c", "quantity": 2, "price_cents": 7900 }
    ]
  }
]
```

## Recommendations

### `GET /recommendations/{user_id}`

Response:

```json
{
  "user_id": "e2b4a4b3-2b1a-4d8a-b64b-1dcab52d89f3",
  "products": [
    {
      "id": "8e6f6b63-bc85-4d2a-9cd9-d684b4a9c59c",
      "name": "Trail Backpack",
      "description": "Lightweight pack for day hikes and commutes.",
      "category": "outdoor",
      "price_cents": 7900,
      "currency": "USD",
      "created_at": "2024-01-01T10:00:00.000Z"
    }
  ]
}
```

## Example Flow

The following sequence mirrors the integration test in `tests/integration`:

1. Call `/health` to confirm the service is running.
2. `POST /auth/signup` with a demo user.
3. `POST /auth/login` with that user.
4. `POST /products` to add a product.
5. `POST /orders` to create an order with the product.
6. `GET /recommendations/{user_id}` to see category-based results.

## OpenAPI Reference

The local API contract is documented in `api_gateway/api.yaml`. It mirrors the
routes implemented by `src/ecommerce_platform/api.py` and can be imported into
OpenAPI tooling if needed.
