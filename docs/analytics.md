# Visitor analytics

The site keeps its own analytics: which pages people see, where they come
from, and what they do. Events go to the site's Worker, which writes them to
[Workers Analytics Engine](https://developers.cloudflare.com/analytics/analytics-engine/)
in the same Cloudflare account. Nothing goes to a third party.

## Why this approach

- **Nothing else to sign up for.** The Worker already runs on `/api/*`. The
  dataset (`project_carlo_events`) is created on the first write after deploy,
  so there's no dashboard setup or script tag ID.
- **Private by design.** There are no cookies and no persistent visitor ID.
  The page never sees an IP address, and the Worker records only Cloudflare's
  country code for the request. No free text is ever sent: no search queries,
  no place names. Visitors with Global Privacy Control or Do Not Track turned
  on send nothing.
- **Cheap.** A page's events go in one batched request when the page is
  hidden or left, so each page costs one Worker invocation. Workers Free
  includes 100,000 data points a day (one per event) and 10,000 queries a day.
  Data is kept for three months.
- **Pages and actions in one place.** Cloudflare Web Analytics would count
  pageviews, but it can't record actions such as "picked a church in search"
  or "opened the bulletin". Here both are rows in the same dataset, so you can
  query them together.

Two limits to know. A tab killed without being hidden first loses that page's
unsent events. Automated browsers (`navigator.webdriver`) never send, so
end-to-end tests don't add traffic (`e2e/analytics.spec.ts` turns this off to
test the pipeline). The Worker also drops batches from crawler User-Agents.

## What's recorded

Each event is one row. The columns are fixed by position, so queries name
them as `blobN`, `doubleN` and `index1`:

| Column | Meaning |
| :-- | :-- |
| `index1` | Visit ID: random, kept in the tab's `sessionStorage`, and replaced after 30 idle minutes |
| `blob1` | Event name (below) |
| `blob2` | Page path, without the query string |
| `blob3` | Host that served the page: `projectcarlo.com`, or a preview's `*.workers.dev` |
| `blob4` | Country code (Cloudflare's) |
| `blob5` | `mobile`, `tablet` or `desktop`, by viewport width |
| `blob6` | `kind` (per event) |
| `blob7` | `target` (per event) |
| `blob8` | `detail` (per event) |
| `blob9` | Referring site's host (pageviews from another site only) |
| `blob10` | `utm_source` or `ref` from the landing URL (pageviews only) |
| `double1` | 1 if this pageview began the visit, else 0 |
| `_sample_interval` | How many events the row stands for (Analytics Engine samples heavy traffic) |

| Event | Sent when | `kind` | `target` | `detail` |
| :-- | :-- | :-- | :-- | :-- |
| `pageview` | A page is shown (prerendered or in the app) | | | |
| `search_select` | A search result is picked | `church` or `place` | Church slug | |
| `locate` | "Use my location" answers | `located`, `denied`, `unavailable`, `unsupported` | | |
| `filter` | A map filter changes | `event_type`, `days`, `clear` | | Event type |
| `map_open` | A city or church page's map opens full screen | | | |
| `feedback_open` | The feedback form opens | | Church slug | |
| `outbound` | A link off the site is followed | The link's `data-track` (`bulletin`, `bulletin_page`, `parish_website`), else `link` | Host | |

Preview deployments write to the same dataset. Filter on `blob3` to keep them
apart.

## Reading it

```bash
pnpm analytics               # last 7 days on projectcarlo.com
pnpm analytics --days 30
pnpm analytics --host <preview-host>.workers.dev
pnpm analytics --sql "SELECT blob6 AS kind, SUM(_sample_interval) AS n FROM project_carlo_events WHERE blob1 = 'locate' GROUP BY kind"
```

The report covers visits and pageviews by day, top pages, landing pages,
referrers, campaigns, countries, devices, actions, the churches picked in
search, and outbound links. It needs `CLOUDFLARE_ACCOUNT_ID` and a
`CLOUDFLARE_API_TOKEN` with **Account → Account Analytics → Read**, set in
the environment or the repo's `.env`. Create the token under Cloudflare
dashboard → My Profile → API Tokens. Use a separate token from the deploy one.

Count with `SUM(_sample_interval)`, not `COUNT()`. Count visits with
`SUM(_sample_interval * double1)` on pageviews. See the
[SQL reference](https://developers.cloudflare.com/analytics/analytics-engine/sql-reference/)
for the dialect. The reports themselves live in
`apps/web/src/lib/analyticsReports.ts`, shared with the dashboard below.

## The dashboard

The same reports are on a web page at
[projectcarlo.com/admin/analytics](https://projectcarlo.com/admin/analytics),
laid out for a phone: totals, visits by day, then each ranked report, with
7, 30 and 90 day periods and a picker for preview hosts. The page reads
`/api/admin/analytics`, where the Worker runs the queries with its own read
token. The dashboard's own views are not recorded.

Two locks keep it private:

1. **Cloudflare Access** stands in front of both paths and lets in only the
   people its policy names, after a one-time code by email.
2. **The Worker checks Access's sign-in itself.** It verifies the
   `Cf-Access-Jwt-Assertion` token against the Access application's
   audience tag before it answers (`src/lib/accessAuth.ts`). Access on
   projectcarlo.com doesn't cover the Worker's workers.dev and preview URLs,
   so the check is what keeps those closed. Without the settings below, the
   endpoint answers 503 and never the data.

### Setting it up (once)

1. **A read token.** Create one under My Profile → API Tokens with
   **Account → Account Analytics → Read**, as for `pnpm analytics` (the same
   token works). Never the deploy token.
2. **An Access application.** In the Cloudflare dashboard, open Zero Trust →
   Access → Applications → Add an application → Self-hosted. Add two public
   hostnames on `projectcarlo.com`, one with path `admin/analytics` and one
   with path `api/admin/*`. Add a policy with action Allow that includes your
   email address, and turn on the One-time PIN login method if no other is
   set up. Save it, then copy the application's **Application Audience (AUD)
   tag** from its overview. Your **team domain** (`<team>.cloudflareaccess.com`)
   is under Zero Trust → Settings → Team name and domain.
3. **The Worker's secrets.** From `apps/web`, set each one. Secrets survive
   deploys, which plain vars in `wrangler.jsonc` would overwrite.

   ```bash
   pnpm exec wrangler secret put CLOUDFLARE_ACCOUNT_ID
   pnpm exec wrangler secret put ANALYTICS_API_TOKEN   # the read token
   pnpm exec wrangler secret put ACCESS_TEAM_DOMAIN    # <team>.cloudflareaccess.com
   pnpm exec wrangler secret put ACCESS_AUD            # the AUD tag
   ```

4. **On your phone**, open projectcarlo.com/admin/analytics, sign in with the
   emailed code, and add the page to your home screen. When the sign-in
   lapses (24 hours by default, set on the Access application), the page asks
   you to sign in again.

A dashboard load runs 11 queries, well inside Workers Free's 50 subrequests
per invocation and 10,000 SQL API queries a day.

### Trying it locally

Put the read token in `apps/web/.dev.vars` (gitignored):

```bash
CLOUDFLARE_ACCOUNT_ID=...
ANALYTICS_API_TOKEN=...
ANALYTICS_DASHBOARD_LOCAL=1
```

Then run `pnpm preview` and open
<http://localhost:8787/admin/analytics?host=projectcarlo.com>.
`ANALYTICS_DASHBOARD_LOCAL` skips Access only for requests to `localhost` or
`127.0.0.1`, which no request through Cloudflare can be.

## Adding an event

1. Add its name to `ANALYTICS_EVENT_NAMES` in `apps/web/src/lib/analyticsApi.ts`.
   The Worker drops any name not on that list.
2. Call `track("name", { kind, target, detail })` from `src/lib/analytics.ts`
   where it happens. Keep the values to slugs and fixed words, never what
   someone typed or where they are.
3. A link off the site needs no code: give it `data-track="what-it-is"`.
4. Add it to the table above.
