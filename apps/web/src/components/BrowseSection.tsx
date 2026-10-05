import {
  MAIN_CITY_MIN_CHURCHES,
  cityPath,
  dioceseChurchCounts,
  dioceses,
  diocesePath,
  placesCities,
  statePath,
} from "@/lib/places";
import { CHURCH_INDEX_PATH } from "@/lib/seo";
import { SiteLink } from "./SiteLink";

const LINK = "rubric-link font-serif text-[0.9375rem]";
const HEADING = "smallcaps mb-4 text-[0.9375rem] text-ink-soft";

/**
 * The landing page's "browse" block: dioceses (with church counts), main
 * cities, and the A–Z directory. Reads only the committed places data, so it
 * renders synchronously and identically in the SPA and the static prerender.
 * Links go to prerendered pages, so they are plain anchors.
 */
export function BrowseSection() {
  const counts = dioceseChurchCounts();
  const list = dioceses()
    .map((d) => ({ diocese: d, count: counts[d.key] ?? 0 }))
    .filter((d) => d.count > 0)
    .sort((a, b) => b.count - a.count || a.diocese.shortName.localeCompare(b.diocese.shortName));
  const cities = placesCities(MAIN_CITY_MIN_CHURCHES);

  return (
    <section
      id="browse"
      aria-label="Browse parishes"
      className="mx-auto w-full max-w-[720px] scroll-mt-6 px-7 py-14 md:px-0 md:py-20"
    >
      <h2 className={HEADING}>Browse by diocese</h2>
      <ul className="grid gap-3 sm:grid-cols-2">
        {list.map(({ diocese, count }) => (
          <li key={diocese.key}>
            <SiteLink
              spa
              href={diocesePath(diocese.key)}
              className="missal-focus block border border-rule-strong px-4 py-3 transition-colors hover:bg-paper-deep/50"
            >
              <span className="block font-display text-[1.125rem] leading-tight text-ink">
                {diocese.shortName}
              </span>
              <span className="mt-1 block font-serif text-[0.875rem] text-ink-soft">
                {count} {count === 1 ? "church" : "churches"}
              </span>
            </SiteLink>
          </li>
        ))}
      </ul>

      <h2 className={`${HEADING} mt-12`}>Main cities</h2>
      <ul className="flex flex-wrap gap-x-5 gap-y-2">
        {cities.map((c) => (
          <li key={`${c.state}/${c.slug}`}>
            <SiteLink spa href={cityPath(c.state, c.name)} className={LINK}>
              {c.name}
              <span className="font-serif text-[0.8125rem] text-ink-faint">
                {c.count}
              </span>
            </SiteLink>
          </li>
        ))}
      </ul>

      <p className="mt-10 flex flex-wrap gap-x-6 gap-y-2">
        <SiteLink href={CHURCH_INDEX_PATH} className={LINK}>
          All parishes A–Z
        </SiteLink>
        <SiteLink spa href={statePath()} className={LINK}>
          All of New York
        </SiteLink>
      </p>

      <p className="mt-10 text-center font-serif text-[0.9rem] italic text-ink-faint">
        Schedules are read from each parish&rsquo;s latest weekly bulletin.
      </p>
    </section>
  );
}
