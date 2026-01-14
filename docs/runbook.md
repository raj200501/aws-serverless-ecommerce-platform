# Operations Runbook

This runbook describes how to operate the local e-commerce platform in a
repeatable manner.

## Startup Checklist

1. Confirm Python 3.11 is installed.
2. Ensure the repository root is the current working directory.
3. Copy `.env.example` to `.env` if you need custom settings.
4. Start the service:
   ```bash
   ./scripts/run.sh
   ```

## Verifying the Service

Use these commands to verify the service is healthy:

```bash
curl http://localhost:8000/health
```

Expect:

```json
{"status": "ok", "environment": "local"}
```

## Data Management

### Resetting Local Data

To reset all local data:

```bash
rm -f data/ecommerce.db
```

Then re-run:

```bash
./scripts/run.sh
```

### Seeding Data Manually

If you want to seed demo data without starting the server:

```bash
PYTHONPATH=src python -m ecommerce_platform.cli seed
```

## Observability

The local app emits standard output logs from Uvicorn. For more detailed
logging, set:

```bash
LOG_LEVEL=debug ./scripts/run.sh
```

## API Contract Changes

If you need to adjust endpoints:

1. Update `src/ecommerce_platform/api.py`.
2. Update `api_gateway/api.yaml`.
3. Update `docs/api.md`.
4. Update tests in `tests/integration/test_smoke.py`.

## AWS Migration Notes

This repo keeps the AWS serverless configuration for future use. When
transitioning to AWS:

1. Replace the SQLite repositories with DynamoDB adapters.
2. Update Serverless Framework configuration in `infrastructure/serverless.yml`.
3. Add AWS credentials for deployment.
4. Expand CI to include deployed integration tests.
