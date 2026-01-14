# Troubleshooting

This guide collects common pitfalls when running the local e-commerce platform.

## Port Already In Use

**Symptom:** `OSError: [Errno 98] Address already in use`

**Fix:**

1. Change the port before running:
   ```bash
   PORT=8080 ./scripts/run.sh
   ```
2. Or stop the existing process listening on port 8000.

## Database Path Errors

**Symptom:** `sqlite3.OperationalError: unable to open database file`

**Fix:**

1. Ensure the directory in `DATABASE_URL` exists.
2. Verify you have write permissions.
3. Run `PYTHONPATH=src python -m ecommerce_platform.cli init-db` to create the DB file.

## Username/Email Already Exists

**Symptom:** API returns `400` with `username already exists` or `email already exists`.

**Fix:**

- Delete the SQLite database file to reset state:
  ```bash
  rm -f data/ecommerce.db
  ```
- Re-run the seed command if needed.

## Failed Login

**Symptom:** `401` on `/auth/login`.

**Fix:**

- Ensure the username exists.
- Ensure the password matches exactly (case sensitive).
- If using demo data, the default credentials are `demo` / `password123`.

## Missing Dependencies

**Symptom:** Import error for a third-party package.

**Fix:** This repository is designed to run without third-party dependencies.
If you see an import error, ensure you are using the latest code and did not
introduce optional dependencies without updating documentation.

## Test Failures

**Symptom:** `unittest` reports failures in integration tests.

**Fix:**

1. Ensure the tests run in a clean environment (delete `data/` if needed).
2. Check that you did not modify the API routes without updating tests.
3. Inspect the failing assertion for unexpected JSON responses.
