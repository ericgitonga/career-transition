"""Golden path: the page loads and every section renders."""

import re

from _common import browser_page

SECTION_HEADINGS = {
    "pain-points": "Does this sound familiar?",
    "what-you-get": "What you get",
    "who-for": "Who this is for",
    "how-it-works": "How it works",
    "pricing": "Simple, upfront pricing",
    "testimonials": "What clients have said",
    "contact": "Ready to stop guessing and start executing?",
}


def test_index_loads():
    with browser_page() as page:
        resp = page.goto("/")
        assert resp.status == 200
        assert page.title() == (
            "Career Transition Planning — Your next career isn't a guess. It's a plan."
        )
        assert page.locator('meta[name="description"]').get_attribute("content")

        heading = page.locator("h1")
        assert heading.is_visible()
        assert "isn't a guess" in heading.inner_text()


def test_all_sections_render():
    with browser_page() as page:
        page.goto("/")
        for section_id, heading_text in SECTION_HEADINGS.items():
            section = page.locator(f"#{section_id}")
            assert section.is_visible(), f"#{section_id} not visible"
            assert section.get_by_role("heading", name=heading_text).is_visible()


def test_footer_copyright():
    with browser_page() as page:
        page.goto("/")
        footer_text = page.get_by_role("contentinfo").inner_text()
        assert re.search(r"©\s*\d{4}\s+Career Transition Planning\.", footer_text)


TESTS = [test_index_loads, test_all_sections_render, test_footer_copyright]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
