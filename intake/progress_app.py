"""
Progress-linked plan adaptation spike (career-transition issue #75).

Tests one mechanic before any billing/multi-tenancy work: does regenerating a
"where you actually stand" note from a client's logged milestone progress read as
genuinely useful, or as a restatement of the plan they already have? See
extras/musings/career-income.md for the full context and GitHub issue #75 for
this slice's scope.

Local-only tool, never deployed. `app.py` runs on Vercel with no database and an
ephemeral filesystem, so a milestone log written to disk there would not persist.
This script is deliberately separate — not wired into vercel.json — same pattern
as generate_plan.py and generate_gap_note.py.

Run:  conda run -n ds python progress_app.py
Requires SECRET_KEY, PROGRESS_PAGE_PASSWORD, and ANTHROPIC_API_KEY in the
environment. Refuses to start without the first two. Binds 127.0.0.1 only.

Known limitation: single shared password, no CSRF token beyond Flask-WTF's
default per-session token, no rate limiting on /login — acceptable for a
local, single-consultant prototype but flagged here so it isn't mistaken for a
production auth posture if this ever gets deployed.
"""

import hmac
import importlib.util
import json
import os
from datetime import date
from pathlib import Path

import anthropic
from flask import Flask, redirect, render_template_string, request, session, url_for
from flask_wtf.csrf import CSRFProtect

HERE = Path(__file__).resolve().parent
CLIENT_NAME = "Alex Mercer"
CLIENT_DIR = HERE / "Clients" / CLIENT_NAME
MILESTONE_LOG_PATH = CLIENT_DIR / "milestone_log.json"
LATEST_NOTE_PATH = CLIENT_DIR / "latest_adaptation_note.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
CSRFProtect(app)
PROGRESS_PAGE_PASSWORD = os.environ["PROGRESS_PAGE_PASSWORD"]


def load_plan():
    """Load Clients/Alex Mercer/plan_data.py's PLAN dict — mirrors generate_plan.py."""
    data_path = CLIENT_DIR / "plan_data.py"
    spec = importlib.util.spec_from_file_location("plan_data", data_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PLAN


def roadmap_overview_text(plan):
    """Flatten the semester table + opening tagline into plain text for the Claude prompt."""
    lines = [plan["opening_tagline"]]
    for block in plan["section_4"]["blocks"]:
        table = block.get("table")
        if table:
            for sem, theme, duration, period, key_output in table["rows"]:
                lines.append(
                    f"Semester {sem} ({period}, {duration}): {theme} — key output: {key_output}"
                )
    return "\n".join(lines)


def seed_milestone_log(plan):
    return [
        {
            "milestone": m["milestone"],
            "target_date": m["target_date"],
            "status": "pending",
            "note": "",
        }
        for m in plan["section_11"]["metrics"]
    ]


def load_milestone_log(plan, path=None):
    path = path or MILESTONE_LOG_PATH
    if not path.exists():
        milestones = seed_milestone_log(plan)
        save_milestone_log(milestones, path=path)
        return milestones
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(
            f"{path} exists but could not be read as JSON ({exc}) — "
            "fix or delete it before continuing; refusing to silently overwrite logged progress."
        )


def save_milestone_log(milestones, path=None):
    path = path or MILESTONE_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(milestones, indent=2))


def load_latest_note(path=None):
    path = path or LATEST_NOTE_PATH
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def save_latest_note(note_text, today, path=None):
    path = path or LATEST_NOTE_PATH
    path.write_text(json.dumps({"note": note_text, "generated_at": today.isoformat()}, indent=2))


def generate_adaptation_note(plan, milestones, today):
    """One Claude call: original roadmap + milestone log + today's date -> a short,
    concrete "where you stand / what shifts" note. No tools, no structured output —
    this is a single synthesis call, not an agentic task."""
    client = anthropic.Anthropic()
    milestone_lines = "\n".join(
        f"- [{'DONE' if m['status'] == 'done' else 'pending'}] {m['milestone']} "
        f"(target: {m['target_date']})" + (f" — note: {m['note']}" if m["note"] else "")
        for m in milestones
    )
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        output_config={"effort": "medium"},
        system=(
            "You are an experienced career transition consultant reviewing one client's "
            "actual logged progress against the 18-month roadmap you originally wrote for "
            "them. Write a short, concrete note: where the client actually stands relative "
            "to the original timeline, and what should shift in the remaining roadmap as a "
            "result. Do not restate the milestone list back to the client — synthesize what "
            "it means."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Today's date: {today.isoformat()}\n\n"
                f"Original roadmap overview:\n{roadmap_overview_text(plan)}\n\n"
                f"Milestone log:\n{milestone_lines}"
            ),
        }],
    )
    return next(block.text for block in response.content if block.type == "text")


LOGIN_PAGE = """
<!doctype html><title>Progress tracker — login</title>
<form method="post" action="{{ url_for('login') }}">
  {{ csrf_field | safe }}
  <label>Password: <input type="password" name="password" autofocus></label>
  <button type="submit">Log in</button>
</form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
"""

MILESTONES_PAGE = """
<!doctype html><title>{{ client_name }} — progress</title>
<h1>{{ client_name }} — milestone progress</h1>
<form method="post" action="{{ url_for('logout') }}"><button type="submit">Log out</button></form>

{% if latest_note %}
<h2>Latest adaptation note ({{ latest_note.generated_at }})</h2>
<pre style="white-space: pre-wrap; max-width: 60em;">{{ latest_note.note }}</pre>
{% endif %}

<h2>Milestones</h2>
<form method="post" action="{{ url_for('update') }}">
  {{ csrf_field | safe }}
  <table border="1" cellpadding="6">
    <tr><th>Done</th><th>Milestone</th><th>Target date</th><th>Note (what actually happened)</th></tr>
    {% for m in milestones %}
    <tr>
      <td><input type="checkbox" name="done_{{ loop.index0 }}" {% if m.status == "done" %}checked{% endif %}></td>
      <td>{{ m.milestone }}</td>
      <td>{{ m.target_date }}</td>
      <td><input type="text" name="note_{{ loop.index0 }}" value="{{ m.note }}" size="40"></td>
    </tr>
    {% endfor %}
  </table>
  <button type="submit">Save and regenerate note</button>
</form>
"""


def require_auth():
    return session.get("progress_authed") is True


@app.route("/", methods=["GET"])
def index():
    if not require_auth():
        return render_template_string(LOGIN_PAGE, csrf_field=_csrf_field(), error=None)
    plan = load_plan()
    milestones = load_milestone_log(plan)
    return render_template_string(
        MILESTONES_PAGE,
        client_name=CLIENT_NAME,
        milestones=milestones,
        latest_note=load_latest_note(),
        csrf_field=_csrf_field(),
    )


@app.route("/login", methods=["POST"])
def login():
    submitted = request.form.get("password", "")
    if hmac.compare_digest(submitted, PROGRESS_PAGE_PASSWORD):
        session["progress_authed"] = True
        return redirect(url_for("index"))
    return render_template_string(LOGIN_PAGE, csrf_field=_csrf_field(), error="Wrong password.")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("progress_authed", None)
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    if not require_auth():
        return redirect(url_for("index"))
    plan = load_plan()
    milestones = load_milestone_log(plan)
    for i, m in enumerate(milestones):
        m["status"] = "done" if request.form.get(f"done_{i}") else "pending"
        m["note"] = request.form.get(f"note_{i}", "")
    save_milestone_log(milestones)
    today = date.today()
    note_text = generate_adaptation_note(plan, milestones, today)
    save_latest_note(note_text, today)
    return redirect(url_for("index"))


def _csrf_field():
    from flask_wtf.csrf import generate_csrf
    return f'<input type="hidden" name="csrf_token" value="{generate_csrf()}">'


if __name__ == "__main__":
    port = int(os.environ.get("PROGRESS_APP_PORT", 5051))
    app.run(host="127.0.0.1", port=port)
