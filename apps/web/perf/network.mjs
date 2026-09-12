// Network environment for measurement runs, shared by bench.mjs and profile.mjs.
//
// Both tools must see the same workload: a profile taken under different
// network conditions than the benchmark points at the wrong hot functions.
// (profile.mjs used to 503 every off-origin request, tiles included, so it
// profiled Leaflet's tile-error path rather than the path bench.mjs measures.)

// 1x1 transparent PNG — every map tile resolves to this, so tile loading costs
// the same in every run and never touches the network.
export const BLANK_PNG = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "base64",
);

/** Route handler: same-origin requests pass through, everything else is stubbed. */
export async function stubOffOrigin(context, origin) {
  await context.route("**/*", async (route) => {
    const url = route.request().url();
    if (url.startsWith(origin)) return route.fallback();
    if (/\.png($|\?)/.test(url) || url.includes("tile.")) {
      return route.fulfill({ status: 200, contentType: "image/png", body: BLANK_PNG });
    }
    return route.fulfill({ status: 503, contentType: "application/json", body: "{}" });
  });
}
