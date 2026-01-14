# Development Guide

This guide covers common development tasks for the local e-commerce platform.

## Setup

No third-party dependencies are required for local development beyond Python
3.11+.

## Running the API

```bash
./scripts/run.sh
```

## Running Tests

```bash
./scripts/verify.sh
```

## Code Layout

- `src/ecommerce_platform/` holds the Python package.
- `lambda_functions/` holds Lambda-compatible wrappers.
- `scripts/` contains the canonical run and verify commands.
- `docs/` contains reference documentation.

## Common Tasks

### Adding a New Endpoint

1. Add a new route in `src/ecommerce_platform/api.py`.
2. Add request/response models in `src/ecommerce_platform/models.py`.
3. Implement business logic in `src/ecommerce_platform/services.py`.
4. Add tests in `tests/integration/`.
5. Update `docs/api.md` and `api_gateway/api.yaml`.

### Adding a New Table

1. Add a new SQL statement in `src/ecommerce_platform/db.py`.
2. Add repository methods in `src/ecommerce_platform/repositories.py`.
3. Add domain logic in `src/ecommerce_platform/services.py`.
4. Add tests to cover CRUD behaviors.

### Validations

The service layer is responsible for validating inputs. If you need stricter
validation (e.g., SKU formats), add it in `services.py` and expose validation
errors through the API layer.

## Review Checklist

- [ ] Tests updated or added.
- [ ] API reference updated.
- [ ] README updated if user-facing behavior changes.
- [ ] `scripts/verify.sh` still passes.
