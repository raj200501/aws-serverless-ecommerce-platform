# FAQ

## Why is this called "serverless" if it runs locally?

The repository originally targeted AWS serverless services. The local runtime
is a development adapter that preserves the service boundaries (auth, products,
orders, recommendations) without requiring AWS credentials. It lets you
exercise the workflows described in the README while keeping the option open to
move to real AWS services later.

## Can I deploy this to AWS?

Yes, but you will need to replace the SQLite repositories with DynamoDB
implementations and wire the Lambda handlers accordingly. The `serverless.yml`
file documents the expected handlers and endpoints.

## Does the API require authentication?

The local API returns a token on login but does not enforce it on requests. This
keeps the demo simple. If you need full auth enforcement, add a request
validation layer that checks tokens before invoking the handler.

## How do I reset the demo data?

Delete the SQLite database file and re-seed:

```bash
rm -f data/ecommerce.db
PYTHONPATH=src python -m ecommerce_platform.cli seed
```

## What is the demo user?

The seeded demo user is:

- Username: `demo`
- Password: `password123`

## Why is there no frontend?

The frontend assets are placeholders. The local focus is on the backend
workflows and deterministic testing.
