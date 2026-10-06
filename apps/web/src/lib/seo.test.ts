import { describe, expect, it } from "vitest";
import type { ChurchDetail } from "../types";
import {
  buildCityDescription,
  churchBreadcrumbJsonLd,
  churchJsonLd,
  cityJsonLd,
} from "./seo";

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

describe("churchBreadcrumbJsonLd", () => {
  const url = "https://projectcarlo.com/churches/st-charles-borromeo/";
  const names = (jsonLd: Record<string, unknown>) =>
    (jsonLd.itemListElement as { name: string; item: string }[]).map((c) => c.item);

  it("puts the church's city page between the index and the church", () => {
    expect(names(churchBreadcrumbJsonLd(church, url))).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      "https://projectcarlo.com/mass-times/rochester-ny/",
      url,
    ]);
  });

  it("leaves the city out when the address has none", () => {
    expect(names(churchBreadcrumbJsonLd({ ...church, city: null }, url))).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      url,
    ]);
  });
});

describe("city page metadata", () => {
  const city = { label: "Rochester, NY", churches: [church] };

  it("names the only church, or counts several", () => {
    expect(buildCityDescription(city)).toContain("St. Charles Borromeo in Rochester, NY");
    expect(buildCityDescription({ ...city, churches: [church, church] })).toContain(
      "the 2 Catholic churches in Rochester, NY",
    );
  });

  it("lists the city's church pages and its breadcrumbs", () => {
    const [page, crumbs] = cityJsonLd(city, "https://projectcarlo.com/mass-times/rochester-ny/");
    expect(page).toMatchObject({
      "@type": "CollectionPage",
      mainEntity: {
        itemListElement: [
          {
            position: 1,
            url: "https://projectcarlo.com/churches/st-charles-borromeo/",
          },
        ],
      },
    });
    expect(crumbs).toMatchObject({ "@type": "BreadcrumbList" });
  });
});
