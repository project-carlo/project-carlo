import { beforeAll, describe, expect, it } from "vitest";
import { normalizeTeamDomain, verifyAccessJwt } from "./accessAuth";

const TEAM = "carlo.cloudflareaccess.com";
const AUD = "a1b2c3";
const NOW = Date.UTC(2026, 9, 12, 12);
const CONFIG = { teamDomain: TEAM, audience: AUD };

let privateKey: CryptoKey;
let publicJwk: JsonWebKey;

beforeAll(async () => {
  const pair = await crypto.subtle.generateKey(
    {
      name: "RSASSA-PKCS1-v1_5",
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: "SHA-256",
    },
    true,
    ["sign", "verify"],
  );
  privateKey = pair.privateKey;
  publicJwk = await crypto.subtle.exportKey("jwk", pair.publicKey);
});

function base64Url(bytes: Uint8Array | string): string {
  const data = typeof bytes === "string" ? new TextEncoder().encode(bytes) : bytes;
  return btoa(String.fromCharCode(...data))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function sign(
  claims: Record<string, unknown>,
  header: Record<string, unknown> = { alg: "RS256", kid: "k1" },
): Promise<string> {
  const head = `${base64Url(JSON.stringify(header))}.${base64Url(JSON.stringify(claims))}`;
  const signature = await crypto.subtle.sign(
    "RSASSA-PKCS1-v1_5",
    privateKey,
    new TextEncoder().encode(head),
  );
  return `${head}.${base64Url(new Uint8Array(signature))}`;
}

function validClaims(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    aud: [AUD],
    iss: `https://${TEAM}`,
    email: "owner@example.com",
    exp: NOW / 1000 + 3600,
    nbf: NOW / 1000 - 10,
    ...overrides,
  };
}

/** Serves the test key as Access's certs endpoint, counting requests. */
function keysFetch(kid = "k1"): typeof fetch & { calls: string[] } {
  const calls: string[] = [];
  const impl = (async (input: RequestInfo | URL) => {
    calls.push(String(input));
    return Response.json({ keys: [{ ...publicJwk, kid }] });
  }) as typeof fetch & { calls: string[] };
  impl.calls = calls;
  return impl;
}

describe("verifyAccessJwt", () => {
  it("accepts a token Access signed for this application", async () => {
    const fetchImpl = keysFetch();
    const token = await sign(validClaims());
    await expect(verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl })).resolves.toEqual({
      email: "owner@example.com",
    });
    expect(fetchImpl.calls).toEqual([`https://${TEAM}/cdn-cgi/access/certs`]);
  });

  it("accepts a single audience given as a string", async () => {
    const token = await sign(validClaims({ aud: AUD }));
    const identity = await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() });
    expect(identity).not.toBeNull();
  });

  it("refuses a missing or malformed token", async () => {
    const fetchImpl = keysFetch();
    expect(await verifyAccessJwt(null, CONFIG, { now: NOW, fetchImpl })).toBeNull();
    expect(await verifyAccessJwt("not-a-jwt", CONFIG, { now: NOW, fetchImpl })).toBeNull();
    expect(await verifyAccessJwt("a.b.c", CONFIG, { now: NOW, fetchImpl })).toBeNull();
  });

  it("refuses another application's token", async () => {
    const token = await sign(validClaims({ aud: ["someone-else"] }));
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses another issuer", async () => {
    const token = await sign(validClaims({ iss: "https://evil.cloudflareaccess.com" }));
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses an expired token", async () => {
    const token = await sign(validClaims({ exp: NOW / 1000 - 3600 }));
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses a token not yet valid", async () => {
    const token = await sign(validClaims({ nbf: NOW / 1000 + 3600 }));
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses a tampered token", async () => {
    const token = await sign(validClaims());
    const [head, , signature] = token.split(".");
    const forged = `${head}.${base64Url(JSON.stringify(validClaims({ email: "x@example.com" })))}.${signature}`;
    expect(await verifyAccessJwt(forged, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses an unsigned token", async () => {
    const token = await sign(validClaims(), { alg: "none", kid: "k1" });
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl: keysFetch() })).toBeNull();
  });

  it("refuses a key Access doesn't publish, after looking again once", async () => {
    const fetchImpl = keysFetch("other");
    const token = await sign(validClaims(), { alg: "RS256", kid: "unknown" });
    expect(await verifyAccessJwt(token, CONFIG, { now: NOW, fetchImpl })).toBeNull();
    // The cached keys, if fresh, then one refetch: never a fetch per attempt beyond that.
    expect(fetchImpl.calls.length).toBeGreaterThanOrEqual(1);
    expect(fetchImpl.calls.length).toBeLessThanOrEqual(2);
  });

  it("refuses everything when not configured", async () => {
    const token = await sign(validClaims());
    const fetchImpl = keysFetch();
    expect(
      await verifyAccessJwt(token, { teamDomain: "", audience: AUD }, { now: NOW, fetchImpl }),
    ).toBeNull();
    expect(
      await verifyAccessJwt(token, { teamDomain: TEAM, audience: "" }, { now: NOW, fetchImpl }),
    ).toBeNull();
    expect(fetchImpl.calls).toEqual([]);
  });
});

describe("normalizeTeamDomain", () => {
  it("takes a bare domain or a URL", () => {
    expect(normalizeTeamDomain("Carlo.cloudflareaccess.com")).toBe(TEAM);
    expect(normalizeTeamDomain("https://carlo.cloudflareaccess.com/")).toBe(TEAM);
  });

  it("refuses anything that isn't an Access team domain", () => {
    expect(normalizeTeamDomain("example.com")).toBeNull();
    expect(normalizeTeamDomain("carlo.cloudflareaccess.com.example.com")).toBeNull();
    expect(normalizeTeamDomain("")).toBeNull();
  });
});
