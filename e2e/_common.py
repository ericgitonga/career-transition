"""Shared helpers for the Playwright E2E smoke suite.

Written against the Python `playwright` package (already present in the `ds`
conda env, browsers pre-cached), matching the umoja-voices/ebc-songs/
merch-mockup e2e convention. Run each spec directly, or all of them via
`run.py`:

    conda run -n ds python e2e/run.py
    conda run -n ds python e2e/test_landing_page.py

BASE_URL defaults to local dev; CI overrides it to point at a production
build (`next build && next start`) rather than a dev server.

career-transition is a static marketing page with no accounts, database, or
forms of its own — every request is anonymous, so unlike umoja-voices'
_common.py there's no login/session caching here.
"""

import os
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000").rstrip("/")

INTAKE_URL = "https://career-transition-intake.vercel.app"
CONTACT_EMAIL = "gitonga@gmail.com"


@contextmanager
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(base_url=BASE_URL)
            yield page
        finally:
            browser.close()
