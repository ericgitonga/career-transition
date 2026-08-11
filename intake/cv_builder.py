"""
Shared CV PDF engine — for condensing/reframing a client's own CV on request.

Same philosophy as report_builder.py: one shared engine, all ReportLab code
here; a client's own file (Clients/<Name>/cv_data.py) holds only content — a
CV dict, never ReportLab code. See generate_cv.py for the CLI that ties the
two together.

Reuses report_builder.py's palette and generic layout helpers (two_col,
data_table, rule, footer_canvas_factory) for visual consistency with the
Transition Plan, but the layout itself is deliberately plainer and more
ATS-safe: single-column body flow throughout, no priority-colour cells or
card headers, minimal use of tables (only for genuinely tabular content).
Colour is used only for the name and section headers — ATS parsers extract
text, not colour, so this does not affect machine-readability; what would
break it is multi-column body text or content rendered as images, neither
of which this engine does.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
)

from report_builder import (
    NAVY, TEAL, GOLD, MGRAY, BLACK, WHITE,
    W, H, MARGIN, INNER_W,
    two_col, data_table, rule, footer_canvas_factory, esc,
)

CV_ST = {
    "name":        ParagraphStyle("cvname", fontName="Helvetica-Bold", fontSize=20,
                                  textColor=NAVY, leading=24, alignment=TA_LEFT),
    "contact":     ParagraphStyle("cvcontact", fontName="Helvetica", fontSize=9,
                                  textColor=colors.HexColor("#555555"), leading=13),
    "section":     ParagraphStyle("cvsec", fontName="Helvetica-Bold", fontSize=11,
                                  textColor=NAVY, leading=14, spaceBefore=10, spaceAfter=2),
    "summary":     ParagraphStyle("cvsum", fontName="Helvetica", fontSize=9.5,
                                  textColor=BLACK, leading=14, alignment=TA_JUSTIFY),
    "entry_title": ParagraphStyle("cvet", fontName="Helvetica-Bold", fontSize=10,
                                  textColor=BLACK, leading=13),
    "entry_org":   ParagraphStyle("cveo", fontName="Helvetica-Oblique", fontSize=9.5,
                                  textColor=TEAL, leading=13),
    "entry_dates": ParagraphStyle("cved", fontName="Helvetica-Oblique", fontSize=9,
                                  textColor=colors.HexColor("#555555"), leading=13,
                                  alignment=TA_CENTER),
    "bullet":      ParagraphStyle("cvbu", fontName="Helvetica", fontSize=9,
                                  textColor=BLACK, leading=12.5, spaceAfter=2, leftIndent=10),
    "condensed":   ParagraphStyle("cvco", fontName="Helvetica", fontSize=9,
                                  textColor=BLACK, leading=12.5, spaceAfter=4),
    "plain_list":  ParagraphStyle("cvpl", fontName="Helvetica", fontSize=9,
                                  textColor=BLACK, leading=13, spaceAfter=1, leftIndent=10),
}


def section_header(text, story):
    story.append(Paragraph(esc(text).upper(), CV_ST["section"]))
    story.append(rule(color=GOLD, thick=0.75, before=1, after=6))


def render_header(client, story):
    story.append(Paragraph(esc(client["name"]), CV_ST["name"]))
    contact_bits = [client["location"], client["email"]]
    if client.get("languages_line"):
        contact_bits.append(client["languages_line"])
    if client.get("links"):
        contact_bits.extend(client["links"])
    story.append(Paragraph("  ·  ".join(esc(b) for b in contact_bits), CV_ST["contact"]))
    story.append(Spacer(1, 8))


def render_summary(text, story):
    section_header("Professional Summary", story)
    story.append(Paragraph(esc(text), CV_ST["summary"]))
    story.append(Spacer(1, 8))


def render_competencies(items, story):
    section_header("Core Competencies", story)
    half = (len(items) + 1) // 2
    story.append(two_col(items[:half], items[half:]))
    story.append(Spacer(1, 8))


def render_experience(entries, story, heading="Professional Experience"):
    section_header(heading, story)
    for e in entries:
        header = Table(
            [[Paragraph(esc(e["title"]), CV_ST["entry_title"]),
              Paragraph(esc(e["dates"]), CV_ST["entry_dates"])]],
            colWidths=[INNER_W * 0.72, INNER_W * 0.28],
        )
        header.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ]))
        story.append(header)
        story.append(Paragraph(esc(e["org"]), CV_ST["entry_org"]))
        story.append(Spacer(1, 2))
        for b in e["bullets"]:
            story.append(Paragraph(f"•  {esc(b)}", CV_ST["bullet"]))
        story.append(Spacer(1, 8))


def render_condensed_experience(entries, story, heading="Earlier Experience"):
    section_header(heading, story)
    for e in entries:
        story.append(Paragraph(
            f"<b>{esc(e['title'])}</b>, {esc(e['org'])} "
            f"<font color='#555555'><i>({esc(e['dates'])})</i></font> — {esc(e['summary'])}",
            CV_ST["condensed"],
        ))
    story.append(Spacer(1, 8))


def render_table_section(heading, headers, rows, col_ratios, story):
    section_header(heading, story)
    story.append(data_table(headers, rows, col_ratios))
    story.append(Spacer(1, 8))


def render_plain_list_section(heading, items, story):
    section_header(heading, story)
    for item in items:
        story.append(Paragraph(f"•  {esc(item)}", CV_ST["plain_list"]))
    story.append(Spacer(1, 8))


def render_references(entries, story):
    """entries: list of {name, title, org, phone (optional), email (optional)}."""
    section_header("References", story)
    for e in entries:
        story.append(Paragraph(
            f"<b>{esc(e['name'])}</b> — {esc(e['title'])}, {esc(e['org'])}",
            CV_ST["condensed"],
        ))
        contact_bits = []
        if e.get("phone"):
            contact_bits.append(f"Tel: {e['phone']}")
        if e.get("email"):
            contact_bits.append(f"Email: {e['email']}")
        if contact_bits:
            story.append(Paragraph(esc("  ·  ".join(contact_bits)), CV_ST["contact"]))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 4))


def build_cv(data, output_path):
    client = data["client"]
    doc_title = f"{client['name']} — CV"

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.2 * cm,
        title=doc_title,
    )
    story = []

    render_header(client, story)
    render_summary(data["summary"], story)
    render_competencies(data["core_competencies"], story)
    render_experience(data["experience"], story)
    if data.get("earlier_experience"):
        render_condensed_experience(data["earlier_experience"], story)
    if data.get("additional_experience"):
        ae = data["additional_experience"]
        render_table_section(
            ae["heading"], ae["headers"], ae["rows"], ae.get("col_ratios"), story,
        )
    if data.get("institutional_relationships"):
        render_plain_list_section(
            "Institutional Relationships & Recognition",
            data["institutional_relationships"], story,
        )
    render_plain_list_section("Education", data["education"], story)
    if data.get("certifications"):
        render_plain_list_section("Certifications", data["certifications"], story)
    if data.get("professional_courses"):
        render_plain_list_section("Professional Courses (Selected)", data["professional_courses"], story)
    if data.get("references"):
        render_references(data["references"], story)

    doc.build(story, onFirstPage=footer_canvas_factory(doc_title), onLaterPages=footer_canvas_factory(doc_title))
