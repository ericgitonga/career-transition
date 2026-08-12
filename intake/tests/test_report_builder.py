"""Unit tests for report_builder.py's escaping helpers.

esc()/esc_markup() are the engine behind every generated client deliverable
(transition plans, CV rewrites — see generate_plan.py, cv_builder.py). This
locks in the R-05 incident permanently: a fix for a PDF-crashing stray
"<"/"&" (closed #52) had to be re-fixed (#55-#57) after it also escaped the
literal "<b>"/"<i>" tags consultants intentionally type as their bold/italic
convention. Both failure modes get a regression test here.
"""

from report_builder import esc, esc_markup, interview_prep_mailto, RECIPIENT


# ── esc() — always escapes, no markup exceptions ───────────────────────────────

def test_esc_escapes_angle_brackets_and_ampersand():
    assert esc("Salary < 100k & > previous") == "Salary &lt; 100k &amp; &gt; previous"


def test_esc_escapes_literal_bold_tags_too():
    # esc() has no markup exception — call sites that want <b>/<i> to render
    # must use esc_markup() instead.
    assert esc("<b>bold</b>") == "&lt;b&gt;bold&lt;/b&gt;"


def test_esc_coerces_non_string_input():
    assert esc(42) == "42"


# ── esc_markup() — preserves <b>/<i>, escapes everything else (R-05) ──────────

def test_esc_markup_preserves_bold_and_italic_tags():
    assert esc_markup("This is <b>bold</b> and <i>italic</i>") == (
        "This is <b>bold</b> and <i>italic</i>"
    )


def test_esc_markup_still_escapes_stray_angle_brackets_and_ampersand():
    # The original R-05 crash: a stray "<"/">"/"&" from copy-pasted prose
    # must still be escaped even though <b>/<i> are exempted.
    assert esc_markup("5 < 10 & 20 > 15") == "5 &lt; 10 &amp; 20 &gt; 15"


def test_esc_markup_escapes_tags_outside_the_allowed_set():
    # The regression this test guards: only literal <b>, </b>, <i>, </i>
    # tokens are exempted — any other tag (even a plausible-looking one) is
    # escaped like ordinary text, not treated as trusted markup.
    assert esc_markup("<bold>not real</bold>") == "&lt;bold&gt;not real&lt;/bold&gt;"


def test_esc_markup_mixed_content():
    result = esc_markup("Priority: <b>HIGH</b> (score < 5 & rising)")
    assert "<b>HIGH</b>" in result
    assert "&lt;" in result and "&amp;" in result
    assert "score &lt; 5" in result


# ── interview_prep_mailto() — the plan's closing interview-prep CTA link ───────

def test_interview_prep_mailto_targets_recipient():
    assert interview_prep_mailto("Alex Mercer").startswith(f"mailto:{RECIPIENT}?")


def test_interview_prep_mailto_percent_encodes_spaces_and_punctuation():
    # Client name flows into the "subject" query param, which must be a
    # valid, spaceless URL component — not raw text with literal spaces.
    mailto = interview_prep_mailto("Alex Mercer")
    assert " " not in mailto
    assert "Alex%20Mercer" in mailto


def test_interview_prep_mailto_escapes_ampersand_for_xml_embedding():
    # This string is embedded directly into a ReportLab Paragraph's
    # pseudo-XML, so the subject/body separator must be "&amp;", not a bare
    # "&" that ReportLab's parser would choke on.
    mailto = interview_prep_mailto("Alex Mercer")
    assert "&amp;body=" in mailto
    assert "&body=" not in mailto


def test_interview_prep_mailto_percent_encodes_name_with_special_characters():
    # A client name containing "&" must not itself introduce a bare,
    # unescaped "&" into the mailto string.
    mailto = interview_prep_mailto("Smith & Jones")
    assert "&body=" not in mailto or "&amp;body=" in mailto
    assert "Smith%20%26%20Jones" in mailto
