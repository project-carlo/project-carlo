/**
 * Recovery for a page that outlives the deploy that served it. Each deploy
 * carries the previous builds' hashed chunks over for RETENTION_DAYS
 * (lib/assetManifest.ts), so a page loaded before one usually keeps working.
 * A chunk can still be gone: the tab is older than that, the carry-over
 * couldn't download it, or it was over the file cap. The page then gets
 * 404.html back and the lazy import fails. Reloading fetches the new
 * version's HTML, whose chunks do exist.
 */

const STORAGE_KEY = "project-carlo:stale-deploy-reload";

/** A second failure this soon after a reload means the live version is
 *  broken too, not that this page is stale: show the error instead of
 *  reloading forever. */
const RELOAD_COOLDOWN_MS = 10_000;

let reloading = false;

/** Whether a reload for a new version is under way. */
export function isReloadingForNewVersion(): boolean {
  return reloading;
}

/**
 * Reloads the page to pick up the deployed version, unless it already did so
 * moments ago. Given `href`, loads that page instead. Returns whether a
 * reload is under way.
 */
export function reloadForNewVersion(href?: string): boolean {
  if (reloading) return true;
  try {
    const elapsed = Date.now() - Number(sessionStorage.getItem(STORAGE_KEY));
    if (elapsed >= 0 && elapsed < RELOAD_COOLDOWN_MS) return false;
    sessionStorage.setItem(STORAGE_KEY, String(Date.now()));
  } catch {
    // Without storage there's no loop guard, so don't risk one.
    return false;
  }
  reloading = true;
  if (href) window.location.assign(href);
  else window.location.reload();
  return true;
}

/**
 * Reloads when a lazy chunk fails to load. Vite fires `vite:preloadError` for
 * every failed dynamic import in a build. The error still propagates, so
 * whatever renders it (RouteError) shows a loading state while the reload
 * happens.
 *
 * `pendingHref` names the page a move between pages is on its way to, if one
 * is: the router loads a page's chunk before it changes the URL, so a plain
 * reload would land back on the page the visitor was leaving.
 */
export function reloadOnStaleChunk(pendingHref: () => string | undefined = () => undefined): void {
  window.addEventListener("vite:preloadError", () => {
    reloadForNewVersion(pendingHref());
  });
}
