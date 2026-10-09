import { describe, expect, it } from "vitest";
import type { ChurchDetail } from "../types";
import { buildCityIndex } from "./cities";
import { buildDioceseIndex } from "./dioceses";
import {
  buildChurchTitle,
  buildCityDescription,
  buildDioceseDescription,
  buildDioceseIndexDescription,
  buildDioceseTitle,
  churchBreadcrumbJsonLd,
  churchJsonLd,
  cityJsonLd,
  dioceseIndexJsonLd,
  dioceseJsonLd,
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
  bulletin_week: null,
};

describe("churchJsonLd", () => {
  it("emits the church as Church structured data", () => {
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

  it("does not classify a recurring church schedule as Event structured data", () => {
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
    const city = { slug: "rochester-ny", label: "Rochester, NY" };
    expect(names(churchBreadcrumbJsonLd(church, city, null, url))).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      "https://projectcarlo.com/mass-times/rochester-ny/",
      url,
    ]);
  });

  it("puts the diocese's page before the city's, when it has one", () => {
    const city = { slug: "rochester-ny", label: "Rochester, NY" };
    const diocese = { slug: "rochester", label: "Diocese of Rochester" };
    expect(names(churchBreadcrumbJsonLd(church, city, diocese, url))).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      "https://projectcarlo.com/dioceses/rochester/",
      "https://projectcarlo.com/mass-times/rochester-ny/",
      url,
    ]);
  });

  it("leaves the city out when the address has none", () => {
    expect(names(churchBreadcrumbJsonLd({ ...church, city: null }, null, null, url))).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      url,
    ]);
  });
});

describe("church page title", () => {
  it("leads with the church and its town", () => {
    expect(buildChurchTitle(church)).toBe(
      "St. Charles Borromeo, Rochester — Mass & Confession Times",
    );
  });

  it("falls back to the state, then to the name alone", () => {
    expect(buildChurchTitle({ ...church, city: null })).toBe(
      "St. Charles Borromeo, NY — Mass & Confession Times",
    );
    expect(buildChurchTitle({ ...church, city: " ", state: null })).toBe(
      "St. Charles Borromeo — Mass & Confession Times",
    );
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
    const [page, crumbs] = cityJsonLd(
      city,
      { slug: "rochester", label: "Diocese of Rochester" },
      "https://projectcarlo.com/mass-times/rochester-ny/",
    );
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
    expect(
      (crumbs.itemListElement as { item: string }[]).map((c) => c.item),
    ).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      "https://projectcarlo.com/dioceses/rochester/",
      "https://projectcarlo.com/mass-times/rochester-ny/",
    ]);
  });
});

describe("diocese page metadata", () => {
  const churches = [
    church,
    { ...church, id: 2, slug: "holy-cross", name: "Holy Cross" },
    { ...church, id: 3, slug: "st-mary-canandaigua", city: "Canandaigua" },
  ];
  const { cities } = buildCityIndex(churches);
  const [diocese] = buildDioceseIndex(churches, cities, {
    rochester: {
      name: "Roman Catholic Diocese of Rochester",
      state: "NY",
      website: "https://www.dor.org",
      covered: true,
      churches: churches.map((c) => c.slug),
    },
  }).dioceses;
  const url = "https://projectcarlo.com/dioceses/rochester/";

  it("names the diocese in the title and counts its churches and towns", () => {
    expect(buildDioceseTitle(diocese)).toBe(
      "Catholic Mass Times in the Diocese of Rochester — Confession & Adoration · Project Carlo",
    );
    expect(buildDioceseDescription(diocese)).toBe(
      "Mass, Confession, and Adoration times at 3 Catholic churches in 2 cities and towns " +
        "across the Diocese of Rochester, from each parish’s weekly bulletin.",
    );
  });

  it("lists the diocese's city pages and its breadcrumbs", () => {
    const [page, crumbs] = dioceseJsonLd(diocese, url);
    expect(page).toMatchObject({
      "@type": "CollectionPage",
      url,
      mainEntity: {
        "@type": "ItemList",
        itemListElement: [
          {
            position: 1,
            name: "Canandaigua, NY",
            url: "https://projectcarlo.com/mass-times/canandaigua-ny/",
          },
          {
            position: 2,
            name: "Rochester, NY",
            url: "https://projectcarlo.com/mass-times/rochester-ny/",
          },
        ],
      },
    });
    expect(
      (crumbs.itemListElement as { name: string }[]).map((c) => c.name),
    ).toEqual(["Project Carlo", "All churches", "Diocese of Rochester"]);
  });

  it("lists the dioceses with pages", () => {
    const dioceses = [
      { slug: "albany", label: "Diocese of Albany" },
      { slug: "new-york", label: "Archdiocese of New York" },
      { slug: "rochester", label: "Diocese of Rochester" },
    ];
    expect(buildDioceseIndexDescription(dioceses)).toBe(
      "Browse Catholic churches by diocese (Albany, New York and Rochester) and find " +
        "Mass, Confession, and Adoration times from each parish’s weekly bulletin.",
    );
    const [page, crumbs] = dioceseIndexJsonLd(dioceses, "https://projectcarlo.com/dioceses/");
    expect(page).toMatchObject({
      mainEntity: {
        itemListElement: [
          { position: 1, url: "https://projectcarlo.com/dioceses/albany/" },
          { position: 2, url: "https://projectcarlo.com/dioceses/new-york/" },
          { position: 3, url: "https://projectcarlo.com/dioceses/rochester/" },
        ],
      },
    });
    expect(
      (crumbs.itemListElement as { item: string }[]).map((c) => c.item),
    ).toEqual([
      "https://projectcarlo.com/",
      "https://projectcarlo.com/churches/",
      "https://projectcarlo.com/dioceses/",
    ]);
  });
});
