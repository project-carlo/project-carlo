import { createContext, useContext } from "react";

/**
 * True where the app's router isn't running: the city map a prerendered page
 * mounts on its own. A router link there would only change the address bar,
 * so in-app links load their page instead.
 */
export const DocumentLinksContext = createContext(false);

/** Whether in-app links must load their page rather than route to it. */
export function useDocumentLinks(): boolean {
  return useContext(DocumentLinksContext);
}
