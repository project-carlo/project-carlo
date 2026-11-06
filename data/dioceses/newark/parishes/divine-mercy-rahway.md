---
name: Divine Mercy Parish, Rahway
website: https://www.divinemercyrahway.church/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:20836']
group: ''
evidence:
- url: https://files.ecatholic.com/20836/bulletins/20261101.pdf
  seen: 2026-11-05
  note: '1 November 2026 issue, 6 pages, image-only (no text layer; read pages 1-2 with render.py). Page
    1 masthead: ''DIVINE MERCY PARISH / PARROQUIA DIVINA MISERICORDIA'', ''Serving Jesus Christ since
    1854 and 1871 / Formerly St. Mary''s and St. Mark''s Roman Catholic Churches'', Very Rev. Alexander
    T. Cruz, VF, Pastor; ''232 Central Avenue, Rahway, NJ 07065''; Mass Schedule: Weekdays 12:00pm Monday-Friday;
    Martes 7:00pm Misa en Español; Saturday 9:00am, 4:00pm (Vigil Mass); Sunday 8:00am, 9:30am, 11:00am,
    12:30pm Misa en Español. No building other than 232 Central Avenue is named. Page 2 Mass intentions
    31 Oct-8 Nov match; ''This week at Divine Mercy'' places events only in the Church, Connell Hall,
    the Annex and rooms.'
- url: https://www.divinemercyrahway.church/bulletins
  seen: 2026-11-05
  note: 'eCatholic site (probe get/probe url 403; read with visit.py): ''Bulletin ARCHIVE 2026'' lists
    weekly issues from April 12 to ''November 1, 2026'', linking files.ecatholic.com/20836/bulletins/<yyyymmdd>.pdf.'
- url: https://www.divinemercyrahway.church/parish-history
  seen: 2026-11-05
  quote: Our current church edifice is the former St. Mary's Church.
  note: 'Read with visit.py. Also: Fr. Dennis Kaelin was pastor of St. Mary''s ''until its merger with
    nearby St. Mark''s Church in 2010 to form the Divine Mercy Parish'', and ''The old bells of St. Mark''s
    Church were placed in front of the rectory to serve as reminder of the previous church edifice''.'
bulletin_status: available
---

## Publisher

Divine Mercy Parish, Rahway (the 2010 merger of St. Mary and St. Mark), posts a weekly bulletin on its eCatholic site (ecatholic:20836). I read the 1 November 2026 issue, which is image-only: page 1 masthead 'DIVINE MERCY PARISH / PARROQUIA DIVINA MISERICORDIA', 'Formerly St. Mary's and St. Mark's Roman Catholic Churches', pastor Very Rev. Alexander T. Cruz, VF, 232 Central Avenue, with one Mass schedule (read by eye from the render; `recheck` can't find it in a text layer). The footer has no printer code: the issue looks parish-designed.

## Worship sites

- Divine Mercy Church, the former St. Mary's, 232 Central Avenue (`divine-mercy-rahway`): weekdays 12:00pm; Tuesday 7:00pm Spanish; Saturday 9:00am and 4:00pm vigil; Sunday 8:00, 9:30, 11:00am, 12:30pm Spanish (page 1).

Ruled out: St. Mark, 287 Hamilton Street (GCatholic 59526), the other merged church. The bulletin names no second church, the parish history calls St. Mary's 'our current church edifice' and St. Mark's 'the previous church edifice', and Rahway Rising reported on 9 August 2018 that its demolition had begun: `excluded/st-mark-rahway`. The rcan.org sacramental-records table (2025-05-22) lists both Saint Mary and Saint Mark, Rahway as 'Merged' into Divine Mercy Parish. The directory (172) and GCatholic (18540) give the parish at 232 Central Avenue. The Syro-Malankara St. Thomas mission (GCatholic 17006), whose GCatholic address is 'St. Mark Church, 287 Hamilton St.', is excluded as another jurisdiction by its own batch; Divine Mercy's bulletin does not carry its services.

## Website and bulletin provider

https://www.divinemercyrahway.church/ (the directory's link) is the eCatholic site: `probe url` gets 403 (Cloudflare), `visit.py` loads it and reports ecatholic:20836, and its /bulletins page lists the dated files.ecatholic.com/20836 issues. The masthead's 'www.divinemercyparishrahway.church' and GCatholic's divinemercyparishnj.com both answer DEAD-DNS (probe url, 2026-11-05). Provider `ecatholic`. The issues are image-only, so the pipeline has to read them as images.

Fetch check (2026-11-05, headed): transport ok, PDF, picked files.ecatholic.com/20836/bulletins/20261101.pdf, the 1 November 2026 issue read above (date inferred from the file name); freshness fresh (4 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it.

## Not yet confirmed

Pages 3-6 of the issue were not read (image-only); the Mass schedule and intentions on pages 1-2 settle the worship sites.
