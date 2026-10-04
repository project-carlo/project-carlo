import type { ReactNode } from "react";
import { Link, useInRouterContext } from "react-router-dom";

interface SiteLinkProps {
  href: string;
  className?: string;
  children: ReactNode;
  "aria-label"?: string;
  "aria-current"?: "page";
  /**
   * True for pages that have a client-side route: inside a router the link
   * navigates in-app instead of reloading. Leave false for pages that only
   * exist as prerendered HTML (diocese/city/state pages until they get client
   * routes); those are always plain anchors, so a full page load serves the
   * static file.
   */
  spa?: boolean;
}

/**
 * A link that works in both the SPA and the static prerender. Outside a router
 * (the A–Z index) it is a plain `<a>`; inside one (SPA, or the prerender's
 * MemoryRouter) `spa` links use `<Link>`, which renders the same `<a href>`.
 */
export function SiteLink({ href, spa = false, children, ...rest }: SiteLinkProps) {
  const inRouter = useInRouterContext();
  if (spa && inRouter) {
    return (
      <Link to={href} {...rest}>
        {children}
      </Link>
    );
  }
  return (
    <a href={href} {...rest}>
      {children}
    </a>
  );
}
