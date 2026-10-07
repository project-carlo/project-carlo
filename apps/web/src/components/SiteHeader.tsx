import { Link } from "react-router-dom";
import { MapIcon } from "@/components/icons";
import { Masthead } from "@/components/Masthead";
import { useHomeHref } from "@/hooks/useHomeHref";
import { MAP_LINK } from "@/copy";

/**
 * The sticky strip atop the church and city pages: a link to the map and the
 * wordmark. The link says "Map", not "Back to map": most visits to these pages
 * start on a search engine, with no map to go back to.
 */
export function SiteHeader() {
  const homeHref = useHomeHref();
  return (
    <header className="sticky top-0 z-40 border-b border-rule-strong bg-paper/95 backdrop-blur supports-[backdrop-filter]:bg-paper/85">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 pt-[calc(0.85rem+var(--safe-area-inset-top))] pb-3">
        <Link to={homeHref} className="rubric-link font-serif text-[0.9375rem]">
          <MapIcon className="size-3.5" />
          {MAP_LINK}
        </Link>
        <Masthead compact />
      </div>
    </header>
  );
}
