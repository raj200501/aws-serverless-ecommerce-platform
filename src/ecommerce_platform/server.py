"""Minimal HTTP server for the local e-commerce API."""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple
from urllib.parse import urlparse

from .api import EcommerceAPI, ApiResponse, create_api
from .config import Settings, load_settings


class EcommerceRequestHandler(BaseHTTPRequestHandler):
    api: EcommerceAPI

    def do_GET(self) -> None:
        self._handle_request()

    def do_POST(self) -> None:
        self._handle_request()

    def _handle_request(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else None
        response = self.api.handle(self.command, urlparse(self.path).path, body)
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.body)

    def log_message(self, format: str, *args) -> None:
        return


def _build_handler(api: EcommerceAPI):
    class BoundHandler(EcommerceRequestHandler):
        pass

    BoundHandler.api = api
    return BoundHandler


def create_server(settings: Settings | None = None) -> Tuple[ThreadingHTTPServer, threading.Thread]:
    settings = settings or load_settings()
    api = create_api(settings)
    handler = _build_handler(api)

    server = ThreadingHTTPServer(("0.0.0.0", int(settings.port)), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    return server, thread


def run() -> None:
    settings = load_settings()
    api = create_api(settings)
    handler = _build_handler(api)

    server = ThreadingHTTPServer(("0.0.0.0", int(settings.port)), handler)
    print(f"Serving API on http://0.0.0.0:{settings.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
