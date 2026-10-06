import { Fragment } from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

export interface Crumb {
  label: string;
  /** In-app route; rendered as a router link. */
  to?: string;
  /**
   * A page only the prerenderer writes (the all-parishes index), which the
   * SPA has no route for: a plain link, so the browser loads it.
   */
  href?: string;
}

/** A trail of links ending in the current page, e.g. "All parishes › East Aurora, NY › St. Mary". */
export function Breadcrumbs({
  crumbs,
  className,
}: {
  crumbs: Crumb[];
  className?: string;
}) {
  return (
    <nav aria-label="Breadcrumb" className={cn("font-serif text-[0.9rem]", className)}>
      <ol className="flex flex-wrap items-baseline justify-center gap-x-2 gap-y-1 text-ink-soft">
        {crumbs.map((crumb, i) => {
          const last = i === crumbs.length - 1;
          return (
            <Fragment key={`${i}-${crumb.label}`}>
              {i > 0 ? (
                <li aria-hidden="true" className="text-ink-faint">
                  ›
                </li>
              ) : null}
              <li>
                {last ? (
                  <span aria-current="page">{crumb.label}</span>
                ) : crumb.to ? (
                  <Link to={crumb.to} className="rubric-link">
                    {crumb.label}
                  </Link>
                ) : (
                  <a href={crumb.href} className="rubric-link">
                    {crumb.label}
                  </a>
                )}
              </li>
            </Fragment>
          );
        })}
      </ol>
    </nav>
  );
}
