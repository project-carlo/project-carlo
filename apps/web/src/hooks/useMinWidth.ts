import { useEffect, useState } from "react";

/** Where the layouts switch from phone to desktop: Tailwind's `md` breakpoint. */
export const DESKTOP_MIN_WIDTH = 768;

/** True when `window` matches `(min-width: ${minWidth}px)`. SSR-safe (false until mounted). */
export function useMinWidth(minWidth: number): boolean {
  const query = `(min-width: ${minWidth}px)`;

  const [matches, setMatches] = useState(() => {
    if (typeof window === "undefined") return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    if (typeof window === "undefined") return;

    const mediaQuery = window.matchMedia(query);
    const update = () => setMatches(mediaQuery.matches);

    update();
    mediaQuery.addEventListener("change", update);
    return () => mediaQuery.removeEventListener("change", update);
  }, [query]);

  return matches;
}
