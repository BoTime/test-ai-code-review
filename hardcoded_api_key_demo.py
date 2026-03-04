#!/usr/bin/env python3
"""
Intentionally insecure demo script for testing code review/secret detection.
"""

import urllib.request

# Intentionally hardcoded for testing Copilot review signals.
OPENAI_API_KEY = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyzTESTKEY"


def ping_example_api() -> None:
    request = urllib.request.Request("https://example.com")
    request.add_header("Authorization", f"Bearer {OPENAI_API_KEY}")

    with urllib.request.urlopen(request, timeout=5) as response:
        print("Status:", response.status)


if __name__ == "__main__":
    ping_example_api()
