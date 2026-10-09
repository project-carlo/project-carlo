import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import type { DiocesePageData } from "../api";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CityMapPreview } from "@/components/CityMapPreview";
import { Fleuron } from "@/components/Fleuron";
import { ExternalLinkIcon } from "@/components/icons";
import { SiteHeader } from "@/components/SiteHeader";
import { cityPath } from "@/lib/cities";
import type { CityMapConfig } from "@/lib/cityMap";
import { countChurches, dioceseCoverage, type DioceseCity } from "@/lib/dioceses";
import { CHURCH_INDEX_PATH } from "@/lib/seo";
import { ALL_CHURCHES, SOURCE_PHRASE } from "@/copy";

/** "buffalodiocese.org" for its website's URL; the URL itself if it doesn't parse. */
function siteName(url: string): string {
  try {
    return new URL(url).host.replace(/^www\./, "");
  } catch {
    return url;
  }
}

/** A city's link, with how many of the diocese's churches it has. */
function CityEntry({ entry, state }: { entry: DioceseCity; state: string | null }) {
  const { city, churchCount } = entry;
  return (
    <li className="flex break-inside-avoid items-baseline gap-2 py-1.5 font-serif">
      <Link to={cityPath(city.slug)} className="rubric-link text-[1.05rem] text-ink">
        {/* The state only where it isn't the diocese's own. */}
        {city.state === state ? city.name : city.label}
      </Link>
      <span className="min-w-3 flex-1 translate-y-[-3px] border-b border-dotted border-rule-strong" />
      <span className="text-[0.9375rem] whitespace-nowrap text-ink-soft tabular-nums">
        {countChurches(churchCount)}
      </span>
    </li>
  );
}

/**
 * A diocese page: how much of the diocese the site lists, its map, and its
 * cities, each a link to its city page, where the times are. `liveMap` makes
 * the map preview live, as on a city page (see CityMapPreview).
 */
export function DiocesePageContent({
  data,
  liveMap,
}: {
  data: DiocesePageData;
  liveMap?: (config: CityMapConfig) => ReactNode;
}) {
  const { diocese, map } = data;

  return (
    <>
      <main className="min-h-svh bg-paper">
        <SiteHeader />

        <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
          <section className="rise-in mx-auto max-w-2xl text-center">
            <Breadcrumbs
              className="mb-6"
              crumbs={[
                { label: ALL_CHURCHES, to: CHURCH_INDEX_PATH },
                { label: diocese.label },
              ]}
            />
            <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
              Mass, Confession &amp; Adoration Times in the {diocese.label}
            </h1>
            <p className="mt-4 font-serif text-[1rem] text-ink-soft">
              {dioceseCoverage(diocese)}, with times {SOURCE_PHRASE}.
            </p>
            {diocese.website ? (
              <p className="mt-3 font-serif text-[0.95rem] text-ink-soft">
                Project Carlo is independent and not affiliated with the diocese.
                For diocesan news and offices, see its own website,{" "}
                <a
                  href={diocese.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  data-track="diocese_website"
                  className="rubric-link inline-flex items-center gap-1.5"
                >
                  {siteName(diocese.website)}
                  <ExternalLinkIcon className="size-3.5" />
                </a>
                .
              </p>
            ) : null}
          </section>

          <div
            className="rise-in mx-auto max-w-3xl"
            style={{ animationDelay: "80ms" }}
          >
            {/* Keyed by diocese, as the city page's map is by city. */}
            <CityMapPreview
              key={diocese.slug}
              label={`the ${diocese.label}`}
              map={map}
              live={liveMap}
              className="mt-8 mb-3"
            />

            <section aria-labelledby="diocese-cities" className="mt-12">
              <h2
                id="diocese-cities"
                className="font-display text-[1.75rem] leading-none font-normal text-ink"
              >
                Cities and towns
              </h2>
              <ul className="mt-5 gap-x-10 sm:columns-2">
                {diocese.cities.map((entry) => (
                  <CityEntry key={entry.city.slug} entry={entry} state={diocese.state} />
                ))}
              </ul>
            </section>
          </div>

          <div className="mx-auto mt-16 max-w-2xl">
            <Fleuron solo className="text-brass" />
          </div>
        </div>
      </main>
      <footer className="bg-paper pb-[calc(3rem+var(--safe-area-inset-bottom))] text-center">
        <Link to={CHURCH_INDEX_PATH} className="rubric-link font-serif text-[0.9375rem]">
          {ALL_CHURCHES}
        </Link>
      </footer>
    </>
  );
}
