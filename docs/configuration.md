# Configuration Guide

This project uses a small configuration system to keep local development simple
and deterministic. Configuration values are loaded from `.env` if present,
otherwise environment variables and defaults are used.

## Configuration File

Copy the template:

```bash
cp .env.example .env
```

Edit values as needed.

## Supported Variables

| Variable | Example | Description |
| --- | --- | --- |
| `APP_ENV` | `local` | Environment label. |
| `DATABASE_URL` | `sqlite:///./data/ecommerce.db` | SQLite DB file path. |
| `LOG_LEVEL` | `info` | Uvicorn logging level. |
| `TOKEN_SECRET` | `change-me` | Secret used for token issuance. |
| `TOKEN_TTL_MINUTES` | `60` | Token lifetime. |
| `RECOMMENDATIONS_PER_USER` | `3` | Recommendation result size. |
| `SEED_DEMO` | `true` | Seed demo data when running. |
| `PORT` | `8000` | HTTP server port. |

## Overrides

You can override any variable in the shell. For example:

```bash
DATABASE_URL=sqlite:///./data/custom.db PORT=9000 ./scripts/run.sh
```

The config loader (`src/ecommerce_platform/config.py`) reads `.env` first and
then applies environment variables so overrides always take precedence.

## Example Configurations

### Use an Alternate Database File

```bash
DATABASE_URL=sqlite:///./data/staging.db ./scripts/run.sh
```

### Reduce Recommendation Size

```bash
RECOMMENDATIONS_PER_USER=1 ./scripts/run.sh
```

### Disable Demo Seeding

```bash
SEED_DEMO=false ./scripts/run.sh
```

## Configuration Safety

Invalid or unsupported configurations will fail fast. For example, if you set
`DATABASE_URL` to a non-SQLite value, the application raises a `ValueError` to
avoid silently misbehaving.
