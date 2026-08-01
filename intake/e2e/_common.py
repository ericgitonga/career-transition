"""Shared helpers for the intake app's Playwright E2E smoke suite.

Written against the Python `playwright` package, matching the umoja-voices/
ebc-songs/merch-mockup/landing e2e convention. Run each spec directly, or all
of them via `run.py`:

    conda run -n ds python e2e/run.py
    conda run -n ds python e2e/test_submission_email.py

BASE_URL defaults to the local Flask dev server (`python app.py`); CI
overrides it to point at that same server started in the workflow.

Unlike landing's _common.py, this app has real server-side state per
request (CSRF session cookie, rate limiting, an outbound email) — every
spec drives a real browser through the actual form so cookies, the CSRF
token, and file uploads all behave exactly as they do for a real client.
"""

import os
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000").rstrip("/")

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEST_CV_PATH = FIXTURES_DIR / "test-cv.pdf"


@contextmanager
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(base_url=BASE_URL)
            yield page
        finally:
            browser.close()
