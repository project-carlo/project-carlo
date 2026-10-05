/** Where the browser's location services put the visitor. */
export interface BrowserLocation {
  lat: number;
  lng: number;
}

/** A failed location request, with a message fit to show the visitor. */
export class BrowserLocationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "BrowserLocationError";
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
        new BrowserLocationError("Location is not available in this browser."),
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
            error.code === error.PERMISSION_DENIED
              ? "Location permission was denied."
              : "Couldn't get your current location.",
          ),
        ),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    );
  });
}

export function browserLocationErrorMessage(error: unknown): string {
  return error instanceof BrowserLocationError
    ? error.message
    : "Couldn't get your current location.";
}
