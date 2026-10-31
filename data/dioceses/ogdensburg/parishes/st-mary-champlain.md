---
name: The Church of St. Mary, Champlain
website: https://stmaryschamplain.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:15646']
group: ''
evidence:
- url: https://files.ecatholic.com/15646/bulletins/20260920.pdf
  seen: 2026-09-30
  note: 'Image-only PDF (1 sheet, no text layer), read with parish-site-access render.py, so `recheck`
    cannot find text in it. The 20 September 2026 issue, "25th Sunday in Ordinary Time, September 20 &
    27, 2026" (a double issue), lists Mass intentions for both weekends: "SATURDAY, SEPTEMBER 19 4:00PM
    MASS + (St. Mary’s) Helen Sample", weekdays "9:00AM (St. Mary’s)" on Thursday and Friday, "SATURDAY,
    SEPTEMBER 26 4:00PM MASS + (St. Mary’s) Helen Hicks", "SATURDAY, OCTOBER 3 4:00PM MASS + (St. Mary’s)
    Robert LaCount", and the Sunday and Monday to Wednesday Masses at St. Patrick’s; the same sheet carries
    "SANCTUARY LAMP / SEPTEMBER 19 - 26 In Memory of Norma & Ivan LaLonde", "STEWARDSHIP - SEPTEMBER 13,
    2026 Envelopes: $2,212 Plate: $261 Fuel: $332 Total: $2,805", "WELCOME TO ST. MARY’S", and "DOUBLE
    BULLETIN ... no new bulletin will be printed for St. Mary’s next weekend". It is a separate St. Mary''s
    publication, not the Rouses Point bulletin.'
- url: https://stmaryschamplain.org/bulletins
  seen: 2026-09-30
  note: 'Bulletins archive page (eCatholic, read in a browser with visit.py on 2026-09-30): "Archive 2026:
    September 20, September 13, September 6, August 30, ... May 3, February 1" and year links back to
    2016; every PDF is at files.ecatholic.com/15646/bulletins/YYYYMMDD.pdf.'
- url: https://stmaryschamplain.org/
  seen: 2026-09-30
  quote: OUR BROTHER PARISH St. Patrick's Church, Rouses Point
  note: 'Home page (eCatholic behind Cloudflare; read in a browser, so `recheck` reports it unreachable).
    Mass Times block: "SATURDAY: 4:00 PM", "THURSDAY: 9:00 AM", "FRIDAY: 9:00 AM", confession "SATURDAY:
    3:00 PM to 3:45 PM or any time by request".'
- url: https://www.rcdony.org/parish/champlain
  seen: 2026-09-30
  note: 'Directory: directory:champlain, St. Mary''s Church, 90 Church Street, Champlain 12919, phone
    518-298-8244, no website, pastor Reverend Nicolas J. Revilla (the same pastor as St. Patrick''s, Rouses
    Point). The diocese''s Parish Bulletins page lists Champlain as "None".'
promoted: 2026-09-30
---

## Publisher

The Church of St. Mary, Champlain publishes its own weekly bulletin on its own eCatholic site (id 15646). The newest issue, 20 September 2026, is an image-only sheet headed "25th Sunday in Ordinary Time, September 20 & 27, 2026" that says "DOUBLE BULLETIN ... no new bulletin will be printed for St. Mary's next weekend", with St. Mary's own Sanctuary Lamp and Stewardship (collection) reports and a "WELCOME TO ST. MARY'S" notice. It lists Mass intentions for St. Mary's (Saturday 4:00 PM, Thursday and Friday 9:00 AM) and, for convenience, the Masses at St. Patrick's, Rouses Point that share the pastor (Fr. Nicolas Revilla). The bulletin is image-only, so the pipeline will need to read it as an image.

This row is separate from `st-patrick-rouses-point` because each church has its own live bulletin channel (README step 5: one live member channel means no merge). The two are "brother parishes" under one pastor with one faith-formation program, and the Rouses Point bulletin also lists St. Mary's Masses; the audit may list the pair.

## Worship sites

- `st-mary-champlain` (90 Church St.): Saturday 4:00 PM, Thursday and Friday 9:00 AM.

Not here: GCatholic's "St. Joseph, 74 Mason Rd., Champlain" (18267) is St. Joseph's Cemetery (`excluded/st-joseph-cemetery-champlain`). Discover Mass has a listing "St. Mary of the Lake Oratory" at 86 Church Street, Champlain, whose website is stmaryschamplain.org: a mislabelled duplicate of this church (and Wikipedia's list says Masses at the real St. Mary of the Lake oratory, Cumberland Head, ended in July 2011), not another site.

## Website and bulletin provider

`stmaryschamplain.org` (eCatholic, id 15646, behind Cloudflare; loaded on the seventh `visit.py` attempt). It is not the directory's link (the directory has no website for Champlain), but it is the church's own site and is named on the Rouses Point site ("St. Mary's Church, Champlain"). Issues fetch without a browser: the 20 September 2026 file answers 200, 27 September and 4 October answer 403 (not posted; the 20 September sheet covers both weekends). Provider id empty.

## Not yet confirmed

- Whether the bulletin keeps to a weekly schedule after the September double issue.
