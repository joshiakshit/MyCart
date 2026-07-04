"""
mitmproxy addon to capture and log Blinkit API traffic.

Usage:
    mitmproxy -s blinkit_capture.py
    mitmdump -s blinkit_capture.py -w ../captured/blinkit_flows.flow
"""

import json
from datetime import datetime

from mitmproxy import http


BLINKIT_DOMAINS = [
    "blinkit.com",
    "grofers.com",
]

INTERESTING_PATHS = [
    "/auth",
    "/login",
    "/otp",
    "/search",
    "/product",
    "/catalog",
    "/cart",
    "/address",
    "/category",
    "/v",  # catches versioned API paths like /v1/, /v2/
]


class BlinkitCapture:
    def __init__(self):
        self.captured_count = 0

    def _is_blinkit(self, host: str) -> bool:
        return any(domain in host for domain in BLINKIT_DOMAINS)

    def _is_interesting(self, path: str) -> bool:
        return any(keyword in path.lower() for keyword in INTERESTING_PATHS)

    def response(self, flow: http.HTTPFlow):
        if not self._is_blinkit(flow.request.host):
            return

        self.captured_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n{'='*80}")
        print(f"[{timestamp}] #{self.captured_count} {flow.request.method} {flow.request.url}")
        print(f"Status: {flow.response.status_code}")

        print("\n--- Request Headers ---")
        for key, value in flow.request.headers.items():
            if key.lower() in ("authorization", "auth", "token", "x-device-id",
                               "x-app-version", "user-agent", "content-type",
                               "x-signature", "x-timestamp"):
                print(f"  {key}: {value}")

        if flow.request.content:
            try:
                body = json.loads(flow.request.content)
                print(f"\n--- Request Body ---")
                print(json.dumps(body, indent=2)[:2000])
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"\n--- Request Body (raw, {len(flow.request.content)} bytes) ---")

        if flow.response.content:
            try:
                body = json.loads(flow.response.content)
                print(f"\n--- Response Body ---")
                print(json.dumps(body, indent=2)[:3000])
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"\n--- Response Body (raw, {len(flow.response.content)} bytes) ---")

        if self._is_interesting(flow.request.path):
            print(f"\n  *** INTERESTING ENDPOINT: {flow.request.path} ***")


addons = [BlinkitCapture()]
