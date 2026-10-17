import { LOCATION_FALLBACK } from "../copy";

/** Where the browser's location services put the visitor. */
export interface BrowserLocation {
  lat: number;
  lng: number;
}

/** Why a location request failed. */
export type BrowserLocationFailure = "unsupported" | "denied" | "unavailable";

/** A failed location request, with a message fit to show the visitor. */
export class BrowserLocationError extends Error {
  readonly reason: BrowserLocationFailure;

  constructor(message: string, reason: BrowserLocationFailure) {
    super(message);
    this.name = "BrowserLocationError";
    this.reason = reason;
  }
}

/**
 * Asks the browser for the visitor's position, prompting for permission the
 * first time. Rejects with a {@link BrowserLocationError} when the browser has
 * no location services, the visitor says no, or no fix arrives in time.
 */
export function requestBrowserLocation(): Promise<BrowserLocation> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(
        new BrowserLocationError(
          `Your browser can’t share your location. ${LOCATION_FALLBACK}`,
          "unsupported",
        ),
      );
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (position) =>
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        }),
      (error) =>
        reject(
          new BrowserLocationError(
            // Once a site is blocked (by the visitor, or by the browser after
            // a few dismissed prompts) the browser stops asking and every
            // request fails at once, so say where to undo it.
            error.code === error.PERMISSION_DENIED
              ? "Location is blocked. Allow it in your browser’s site settings."
              : `Couldn’t find your location. ${LOCATION_FALLBACK}`,
            error.code === error.PERMISSION_DENIED ? "denied" : "unavailable",
          ),
        ),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    );
  });
}

export function browserLocationErrorMessage(error: unknown): string {
  return error instanceof BrowserLocationError
    ? error.message
    : `Couldn’t find your location. ${LOCATION_FALLBACK}`;
}
