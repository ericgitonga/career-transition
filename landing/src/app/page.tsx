const INTAKE_URL = "https://career-transition-intake.vercel.app";
const CONTACT_EMAIL = "gitonga@gmail.com";

type Deliverable = {
  title: string;
  description: string;
};

const DELIVERABLES: Deliverable[] = [
  {
    title: "Where you stand today",
    description:
      "A clear-eyed summary of your strengths and how they read in your target sector.",
  },
  {
    title: "Where you're heading",
    description:
      "3–5 concrete role archetypes you're credibly qualified to pursue, with matching organisations in your market.",
  },
  {
    title: "The gap, mapped precisely",
    description:
      "A skills gap analysis showing what you already have, what you need, and how urgently.",
  },
  {
    title: "An 18-month roadmap",
    description:
      "Structured in semesters, with specific courses, certifications, and milestones for each phase.",
  },
  {
    title: "A certifications plan with costs",
    description: "Real programmes, real providers, real prices — including free options.",
  },
  {
    title: "A networking and visibility strategy",
    description: "How to activate your existing network and build presence in the new sector.",
  },
  {
    title: "A portfolio plan",
    description:
      "6–10 pieces of work you can build now, without needing an employer to give you permission.",
  },
  {
    title: "A monthly action tracker",
    description: "So you know exactly what to do in month one, month six, and month twelve.",
  },
  {
    title: "Your new professional narrative",
    description:
      "An elevator pitch ready to use, and a table that reframes your experience into the language your target sector speaks.",
  },
];

const PAIN_POINTS: string[] = [
  "Tired of collecting career advice from podcasts and LinkedIn posts that never turns into an actual next step?",
  "Spent a weekend making notes, watching videos, and bookmarking courses — and you're no closer to a plan than when you started?",
  "Know you're capable of more, but can't figure out how to say “10 years in regulatory compliance” in the language a new industry actually listens for?",
  "Watched a colleague make the leap into something new and wondered, quietly, why you're still sitting on the same CV?",
];

const WHO_FOR: string[] = [
  "Mid-career professionals ready to pivot to a new sector or specialisation",
  "People leaving corporate employment to start their own consultancy or advisory practice",
  "Professionals who want to layer a new domain — AI, ESG, data compliance, digital transformation — onto an existing career",
  "Anyone who has tried to figure this out alone, generated a mess of notes and YouTube playlists, and still doesn't have a plan",
];

const WHO_NOT_FOR: string[] = [
  "Anyone looking for a quick CV reformat rather than an actual transition strategy",
  "Anyone who wants a six-week coaching relationship with weekly check-in calls",
  "Anyone hoping a document alone will do the work — the plan tells you exactly what to do, but the doing is still yours",
  "Anyone not planning to actually move in the next 12–18 months (this is a working roadmap, not inspirational reading)",
];

type Step = {
  number: string;
  title: string;
  description: string;
};

const STEPS: Step[] = [
  {
    number: "1",
    title: "Send your materials",
    description:
      "Your CV, a job description for the kind of role you want, and any notes on where you'd like to go.",
  },
  {
    number: "2",
    title: "It's built by hand",
    description:
      "Every section is worked through against your specific answers — not templated, not auto-generated. Delivered as a professional PDF within one working day.",
  },
  {
    number: "3",
    title: "It's yours",
    description: "Study it, share it, use it to hold yourself accountable.",
  },
];

type Testimonial = {
  quote: string;
  attribution: string;
};

const TESTIMONIALS: Testimonial[] = [
  {
    quote: "Way above and beyond anything I had tried to generate on my own.",
    attribution: "Compliance & Regulatory Professional, FMCG sector",
  },
  {
    quote:
      "It articulated my aspirations succinctly and mapped out a credible, actionable course of action — it's clarified a lot of my thinking.",
    attribution: "Emmanuel Kitonyo, Software Engineering Professional transitioning to farming",
  },
];

function CtaButton({ className = "" }: { className?: string }) {
  return (
    <a
      href={INTAKE_URL}
      className={`inline-flex items-center justify-center rounded-full bg-[#C9A84C] px-6 py-3 text-base font-semibold text-[#1B2A4A] transition-colors hover:bg-[#dab866] ${className}`}
    >
      Start My Plan
    </a>
  );
}

export default function Home() {
  return (
    <div className="flex flex-col flex-1 font-sans">
      <header className="bg-[#1B2A4A] text-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
          <span className="text-lg font-semibold tracking-tight">
            Career Transition Planning
          </span>
          <CtaButton />
        </div>
      </header>

      <section className="bg-[#1B2A4A] text-white">
        <div className="mx-auto max-w-5xl px-6 pb-20 pt-10 sm:pb-28 sm:pt-16">
          <h1 className="max-w-2xl text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
            Your next career isn&apos;t a guess. It&apos;s a plan.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
            You&apos;ve built real expertise — in compliance, in finance, in operations, in
            development. You&apos;re good at what you do. But the industry&apos;s shifting,
            the role no longer fits, or you&apos;re simply ready for something different.
          </p>
          <p className="mt-4 max-w-xl text-lg font-medium leading-8 text-[#C9A84C]">
            The problem was never your skills. It&apos;s that no one has shown you how to
            translate them.
          </p>
          <CtaButton className="mt-8" />
        </div>
      </section>

      <section id="pain-points" className="bg-white">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
            Does this sound familiar?
          </h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2">
            {PAIN_POINTS.map((point) => (
              <div
                key={point}
                className="rounded-lg border border-slate-200 p-6 text-base leading-7 text-slate-700"
              >
                {point}
              </div>
            ))}
          </div>
          <p className="mt-10 max-w-3xl text-base leading-7 text-slate-600">
            You open a blank document and try to plan your own transition. Twenty minutes
            later you have a list of course names, three tabs open on certifications
            you&apos;re not sure you need, and the same question you started with:{" "}
            <a
              href={INTAKE_URL}
              className="italic font-bold text-[#C9A84C] underline hover:no-underline"
            >
              where do I actually begin?
            </a>
          </p>
          <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600">
            That&apos;s not a you problem. That&apos;s what happens when you try to plan a
            career move with generic advice instead of a structured process built around
            your actual CV, your actual target role, and your actual timeline.
          </p>
          <p className="mt-4 max-w-3xl text-lg font-semibold text-slate-900">
            That&apos;s what this service does.
          </p>
        </div>
      </section>

      <section id="what-you-get" className="bg-slate-50">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
            What you get
          </h2>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
            A professionally designed, personalised Career Transition Plan — not a
            template, not generic advice, but a structured document built around your
            specific CV, your target role, and your timeline.
          </p>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {DELIVERABLES.map((item) => (
              <div key={item.title} className="rounded-lg bg-white p-6 shadow-sm">
                <h3 className="text-base font-semibold text-[#1B2A4A]">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.description}</p>
              </div>
            ))}
          </div>
          <p className="mt-10 max-w-2xl text-base italic leading-7 text-slate-600">
            Nine sections, each one worked through against your actual CV and target role —
            not a five-minute AI summary with your name swapped in. The depth is the point.
          </p>
          <p className="mt-6 max-w-2xl text-base leading-7 text-slate-600">
            Want your CV itself condensed and reframed for your target role, alongside the
            plan? Tick the box on the intake form and it&apos;s handled with the same care —
            no separate reformatting service, no extra back-and-forth.
          </p>
          <CtaButton className="mt-8" />
        </div>
      </section>

      <section id="who-for" className="bg-white">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <div className="grid gap-12 sm:grid-cols-2">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
                Who this is for
              </h2>
              <ul className="mt-6 space-y-4">
                {WHO_FOR.map((item) => (
                  <li key={item} className="flex gap-3 text-base leading-7 text-slate-700">
                    <span className="text-[#0E7C7B]">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
                Who this is NOT for
              </h2>
              <ul className="mt-6 space-y-4">
                {WHO_NOT_FOR.map((item) => (
                  <li key={item} className="flex gap-3 text-base leading-7 text-slate-700">
                    <span className="text-slate-400">✕</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
              <p className="mt-6 text-sm leading-6 text-slate-500">
                If that&apos;s you, this isn&apos;t the right fit — and that&apos;s fine. If
                you&apos;re actually ready to move and just need the path laid out, keep
                reading.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="bg-slate-50">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
            How it works
          </h2>
          <div className="mt-10 grid gap-8 sm:grid-cols-3">
            {STEPS.map((step) => (
              <div key={step.number} className="flex flex-col gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-[#0E7C7B] text-lg font-semibold text-white">
                  {step.number}
                </span>
                <h3 className="text-lg font-semibold text-slate-900">{step.title}</h3>
                <p className="text-sm leading-6 text-slate-600">{step.description}</p>
              </div>
            ))}
          </div>
          <p className="mt-10 text-base font-medium text-slate-700">
            No discovery calls that go nowhere. No six-week coaching programmes. Just one
            document — but a genuinely thorough one, built section by section against your
            actual CV, not skimmed together in an afternoon.
          </p>
        </div>
      </section>

      <section id="pricing" className="bg-white">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
            Simple, upfront pricing
          </h2>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
            One flat fee for the complete Career Transition Plan. No hidden costs, no
            upsells.
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 rounded-lg border border-slate-200 bg-slate-50 p-10 text-center">
            <span className="text-sm font-semibold uppercase tracking-wide text-[#0E7C7B]">
              Introductory offer — 50% off
            </span>
            <div className="flex items-baseline gap-3">
              <span className="text-lg text-slate-400 line-through">KES 7,500</span>
              <span className="text-4xl font-bold text-[#1B2A4A]">KES 3,750</span>
            </div>
            <p className="max-w-md text-sm leading-6 text-slate-600">
              A one-time fee, paid when you submit your intake form.
            </p>
            <CtaButton className="mt-4" />
            <p className="text-xs text-slate-500">
              This introductory price won&apos;t be around for long — once the offer
              closes, it&apos;s back to full price.
            </p>
          </div>
        </div>
      </section>

      <section id="testimonials" className="bg-[#1B2A4A] text-white">
        <div className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-2xl font-semibold tracking-tight">What clients have said</h2>
          <div className="mt-10 grid gap-8 sm:grid-cols-2">
            {TESTIMONIALS.map((testimonial) => (
              <blockquote
                key={testimonial.quote}
                className="rounded-lg border border-white/10 bg-white/5 p-6"
              >
                <p className="text-lg italic leading-8 text-[#C9A84C]">
                  &ldquo;{testimonial.quote}&rdquo;
                </p>
                <footer className="mt-4 text-sm text-slate-300">
                  — {testimonial.attribution}
                </footer>
              </blockquote>
            ))}
          </div>
        </div>
      </section>

      <section id="contact" className="bg-white">
        <div className="mx-auto max-w-5xl px-6 py-20 text-center">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900">
            Ready to stop guessing and start executing?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base leading-7 text-slate-600">
            Send your CV and a job description for the role you want, and you&apos;ll get
            back a complete Career Transition Plan — every section worked through against
            your specific CV and target role, start to finish. Delivered within one
            working day.
          </p>
          <CtaButton className="mt-8" />
          <p className="mt-6 text-sm text-slate-500">
            Prefer to ask a question first?{" "}
            <a href={`mailto:${CONTACT_EMAIL}`} className="font-medium text-[#0E7C7B] hover:underline">
              {CONTACT_EMAIL}
            </a>
          </p>
        </div>
      </section>

      <footer className="bg-slate-950 text-slate-400">
        <div className="mx-auto max-w-5xl px-6 py-8 text-sm">
          © {new Date().getFullYear()} Career Transition Planning.
        </div>
      </footer>
    </div>
  );
}
