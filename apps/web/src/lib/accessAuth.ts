/**
 * Checks the token Cloudflare Access puts on every request it lets through
 * (the `Cf-Access-Jwt-Assertion` header), so a Worker route can refuse anyone
 * Access didn't sign in. Access in front of projectcarlo.com doesn't cover the
 * Worker's workers.dev and preview URLs, so the Worker checks for itself
 * rather than trusting that a request came through Access.
 *
 * See https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/
 */

export const ACCESS_JWT_HEADER = "Cf-Access-Jwt-Assertion";

export interface AccessConfig {
  /** The Zero Trust team domain, `<team>.cloudflareaccess.com`. */
  teamDomain: string;
  /** The Access application's Application Audience (AUD) tag. */
  audience: string;
}

export interface AccessIdentity {
  email: string | null;
}

interface Jwk extends JsonWebKey {
  kid?: string;
}

/** Clock difference tolerated between Cloudflare and this Worker. */
const LEEWAY_SECONDS = 60;
/** Access rotates its signing keys every six weeks or so. */
const KEYS_TTL_MS = 60 * 60 * 1000;

const keyCache = new Map<string, { fetchedAt: number; keys: Jwk[] }>();

/**
 * The team domain as a bare hostname, or null if it isn't one of Access's.
 * Keys are only ever fetched from cloudflareaccess.com, so a mistyped setting
 * can't point the check at someone else's keys.
 */
export function normalizeTeamDomain(raw: string): string | null {
  const host = raw.trim().toLowerCase().replace(/^https:\/\//, "").replace(/\/+$/, "");
  return /^[a-z0-9-]+\.cloudflareaccess\.com$/.test(host) ? host : null;
}

function base64UrlDecode(part: string): Uint8Array<ArrayBuffer> {
  const base64 = part.replace(/-/g, "+").replace(/_/g, "/");
  const binary = atob(base64 + "=".repeat((4 - (base64.length % 4)) % 4));
  return Uint8Array.from(binary, (c) => c.charCodeAt(0));
}

function decodeJson(part: string): Record<string, unknown> | null {
  try {
    const value: unknown = JSON.parse(new TextDecoder().decode(base64UrlDecode(part)));
    return value && typeof value === "object" ? (value as Record<string, unknown>) : null;
  } catch {
    return null;
  }
}

async function signingKeys(
  teamDomain: string,
  fetchImpl: typeof fetch,
  now: number,
  refresh: boolean,
): Promise<Jwk[]> {
  const cached = keyCache.get(teamDomain);
  if (cached && !refresh && now - cached.fetchedAt < KEYS_TTL_MS) return cached.keys;
  const res = await fetchImpl(`https://${teamDomain}/cdn-cgi/access/certs`);
  if (!res.ok) throw new Error(`Access keys answered HTTP ${res.status}`);
  const body = (await res.json()) as { keys?: Jwk[] };
  const keys = Array.isArray(body.keys) ? body.keys : [];
  keyCache.set(teamDomain, { fetchedAt: now, keys });
  return keys;
}

/**
 * Who the token says signed in, if Access issued it for this application and
 * it hasn't expired; null otherwise. Throws only if Access's keys can't be
 * fetched.
 */
export async function verifyAccessJwt(
  token: string | null,
  config: AccessConfig,
  { now = Date.now(), fetchImpl = fetch }: { now?: number; fetchImpl?: typeof fetch } = {},
): Promise<AccessIdentity | null> {
  const teamDomain = normalizeTeamDomain(config.teamDomain);
  if (!token || !teamDomain || !config.audience) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const header = decodeJson(parts[0]);
  const claims = decodeJson(parts[1]);
  if (!header || !claims || header.alg !== "RS256" || typeof header.kid !== "string") return null;

  let keys = await signingKeys(teamDomain, fetchImpl, now, false);
  let jwk = keys.find((key) => key.kid === header.kid);
  if (!jwk) {
    // A key Access has rotated in since the cache was filled.
    keys = await signingKeys(teamDomain, fetchImpl, now, true);
    jwk = keys.find((key) => key.kid === header.kid);
  }
  if (!jwk || jwk.kty !== "RSA") return null;

  let valid: boolean;
  try {
    const key = await crypto.subtle.importKey(
      "jwk",
      { kty: jwk.kty, n: jwk.n, e: jwk.e },
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false,
      ["verify"],
    );
    valid = await crypto.subtle.verify(
      "RSASSA-PKCS1-v1_5",
      key,
      base64UrlDecode(parts[2]),
      new TextEncoder().encode(`${parts[0]}.${parts[1]}`),
    );
  } catch {
    return null;
  }
  if (!valid) return null;

  const seconds = now / 1000;
  const audiences = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (!audiences.includes(config.audience)) return null;
  if (claims.iss !== `https://${teamDomain}`) return null;
  if (typeof claims.exp !== "number" || claims.exp + LEEWAY_SECONDS < seconds) return null;
  if (typeof claims.nbf === "number" && claims.nbf - LEEWAY_SECONDS > seconds) return null;
  return { email: typeof claims.email === "string" ? claims.email : null };
}
