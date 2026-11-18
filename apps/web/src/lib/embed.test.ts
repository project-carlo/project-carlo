import { describe, expect, it } from "vitest";
import { embedDiocese, fullSiteMapHref } from "./embed";

describe("embedDiocese", () => {
  it("reads the diocese an embed asks for", () => {
    expect(embedDiocese("?diocese=syracuse&ref=diocese-syracuse")).toBe("syracuse");
    expect(embedDiocese("?diocese=%20Syracuse%20")).toBe("syracuse");
  });

  it("is null when the embed names none", () => {
    expect(embedDiocese("")).toBeNull();
    expect(embedDiocese("?diocese=")).toBeNull();
    expect(embedDiocese("?ref=x")).toBeNull();
  });

  it("keeps a diocese the site doesn't cover, for the embed to say so", () => {
    expect(embedDiocese("?diocese=nowhere")).toBe("nowhere");
  });
});

describe("fullSiteMapHref", () => {
  it("keeps the view, filters and campaign but not the diocese", () => {
    expect(
      fullSiteMapHref("?diocese=syracuse&lat=43.05&lng=-76.15&z=9&type=confession&ref=d"),
    ).toBe("/?lat=43.05&lng=-76.15&z=9&type=confession&ref=d");
  });

  it("is the bare map when nothing else is in the query", () => {
    expect(fullSiteMapHref("?diocese=syracuse")).toBe("/");
    expect(fullSiteMapHref("")).toBe("/");
  });
});
