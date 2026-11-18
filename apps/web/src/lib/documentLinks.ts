import { createContext, useContext } from "react";

/**
 * True where the app's router isn't running: the city map a prerendered page
 * mounts on its own. A router link there would only change the address bar,
 * so in-app links load their page instead.
 */
export const DocumentLinksContext = createContext(false);

/**
 * True inside the embed (src/lib/embed.ts), framed on another site: an
 * in-app link opens its page on the full site in a new tab, rather than
 * inside the frame, where it would be stuck in a box on the host's page and
 * add to the host page's history.
 */
export const NewTabLinksContext = createContext(false);

/** Whether in-app links must load their page rather than route to it. */
export function useDocumentLinks(): boolean {
  return useContext(DocumentLinksContext);
}

/** The props an in-app `<Link>` takes so it opens the way this page needs. */
export interface InAppLinkProps {
  reloadDocument: boolean;
  target?: "_blank";
  rel?: string;
}

/**
 * Props for an in-app `<Link>`: routed normally, a full page load where no
 * router runs, and a new tab in the embed. React Router leaves a link with a
 * target to the browser, and its relative URL resolves against the frame's
 * own origin, the full site.
 */
export function useInAppLinkProps(): InAppLinkProps {
  const documentLinks = useContext(DocumentLinksContext);
  const newTab = useContext(NewTabLinksContext);
  return newTab
    ? { reloadDocument: true, target: "_blank", rel: "noopener" }
    : { reloadDocument: documentLinks };
}
