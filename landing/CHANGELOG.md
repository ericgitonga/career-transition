# Changelog

All notable changes to this project are documented here. Versioning follows
[Semantic Versioning](https://semver.org): MAJOR.MINOR.PATCH. This project is
pre-1.0 (initial development) — the major version stays at `0` until a stable,
production-ready release is declared. MINOR bumps cover new features and
user-facing changes; PATCH bumps cover fixes, docs, and housekeeping.

## [0.3.0] - 2026-08-01

### Changed

- The pain-points copy's "where do I actually begin?" is now a link to the
  intake form (`INTAKE_URL`), styled italic + underline, giving that line a
  direct path into the funnel instead of relying solely on the `CtaButton`s
  elsewhere on the page. (closes #22)
- Added `__pycache__/`/`*.pyc` to `.gitignore` — the `e2e/` suite is Python
  but this Next.js project's `.gitignore` had no Python entries.

tag: `v0.3.0`

## [0.2.0] - 2026-07-29

### Added

- Playwright-based E2E smoke suite in `e2e/` covering the golden path (page
  loads, metadata correct, every section renders, footer copyright present)
  and every "Start My Plan" CTA / contact link pointing at the right target
  — mirroring the pattern used in `umoja-voices`/`ebc-songs`/`merch-mockup`,
  simplified since this app has no auth/database/forms of its own.
- `.github/workflows/e2e.yml` gates every PR to `main` on the suite, running
  it against a production build (`next build && next start`) on the runner
  — no Vercel/Supabase secrets needed since there's nothing here to diverge
  from a real deployment. (closes #1)

tag: `v0.2.0`

## [0.1.0] - 2026-07-28

### Added

- Initial scaffold of the Career Transition Planning landing page: Next.js
  (App Router, TypeScript, Tailwind CSS), same stack as `en-mascaradores`.
  Hero, pain points, deliverables, who-it's-for/who-it's-not, how-it-works,
  testimonials, and contact sections, with the primary CTA linking out to
  the client intake form hosted separately at
  `career-transition-loading.onrender.com`.
- Semantic versioning and this changelog, following the convention used in
  `umoja-voices`/`ebc-songs`/`merch-mockup` (closes #2).

tag: `v0.1.0`
