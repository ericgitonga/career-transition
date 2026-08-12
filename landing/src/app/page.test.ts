import { describe, expect, it } from "vitest";
import {
  CONTACT_EMAIL,
  DELIVERABLES,
  INTAKE_URL,
  PAIN_POINTS,
  PRICING_TIERS,
  STEPS,
  TESTIMONIALS,
  WHO_FOR,
  WHO_NOT_FOR,
} from "./page";

describe("INTAKE_URL", () => {
  it("is a valid https URL", () => {
    expect(() => new URL(INTAKE_URL)).not.toThrow();
    expect(new URL(INTAKE_URL).protocol).toBe("https:");
  });
});

describe("CONTACT_EMAIL", () => {
  it("looks like an email address", () => {
    expect(CONTACT_EMAIL).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  });
});

describe("DELIVERABLES", () => {
  it("has no entries with an empty title or description", () => {
    for (const d of DELIVERABLES) {
      expect(d.title.trim()).not.toBe("");
      expect(d.description.trim()).not.toBe("");
    }
  });
});

describe("STEPS", () => {
  it("is numbered 1..N in order with no gaps", () => {
    expect(STEPS.map((s) => s.number)).toEqual(
      STEPS.map((_, i) => String(i + 1)),
    );
  });

  it("has no entries with an empty title or description", () => {
    for (const s of STEPS) {
      expect(s.title.trim()).not.toBe("");
      expect(s.description.trim()).not.toBe("");
    }
  });
});

describe("TESTIMONIALS", () => {
  it("has no entries with an empty quote or attribution", () => {
    for (const t of TESTIMONIALS) {
      expect(t.quote.trim()).not.toBe("");
      expect(t.attribution.trim()).not.toBe("");
    }
  });
});

describe("PRICING_TIERS", () => {
  it("has exactly two tiers", () => {
    expect(PRICING_TIERS.length).toBe(2);
  });

  it("has no entries with an empty name, price, or empty features", () => {
    for (const tier of PRICING_TIERS) {
      expect(tier.name.trim()).not.toBe("");
      expect(tier.introPrice.trim()).not.toBe("");
      expect(tier.regularPrice.trim()).not.toBe("");
      expect(tier.features.length).toBeGreaterThan(0);
      for (const feature of tier.features) {
        expect(feature.trim()).not.toBe("");
      }
    }
  });

  it("has extraNote only on the highlighted (Advanced) tier", () => {
    for (const tier of PRICING_TIERS) {
      if (tier.extraNote) {
        expect(tier.highlighted).toBe(true);
      }
    }
  });
});

describe("PAIN_POINTS / WHO_FOR / WHO_NOT_FOR", () => {
  it("are all non-empty lists of non-empty strings", () => {
    for (const list of [PAIN_POINTS, WHO_FOR, WHO_NOT_FOR]) {
      expect(list.length).toBeGreaterThan(0);
      for (const item of list) {
        expect(item.trim()).not.toBe("");
      }
    }
  });
});
