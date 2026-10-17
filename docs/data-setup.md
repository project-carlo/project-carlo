# Data storage setup

Pipeline data lives in a Cloudflare R2 bucket. This page covers the bucket,
its API tokens and the repository secrets that use them, then day-to-day
operation. Steps 1–3 can be done from a phone browser.

## 1. Create the bucket

Cloudflare dashboard → **R2 Object Storage** → **Create bucket**.

- Name: `project-carlo-data`. If you pick another name, also add a repository
  **variable** (not a secret) `R2_BUCKET` with that name in step 3.
- Location: automatic. Default storage class.
- Leave public access off. Nothing here needs to be public.

If R2 hasn't been enabled on the account yet, Cloudflare asks you to turn it
on first. The free tier covers 10 GB. Nearly all of the bucket is bulletin
PDFs, one per parish per week: `fetch` stores only the pages the pipeline
reads, with images downsampled to 150 dpi, and old runs are pruned after each
publish (see [Day to day](#day-to-day)). To cap the PDFs too, add a lifecycle
rule on the `bulletins/` prefix (bucket → **Settings** → **Object lifecycle
rules**): an old bulletin is only needed to re-extract it with a new
classifier, and a missing one is skipped with a warning.

If you chose a **jurisdiction** (e.g. EU) instead of automatic, the bucket's
S3 endpoint looks like `https://<ACCOUNT_ID>.eu.r2.cloudflarestorage.com`.
Add it as a repository **variable** named `R2_ENDPOINT_URL` in step 3 (and
as an environment variable wherever else you use the keys). With the default
location you don't need it.

Note the **Account ID**. It's on the R2 overview page, and also in the
endpoint URL `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.

## 2. Create two API tokens

R2 overview → **Manage API tokens** (or *API* → *Manage API tokens*) →
**Create API token**. Create two tokens, each scoped to **only** the
`project-carlo-data` bucket:

| Token name | Permission | Used by |
| :-- | :-- | :-- |
| `project-carlo-write` | Object Read & Write | the weekly and publish workflows |
| `project-carlo-read` | Object Read only | site deploys, your laptop |

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
| `GEMINI_API_KEY` | the Gemini API key |
| `OPENAI_API_KEY` | the OpenAI API key, for update-mode (seeded) parishes, which run on `gpt-6-luna` |

Optional: `HEALTHCHECK_URL`, a ping URL from a service such as
[healthchecks.io](https://healthchecks.io) (free). Set its schedule to weekly
with a day of grace. It alerts you when a successful publish *doesn't* happen,
which covers the case where the job never runs at all.

## Day to day

- **Held or failed runs:** each run's summary page has its change report. A
  held or failed run also opens (or comments on) an issue labelled
  `data-refresh` that says why. To publish a held run anyway, go to
  **Actions** → **Publish Data Run** → **Run workflow** and enter the run id.
- **See what's live:** `pnpm data:status`, or R2 → `pipeline/latest.json`.
- **Roll back:** run **Publish Data Run** with an earlier run id (listed, with
  each run's status, by `pnpm data:status`) and tick **rollback**.
- **Old runs:** after each publish, the weekly job deletes old runs, keeping
  the published run and anything newer, the 8 most recent runs, and for each
  of the 12 most recent months that month's last run that passed or was
  published (held runs nobody published don't count). Those are the runs you can roll
  back to. `pnpm data:prune` shows what it would delete now;
  `--keep-recent` and `--keep-monthly` change the policy.
- **Inspect a held run locally:** `pnpm data:pull --run-id <id>`, then query
  `data/parish_events.db`, e.g. the `run_parish_result` table for that run.
- **Claude sessions:** cloud sessions don't get R2 keys, so they work from
  the code and the CSVs, not the pulled data. To give one the data later, add
  the read-only keys as the session environment's `R2_ACCOUNT_ID`,
  `R2_ACCESS_KEY_ID` and `R2_SECRET_ACCESS_KEY` and run `pnpm data:pull`.
  Never give them the write keys.
- **Rotate a key:** create a new token, update the secret, delete the old
  token.
