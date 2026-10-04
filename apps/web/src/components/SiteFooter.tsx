import { cn } from "@/lib/utils";
import { Fleuron } from "@/components/Fleuron";
import {
  MAIN_CITY_MIN_CHURCHES,
  cityPath,
  dioceses,
  diocesePath,
  placesCities,
  statePath,
} from "@/lib/places";
import { CHURCH_INDEX_PATH } from "@/lib/seo";
import { SiteLink } from "./SiteLink";

/** A city link in the footer. */
export interface FooterCity {
  name: string;
  path: string;
}

interface SiteFooterProps {
  /** Cities to list. Defaults to the cities with 3+ churches in the committed
   *  places data, so the footer needs no snapshot. */
  cities?: FooterCity[];
  mapHref?: string;
  showAbout?: boolean;
  className?: string;
}

const LINK = "rubric-link font-serif text-[0.9375rem]";
const HEADING = "smallcaps mb-3 text-[0.875rem] text-ink-soft";

function defaultCities(): FooterCity[] {
  return placesCities(MAIN_CITY_MIN_CHURCHES).map((c) => ({
    name: c.name,
    path: cityPath(c.state, c.name),
  }));
}

/**
 * Site footer: browse links (state hub, every diocese, main cities, the A–Z
 * directory) and the data-freshness note. Plain anchors to the prerendered
 * pages; pure, so it renders in the SPA and the static prerender alike.
 */
export function SiteFooter({
  cities = defaultCities(),
  mapHref = "/map",
  showAbout = false,
  className,
}: SiteFooterProps) {
  return (
    <footer
      className={cn(
        "bg-paper px-6 pt-4 pb-[calc(2.5rem+var(--safe-area-inset-bottom))]",
        className,
      )}
    >
      <div className="mx-auto w-full max-w-5xl">
        <Fleuron className="mb-8" />
        <div className="grid gap-x-10 gap-y-8 sm:grid-cols-2 md:grid-cols-[1fr_1fr_1.6fr]">
          <nav aria-label="Browse">
            <h2 className={HEADING}>Browse</h2>
            <ul className="space-y-1.5">
              <li>
                <SiteLink spa href={mapHref} className={LINK}>
                  Map
                </SiteLink>
              </li>
              <li>
                <SiteLink href={statePath()} className={LINK}>
                  Mass times in New York
                </SiteLink>
              </li>
              <li>
                <SiteLink href={CHURCH_INDEX_PATH} className={LINK}>
                  All parishes A–Z
                </SiteLink>
              </li>
              {showAbout ? (
                <li>
                  <SiteLink spa href="/about" className={LINK}>
                    About
                  </SiteLink>
                </li>
              ) : null}
            </ul>
          </nav>

          <nav aria-label="Dioceses">
            <h2 className={HEADING}>Dioceses</h2>
            <ul className="space-y-1.5">
              {dioceses().map((d) => (
                <li key={d.key}>
                  <SiteLink href={diocesePath(d.key)} className={LINK}>
                    {d.shortName}
                  </SiteLink>
                </li>
              ))}
            </ul>
          </nav>

          {cities.length > 0 ? (
            <nav aria-label="Main cities" className="sm:col-span-2 md:col-span-1">
              <h2 className={HEADING}>Main cities</h2>
              <ul className="flex flex-wrap gap-x-4 gap-y-1.5">
                {cities.map((c) => (
                  <li key={c.path}>
                    <SiteLink href={c.path} className={LINK}>
                      {c.name}
                    </SiteLink>
                  </li>
                ))}
              </ul>
            </nav>
          ) : null}
        </div>

        <p className="mt-10 text-center font-serif text-[0.9rem] italic text-ink-faint">
          Schedules read from parish bulletins &middot; Project Carlo
        </p>
      </div>
    </footer>
  );
}
