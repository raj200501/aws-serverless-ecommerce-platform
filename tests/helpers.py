from __future__ import annotations

import json
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, Tuple
from urllib import request

from ecommerce_platform.config import Settings
from ecommerce_platform.db import init_db
from ecommerce_platform.server import create_server
from ecommerce_platform.services import EcommerceService


@dataclass
class TestEnvironment:
    temp_dir: tempfile.TemporaryDirectory
    settings: Settings
    service: EcommerceService

    def cleanup(self) -> None:
        self.temp_dir.cleanup()


def build_test_environment() -> TestEnvironment:
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "ecommerce.db"
    settings = Settings(
        env="test",
        database_url=f"sqlite:///{db_path}",
        log_level="info",
        token_secret="test-secret",
        token_ttl_minutes=15,
        allow_test_mode=True,
        recommendations_per_user=3,
        port=0,
    )
    db = init_db(settings)
    service = EcommerceService(settings=settings, db=db)
    return TestEnvironment(temp_dir=temp_dir, settings=settings, service=service)


@contextmanager
def run_test_server(env: TestEnvironment) -> Generator[str, None, None]:
    server, thread = create_server(env.settings)
    thread.start()
    _, port = server.server_address
    base_url = f"http://127.0.0.1:{port}"
    try:
        yield base_url
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


def json_request(method: str, url: str, payload: Dict | None = None) -> Tuple[int, Dict]:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    with request.urlopen(req) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)
