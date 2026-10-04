import { cn } from "@/lib/utils";
import { SiteLink } from "./SiteLink";

export interface BreadcrumbLink {
  name: string;
  /** Site-relative path. The last item is the current page and is not linked. */
  path: string;
}

/**
 * "Home › New York › Buffalo" trail. Pure (no router hooks); every level
 * links with `spa`, so inside the SPA it navigates in-app and in the static
 * prerender it is a plain anchor. The last item is the current page.
 */
export function Breadcrumbs({
  items,
  className,
}: {
  items: BreadcrumbLink[];
  className?: string;
}) {
  return (
    <nav aria-label="Breadcrumb" className={cn("font-serif text-[0.9rem]", className)}>
      <ol className="flex flex-wrap items-baseline gap-x-2 gap-y-1 text-ink-soft">
        {items.map((item, i) => {
          const last = i === items.length - 1;
          return (
            <li key={item.path} className="flex items-baseline gap-2">
              {last ? (
                <span aria-current="page" className="text-ink-faint">
                  {item.name}
                </span>
              ) : (
                <>
                  <SiteLink spa href={item.path} className="rubric-link">
                    {item.name}
                  </SiteLink>
                  <span aria-hidden className="text-brass">
                    ›
                  </span>
                </>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
