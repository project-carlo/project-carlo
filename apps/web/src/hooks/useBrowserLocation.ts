import { useCallback, useEffect, useState } from "react";
import {
  browserLocationErrorMessage,
  requestBrowserLocation,
  type BrowserLocation,
} from "../lib/browserLocation";

export type BrowserLocationStatus = "idle" | "requesting" | "error";

/** How long a failed request's message stays up before clearing itself. */
const ERROR_DISPLAY_MS = 6000;

/**
 * Asks the browser for the visitor's position when `request` is called,
 * tracking the request so the control that asked can show it's working and,
 * if it fails, why (`error` is set only while `status` is "error").
 * `onLocated` gets the position.
 */
export function useBrowserLocation(
  onLocated: (location: BrowserLocation) => void,
) {
  const [status, setStatus] = useState<BrowserLocationStatus>("idle");
  const [error, setError] = useState<string | null>(null);

  const request = useCallback(() => {
    setStatus("requesting");
    setError(null);
    requestBrowserLocation().then(
      (location) => {
        setStatus("idle");
        onLocated(location);
      },
      (reason: unknown) => {
        setStatus("error");
        setError(browserLocationErrorMessage(reason));
      },
    );
  }, [onLocated]);

  useEffect(() => {
    if (status !== "error") return;
    const id = window.setTimeout(() => {
      setStatus("idle");
      setError(null);
    }, ERROR_DISPLAY_MS);
    return () => window.clearTimeout(id);
  }, [status]);

  return { status, error, request };
}
