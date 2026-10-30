---
name: Our Lady of the Angels Parish
website: https://www.ourladyoftheangels.net/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-the-angels-cape-may-court-house-nj-08210
publication: ['url:https://www.church-bulletin.org/our-lady-of-the-angels-cape-may-court-house-nj-08210#john-patrick-564']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-the-angels-cape-may-court-house-nj-08210/2026-11-01.pdf
  seen: 2026-10-29
  note: 'Image-only PDF (12 pages, no text layer; pages 1-2 rendered with render.py and read). Page 1
    is headed ''OUR LADY OF THE ANGELS - NOV. 1, 2026'' and ''Rev. Thomas Barcellona, Pastor - Deacon
    Peter Davidson - Deacon Geoge Ferland, 35 E. Mechanic Street - Cape May Court House, NJ 08210''. Page
    2 gives the parish address, ''Mission Church: St. Elizabeth Rte. 47, Goshen'' and one ''Winter Mass
    Schedule'' for Our Lady of the Angels (Daily Mon-Fri 8:00AM; Saturday 5:00PM; Sunday 8:00AM, 10:30AM).
    It names this parish alone; recheck cannot find the words as text.'
- url: https://www.church-bulletin.org/our-lady-of-the-angels-cape-may-court-house-nj-08210
  seen: 2026-10-29
  note: 'John Patrick listing (id 564): dated weekly PDFs /bulletin/our-lady-of-the-angels-cape-may-court-house-nj-08210/<date>.pdf,
    newest 2026-11-01, then 2026-10-25, 10-18, 10-11, 10-04.'
- url: https://www.ourladyoftheangels.net/
  seen: 2026-10-29
  quote: http://www.jppc.net/onlinebulletins/564template.pdf
  note: probe url on the parish site lists this bulletin link; curl -sIL shows it redirecting (301, 301,
    302) to the church-bulletin.org listing above. The home page's Mass Schedule block also gives 'Winter
    Schedule (Sept 20, 2026 - May 2, 2027)' and 'No Mass at St. Elizabeth from October through the end
    of April'.
bulletin_status: available
---

## Publisher

John Patrick Publishing (id 564) prints Our Lady of the Angels' bulletin, and the church-bulletin.org listing serves it (checked 2026-10-29). The 1 November 2026 issue is image-only; its page 1 names the parish, Rev. Thomas Barcellona as pastor and the parish office at 35 E. Mechanic Street, and page 2 gives the one Mass schedule, for Our Lady of the Angels, with St. Elizabeth, Goshen named as its mission church. It is no other parish's bulletin. The directory (2015) and the 2025-2026 clergy assignments name the same pastor.

## Worship sites

Two, each with its own church record: Our Lady of the Angels, 35 E. Mechanic Street (`our-lady-of-the-angels-cape-may-court-house`), and St. Elizabeth, Route 47, Goshen (`st-elizabeth-goshen`), a summer-only mission (Sunday 10:15 AM; the parish's schedule says no Mass there October through April). St. Elizabeth is in the 2026 summer guide and in no other roster. The 2011 decree for the Parish of St. Maximilian Kolbe, Marmora, also named 'St. Elizabeth's Church, 561 Rt. 47 N., Goshen' as a worship site of that parish, but Kolbe's October 2026 bulletin lists only Resurrection and St. Casimir, and Our Lady of the Angels' bulletin and website now list it, so it is recorded here (lead for the Kolbe batch).

## Website and bulletin provider

`other` with a `page-pdfs` recipe on the church-bulletin.org listing, which has uniform dated names. The parish's site links the listing through jppc.net/onlinebulletins/564template.pdf. `fetch:check` (2026-10-29) picks the 2026-11-01 issue (freshness 'future': posted before its Sunday). The issues are image-only, so the pipeline has to read them as images.

## Not yet confirmed

Nothing open for the row.
