/**
 * Recovery for a page that outlives the deploy that served it. A deploy
 * replaces the site's assets wholesale (Workers static assets keep no older
 * versions), so a page loaded before one, whether an open tab or a load that
 * straddles the switch, asks for hashed chunks that no longer exist. It gets
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
 * moments ago. Returns whether a reload is under way.
 */
export function reloadForNewVersion(): boolean {
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
  window.location.reload();
  return true;
}

/**
 * Reloads when a lazy chunk fails to load. Vite fires `vite:preloadError` for
 * every failed dynamic import in a build. The error still propagates, so
 * whatever renders it (RouteError) shows a loading state while the reload
 * happens.
 */
export function reloadOnStaleChunk(): void {
  window.addEventListener("vite:preloadError", () => {
    reloadForNewVersion();
  });
}
