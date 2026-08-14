"""Golden path: a real form submission must actually email the consultant.

Regression test for the incident where RESEND_API_KEY was never configured
in Vercel — every submission silently skipped the email step (the PDF still
downloaded fine, so nothing looked wrong to a client) until it was noticed
and fixed by hand. See app.py's send_email()/submit() for the code path:
email_status is "sent" only if RESEND_API_KEY is set *and* the Resend API
call succeeds; form.js only appends "A copy has been emailed to your
consultant." to the success message when the X-Email-Status response
header is "sent". Asserting on that visible sentence — rather than reading
the header directly — exercises the exact same signal a real client sees,
so this fails the same way the real incident would have looked to one.

Only full_name, a CV upload, and the two consent checkboxes are filled in:
per SKILL.md, those are the only requirements enforced by both form.js and
submit() — everything else in the form is optional and irrelevant to
whether the email fires.
"""

from playwright.sync_api import expect

from _common import TEST_CV_PATH, browser_page


def test_submission_emails_consultant():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[name="full_name"]', "E2E Test Submission")
        page.set_input_files('input[name="cv_file"]', str(TEST_CV_PATH))
        page.check("#consent-processing")
        page.check("#consent-sensitive")

        with page.expect_download():
            page.click("#submit-btn")

        status = page.locator("#status")
        expect(status).to_contain_text(
            "A copy has been emailed to your consultant.", timeout=20_000
        )


TESTS = [test_submission_emails_consultant]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
