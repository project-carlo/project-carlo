import { Link } from "react-router-dom";
import type { ChurchBase } from "../types";
import { cityPath, citySlugFor, type City } from "@/lib/cities";
import { DIOCESE_INDEX_PATH, diocesePath, type Diocese } from "@/lib/dioceses";
import { churchPath } from "@/lib/seo";
import { ALL_CHURCHES, SOURCE_PHRASE, UNNAMED_CHURCH } from "@/copy";
import { SiteHeader } from "@/components/SiteHeader";

/** What the all-churches index lists for each church. */
export type ChurchIndexEntry = Pick<ChurchBase, "slug" | "name" | "city" | "state">;

/** The city pages, as `cityIndex` builds them, so headings match their titles. */
export type ChurchIndexCity = Pick<City, "slug" | "label" | "churches">;

/** The dioceses, as `dioceseIndex` builds them; only a covered one has a page. */
export type ChurchIndexDiocese = Pick<Diocese, "slug" | "label" | "covered"> & {
  churches: Pick<ChurchBase, "slug">[];
};

interface CityGroup {
  label: string;
  /** Slug of the city's page; null for the "Other locations" group. */
  slug: string | null;
  churches: ChurchIndexEntry[];
}

interface DioceseGroup {
  /** Null when no church has a known diocese, and the cities stand alone. */
  label: string | null;
  /** Slug of the diocese's page; null when it has none. */
  slug: string | null;
  cities: CityGroup[];
}

const UNKNOWN_CITY = "Other locations";
const UNKNOWN_DIOCESE = "Other churches";

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
 * The city groups again, under their dioceses (in `dioceses`' order), each
 * with only that diocese's churches, then any churches in no diocese. A city
 * split between dioceses is listed under each.
 */
function groupByDiocese(
  cityGroups: CityGroup[],
  dioceses: ChurchIndexDiocese[],
): DioceseGroup[] {
  if (dioceses.length === 0) return [{ label: null, slug: null, cities: cityGroups }];
  const dioceseOf = new Map<string, ChurchIndexDiocese>();
  for (const diocese of dioceses) {
    for (const church of diocese.churches) dioceseOf.set(church.slug, diocese);
  }
  const groups = new Map<ChurchIndexDiocese | null, CityGroup[]>();
  for (const group of cityGroups) {
    const parts = new Map<ChurchIndexDiocese | null, ChurchIndexEntry[]>();
    for (const church of group.churches) {
      const diocese = dioceseOf.get(church.slug) ?? null;
      const part = parts.get(diocese);
      if (part) part.push(church);
      else parts.set(diocese, [church]);
    }
    for (const [diocese, churches] of parts) {
      const list = groups.get(diocese);
      if (list) list.push({ ...group, churches });
      else groups.set(diocese, [{ ...group, churches }]);
    }
  }
  return [
    ...dioceses.map((diocese) => ({
      label: diocese.label,
      slug: diocese.covered ? diocese.slug : null,
      cities: groups.get(diocese) ?? [],
    })),
    { label: UNKNOWN_DIOCESE, slug: null, cities: groups.get(null) ?? [] },
  ].filter((group) => group.cities.length > 0);
}

/** A city's churches, under the city's name (linking its page). */
function CityGroupSection({ group, nested }: { group: CityGroup; nested: boolean }) {
  const Heading = nested ? "h3" : "h2";
  return (
    <section data-city-group="">
      <Heading
        data-city-heading=""
        className="smallcaps border-b border-rule-strong pb-2 text-[0.95rem] text-ink"
      >
        {group.slug ? (
          <Link to={cityPath(group.slug)} className="rubric-link">
            {group.label}
          </Link>
        ) : (
          group.label
        )}
      </Heading>
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
  );
}

/**
 * The all-churches index: every church, grouped under its diocese and city.
 * Prerendered (StaticChurchIndexPage) and in the app (ChurchIndexPage) alike;
 * its search box is wired up by src/lib/churchIndexSearch.ts, over this markup.
 */
export function ChurchIndexContent({
  churches,
  cities,
  dioceses,
}: {
  churches: ChurchIndexEntry[];
  cities: ChurchIndexCity[];
  dioceses: ChurchIndexDiocese[];
}) {
  const groups = groupByDiocese(groupByCity(churches, cities), dioceses);
  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />

      <div className="mx-auto w-full max-w-3xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        <section className="mx-auto max-w-2xl text-center">
          <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
            {ALL_CHURCHES}
          </h1>
          <p className="mt-4 font-serif text-[1rem] text-ink-soft">
            Mass, Confession, and Adoration times at {churches.length} Catholic
            churches, {SOURCE_PHRASE}.
          </p>
          {dioceses.some((diocese) => diocese.covered) ? (
            <p className="mt-3">
              <Link
                to={DIOCESE_INDEX_PATH}
                className="rubric-link font-serif text-[0.9375rem]"
              >
                Browse by diocese
                <span aria-hidden="true">→</span>
              </Link>
            </p>
          ) : null}
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

        <div className="mt-8 space-y-16">
          {groups.map((diocese) =>
            diocese.label === null ? (
              <div key="" className="space-y-10">
                {diocese.cities.map((group) => (
                  <CityGroupSection key={group.label} group={group} nested={false} />
                ))}
              </div>
            ) : (
              <section key={diocese.label} data-diocese-group="">
                <h2 className="font-display text-[1.75rem] leading-tight font-normal text-ink">
                  {diocese.slug ? (
                    <Link to={diocesePath(diocese.slug)} className="hover:text-rubric-deep">
                      {diocese.label}
                    </Link>
                  ) : (
                    diocese.label
                  )}
                </h2>
                <div className="mt-6 space-y-10">
                  {diocese.cities.map((group) => (
                    <CityGroupSection key={group.label} group={group} nested />
                  ))}
                </div>
              </section>
            ),
          )}
        </div>
      </div>
    </main>
  );
}
