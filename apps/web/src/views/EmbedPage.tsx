import type { MouseEvent } from "react";
import { embedLinkHref } from "../lib/embed";
import { HomePage } from "./HomePage";

/**
 * Opens a link clicked anywhere in the embed (a church's popup, the credit,
 * the map's attribution, whatever adds one next) on the full site in a new
 * tab, with the embed's campaign, rather than inside the frame, where it
 * would be stuck in a box on the host's page and add to its history.
 * Captured, so it runs before a router `<Link>` or Leaflet sees the click,
 * and the middle button's too. Fragment links are in-page controls (Leaflet's
 * popup close button is `href="#close"`), so they're left alone.
 */
function openLinkInNewTab(event: MouseEvent<HTMLDivElement>) {
  if (event.defaultPrevented || event.button > 1) return;
  const link = (event.target as Element | null)?.closest?.("a[href]");
  if (!(link instanceof HTMLAnchorElement)) return;
  if (link.getAttribute("href")?.startsWith("#") || !link.protocol.startsWith("http")) return;
  event.preventDefault();
  window.open(embedLinkHref(link.href, window.location.href), "_blank", "noopener");
}

/**
 * The embed at /embed (src/lib/embed.ts): the home map, framed on another
 * site, with every link opening the full site in a new tab.
 */
export function EmbedPage() {
  return (
    <div className="contents" onClickCapture={openLinkInNewTab} onAuxClickCapture={openLinkInNewTab}>
      <HomePage embed />
    </div>
  );
}
