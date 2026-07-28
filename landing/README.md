# Career Transition Planning — Landing Page

Marketing landing page for the Career Transition Planning service. Copy lives in
[`career-transition-intake`](https://github.com/ericgitonga/career-transition-intake)'s
`Clients/Eric/eric_copy.md`, rewritten against the "Build A Sales Page That Converts"
framework (headline, pain points, offer, who-it's-for / who-it's-not, CTA, testimonials).

The primary call-to-action links out to the client intake form, hosted separately at
https://career-transition-loading.onrender.com. Payment collection and on-page pricing are
not yet wired up — that's a deliberate future addition, not an oversight.

## Stack

Next.js (App Router, TypeScript, Tailwind CSS) — same setup as
[en-mascaradores](https://github.com/ericgitonga/en-mascaradores), kept separate from the
intake form because the two are different concerns on different platforms: this is a
static marketing page on Vercel, the intake form is a Flask app on Render.

## Run locally

```bash
npm install
npm run dev
```

Opens on `http://localhost:3000`.

## Deployment

Runs on [Vercel](https://vercel.com): every PR gets a Preview deployment, merging to
`main` promotes to production.
