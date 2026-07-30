# Career Transition Intake

Client onboarding form for the Career Transition Planning service.
Collects structured intake responses across 10 sections, compiles them into a PDF, and emails the PDF and any uploaded documents to the consultant automatically via [Resend](https://resend.com).

The public-facing marketing page lives alongside this app at
[`../landing`](../landing) (Next.js) — a sibling directory in the same repo, not a
separate one (see the root README), kept as its own subdirectory/Vercel project since
it's a different stack (Next.js vs. Flask). Its call-to-action links to this service's
client entry point.

## Deployment

Deployed to [Vercel](https://vercel.com) as a Python (Flask) Serverless Function —
migrated off Render (see #38). Vercel redeploys automatically on every push to `main`.

**Note:** [hosting.pdf](hosting.pdf) still describes the old Render setup and hasn't
been regenerated for Vercel yet.
