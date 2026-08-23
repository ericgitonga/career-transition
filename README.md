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

Each app has its own path-filtered workflows, so a change to one doesn't trigger the other's
suite:

- `landing/`: `.github/workflows/e2e.yml` runs its Playwright E2E suite (`landing/**`).
- `intake/`: `.github/workflows/e2e-intake.yml` runs its Playwright E2E suite and
  `.github/workflows/unit-intake.yml` runs its pytest unit suite and lint (`intake/**`).

## Deployment

Both Vercel projects are linked to this repo, each with its own **Root Directory**
setting (`landing` / `intake`) so they build and deploy independently — a change to one
app doesn't trigger a rebuild of the other.
