import { useEffect, useState } from "react";

export type Route =
  | { page: "queue" }
  | { page: "bulletin"; parish: string; hash: string }
  | { page: "seeds" }
  | { page: "seed"; parish: string };

export function parseRoute(hash: string): Route {
  const m = /^#\/b\/([a-z0-9-]+)\/([0-9a-f]{64})$/.exec(hash);
  if (m) return { page: "bulletin", parish: m[1], hash: m[2] };
  if (hash === "#/seeds") return { page: "seeds" };
  const s = /^#\/s\/([a-z0-9-]+)$/.exec(hash);
  return s ? { page: "seed", parish: s[1] } : { page: "queue" };
}

export const SEEDS_HREF = "#/seeds";

export function seedHref(parish: string): string {
  return `#/s/${parish}`;
}

export function bulletinHref(parish: string, hash: string): string {
  return `#/b/${parish}/${hash}`;
}

export function navigate(href: string): void {
  window.location.hash = href;
}

export function useRoute(): Route {
  const [route, setRoute] = useState(() => parseRoute(window.location.hash));
  useEffect(() => {
    const onChange = () => setRoute(parseRoute(window.location.hash));
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return route;
}
