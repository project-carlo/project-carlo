import { cn } from "@/lib/utils";
import { DIOCESE_INDEX_PATH, MAP_PATH, statePath } from "@/lib/places";
import { SiteLink } from "./SiteLink";

interface SiteNavProps {
  /** Where the Map link goes — pass the remembered map query (`useMapHref()`)
   *  to restore filters and view. */
  mapHref?: string;
  /** Show the About link (the about page is behind a build-time flag). */
  showAbout?: boolean;
  className?: string;
}

/** The primary site links, shared by the header and the landing page's corner nav. */
export function SiteNav({
  mapHref = MAP_PATH,
  showAbout = false,
  className,
}: SiteNavProps) {
  const link = "rubric-link font-serif text-[0.9375rem] leading-none";
  return (
    <nav
      aria-label="Site"
      className={cn("flex flex-wrap items-baseline gap-x-5 gap-y-1", className)}
    >
      <SiteLink spa href={mapHref} className={link}>
        Map
      </SiteLink>
      <SiteLink href={statePath()} className={link}>
        Places
      </SiteLink>
      <SiteLink href={DIOCESE_INDEX_PATH} className={link}>
        Dioceses
      </SiteLink>
      {showAbout ? (
        <SiteLink spa href="/about" className={link}>
          About
        </SiteLink>
      ) : null}
    </nav>
  );
}

interface SiteHeaderProps extends SiteNavProps {
  /** Stick to the top while scrolling (church pages). */
  sticky?: boolean;
}

/**
 * Slim site header: wordmark → home, then Map · Places · Dioceses (· About).
 * Pure — no router hooks — so it renders in the SPA and the static prerender.
 */
export function SiteHeader({
  sticky = false,
  className,
  ...nav
}: SiteHeaderProps) {
  return (
    <header
      className={cn(
        "border-b border-rule-strong bg-paper/95 backdrop-blur supports-[backdrop-filter]:bg-paper/85",
        sticky && "sticky top-0 z-40",
        className,
      )}
    >
      <div className="mx-auto flex w-full max-w-5xl flex-wrap items-baseline justify-between gap-x-6 gap-y-2 px-6 pt-[calc(0.85rem+var(--safe-area-inset-top))] pb-3">
        <SiteLink
          spa
          href="/"
          aria-label="Project Carlo — home"
          className="font-display text-lg leading-none font-normal tracking-tight text-ink"
        >
          Project <span className="italic text-rubric">Carlo</span>
        </SiteLink>
        <SiteNav {...nav} />
      </div>
    </header>
  );
}
