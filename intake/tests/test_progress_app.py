"""Unit tests for progress_app.py — the issue #75 progress-adaptation spike.

Fast, no real network calls: the Claude API is always mocked. Sets SECRET_KEY /
PROGRESS_PAGE_PASSWORD before import since progress_app.py hard-requires them
at module load (a local-only script, unlike app.py's Vercel-friendly fallback).

Never loads the real Clients/Alex Mercer/plan_data.py: Clients/ is gitignored
project-wide (see intake/.gitignore), so that file doesn't exist on a fresh
checkout or in CI — only on a machine where it's been hand-authored locally.
Tests use a small synthetic PLAN fixture matching plan_data.py's schema
instead, same as the rest of this suite never reading real client data.
"""

import json
import os
import re
from datetime import date

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("PROGRESS_PAGE_PASSWORD", "test-password")

import pytest

import progress_app

FAKE_PLAN = {
    "opening_tagline": "This is a test tagline for a synthetic plan.",
    "section_4": {
        "blocks": [
            {"paragraph": "An intro paragraph with no table."},
            {
                "table": {
                    "headers": ["Sem", "Theme", "Duration", "Period", "Key Output"],
                    "rows": [
                        ["1", "Foundations", "3 months", "Jul - Sep 2026", "First deliverable"],
                        ["2", "Build", "3 months", "Oct - Dec 2026", "Second deliverable"],
                    ],
                },
            },
        ],
    },
    "section_11": {
        "metrics": [
            {"milestone": "Milestone A completed", "target_date": "Jul 2026"},
            {"milestone": "Milestone B completed", "target_date": "Sep 2026"},
            {"milestone": "Milestone C completed", "target_date": "Dec 2026"},
        ],
    },
}


def _csrf_token(html_bytes):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', html_bytes)
    assert match, "no CSRF token found in response"
    return match.group(1).decode()


@pytest.fixture
def plan():
    return FAKE_PLAN


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(progress_app, "load_plan", lambda: FAKE_PLAN)
    monkeypatch.setattr(progress_app, "MILESTONE_LOG_PATH", tmp_path / "milestone_log.json")
    monkeypatch.setattr(progress_app, "LATEST_NOTE_PATH", tmp_path / "latest_adaptation_note.json")
    progress_app.app.config["TESTING"] = True
    return progress_app.app.test_client()


# ── seed_milestone_log / load_milestone_log / save_milestone_log ──────────────

def test_seed_milestone_log_matches_plan_metrics(plan):
    seeded = progress_app.seed_milestone_log(plan)
    metrics = plan["section_11"]["metrics"]
    assert len(seeded) == len(metrics)
    assert all(m["status"] == "pending" and m["note"] == "" for m in seeded)
    assert [m["milestone"] for m in seeded] == [m["milestone"] for m in metrics]


def test_load_milestone_log_seeds_file_on_first_run(plan, tmp_path):
    path = tmp_path / "milestone_log.json"
    assert not path.exists()
    milestones = progress_app.load_milestone_log(plan, path=path)
    assert path.exists()
    assert milestones == progress_app.seed_milestone_log(plan)


def test_load_milestone_log_round_trips_saved_state(plan, tmp_path):
    path = tmp_path / "milestone_log.json"
    milestones = progress_app.seed_milestone_log(plan)
    milestones[0]["status"] = "done"
    milestones[0]["note"] = "finished early"
    progress_app.save_milestone_log(milestones, path=path)

    reloaded = progress_app.load_milestone_log(plan, path=path)
    assert reloaded[0]["status"] == "done"
    assert reloaded[0]["note"] == "finished early"


def test_load_milestone_log_fails_closed_on_corrupt_file(plan, tmp_path):
    path = tmp_path / "milestone_log.json"
    path.write_text("not valid json {{{")
    with pytest.raises(RuntimeError, match="could not be read as JSON"):
        progress_app.load_milestone_log(plan, path=path)


# ── roadmap_overview_text ──────────────────────────────────────────────────────

def test_roadmap_overview_text_includes_tagline_and_semesters(plan):
    text = progress_app.roadmap_overview_text(plan)
    assert plan["opening_tagline"] in text
    for sem, _theme, _duration, _period, key_output in (
        plan["section_4"]["blocks"][1]["table"]["rows"]
    ):
        assert f"Semester {sem}" in text
        assert key_output in text


# ── generate_adaptation_note ───────────────────────────────────────────────────

class _FakeTextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeMessages:
    def __init__(self, capture):
        self._capture = capture

    def create(self, **kwargs):
        self._capture.append(kwargs)
        return type("Resp", (), {"content": [_FakeTextBlock("mocked adaptation note")]})()


class _FakeAnthropicClient:
    def __init__(self, capture):
        self.messages = _FakeMessages(capture)


def test_generate_adaptation_note_includes_milestones_and_date(monkeypatch, plan):
    captured = []
    monkeypatch.setattr(progress_app.anthropic, "Anthropic", lambda: _FakeAnthropicClient(captured))

    milestones = progress_app.seed_milestone_log(plan)
    milestones[0]["status"] = "done"
    milestones[0]["note"] = "shipped ahead of plan"
    today = date(2026, 8, 13)

    note = progress_app.generate_adaptation_note(plan, milestones, today)

    assert note == "mocked adaptation note"
    assert len(captured) == 1
    prompt = captured[0]["messages"][0]["content"]
    assert "2026-08-13" in prompt
    assert milestones[0]["milestone"] in prompt
    assert "shipped ahead of plan" in prompt
    assert captured[0]["model"] == "claude-opus-5"


# ── Flask routes ────────────────────────────────────────────────────────────────

def test_index_unauthenticated_shows_login_not_milestones(client, plan):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Password" in resp.data
    assert plan["section_11"]["metrics"][0]["milestone"].encode() not in resp.data


def test_login_wrong_password_does_not_authenticate(client):
    token = _csrf_token(client.get("/").data)
    resp = client.post("/login", data={"password": "wrong", "csrf_token": token})
    assert b"Wrong password" in resp.data
    with client.session_transaction() as sess:
        assert not sess.get("progress_authed")


def test_login_correct_password_authenticates_and_shows_milestones(client, plan):
    token = _csrf_token(client.get("/").data)
    resp = client.post(
        "/login",
        data={"password": "test-password", "csrf_token": token},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert plan["section_11"]["metrics"][0]["milestone"].encode() in resp.data


def test_update_requires_auth(client):
    token = _csrf_token(client.get("/").data)
    resp = client.post("/update", data={"csrf_token": token}, follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_update_saves_log_and_stores_generated_note(monkeypatch, client, plan, tmp_path):
    monkeypatch.setattr(progress_app, "generate_adaptation_note", lambda *a, **k: "note from claude")

    login_token = _csrf_token(client.get("/").data)
    resp = client.post(
        "/login",
        data={"password": "test-password", "csrf_token": login_token},
        follow_redirects=True,
    )
    milestones = progress_app.load_milestone_log(plan, path=progress_app.MILESTONE_LOG_PATH)

    form = {"csrf_token": _csrf_token(resp.data)}
    for i, _m in enumerate(milestones):
        if i == 0:
            form[f"done_{i}"] = "on"
            form[f"note_{i}"] = "did it differently"
        else:
            form[f"note_{i}"] = ""
    client.post("/update", data=form, follow_redirects=True)

    saved = json.loads(progress_app.MILESTONE_LOG_PATH.read_text())
    assert saved[0]["status"] == "done"
    assert saved[0]["note"] == "did it differently"
    assert saved[1]["status"] == "pending"

    note = json.loads(progress_app.LATEST_NOTE_PATH.read_text())
    assert note["note"] == "note from claude"
