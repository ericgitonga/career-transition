"""Unit tests for the pure helper functions in app.py.

Fast, no server/network/filesystem involved — complements (not replaces) the
Playwright suite in e2e/, which only exercises these through a full HTTP
round-trip. Run: pytest (from intake/, or via CI's unit-test job).
"""

import pytest

from app import (
    _clip,
    _client_slug,
    _is_entrepreneur_type,
    _log_field,
    _qa,
    _safe_suffix,
    _sanitize,
    _sec4_pairs,
)


# ── _safe_suffix (S-03/S-14) ───────────────────────────────────────────────────

@pytest.mark.parametrize(
    "filename,expected",
    [
        ("resume.pdf", ".pdf"),
        ("resume.PDF", ".pdf"),
        ("cv.docx", ".docx"),
        ("photo.JPEG", ".jpeg"),
    ],
)
def test_safe_suffix_allows_whitelisted_extensions(filename, expected):
    assert _safe_suffix(filename) == expected


@pytest.mark.parametrize(
    "filename",
    ["malware.exe", "script.sh", "noextension", "archive.zip"],
)
def test_safe_suffix_rejects_non_whitelisted_extensions(filename):
    with pytest.raises(ValueError):
        _safe_suffix(filename)


# ── _clip (S-11) ───────────────────────────────────────────────────────────────

def test_clip_leaves_short_strings_untouched():
    assert _clip("hello", max_len=10) == "hello"


def test_clip_truncates_long_strings():
    value = "x" * 6000
    assert _clip(value) == "x" * 5000


def test_clip_none_returns_empty_string():
    assert _clip(None) == ""


def test_clip_non_string_passthrough():
    assert _clip(["a", "b"]) == ["a", "b"]


# ── _sanitize (S-12) ───────────────────────────────────────────────────────────

def test_sanitize_strips_control_characters_and_newlines():
    # The exact attack S-12 exists to prevent: a newline in a client-typed
    # name injecting a fake header/line into the plain-text email body.
    assert _sanitize("Alex\nBcc: attacker@evil.com") == "AlexBcc: attacker@evil.com"


def test_sanitize_strips_leading_trailing_whitespace():
    assert _sanitize("  Alex Mercer  ") == "Alex Mercer"


def test_sanitize_none_returns_empty_string():
    assert _sanitize(None) == ""


# ── _log_field (S-16) ──────────────────────────────────────────────────────────

def test_log_field_neutralizes_delimiter_like_tokens():
    # The exact attack S-16 exists to prevent: a value containing a literal
    # "uploads=999"/"email=..." token that could otherwise hijack
    # extras/pull_render_logs.py's fixed-token regex parser.
    encoded = _log_field("Attacker uploads=999 email=fake@evil.com")
    assert "uploads=" not in encoded
    assert "email=" not in encoded
    assert " " not in encoded


def test_log_field_is_percent_encoded():
    assert _log_field("Alex Mercer") == "Alex%20Mercer"


# ── _client_slug (S-19) ────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "full_name,expected",
    [
        ("Alex Mercer", "AlexM"),
        ("Marie Anne Curie", "MarieAC"),
        ("Jean-Paul Sartre", "Jean-PaulS"),
        ("", "Client"),
        ("   ", "Client"),
    ],
)
def test_client_slug_matches_documented_examples(full_name, expected):
    assert _client_slug(full_name) == expected


def test_client_slug_strips_path_traversal_sequences():
    # S-19: a slug must never carry a path-like sequence into a ZIP entry
    # name or download filename.
    slug = _client_slug("../../etc/passwd")
    assert "/" not in slug
    assert ".." not in slug


# ── _qa (S-20, closed #52, re-fixed #55-#57) ───────────────────────────────────

def test_qa_renders_blank_answer_as_em_dash():
    _, answer, _ = _qa("Full name", None)
    assert answer.text == "—"


def test_qa_joins_list_answers_with_commas():
    _, answer, _ = _qa("Skills", ["Python", "SQL", "Leadership"])
    assert answer.text == "Python, SQL, Leadership"


def test_qa_escapes_markup_characters_so_reportlab_does_not_crash():
    # A stray "<", ">", or "&" — or a copy-pasted HTML-like fragment — in
    # client-typed text must never reach Paragraph() unescaped: this is what
    # crashed PDF generation before S-20, then broke intentional bold text
    # when the first fix over-corrected (#55-#57). app.py's _qa always
    # escapes fully (unlike report_builder.py's esc_markup, which is only
    # used for consultant-authored prose elsewhere) — client input is never
    # trusted to carry real markup.
    _, answer, _ = _qa("Notes", "Salary < 100k & > previous <b>role</b>")
    assert "<b>" not in answer.text
    assert "<" not in answer.text
    assert "&lt;" in answer.text
    assert "&amp;" in answer.text


# ── _is_entrepreneur_type / _sec4_pairs ────────────────────────────────────────

@pytest.mark.parametrize(
    "client_type,expected",
    [
        ("Entrepreneur or business owner", True),
        ("Freelancer or independent consultant", True),
        ("Employed professional", False),
        ("", False),
    ],
)
def test_is_entrepreneur_type(client_type, expected):
    assert _is_entrepreneur_type(client_type) is expected


def test_sec4_pairs_entrepreneur_branch_asks_business_status():
    pairs = _sec4_pairs({"client_type": "Entrepreneur or business owner"})
    labels = [label for label, _ in pairs]
    assert "Business operating status" in labels
    assert "Currently employed?" not in labels


def test_sec4_pairs_employed_yes_asks_transition_status():
    pairs = _sec4_pairs({"client_type": "Employed professional", "employed": "Yes"})
    labels = [label for label, _ in pairs]
    assert "Currently employed?" in labels
    assert "Transitioning while working or planning to leave?" in labels


def test_sec4_pairs_employed_no_skips_transition_question():
    pairs = _sec4_pairs({"client_type": "Employed professional", "employed": "No"})
    labels = [label for label, _ in pairs]
    assert "Currently employed?" in labels
    assert "Transitioning while working or planning to leave?" not in labels
