# Data storage setup

One-time setup for storing pipeline data in Cloudflare R2 instead of git. You
can do steps 1–6 from a phone browser. Step 7 needs the computer that holds the
old bulletin PDFs.

## 1. Create the bucket

Cloudflare dashboard → **R2 Object Storage** → **Create bucket**.

- Name: `project-carlo-data`. If you pick another name, also add a repository
  **variable** (not a secret) `R2_BUCKET` with that name in step 3.
- Location: automatic. Default storage class.
- Leave public access off. Nothing here needs to be public.

If R2 hasn't been enabled on the account yet, Cloudflare asks you to turn it
on first. The free tier (10 GB) covers this project many times over; the
database and PDFs add up to tens of MB a year.

Note the **Account ID**. It's on the R2 overview page, and also in the
endpoint URL `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.

## 2. Create two API tokens

R2 overview → **Manage API tokens** (or *API* → *Manage API tokens*) →
**Create API token**. Create two tokens, each scoped to **only** the
`project-carlo-data` bucket:

| Token name | Permission | Used by |
| :-- | :-- | :-- |
| `project-carlo-write` | Object Read & Write | the weekly and publish workflows |
| `project-carlo-read` | Object Read only | site deploys, your laptop, Claude sessions |

After creating each token, Cloudflare shows its **Access Key ID** and
**Secret Access Key** only once. Keep the page open until they're saved in
step 3.

## 3. Add the GitHub secrets

github.com → the repository → **Settings** → **Secrets and variables** →
**Actions** → **New repository secret**. (The GitHub mobile app can't edit
secrets; use the website in a mobile browser.)

| Secret | Value |
| :-- | :-- |
| `R2_ACCOUNT_ID` | the Account ID from step 1 |
| `R2_WRITE_ACCESS_KEY_ID` | Access Key ID of `project-carlo-write` |
| `R2_WRITE_SECRET_ACCESS_KEY` | Secret Access Key of `project-carlo-write` |
| `R2_READ_ACCESS_KEY_ID` | Access Key ID of `project-carlo-read` |
| `R2_READ_SECRET_ACCESS_KEY` | Secret Access Key of `project-carlo-read` |
| `GEMINI_API_KEY` | already set |

Optional: `HEALTHCHECK_URL`, a ping URL from a service such as
[healthchecks.io](https://healthchecks.io) (free). Set its schedule to weekly
with a day of grace. It alerts you when a successful publish *doesn't* happen,
which covers the case where the job never runs at all.

## 4. Give Claude sessions read access

In the Claude app, open the cloud environment's settings (the environment menu
in a session's title bar → **Edit**) and add these environment variables,
using the **read-only** token:

```
R2_ACCOUNT_ID=<account id>
R2_ACCESS_KEY_ID=<project-carlo-read access key id>
R2_SECRET_ACCESS_KEY=<project-carlo-read secret access key>
```

New sessions pick them up, and the SessionStart hook pulls the published
database automatically. Don't give sessions the write token.

If a session reports that `<account id>.r2.cloudflarestorage.com` is blocked,
add `*.r2.cloudflarestorage.com` to the environment's allowed domains under
**Network access**.

## 5. Merge the pull request

Merging removes `data/metadata.json`, `data/events.json`,
`data/event_history.json` and `apps/web/public/frontend.snapshot` from the
repository. The site keeps working in the meantime: until the first run is
published, deploys reuse the snapshot the live site is already serving.

## 6. Run the first (bootstrap) refresh

github.com → **Actions** → **Weekly Data Refresh** → **Run workflow** → tick
**bootstrap** → **Run workflow**.

This builds the database from the last committed JSON files (the same data
the site shows today), runs a normal weekly pass on top, and publishes it if
the checks pass. After that, the Sunday schedule takes over with no bootstrap.

Check the run's summary page for the change report. If the run is **held**, an
issue labelled `data-refresh` explains why. To publish it anyway, go to
**Actions** → **Publish Data Run** → **Run workflow** and enter the run id.

## 7. Upload the old bulletin PDFs (at your computer, whenever convenient)

Until now, bulletin PDFs only existed on the machine that ran the pipeline.
New ones go to R2 automatically. To upload the old ones too, run this from the
repository on that machine with the **write** token:

```bash
export R2_ACCOUNT_ID=... R2_ACCESS_KEY_ID=... R2_SECRET_ACCESS_KEY=... CARLO_REMOTE_WRITE=1
pnpm data:upload-bulletins
```

It skips PDFs the bucket already has, so it's safe to re-run. Nothing depends
on this for the weekly run; it just makes old bulletins available for
`pnpm extract` / `pnpm compare` experiments and to agents.

## Day to day

- **See what's live:** `pnpm data:status`, or R2 → `pipeline/latest.json`.
- **Roll back:** run **Publish Data Run** with an earlier run id (listed by
  `pnpm data:status`).
- **Inspect a held run locally:** `pnpm data:pull -- --run-id <id>`, then query
  `data/parish_events.db`, e.g. the `run_parish_result` table for that run.
- **Rotate a key:** create a new token, update the secret, delete the old
  token.
