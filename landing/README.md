# Career Transition Planning — Landing Page

Marketing landing page for the Career Transition Planning service. Copy lives in
[`../intake`](../intake)'s `Clients/Eric/eric_copy.md`, rewritten against the "Build A
Sales Page That Converts" framework (headline, pain points, offer, who-it's-for /
who-it's-not, CTA, testimonials).

The primary call-to-action links out to the client intake form at
https://career-transition-intake.vercel.app. On-page pricing (KES 7,500 flat) is live;
payment collection at submission time is not yet wired up — see [`../intake`](../intake)'s
issue #37, a deliberate future addition, not an oversight.

## Stack

Next.js (App Router, TypeScript, Tailwind CSS) — same setup as
[en-mascaradores](https://github.com/ericgitonga/en-mascaradores). Kept as a separate
subdirectory from `../intake` (not a separate repo — see the root README) since the two
are different stacks (Next.js vs. Flask) deployed as separate Vercel projects, even
though they now share one git history.

## Run locally

```bash
npm install
npm run dev
```

Opens on `http://localhost:3000`.

## Deployment

Runs on [Vercel](https://vercel.com): every PR gets a Preview deployment, merging to
`main` promotes to production.
