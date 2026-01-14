# Architecture Overview

This document explains how the local serverless e-commerce platform is wired
internally. It is intentionally verbose so a new maintainer can understand the
data flow without hunting across modules.

## Goals

1. Keep the local runtime deterministic, repeatable, and dependency-light.
2. Preserve the spirit of the AWS serverless design while enabling offline
   development.
3. Provide clear seams for swapping the SQLite persistence layer with AWS
   services later.

## Component Map

| Area | Module | Purpose |
| --- | --- | --- |
| API | `src/ecommerce_platform/api.py` | HTTP-agnostic request handler. |
| Config | `src/ecommerce_platform/config.py` | Environment parsing and configuration defaults. |
| Storage | `src/ecommerce_platform/db.py` | SQLite initialization and schema management. |
| Domain | `src/ecommerce_platform/services.py` | Core business logic (users, products, orders). |
| Data access | `src/ecommerce_platform/repositories.py` | SQL queries for CRUD operations. |
| Auth | `src/ecommerce_platform/auth.py` | Password hashing and token issuance. |
| CLI | `src/ecommerce_platform/cli.py` | One-off commands for seeding and setup. |
| Scripts | `scripts/run.sh` | Local run command with seed data. |
| Scripts | `scripts/verify.sh` | Deterministic verification entrypoint. |

## Runtime Diagram (Text)

```
Client
  │
  ▼
HTTP Router ──► EcommerceService ──► Repository ──► SQLite
  │                    │
  ▼                    ▼
API responses      Auth helpers
```

## Data Model

### Users

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID (TEXT) | Primary key. |
| `email` | TEXT | Unique. |
| `username` | TEXT | Unique. |
| `password_hash` | TEXT | PBKDF2 hash. |
| `password_salt` | TEXT | Random salt. |
| `created_at` | TEXT | ISO-8601 timestamp. |

### Products

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID (TEXT) | Primary key. |
| `name` | TEXT | Display name. |
| `description` | TEXT | Rich description. |
| `category` | TEXT | Used by recommendations. |
| `price_cents` | INTEGER | Stored in cents to avoid floating point drift. |
| `currency` | TEXT | 3-letter ISO currency code. |
| `created_at` | TEXT | ISO-8601 timestamp. |

### Orders

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID (TEXT) | Primary key. |
| `user_id` | TEXT | Foreign key to `users`. |
| `total_cents` | INTEGER | Sum of order items. |
| `currency` | TEXT | 3-letter ISO code. |
| `status` | TEXT | `created`, `processing`, `completed`, etc. |
| `created_at` | TEXT | ISO-8601 timestamp. |

### Order Items

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID (TEXT) | Primary key. |
| `order_id` | TEXT | Foreign key to `orders`. |
| `product_id` | TEXT | Foreign key to `products`. |
| `quantity` | INTEGER | Quantity purchased. |
| `price_cents` | INTEGER | Price snapshot at order time. |

## Request Flows

### Signup

1. `POST /auth/signup` is invoked with user details.
2. The API hashes the password using PBKDF2.
3. `EcommerceService.create_user` validates the input and stores the record.
4. The API responds with the new user.

### Login

1. `POST /auth/login` is invoked with credentials.
2. `EcommerceService.login` validates the password and issues a token.
3. The API responds with the token and TTL.

### Product Creation

1. `POST /products` is invoked.
2. `EcommerceService.create_product` validates fields and writes to SQLite.
3. The API returns the created product with the generated ID.

### Order Creation

1. `POST /orders` is invoked with a user ID and list of items.
2. The service verifies the user exists.
3. Each product is fetched for pricing and validation.
4. `OrderRepository.create` writes the order and items in one transaction.
5. The API returns the order + items.

### Recommendations

1. `GET /recommendations/{user_id}` is invoked.
2. The service examines prior orders and extracts preferred categories.
3. Products are filtered by the top category.
4. The list is truncated to `RECOMMENDATIONS_PER_USER`.

## Extending to AWS

The local platform keeps a consistent shape with the original serverless intent
and can be swapped with AWS services using the seams below:

- Replace `repositories.py` with DynamoDB implementations.
- Replace `auth.py` with Cognito-based token validation.
- Replace `scripts/run.sh` with a Serverless Framework deployment.

## Configuration Defaults

| Variable | Default | Description |
| --- | --- | --- |
| `APP_ENV` | `local` | Environment label for logging. |
| `DATABASE_URL` | `sqlite:///./data/ecommerce.db` | SQLite file location. |
| `TOKEN_SECRET` | `local-dev-secret` | Secret used to sign tokens. |
| `TOKEN_TTL_MINUTES` | `60` | Token expiration window. |
| `RECOMMENDATIONS_PER_USER` | `3` | Number of products to return. |
| `SEED_DEMO` | `true` | Seed demo data when running locally. |

## Operational Notes

- SQLite is chosen for local determinism; it requires no external service.
- All writes are wrapped in transactions via `db_session`.
- Password hashing uses PBKDF2 with 120k iterations.
- Token issuance is deterministic based on a shared secret for local use.
- The API is HTTP-agnostic, allowing both the server and tests to reuse the same
  handler without third-party frameworks.

## Directory Layout

```
.
├── api_gateway/           # API Gateway contract (OpenAPI/Swagger)
├── cognito/               # Local auth seeding script
├── data/                  # Runtime data (SQLite + pseudo S3 bucket)
├── docs/                  # Long-form documentation
├── dynamodb/              # Local database bootstrap (SQLite)
├── lambda_functions/      # Lambda-compatible entrypoints
├── scripts/               # run/verify helpers
├── src/                   # Python package source
└── tests/                 # Unit + integration tests
```

## Design Decisions

### Why a repository layer?

The repository layer exists to isolate data access. This gives the service layer
an in-memory interface and makes it easier to port to DynamoDB later. The
repository is small and focused but central to future AWS work.

### Why store prices in cents?

Floating point math can introduce rounding errors. Storing integer cents avoids
precision problems and makes totals reproducible in tests and smoke checks.

### Why avoid external .env libraries?

While packages like python-dotenv are convenient, they introduce runtime
variability. A small parser keeps the project deterministic for CI and offline
usage.

### Why use a minimal HTTP server?

Using the standard library keeps the runtime fully offline and deterministic,
which is essential for repeatable CI runs in constrained environments.

## Security Notes

This local implementation is not intended for production. The token and password
strategy are sufficient for local demos but not hardened for a public service.
When moving to AWS, you should:

- Enable Cognito with MFA.
- Store secrets in AWS Secrets Manager.
- Use AWS WAF in front of API Gateway.
- Implement rate limiting and audit logging.

## Upgrade Checklist

- [ ] Replace SQLite with DynamoDB adapters.
- [ ] Replace token issuance with Cognito JWTs.
- [ ] Move data seeding to a data migration script.
- [ ] Update the CI pipeline to run end-to-end tests against deployed stacks.
