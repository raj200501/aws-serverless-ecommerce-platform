"""Configuration loading for the local platform.

We avoid external dependencies by using a small .env parser and environment
variables. This keeps the project self-contained while still supporting
configuration overrides in CI or local runs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    return key.strip(), value.strip().strip('"')


def load_env_file(path: Path) -> Dict[str, str]:
    """Load environment variables from a .env style file.

    We keep this minimal to avoid pulling in external dependencies while
    retaining deterministic behavior for CI.
    """

    if not path.exists():
        return {}
    values: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(line)
        if parsed is None:
            continue
        key, value = parsed
        values[key] = value
    return values


@dataclass(frozen=True)
class Settings:
    env: str
    database_url: str
    log_level: str
    token_secret: str
    token_ttl_minutes: int
    allow_test_mode: bool
    recommendations_per_user: int
    port: int

    @property
    def sqlite_path(self) -> Path:
        if not self.database_url.startswith("sqlite:///"):
            raise ValueError("Only sqlite databases are supported in local mode")
        return Path(self.database_url.replace("sqlite:///", "", 1))


def _apply_overrides(base: Dict[str, str], overrides: Iterable[Dict[str, str]]) -> Dict[str, str]:
    merged = dict(base)
    for override in overrides:
        merged.update({k: v for k, v in override.items() if v is not None})
    return merged


def load_settings(env_file: str | None = None) -> Settings:
    """Load Settings from the environment or an optional .env file."""

    cwd_env = Path(env_file) if env_file else Path(".env")
    file_values = load_env_file(cwd_env)
    values = _apply_overrides(file_values, [os.environ])
    return Settings(
        env=values.get("APP_ENV", "local"),
        database_url=values.get("DATABASE_URL", "sqlite:///./data/ecommerce.db"),
        log_level=values.get("LOG_LEVEL", "info"),
        token_secret=values.get("TOKEN_SECRET", "local-dev-secret"),
        token_ttl_minutes=int(values.get("TOKEN_TTL_MINUTES", "60")),
        allow_test_mode=values.get("ALLOW_TEST_MODE", "false").lower() == "true",
        recommendations_per_user=int(values.get("RECOMMENDATIONS_PER_USER", "3")),
        port=int(values.get("PORT", "8000")),
    )
