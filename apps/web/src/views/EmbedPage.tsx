import { NewTabLinksContext } from "../lib/documentLinks";
import { HomePage } from "./HomePage";

/**
 * The embed at /embed (src/lib/embed.ts): the home map, framed on another
 * site, with every in-app link opening the full site in a new tab.
 */
export function EmbedPage() {
  return (
    <NewTabLinksContext.Provider value={true}>
      <HomePage embed />
    </NewTabLinksContext.Provider>
  );
}
