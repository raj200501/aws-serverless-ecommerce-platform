# Testing Guide

This repository uses Python's built-in `unittest` framework for unit tests and
integration smoke checks. The canonical entrypoint is `./scripts/verify.sh`.

## What Is Covered

| Test Type | File(s) | Intent |
| --- | --- | --- |
| Unit | `tests/unit/test_auth.py` | Password hashing and token issuance. |
| Unit | `tests/unit/test_config.py` | Environment parsing behavior. |
| Unit | `tests/unit/test_repositories.py` | SQLite repository CRUD. |
| Unit | `tests/unit/test_services.py` | Core business logic. |
| Integration | `tests/integration/test_smoke.py` | Full HTTP flow. |

## Running Tests Locally

```bash
./scripts/verify.sh
```

The script runs:

1. `python -m unittest discover -s tests -p "test_*.py"`

## Determinism Notes

- Tests run against a temporary SQLite database created via `tmp_path`.
- No external services or AWS credentials are required.
- Password hashing is deterministic and uses local secrets.

## Adding New Tests

When adding tests:

1. Prefer unit tests for service logic.
2. Prefer integration tests for HTTP flows.
3. Use fixtures from `tests/conftest.py` to reuse the test database.

## CI Integration

GitHub Actions runs `./scripts/verify.sh` on every `push` and `pull_request`.
If you add new dependencies in the future, update the documentation and
verification script so CI installs them deterministically.

## Troubleshooting

If tests fail with database errors, check that:

- The `DATABASE_URL` is a valid SQLite path.
- The directory for the SQLite database is writable.
- The schema version matches `SCHEMA_VERSION` in `db.py`.

If tests fail with import errors, confirm that:

- `PYTHONPATH` includes `src/`.
- The test runner uses the root of the repository.
