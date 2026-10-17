import { Link } from "react-router-dom";
import type { ChurchBase } from "../types";
import { cityPath, citySlugFor, type City } from "@/lib/cities";
import { churchPath } from "@/lib/seo";
import { CHURCH_LIST, SOURCE_PHRASE, UNNAMED_CHURCH } from "@/copy";
import { SiteHeader } from "@/components/SiteHeader";

/** What the all-churches index lists for each church. */
export type ChurchIndexEntry = Pick<ChurchBase, "slug" | "name" | "city" | "state">;

/** The city pages, as `cityIndex` builds them, so headings match their titles. */
export type ChurchIndexCity = Pick<City, "slug" | "label" | "churches">;

interface CityGroup {
  label: string;
  /** Slug of the city's page; null for the "Other locations" group. */
  slug: string | null;
  churches: ChurchIndexEntry[];
}

const UNKNOWN_CITY = "Other locations";

/**
 * One group per city page, under that page's label (alphabetical), then the
 * churches whose address has no city.
 */
function groupByCity(
  churches: ChurchIndexEntry[],
  cities: ChurchIndexCity[],
): CityGroup[] {
  const groups: CityGroup[] = cities.map((city) => ({
    label: city.label,
    slug: city.slug,
    churches: city.churches,
  }));
  const unknown = churches
    .filter((church) => citySlugFor(church) === null)
    .sort((a, b) => (a.name ?? "").localeCompare(b.name ?? ""));
  if (unknown.length > 0) {
    groups.push({ label: UNKNOWN_CITY, slug: null, churches: unknown });
  }
  return groups;
}

/**
 * The all-churches index: every church, grouped under its city. Prerendered
 * (StaticChurchIndexPage) and in the app (ChurchIndexPage) alike; its search
 * box is wired up by src/lib/churchIndexSearch.ts, over this markup.
 */
export function ChurchIndexContent({
  churches,
  cities,
}: {
  churches: ChurchIndexEntry[];
  cities: ChurchIndexCity[];
}) {
  const groups = groupByCity(churches, cities);
  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />

      <div className="mx-auto w-full max-w-3xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        <section className="mx-auto max-w-2xl text-center">
          <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
            {CHURCH_LIST}
          </h1>
          <p className="mt-4 font-serif text-[1rem] text-ink-soft">
            Mass, Confession, and Adoration times at {churches.length} Catholic
            churches, {SOURCE_PHRASE}.
          </p>
        </section>

        <form id="church-search-form" role="search" hidden className="mt-8">
          <label htmlFor="church-search" className="sr-only">
            Search churches and cities
          </label>
          <input
            id="church-search"
            type="search"
            placeholder="Search for a church or city"
            autoComplete="off"
            spellCheck={false}
            className="w-full appearance-none border-b border-rule-strong bg-transparent py-2 font-serif text-[1.0625rem] text-ink outline-none placeholder:text-ink-soft placeholder:italic focus:border-rubric [&::-webkit-search-cancel-button]:appearance-none"
          />
          <p
            id="church-search-status"
            aria-live="polite"
            className="mt-2 min-h-[1.25rem] font-serif text-sm text-ink-soft"
          />
        </form>

        <p
          id="church-search-empty"
          hidden
          className="mt-10 text-center font-serif text-[0.95rem] text-ink-soft"
        >
          {/* The search fills in the text, echoing the query. */}
        </p>

        <div className="mt-8 space-y-10">
          {groups.map((group) => (
            <section key={group.label} data-city-group="">
              <h2 className="smallcaps border-b border-rule-strong pb-2 text-[0.95rem] text-ink">
                {group.slug ? (
                  <Link to={cityPath(group.slug)} className="rubric-link">
                    {group.label}
                  </Link>
                ) : (
                  group.label
                )}
              </h2>
              <ul className="mt-4 space-y-2">
                {group.churches.map((church) => (
                  <li key={church.slug}>
                    <Link
                      to={churchPath(church.slug)}
                      className="rubric-link font-serif text-[1.05rem] text-ink"
                    >
                      {church.name ?? UNNAMED_CHURCH}
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </div>
    </main>
  );
}
