import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, KeepTogether,
)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "hosting.pdf")

NAVY    = colors.HexColor("#1B2A4A")
TEAL    = colors.HexColor("#0E7C7B")
GOLD    = colors.HexColor("#C9A84C")
MGRAY   = colors.HexColor("#D0D6E0")
BLACK   = colors.HexColor("#1A1A1A")
CODE_BG = colors.HexColor("#EAEEF4")

W, H = A4
MARGIN  = 1.5 * cm
INNER_W = W - 2 * MARGIN


def styles():
    """Build and return the named paragraph styles used throughout the PDF.

    Centralising styles here avoids scattering ParagraphStyle calls across
    the layout functions and makes it easy to adjust typography in one place.

    Returns:
        A dictionary mapping short style keys to ParagraphStyle instances:
          - ``"h1"``   — large navy title for the document heading.
          - ``"h3"``   — teal sub-heading for numbered setup steps.
          - ``"body"`` — justified body text for descriptive paragraphs.
          - ``"step"`` — indented body text for bullet-point instructions.
          - ``"code"`` — monospaced Courier style for shell commands.
          - ``"note"`` — small oblique grey text for caveats and asides.
          - ``"bold"`` — teal bold text for emphasis lines.
    """
    return {
        "h1":   ParagraphStyle("h1",   fontName="Helvetica-Bold",   fontSize=18,
                               textColor=NAVY,  leading=24, spaceAfter=6),
        "h3":   ParagraphStyle("h3",   fontName="Helvetica-Bold",   fontSize=10.5,
                               textColor=TEAL,  leading=14, spaceBefore=10, spaceAfter=3),
        "body": ParagraphStyle("body", fontName="Helvetica",         fontSize=9.5,
                               textColor=BLACK, leading=14, spaceAfter=5, alignment=TA_JUSTIFY),
        "step": ParagraphStyle("step", fontName="Helvetica",         fontSize=9.5,
                               textColor=BLACK, leading=14, spaceAfter=4, leftIndent=14),
        "code": ParagraphStyle("code", fontName="Courier",           fontSize=8.5,
                               textColor=BLACK, leading=13, spaceAfter=0,
                               leftIndent=8, rightIndent=8),
        "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8.5,
                               textColor=colors.HexColor("#555555"), leading=12, spaceAfter=6),
        "bold": ParagraphStyle("bold", fontName="Helvetica-Bold",    fontSize=10,
                               textColor=TEAL,  leading=14, spaceAfter=8),
    }


def rule(color=GOLD, thickness=1, before=6, after=8):
    """Create a horizontal rule flowable for visual separation between sections.

    Args:
        color:     ReportLab color for the rule line. Defaults to GOLD.
        thickness: Line thickness in points. Defaults to 1.
        before:    Vertical space in points to insert above the rule. Defaults to 6.
        after:     Vertical space in points to insert below the rule. Defaults to 8.

    Returns:
        A ReportLab HRFlowable spanning the full content width.
    """
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=before, spaceAfter=after)


def code_block(text, s):
    """Render a shell command or code snippet in a styled monospaced block.

    Wraps the text in a single-cell Table with a light grey background and
    a subtle border, visually distinguishing it from surrounding body text.
    Leading and trailing whitespace is stripped before rendering.

    Args:
        text: The command or code string to display (e.g. "git push origin main").
        s:    The styles dictionary returned by ``styles()``. The ``"code"``
              entry is used for the Preformatted paragraph inside the block.

    Returns:
        A ReportLab Table flowable styled as a code block spanning INNER_W.
    """
    from reportlab.platypus import Table, TableStyle
    t = Table([[Preformatted(text.strip(), s["code"])]], colWidths=[INNER_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CODE_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("BOX",           (0, 0), (-1, -1), 0.5, MGRAY),
    ]))
    return t


def section_header(text, s):
    """Create a full-width navy banner used to open each document section.

    Matches the visual language of the intake PDF's section banners so the
    hosting guide feels part of the same design system. The text is rendered
    in bold white on a navy background.

    Args:
        text: The section title to display (e.g. "One-Time Setup").
        s:    The styles dictionary returned by ``styles()`` (accepted for
              API consistency, though this function defines its own inline style).

    Returns:
        A ReportLab Table flowable styled as a full-width navy section header.
    """
    from reportlab.platypus import Table, TableStyle
    p = Paragraph(text, ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=11,
                                        textColor=colors.white, leading=14))
    t = Table([[p]], colWidths=[INNER_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    return t


def build_story(s):
    """Assemble the full list of ReportLab flowables that make up the PDF body.

    Constructs the document narrative in five logical sections:
      1. Introduction — overview of the stack and deployment model.
      2. One-Time Setup — four numbered steps covering Vercel project import
         (with the monorepo Root Directory setting), Resend sign-up, and the
         three environment variables production actually depends on.
      3. How It Works — client-facing UX description and sender address notes.
      4. Deploying Updates — the single ``git push`` workflow and the
         Preview/Production promotion model.
      5. After Deployment — permanent URL, cold-start behaviour, and the
         API key rotation procedure.

    Each major section opens with a ``section_header`` banner and closes with
    a light grey rule. Numbered sub-steps use the ``"step"`` style with a
    bullet prefix.

    Args:
        s: The styles dictionary returned by ``styles()``.

    Returns:
        A list of ReportLab flowables ready to be passed to
        ``SimpleDocTemplate.build()``.
    """
    story = []

    story.append(Paragraph("Hosting the Career Transition Intake Form on Vercel", s["h1"]))
    story.append(rule(color=GOLD, thickness=1.5, before=2, after=10))
    story.append(Paragraph(
        "The intake form is a Flask web application hosted on Vercel as a Serverless "
        "(Fluid Compute) Function. It collects structured client responses across 10 "
        "sections, generates a PDF, and emails it automatically to the consultant via "
        "Resend — no SMTP configuration or credentials are shown to clients. Vercel is "
        "connected to the GitHub repo (<b>ericgitonga/career-transition</b>, a monorepo "
        "shared with the public landing page) and redeploys the intake app automatically "
        "on every push to <b>main</b>.",
        s["body"],
    ))
    story.append(Paragraph(
        "<b>After one-time setup, deploying a change means pushing to GitHub. That's it.</b>",
        s["bold"],
    ))
    story.append(rule(color=MGRAY, thickness=0.5))

    # ── ONE-TIME SETUP ────────────────────────────────────────────────────────
    story.append(KeepTogether([
        section_header("One-Time Setup", s),
        Spacer(1, 0.25 * cm),
        Paragraph("These steps are required once before the first deployment.", s["note"]),
    ]))

    story.append(Paragraph("1. Create a Vercel account", s["h3"]))
    story.append(Paragraph(
        "Go to <b>https://vercel.com</b> and sign up with GitHub — the Hobby tier requires "
        "no credit card.",
        s["body"],
    ))

    story.append(Paragraph("2. Import the repository as a new project", s["h3"]))
    for line in [
        "Click <b>Add New → Project</b> and select the <b>ericgitonga/career-transition</b> "
        "repository",
        "Because this is a monorepo shared with the <b>landing/</b> Next.js app, set "
        "<b>Root Directory</b> to <b>intake</b> before the first deploy — otherwise Vercel "
        "tries to build the repo root, which isn't a valid app on its own",
        "Vercel auto-detects <b>vercel.json</b>'s <b>\"framework\": \"flask\"</b> setting and "
        "configures the build itself — there is no build or start command to enter manually",
        "Click <b>Deploy</b> for the first build (it will complete once the environment "
        "variables from step 4 are added — a failed first deploy due to a missing "
        "<b>RESEND_API_KEY</b> is expected and fine to ignore)",
    ]:
        story.append(Paragraph(f"• {line}", s["step"]))

    story.append(Paragraph("3. Sign up for Resend (email delivery)", s["h3"]))
    story.append(Paragraph(
        "Resend is a transactional email service that sends over HTTPS — it is never blocked "
        "by hosting providers the way SMTP is. The free tier allows 3,000 emails per month.",
        s["body"],
    ))
    for line in [
        "Go to <b>https://resend.com</b> and sign up using the consultant's email address "
        "(e.g. example@gmail.com) — this becomes the verified recipient address",
        "In the Resend dashboard, go to <b>API Keys → Create API Key</b>",
        "Give it a name (e.g. <i>career-transition-form</i>) and copy the key — it is shown only once",
    ]:
        story.append(Paragraph(f"• {line}", s["step"]))

    story.append(Paragraph("4. Add environment variables in Vercel", s["h3"]))
    story.append(Paragraph(
        "In the Vercel project, go to <b>Settings → Environment Variables</b> and add:",
        s["body"],
    ))
    for line in [
        "<b>RESEND_API_KEY</b> — required. The API key copied from step 3.",
        "<b>SECRET_KEY</b> — required in production, and specifically important on Vercel: "
        "without a fixed value the app auto-generates a random one per warm Fluid Compute "
        "instance, causing intermittent CSRF failures once real traffic is split across more "
        "than one instance. Generate one with "
        "<i>python -c \"import secrets; print(secrets.token_hex(32))\"</i> and set it as a "
        "fixed value — never regenerate it after clients start using the live form.",
        "<b>RATELIMIT_STORAGE_URI</b> — required in production. Provision a Redis database via "
        "<b>Storage → Marketplace Database Providers → Upstash</b> in the Vercel dashboard, "
        "then copy the <b>rediss://</b> connection string from the <i>Upstash console's own "
        "\"Connect\" tab</i> — not the REST endpoint Vercel's own integration page surfaces by "
        "default (<b>UPSTASH_REDIS_REST_URL</b>/<b>_TOKEN</b>), which this app's rate limiter "
        "can't use. Without this, every auto-scaled instance keeps its own separate counter, "
        "silently multiplying every rate limit.",
        "<b>FROM_EMAIL</b> — optional. Only needed to send from a verified custom domain "
        "instead of Resend's shared <i>onboarding@resend.dev</i> address.",
    ]:
        story.append(Paragraph(f"• {line}", s["step"]))
    story.append(Paragraph(
        "<i>The app reads all of these from the environment automatically. "
        "Never put a key or connection string in the code or the repository.</i>",
        s["note"],
    ))
    story.append(Paragraph(
        "Save, then redeploy from the <b>Deployments</b> tab so the new variables take effect.",
        s["body"],
    ))

    story.append(rule(color=MGRAY, thickness=0.5))

    # ── HOW IT WORKS ─────────────────────────────────────────────────────────
    story.append(KeepTogether([
        section_header("How It Works", s),
        Spacer(1, 0.25 * cm),
    ]))

    story.append(Paragraph("Client experience", s["h3"]))
    story.append(Paragraph(
        "Clients open the URL, complete the 10-section light-themed accordion form, "
        "optionally upload documents (CV, LinkedIn export, job description, learning plan, "
        "and additional files), then click <b>Submit Onboarding Form</b>. "
        "The server generates a PDF, emails it to the consultant automatically, "
        "and triggers a download in the client's browser. "
        "No credentials, no email settings, and no configuration are shown to clients.",
        s["body"],
    ))

    story.append(Paragraph("Email sender address", s["h3"]))
    story.append(Paragraph(
        "By default the form sends from <b>onboarding@resend.dev</b> (Resend's shared address). "
        "To send from a custom domain (e.g. <i>noreply@yourdomain.com</i>), verify the domain "
        "in the Resend dashboard and set the <b>FROM_EMAIL</b> environment variable in Vercel "
        "with the desired address.",
        s["body"],
    ))

    story.append(rule(color=MGRAY, thickness=0.5))

    # ── DEPLOYING ────────────────────────────────────────────────────────────
    story.append(KeepTogether([
        section_header("Deploying Updates", s),
        Spacer(1, 0.25 * cm),
        Paragraph(
            "Push any change to the main branch — Vercel picks it up and redeploys "
            "automatically:",
            s["body"],
        ),
        Spacer(1, 0.15 * cm),
    ]))
    story.append(code_block("git push origin main", s))
    story.append(Spacer(1, 0.15 * cm))
    story.append(Paragraph(
        "A pull request gets its own throwaway <b>Preview</b> deployment first, so a change "
        "can be checked live before it reaches real clients; merging to <b>main</b> promotes "
        "it to <b>Production</b> at the permanent URL below.",
        s["body"],
    ))

    story.append(rule(color=MGRAY, thickness=0.5))

    # ── AFTER DEPLOYMENT ─────────────────────────────────────────────────────
    story.append(KeepTogether([
        section_header("After Deployment", s),
        Spacer(1, 0.25 * cm),
    ]))

    story.append(Paragraph("Your URL", s["h3"]))
    story.append(Paragraph(
        "Vercel assigns a permanent URL shown at the top of the project dashboard:",
        s["body"],
    ))
    story.append(code_block("https://career-transition-intake.vercel.app", s))
    story.append(Spacer(1, 0.15 * cm))
    story.append(Paragraph(
        "This URL does not change between deploys.",
        s["note"],
    ))

    story.append(Paragraph("Cold starts", s["h3"]))
    story.append(Paragraph(
        "Vercel's Fluid Compute has sub-second cold starts even after a period of "
        "inactivity — unlike a free-tier server that spins down and takes tens of seconds to "
        "wake up, there is no visible loading delay to warn clients about.",
        s["body"],
    ))

    story.append(Paragraph("Rotating the Resend API key", s["h3"]))
    story.append(Paragraph(
        "Go to the Resend dashboard, revoke the old key and create a new one. "
        "Then go to <b>Vercel → Settings → Environment Variables</b>, update "
        "<b>RESEND_API_KEY</b>, and redeploy from the <b>Deployments</b> tab to apply it.",
        s["body"],
    ))

    return story


def make_doc():
    """Build the complete hosting guide PDF and write it to ``OUTPUT_PATH``.

    Orchestrates the full generation pipeline:
      1. Calls ``styles()`` to obtain the shared paragraph style dictionary.
      2. Creates a ``SimpleDocTemplate`` configured for A4 with standard margins.
      3. Defines a ``footer`` callback that ReportLab invokes on every page to
         render a centred grey caption with the service name and page number.
      4. Calls ``build_story()`` to obtain the flowable list.
      5. Builds the document, applying the footer on every page.
      6. Prints the output path to stdout on success.

    The output file is written to the same directory as this script
    (``hosting.pdf``), as defined by ``OUTPUT_PATH``.
    """
    s = styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.5 * cm, bottomMargin=1.8 * cm,
    )

    def footer(canvas, doc):
        """Draw a centred page-number caption at the bottom of each page.

        Called by ReportLab's build pipeline via ``onFirstPage`` and
        ``onLaterPages``. Renders grey 8pt text showing the service name
        and the current page number.

        Args:
            canvas: The ReportLab canvas for the current page.
            doc:    The SimpleDocTemplate being built (provides ``doc.page``).
        """
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawCentredString(W / 2, 0.7 * cm,
                                 f"Career Transition Planning Service  ·  Page {doc.page}")
        canvas.restoreState()

    doc.build(build_story(s), onFirstPage=footer, onLaterPages=footer)
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    make_doc()
