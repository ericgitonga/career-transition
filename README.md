# Career Transition Planning

Monorepo for the Career Transition Planning service — two apps, two independent Vercel
projects, one shared git history.

- **[`landing/`](landing/)** — the public marketing page (Next.js). Deploys to
  `career-transition-psi.vercel.app`.
- **[`intake/`](intake/)** — the client onboarding form (Flask). Deploys to
  `career-transition-intake.vercel.app`. Its call-to-action links from `landing/`.

Each subdirectory has its own `README.md`, `CHANGELOG.md`, `VERSION`, and — since they're
different stacks (Next.js vs. Flask) — its own dependency/build setup. They're combined
here for one point of maintenance (one git history, one issue tracker, one PR review
surface), not because they share code or a deployment.

## History

Previously two separate repos — `career-transition` (landing) and
`career-transition-intake` (intake) — merged into this one via `git filter-repo`, with
each app's full commit history preserved under its own subdirectory rather than
squashed. `career-transition-intake`'s GitHub repo (issues, PRs, releases) stays up as a
historical archive; this repo is where active development happens going forward.

## CI

Each app has its own workflows, gated by a required `e2e`/`unit`/`lint` status check:

- `landing/`: `.github/workflows/e2e.yml` runs its Playwright E2E suite, plus `unit` (Vitest)
  and `lint` (ESLint).
- `intake/`: `.github/workflows/e2e-intake.yml` runs its Playwright E2E suite;
  `.github/workflows/unit-intake.yml` runs its pytest unit suite and `lint` (ruff).

Every workflow triggers on every PR; each starts with a `changes` job that checks whether its
app's directory actually changed and skips the rest of the jobs (not the whole workflow) when
it didn't — a skipped job still satisfies a required status check, so a PR touching neither
`landing/**` nor `intake/**` (e.g. a root-level docs change) isn't stuck waiting on a check that
can never run (see #90).

## Deployment

Both Vercel projects are linked to this repo, each with its own **Root Directory**
setting (`landing` / `intake`) so they build and deploy independently — a change to one
app doesn't trigger a rebuild of the other.
