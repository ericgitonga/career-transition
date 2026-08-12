# Changelog

All notable changes to this project are documented here. Versioning follows
[Semantic Versioning](https://semver.org): MAJOR.MINOR.PATCH. This project is
pre-1.0 (initial development) — the major version stays at `0` until a stable,
production-ready release is declared. MINOR bumps cover new features and
user-facing changes; PATCH bumps cover fixes, docs, and housekeeping.

## [0.7.0] - 2026-08-12

### Changed
- Replaced the single flat-fee pricing card with two tiers — **Basic** (the
  Career Transition Plan + an ATS-safe CV rewrite) and **Advanced** (Basic
  plus one Notesletter — interview prep notes and a tailored cover letter —
  included for a first job application, with additional applications billed
  separately on the intake side). This retires the previous no-CV "Plan
  only" product; Basic is now the pricing floor. Pricing: Basic KES
  10,000 intro / KES 18,500 regular; Advanced KES 14,000 intro / KES 22,000
  regular, both effective immediately through 31 August 2026. New
  `PRICING_TIERS` typed array replaces the hardcoded card, following the
  existing `DELIVERABLES`/`STEPS`/`TESTIMONIALS` convention. Section heading
  changed from "Simple, upfront pricing" to "Two tiers, one flat fee each".
  The "what you get" section's CV-rewrite mention updated to reflect it as
  standard for every client rather than an opt-in checkbox. Grounded in the
  market-pricing deep dive at `intake/extras/career-pricing.pdf`. Paired
  with the intake-side tier-capture change (closes #71).

tag: `landing-v0.7.0`

## [0.6.5] - 2026-08-11

### Added
- Real Vitest unit suite (`src/app/page.test.ts`, 7 tests) covering the
  page's content data and constants (`DELIVERABLES`, `STEPS`,
  `TESTIMONIALS`, `PAIN_POINTS`, `WHO_FOR`, `WHO_NOT_FOR`, `INTAKE_URL`,
  `CONTACT_EMAIL`) — page.tsx has no other pure logic to unit-test, but
  these are real existing values worth asserting non-empty/well-formed
  rather than fabricated test targets. Replaces the `unit` job's `echo`
  placeholder from #62/PR #63 with an actual test run. (closes #64)

tag: `landing-v0.6.5`

## [0.6.4] - 2026-08-11

### Added
- ESLint now runs as its own independently-gated CI check (`lint` job in
  `.github/workflows/e2e.yml`) — it was configured in `package.json` but
  never invoked in CI, so a lint regression that didn't break the build
  could merge unnoticed. Also brings `package.json`'s `"version"` back in
  sync with this file (it had drifted to 0.6.2). (closes #62)
- Added a trivial `unit` job to `e2e.yml`, discovered as a blocker while
  merging the above: the ruleset requires a `unit` status check, but it was
  only ever posted by `unit-intake.yml` (path-filtered to `intake/**`), so
  a landing-only PR could never satisfy it. `landing/` has no unit-test
  suite of its own to actually run yet, so this job is a placeholder —
  mirrors how `e2e`/`e2e-intake.yml` already share a job name so either
  app's changes satisfy that check standalone.

tag: `landing-v0.6.4`

## [0.6.3] - 2026-08-07

### Fixed

- Standardised American spelling to British spelling ("colored" → "coloured")
  in a changelog entry. (closes #58)

## [0.6.2] - 2026-08-04

### Changed

- Pricing section now states the introductory 50% off offer ends August 31, 2026,
  instead of the vague "won't be around for long" — visitors see exactly when it
  reverts to full price. (closes #50)

tag: `landing-v0.6.2`

## [0.6.1] - 2026-08-03

### Changed

- Added first-name attribution to both landing-page testimonials
  (Jacqueline, Emmanuel), and gave the second a from/to transition framing
  (Software Engineering Professional to farming) in place of the
  anonymized "referred within a professional brotherhood" line. Quote
  text unchanged. (closes #48)
- Dropped the hard-coded em-dash prefix in the testimonial footer markup
  in favor of a "Name - Role" separator baked into each attribution
  string.

tag: `landing-v0.6.1`

## [0.6.0] - 2026-08-03

### Changed

- Replaced the second landing-page testimonial (colleague-referral quote)
  with a new direct-referral testimonial, condensed to match the site's
  existing terse, first-person tone. (closes #45)

tag: `landing-v0.6.0`

## [0.5.0] - 2026-08-03

### Added

- Vercel Web Analytics (`@vercel/analytics`) and Speed Insights
  (`@vercel/speed-insights`) instrumentation, rendered from the root
  layout. Feeds pageview/visitor and Core Web Vitals data into the new
  cross-project `vercel-metrics` pipeline. Enabling the Web
  Analytics/Speed Insights toggle in the Vercel project dashboard is a
  manual follow-up. (closes #39)

tag: `landing-v0.5.0`

## [0.4.0] - 2026-08-01

### Changed

- The pain-points copy's "where do I actually begin?" link is now bold and
  coloured `#C9A84C` — the same gold as the "Start My Plan" button's
  background — so it reads as a CTA within the paragraph rather than just
  an italicized link. (closes #27)

tag: `landing-v0.4.0`

## [0.3.1] - 2026-08-01

### Changed

- Backfilled changelog entry — no code change. This app's history was
  relocated into the `career-transition` monorepo as `landing/`, alongside
  `career-transition-intake`'s history as `intake/`, so both apps now
  share one git history, one issue tracker, and one PR review surface
  while staying on separate Vercel projects. Never versioned at the time
  it happened. (refs #8)

tag: `landing-v0.3.1`

## [0.3.0] - 2026-08-01

### Changed

- The pain-points copy's "where do I actually begin?" is now a link to the
  intake form (`INTAKE_URL`), styled italic + underline, giving that line a
  direct path into the funnel instead of relying solely on the `CtaButton`s
  elsewhere on the page. (closes #22)
- Added `__pycache__/`/`*.pyc` to `.gitignore` — the `e2e/` suite is Python
  but this Next.js project's `.gitignore` had no Python entries.

Tagged `landing-v0.3.0` rather than the bare `v0.3.0` used by `v0.1.0`/
`v0.2.0` — the bare `v*` namespace turned out to still hold intake's old
pre-rename tags up through `v0.21.8`, so all landing releases from here
switch to a `landing-` prefix to avoid colliding with them. Existing
`v0.1.0`/`v0.2.0` are left as-is.

tag: `landing-v0.3.0`

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
