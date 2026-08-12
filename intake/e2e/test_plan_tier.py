"""Coverage for the plan_tier radio group added in place of the retired
wants_cv_edit checkbox — previously untested at the e2e layer (the field it
replaces had zero e2e coverage either, per SKILL.md's own audit).

Basic ships pre-checked (see index.html), so the existing minimal-fields
golden path in test_submission_email.py already exercises an implicit
Basic submission unchanged. This spec explicitly selects Advanced and
confirms a real submission still completes end-to-end.
"""

from playwright.sync_api import expect

from _common import TEST_CV_PATH, browser_page


def test_basic_is_preselected():
    with browser_page() as page:
        page.goto("/")
        page.click('button[data-bs-target="#s9"]')
        expect(page.locator("#tier-basic")).to_be_checked()
        expect(page.locator("#tier-advanced")).not_to_be_checked()


def test_advanced_tier_submission_completes():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[name="full_name"]', "E2E Advanced Tier Submission")
        page.set_input_files('input[name="cv_file"]', str(TEST_CV_PATH))
        page.click('button[data-bs-target="#s9"]')
        page.check("#tier-advanced")

        with page.expect_download():
            page.click("#submit-btn")

        status = page.locator("#status")
        expect(status).to_contain_text(
            "A copy has been emailed to your consultant.", timeout=20_000
        )


TESTS = [test_basic_is_preselected, test_advanced_tier_submission_completes]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
