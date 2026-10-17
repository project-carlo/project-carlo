---
name: Saint Ann's Basilica Parish
website: https://stannsbasilicaparish.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://stannsbasilicaparish.org/bulletin/']
group: Saint Ann Basilica Parish
evidence:
- url: https://stannsbasilicaparish.org/SABP-Bulletin/SABPBulletin101126/files/page/1.jpg
  seen: 2026-10-16
  note: 'Page 1 of the 11 October 2026 bulletin (a scanned image in a FlipHTML5 book embedded on /bulletin;
    read as an image): "Saint Ann''s Basilica Parish / SS Peter and Paul Church", pastor Rev. James J.
    Paisley; "Celebration of the Eucharist": daily Mass at St. Ann Mondays 8:00 am, 12 Noon, 3:30 pm,
    6:00 pm, Tuesday-Friday 8:30 am and 7:00 pm, Saturday 8:30 am; SS Peter and Paul Wednesdays 9:00 am;
    Saturday 4:00 pm St. Ann''s Basilica; Sunday 8:30 am and 11:00 am St. Ann''s Basilica, 11:00 am SS
    Peter and Paul Church, 7:00 pm St. Ann''s Basilica. Two rectories: 1250 Saint Ann Street and 1309
    West Locust Street.'
- url: https://stannsbasilicaparish.org/bulletin/
  seen: 2026-10-16
  quote: 'St. Ann''s Mass Schedule: Mon (Novena): 8AM, 12PM, 3:30PM, 6:00PM Tues- Fri: 8:30AM, 7:00 PM
    - Sat: 8:30 AM & 4:00 PM Sun 8:30 AM, 11:00 AM, 7:00PM Saints Peter & Paul: Wed 9:00 AM - Sun 11:00
    AM'
  note: The parish site's Bulletin page. It embeds this week's issue as an iframe, https://stannsbasilicaparish.org/SABP-Bulletin/SABPBulletin101126/SABP-Bulletin-Oct-11-26.html
    (a FlipHTML5 export whose pages are JPEGs, files/page/1.jpg ... 4.jpg, with an empty text index),
    and links /bulletin-archive/.
promoted: 2026-10-17
---

## Publisher

Saint Ann's Basilica Parish (West Scranton; its parochial vicar is a Passionist, C.P.)
publishes one weekly bulletin for its two churches on its own site. The 11 October 2026 issue
(the current one on 16 October) is headed "Saint Ann's Basilica Parish / SS Peter and Paul
Church" and gives one "Celebration of the Eucharist" schedule for St. Ann's Basilica and SS.
Peter and Paul Church, with both rectories. The finder lists both as worship sites of the
one canonical parish, and no other parish shares it.

## Worship sites

- `saint-ann-basilica-scranton`: Monday novena Masses 8 am, noon, 3:30 and 6 pm;
  Tuesday-Friday 8:30 am and 7 pm; Saturday 8:30 am and 4 pm; Sunday 8:30 am, 11 am and 7 pm.
- `sts-peter-and-paul-scranton` (1309 West Locust Street): Wednesday 9 am, Sunday 11 am.

GCatholic's "St. Ann" at 1320 Price Street is the Maronite church, a different parish
(`excluded/`, `other-jurisdiction`).

## Website and bulletin provider

stannsbasilicaparish.org is the parish's site (www.stannbasilica.org in the finder redirects
to it). Its /bulletin page embeds the week's issue as a FlipHTML5 book in an iframe on the
same domain (`SABP-Bulletin/SABPBulletin<MMDDYY>/SABP-Bulletin-<Mon>-<DD>-<YY>.html`). The
book has no PDF and no text: each page is a scanned JPEG at `files/page/<n>.jpg`. The row is
`other` with `url:` of the bulletin page; no `provider_id` recipe is set because no existing
collector reads a self-hosted image flipbook (the flipbook collector only knows third-party
hosts). The pipeline will need a collector for this format, and will have to read the issue
as images.

`fetch:check` after promotion (2026-10-17): "No PDF links found on bulletin page:
https://stannsbasilicaparish.org/bulletin/", as expected. The `page-images` collector reads
one image per issue; this book has four (`files/page/1.jpg` to `4.jpg`, listed in its
`javascript/config.js`), and the fetch stage downloads one file per bulletin, so it is not
pinned. Reading it needs a fetch that assembles several images into one PDF.

## Not yet confirmed

Whether the pipeline can fetch this bulletin at all (see above): until multi-image issues are
supported, expect no PDF.
