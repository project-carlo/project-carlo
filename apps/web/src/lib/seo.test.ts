import { describe, expect, it } from "vitest";
import type { ChurchDetail } from "../types";
import { browsePageJsonLd, churchBreadcrumbJsonLd, churchJsonLd } from "./seo";

const church: ChurchDetail = {
  id: 1,
  parish_id: 10,
  slug: "st-charles-borromeo",
  name: "St. Charles Borromeo",
  address_line1: "3003 Dewey Ave",
  address_line2: null,
  city: "Rochester",
  state: "NY",
  postal_code: "14616",
  latitude: 43.228,
  longitude: -77.647,
  homepage_url: "https://stcharlesgreece.org",
  bulletin_url: null,
};

describe("churchJsonLd", () => {
  it("emits the parish as Church structured data", () => {
    expect(
      churchJsonLd(
        church,
        "https://projectcarlo.com/churches/st-charles-borromeo/",
      ),
    ).toMatchObject({
      "@context": "https://schema.org",
      "@type": "Church",
      name: "St. Charles Borromeo",
      address: {
        "@type": "PostalAddress",
        streetAddress: "3003 Dewey Ave",
        addressLocality: "Rochester",
        addressRegion: "NY",
        postalCode: "14616",
        addressCountry: "US",
      },
    });
  });

  it("does not classify a recurring parish schedule as Event structured data", () => {
    const jsonLd = churchJsonLd(
      church,
      "https://projectcarlo.com/churches/st-charles-borromeo/",
    );

    expect(jsonLd).not.toHaveProperty("event");
    expect(JSON.stringify(jsonLd)).not.toContain('"@type":"Event"');
  });
});

describe("browse page JSON-LD", () => {
  it("emits CollectionPage, ItemList and BreadcrumbList with absolute URLs", () => {
    const nodes = browsePageJsonLd({
      origin: "https://projectcarlo.com",
      path: "/mass-times/ny/troy/",
      title: "Troy",
      description: "d",
      dateModified: "2026-10-04",
      crumbs: [
        { name: "Home", path: "/" },
        { name: "Troy", path: "/mass-times/ny/troy/" },
      ],
      items: [{ name: "St One", path: "/churches/st-one/" }],
    });
    expect(nodes.map((n) => n["@type"])).toEqual([
      "CollectionPage",
      "ItemList",
      "BreadcrumbList",
    ]);
    expect(nodes[0]).toMatchObject({ dateModified: "2026-10-04" });
    expect(nodes[1]).toMatchObject({
      numberOfItems: 1,
      itemListElement: [
        { position: 1, url: "https://projectcarlo.com/churches/st-one/", name: "St One" },
      ],
    });
    expect(nodes[2]).toMatchObject({
      itemListElement: [
        { position: 1, item: "https://projectcarlo.com/" },
        { position: 2, item: "https://projectcarlo.com/mass-times/ny/troy/" },
      ],
    });
  });

  it("builds a church breadcrumb from the supplied trail", () => {
    const node = churchBreadcrumbJsonLd(
      church,
      "https://projectcarlo.com/churches/st-charles-borromeo/",
      [
        { name: "Home", path: "/" },
        { name: "New York", path: "/mass-times/ny/" },
        { name: "St. Charles Borromeo", path: "/churches/st-charles-borromeo/" },
      ],
    );
    expect(JSON.stringify(node)).toContain("https://projectcarlo.com/mass-times/ny/");
  });
});
