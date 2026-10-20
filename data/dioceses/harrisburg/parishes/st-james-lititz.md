---
name: St. James Catholic Church
website: https://stjameslititz.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:24609']
group: ''
evidence:
- url: https://files.ecatholic.com/24609/bulletins/20261018.pdf
  seen: 2026-10-20
  note: 'Image-only issue (13 pages, no text layer), read rendered (render.py). Page 1: "St. James Catholic
    Church, October 18, 2026, 29th Sunday in Ordinary Time ... Father Stephen D. Weitzel-Pastor ... Sunday
    Masses: Saturday Evening 4:00pm, Sunday Morning 8:30am & 10:30am ... Weekday Masses: Mass Tuesday-Friday
    9:00am ... Contact: 505 Woodcrest Ave. Lititz, PA 17543 ... Website: www.stjameslititz.org". Page
    2 "Parish Activities this week" lists each Mass, 17-25 October.'
- url: https://stjameslititz.org/bulletins
  seen: 2026-10-20
  note: 'Behind Cloudflare (visit.py challenged on all of about 26 loads on 19 October, through on the
    first load on 20 October). eCatholic bulletins page: "October 18, 2026" -> files.ecatholic.com/24609/bulletins/20261018.pdf,
    one issue per Sunday back to June 2026 and earlier.'
- url: https://church-bulletin.org/?id=231
  seen: 2026-10-20
  note: John Patrick Publishing has a listing "Saint James Catholic Church, Lititz, PA 17543" (redirects
    to church-bulletin.org/saint-james-catholic-church-lititz-pa-17543) with no bulletins on it (dated
    PDF paths for 27 Sep-25 Oct answer 404); not a live channel.
promoted: 2026-10-20
---

## Publisher

St. James Catholic Church, 505 Woodcrest Avenue, Lititz, publishes its own weekly bulletin on its
eCatholic site. The 18 October 2026 issue (image-only, read rendered on 20 October) has the page 1
masthead "St. James Catholic Church, October 18, 2026", Father Stephen D. Weitzel as pastor,
and one schedule: Saturday 4:00pm; Sunday 8:30am & 10:30am; Mass Tuesday-Friday 9:00am. Page 2
lists the week's Masses in the church. The cover art carries LPi credits; the bulletin is
parish-made and posted only on eCatholic.

## Worship sites

One church, `st-james-lititz`. GCatholic still says the parish is served by the Redemptorists;
the bulletin names a diocesan pastor (FrSWeitzel@hbgdiocese.org).

## Website and bulletin provider

`ecatholic`, website https://stjameslititz.org/ (directory), publication `ecatholic:24609`,
from the bulletins page's file links. Behind Cloudflare; the PDFs on files.ecatholic.com fetch
without a browser. **Image-only bulletin:** the 18 October issue has no text layer, so the
pipeline must read it as an image. A John Patrick listing (id 231) and a Discover Mass page
(st-james-lititz-pa) exist with no bulletins.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): ok, picked files.ecatholic.com/24609/bulletins/20261018.pdf (23 MB), this week's bulletin. The resolver got past the site's Cloudflare where plain curl could not.

## Not yet confirmed

Nothing.
