"""Regression test for R-02: markup-like characters must not crash PDF generation.

`_qa()`/`build_pdf()` in app.py used to pass client-typed text straight into
ReportLab's Paragraph(), which parses a pseudo-XML dialect. Verified directly
against the pinned reportlab: a bare "&"/">" or an unrecognised "<tag>" is
tolerated, but a *recognised* ReportLab tag left unclosed -- e.g. a client
typing "prefer <b>remote-first orgs" and never closing the <b> -- raised a
ValueError and turned the whole submission into a generic 500, losing the
client's entire intake (see #52). Fixed by escaping every field with
xml.sax.saxutils.escape() before it reaches Paragraph().

Uses Alex Mercer's fixture data (see SKILL.md's "Testing the Intake Form"),
plus a "target_domain"/"anything_else" answer built to actually break the
old parser: an unclosed <b> tag alongside a bare "&", "->", and ">", so this
fails the same way a real client's informal markdown-style emphasis would.
"""

from playwright.sync_api import expect

from _common import TEST_CV_PATH, browser_page

SPECIAL_CHARS_ANSWER = (
    "Ops & Infrastructure -> Platform Engineering, prefer <b>remote-first "
    "orgs, R&D-adjacent teams (>150k)"
)


def test_submission_survives_special_characters():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[name="full_name"]', "Alex Mercer")
        page.fill('input[name="mpesa_code"]', "SFH3XXXXXX")

        # target_domain (Section 3) and anything_else (Section 9) live in
        # collapsed accordion panels — expand each before filling it in.
        page.click('button[data-bs-target="#s3"]')
        page.fill('input[name="target_domain"]', SPECIAL_CHARS_ANSWER)
        page.click('button[data-bs-target="#s9"]')
        page.fill('textarea[name="anything_else"]', SPECIAL_CHARS_ANSWER)

        page.set_input_files('input[name="cv_file"]', str(TEST_CV_PATH))
        page.check("#consent-processing")
        page.check("#consent-sensitive")

        with page.expect_download() as download_info:
            page.click("#submit-btn")

        download = download_info.value
        assert download.suggested_filename.endswith(".pdf")

        status = page.locator("#status")
        expect(status).to_contain_text(
            "Your intake form has been submitted", timeout=20_000
        )


TESTS = [test_submission_survives_special_characters]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
