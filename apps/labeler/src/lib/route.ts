import { useEffect, useState } from "react";

export type Route =
  | { page: "queue" }
  | { page: "bulletin"; parish: string; hash: string };

export function parseRoute(hash: string): Route {
  const m = /^#\/b\/([a-z0-9-]+)\/([0-9a-f]{64})$/.exec(hash);
  return m ? { page: "bulletin", parish: m[1], hash: m[2] } : { page: "queue" };
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
