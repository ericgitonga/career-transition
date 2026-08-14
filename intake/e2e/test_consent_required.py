"""DPA gap-analysis fix (s.32): consent is a hard submission blocker.

Both consent checkboxes carry the HTML `required` attribute, so a normal
browser refuses to submit the form at all while either is unticked — this
test bypasses that by calling submit() directly (as a client with JS
disabled, or hitting the endpoint directly, could), confirming the server
enforces the same rule app.js/the browser does.

Uses Alex Mercer's fixture data (see SKILL.md's "Testing the Intake Form").
"""

from playwright.sync_api import expect

from _common import TEST_CV_PATH, BASE_URL, browser_page


def test_submission_blocked_without_consent():
    with browser_page() as page:
        page.goto("/")
        csrf_token = page.locator('input[name="csrf_token"]').get_attribute("value")

        # Deliberately leave both consent checkboxes unticked, then submit
        # directly against /submit — same technique a client with JS
        # disabled (or hitting the endpoint directly) could use, sidestepping
        # the browser's own `required`-attribute enforcement. page.request
        # shares this page's session cookie, so only the CSRF token needs to
        # be supplied explicitly.
        response = page.request.post(
            f"{BASE_URL}/submit",
            multipart={
                "csrf_token": csrf_token,
                "full_name": "Alex Mercer",
                "cv_file": {
                    "name": "test-cv.pdf",
                    "mimeType": "application/pdf",
                    "buffer": TEST_CV_PATH.read_bytes(),
                },
            },
        )
        assert response.status == 400
        assert "consent" in response.text().lower()


TESTS = [test_submission_blocked_without_consent]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
