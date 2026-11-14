---
name: Church of the Assumption
website: https://www.assumptionwestport.org/bulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.assumptionwestport.org/bulletins']
group: ''
evidence:
- url: https://www.assumptionwestport.org/bulletins/154-november-1-2026/file
  seen: 2026-11-12
  note: '1 November 2026 issue, downloaded in the browser (the file answers 403 without it); 8 pages,
    image-only, read by rendering. Page 1 header ''Church of the Assumption'' / ''November 1, 2026'' with
    the parish''s 1876-2026 150-years logo. Page 2 box: ''Daily Mass: Monday - Saturday: 7:30am''; ''Weekend
    Mass Schedule: Saturday Vigil: 5:00pm, Sunday: 7:30am, 9:00am, 11:00am, 5:00pm''; ''Filipino Mass
    - 2nd Sunday 2:00pm''; Holy Days vigil 5:30pm; Reconciliation Saturday 4:00pm-4:45pm; Mass intentions
    for these times, no other place named.'
- url: https://www.assumptionwestport.org/bulletins
  seen: 2026-11-12
  note: 'visit.py (probe url gets 403): the Bulletins page lists ''November 1, 2026'' (/bulletins/154-november-1-2026/file),
    ''October 25, 2026'' (153-...), back weekly through August 2026; no publisher id or widget.'
bulletin_status: unsupported-format
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-12
  url: https://www.assumptionwestport.org/bulletins/154-november-1-2026/file
  note: The Joomla Bulletins page lists one issue per Sunday as /bulletins/<n>-<date>/file links (no .pdf
    name), newest 'November 1, 2026' on 2026-11-12. The site answers 403 to probe get and fetch (Cloudflare);
    fetch:check (page-pdfs on the Bulletins page) reports 'No PDF links found on bulletin page'. In the
    browser, fetch() from the Bulletins page returns the issue as application/pdf (8 MB, 8 pages, image-only).
---

## Publisher

Church of the Assumption, Westport posts its own weekly bulletin on its Joomla site's Bulletins page (`https://www.assumptionwestport.org/bulletins`), one `/file` link per Sunday; no printer is named in it. The 1 November 2026 issue (`https://www.assumptionwestport.org/bulletins/154-november-1-2026/file`, the newest listed on 2026-11-12) was downloaded in the browser and read by rendering (it is image-only, 8 pages): page 1 is headed "Church of the Assumption" and "November 1, 2026"; page 2 gives Daily Mass Monday-Saturday 7:30am, Weekend Mass Saturday Vigil 5:00pm and Sunday 7:30am, 9:00am, 11:00am, 5:00pm, a Filipino Mass on the 2nd Sunday at 2:00pm, and Mass intentions for those times.

## Worship sites

One church, `assumption-westport`. The schedule names no other place.

## Website and bulletin provider

Provider `unsupported`, `fetch_gap` `joomla-file-endpoint`: the site is behind Cloudflare (403 to `probe url`, `probe get` and fetch), and its issue links are Joomla `/file` endpoints with no `.pdf` name, so `fetch:check` on 2026-11-12 (with `page-pdfs` on the Bulletins page) failed with "No PDF links found on bulletin page". The issue itself is a PDF when fetched from inside the browser (`scratch/bridgeport-map-1/tools/browser_download.py`). The bulletin is also image-only, so a collector will have to read it as images. GCatholic's `assumption-westport.org` was not used; the directory gives `assumptionwestport.org`.

## Not yet confirmed

Nothing about the parish is open; the row waits for a collector that reads Joomla `/file` links behind Cloudflare. When one lands, set the provider, run `fetch:check` and clear the gap.
