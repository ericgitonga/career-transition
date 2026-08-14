import type { NextConfig } from "next";

// ── Baseline HTTP security headers ──────────────────────────────────────────
//
// Mirrors the header/CSP shape already applied to the intake Flask app (see
// intake/app.py's `_security_headers`), adapted for this app's actual
// requirements:
//   X-Content-Type-Options  — prevents MIME-type sniffing attacks.
//   X-Frame-Options         — blocks clickjacking via iframe embedding.
//   Referrer-Policy         — limits URL leakage to cross-origin requests.
//   Permissions-Policy      — revokes unnecessary browser feature access.
//   Content-Security-Policy — restricts script/style/font/image sources.
//
// Unlike intake, this app has no third-party CDN dependency (next/font
// self-hosts Geist at build time, and @vercel/analytics + @vercel/speed-insights
// load same-origin `/_vercel/*` paths), so style-src/font-src stay 'self'-only.
// script-src does need 'unsafe-inline': the Next.js App Router injects an
// inline bootstrap script for RSC hydration payloads on every page.
const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "geolocation=(), microphone=()" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline'",
      "style-src 'self'",
      "img-src 'self' data:",
      "font-src 'self'",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
