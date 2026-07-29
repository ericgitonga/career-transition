"""Every call-to-action must actually point at the intake form / contact email."""

from _common import CONTACT_EMAIL, INTAKE_URL, browser_page


def test_cta_buttons_link_to_intake():
    with browser_page() as page:
        page.goto("/")
        ctas = page.get_by_role("link", name="Start My Plan")
        count = ctas.count()
        assert count == 4, f"expected 4 CTA buttons, found {count}"
        for i in range(count):
            assert ctas.nth(i).get_attribute("href") == INTAKE_URL


def test_contact_email_link():
    with browser_page() as page:
        page.goto("/")
        mailto = page.get_by_role("link", name=CONTACT_EMAIL)
        assert mailto.get_attribute("href") == f"mailto:{CONTACT_EMAIL}"


TESTS = [test_cta_buttons_link_to_intake, test_contact_email_link]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
