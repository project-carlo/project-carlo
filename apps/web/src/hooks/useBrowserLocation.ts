import { useCallback, useEffect, useState } from "react";
import {
  BrowserLocationError,
  browserLocationErrorMessage,
  requestBrowserLocation,
  type BrowserLocation,
} from "../lib/browserLocation";
import { track } from "../lib/analytics";

export type BrowserLocationStatus = "idle" | "requesting" | "error";

/** How long a failed request's message stays up before clearing itself. */
const ERROR_DISPLAY_MS = 6000;

/**
 * Asks the browser for the visitor's position when `request` is called,
 * tracking the request so the control that asked can show it's working and,
 * if it fails, why (`error` is set only while `status` is "error").
 * `onLocated` gets the position. Each answer is tracked (never the position).
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
        track("locate", { kind: "located" });
        setStatus("idle");
        onLocated(location);
      },
      (reason: unknown) => {
        track("locate", {
          kind: reason instanceof BrowserLocationError ? reason.reason : "unavailable",
        });
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
