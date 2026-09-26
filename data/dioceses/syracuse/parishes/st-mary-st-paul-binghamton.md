---
name: St. Mary of the Assumption and St. Paul
website: https://www.marypaul.org
bulletin_provider: discover_mass
provider_id: st-mary-of-the-assumption-binghamton-ny
publication: ['discovermass:st-mary-of-the-assumption-binghamton-ny', 'discovermass:st-paul-binghamton-ny',
  'url:https://stmarypaul.wordpress.com/bulletins-2026/']
group: ''
evidence:
- url: https://stmarypaul.wordpress.com/wp-content/uploads/2026/09/2026-09-27.pdf
  seen: 2026-09-26
  quote: St.MaryoftheAssumptionChurch/St.PaulChurch
  note: 'The 27 September 2026 issue, self-hosted (page-3 footer quoted; the text layer runs words together).
    Page 1: "St. Mary of the Assumption 192-194 Court Street" and "Church of St. Paul 282 Chenango Street",
    one pastor (Rev. Ken Kirkman), and one Mass schedule: Saturday Vigil 5:00 p.m. St. Paul''s; Sunday
    7:30 a.m. St. Mary''s, 9:00 a.m. St. Paul''s, 11:30 a.m. St. Mary''s; weekday Masses at both. Page
    2 adds a Sunday 2:00 p.m. Latin Mass at St. Mary''s (SMA).'
- url: https://stmarypaul.wordpress.com/bulletins-2026/
  seen: 2026-09-26
  quote: September 27, 2026 Download
  note: The parishes' "Bulletins 2026" page (marypaul.org redirects to stmarypaul.wordpress.com), listing
    weekly PDFs through 2026-09-27.
- url: https://discovermass.com/church/st-mary-of-the-assumption-binghamton-ny/
  seen: 2026-09-26
  quote: 192-194 Court St, Binghamton, NY 13901
  note: Discover Mass listing for St. Mary of the Assumption; `issues.py discovermass` found issues through
    2026-09-27, and its page 1 is the same masthead as the self-hosted PDF. The St. Paul listing (discovermass.com/church/st-paul-binghamton-ny/,
    "282 Chenango St, Binghamton, NY 13901") serves the same bulletin. The PDF itself says "View this
    bulletin online at www.DiscoverMass.com".
---

## Publisher

St. Mary of the Assumption and St. Paul, two canonical parishes with one pastor (Rev. Kenneth
Kirkman), publish **one** weekly bulletin. I read the 27 September 2026 issue: its page 1 heads
both churches ("St. Mary of the Assumption, 192-194 Court Street" and "Church of St. Paul, 282
Chenango Street") with one Mass schedule that alternates between them (Saturday 5:00 pm St.
Paul's; Sunday 7:30 am and 11:30 am St. Mary's, 9:00 am St. Paul's; weekday noon Masses at both),
and page 2 lists a Sunday 2:00 pm Latin Mass at St. Mary's. Every page footer reads "St. Mary of
the Assumption Church / St. Paul Church". One bulletin, so one row.

## Worship sites

Two: St. Mary of the Assumption (`churches/st-mary-of-the-assumption-binghamton.md`) and St. Paul
(`churches/st-paul-binghamton.md`). The diocese's list has "Assumption of the Blessed Virgin
Mary, Binghamton (CLOSED - See St. Mary of the Assumption)"; it is not in this region's finder
roster and nothing I read gives its building, so nothing is recorded for it.

## Website and bulletin provider

marypaul.org (the directory's website) redirects to stmarypaul.wordpress.com, whose "Bulletins
2026" page links a PDF per Sunday through 27 September 2026. The same issues are on Discover Mass
under two church listings (St. Mary of the Assumption and St. Paul), which serve the same PDF. I
chose `discover_mass` with the St. Mary listing as `provider_id`, because the pipeline fetches
Discover Mass by church slug and the WordPress file URLs carry an upload-month folder that does
not match the issue date (the 9 August issue is under /2026/09/). Both Discover Mass slugs and the
WordPress bulletin page are in `publication`. GCatholic's website for both churches,
downtowncatholic.com, was not checked.

## Not yet confirmed

Nothing about the structure.
