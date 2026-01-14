# Serverless E-Commerce Platform (Local-First)

This repository contains a local-first implementation of a serverless
E-Commerce platform inspired by AWS services. It provides a deterministic,
fully runnable environment that mirrors the AWS workflows (authentication,
products, orders, and recommendations) without requiring AWS credentials.

The AWS resources are still documented and can be re-enabled later, but the
README and tooling focus on a reproducible local runtime.

## Features

- User Authentication (local auth with Cognito-compatible flows)
- Product Management (local HTTP server + SQLite)
- Order Processing (local HTTP server + SQLite)
- Recommendation System (category-based)
- Infrastructure as Code (Serverless Framework config retained for future use)
- Deterministic tests and CI verification

## Repository Layout

```
.
├── api_gateway/           # OpenAPI contract
├── cognito/               # Local auth seeding script
├── dynamodb/              # Local DB bootstrap
├── infrastructure/        # Serverless Framework config
├── lambda_functions/      # Lambda-compatible entrypoints
├── scripts/               # run/verify helpers
├── src/                   # Python application package
├── tests/                 # Unit + integration tests
└── docs/                  # Extended docs
```

## Prerequisites

- Python 3.11+

## Verified Quickstart

These commands were executed successfully in this repository and are guaranteed
by CI:

```bash
./scripts/run.sh
```

The service will start at `http://localhost:8000`.

### Quick API Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "environment": "local"}
```

## Verified Verification

The canonical verification entrypoint is:

```bash
./scripts/verify.sh
```

This command runs unit tests and executes an integration smoke test that
covers signup, login, product creation, order creation, and recommendations.

## Local Setup Details

### Initialize the Database

```bash
python dynamodb/setup_tables.py
```

### Seed a Demo User

```bash
python cognito/setup_cognito.py
```

### Create Local Buckets

```bash
python s3_buckets/setup_buckets.py
```

### Run the API

```bash
./scripts/run.sh
```

The run script will initialize the SQLite database and seed demo data unless
`SEED_DEMO=false` is set.

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | GET | Health check |
| `/auth/signup` | POST | Create a user |
| `/auth/login` | POST | Login and receive token |
| `/products` | GET | List products |
| `/products` | POST | Create product |
| `/orders` | POST | Create order |
| `/orders/{user_id}` | GET | List orders for user |
| `/recommendations/{user_id}` | GET | Get recommendations |

For detailed payloads see:

- `docs/api.md`
- `api_gateway/api.yaml`

## Configuration

Configuration is loaded from `.env` (if present) and environment variables.
Copy the template and modify as needed:

```bash
cp .env.example .env
```

Key settings:

- `DATABASE_URL` (default `sqlite:///./data/ecommerce.db`)
- `TOKEN_SECRET` (used for local token issuance)
- `RECOMMENDATIONS_PER_USER`
- `SEED_DEMO`
- `PORT`

More details are in `docs/configuration.md`.

## Demo Data

The demo seed includes:

- User: `demo` / `password123`
- Four sample products across categories

You can re-seed at any time with:

```bash
PYTHONPATH=src python -m ecommerce_platform.cli seed
```

## AWS Deployment (Optional)

The original AWS Serverless Framework configuration is retained under
`infrastructure/serverless.yml`. It is **not executed in local verification**
because AWS credentials are not required for this repository to run. If you
want to deploy to AWS, you will need to:

1. Replace SQLite repositories with DynamoDB implementations.
2. Configure Cognito User Pools.
3. Provide AWS credentials and run `serverless deploy`.

## Documentation

- `docs/architecture.md` - system overview and data model
- `docs/api.md` - API examples
- `docs/testing.md` - test strategy
- `docs/runbook.md` - operational runbook
- `docs/troubleshooting.md` - common issues
- `docs/faq.md` - frequently asked questions

## License

This project is licensed under the MIT License.
