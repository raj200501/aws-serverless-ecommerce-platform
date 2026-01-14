"""Local database initialization (SQLite)."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ecommerce_platform.config import load_settings
from ecommerce_platform.db import init_db


if __name__ == "__main__":
    settings = load_settings()
    init_db(settings)
    print(f"Initialized local database at {settings.sqlite_path}")
