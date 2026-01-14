from __future__ import annotations

import tempfile
import unittest
import unittest.mock
from pathlib import Path

from ecommerce_platform.config import load_env_file, load_settings


class ConfigTests(unittest.TestCase):
    def test_load_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text("APP_ENV=test\nDATABASE_URL=sqlite:///tmp.db\n", encoding="utf-8")
            values = load_env_file(env_path)
            self.assertEqual(values["APP_ENV"], "test")
            self.assertTrue(values["DATABASE_URL"].endswith("tmp.db"))

    def test_load_settings_from_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text("APP_ENV=test\n", encoding="utf-8")
            with unittest.mock.patch.dict("os.environ", {"DATABASE_URL": "sqlite:///override.db"}):
                settings = load_settings(str(env_path))
                self.assertEqual(settings.env, "test")
                self.assertTrue(settings.database_url.endswith("override.db"))


if __name__ == "__main__":
    unittest.main()
