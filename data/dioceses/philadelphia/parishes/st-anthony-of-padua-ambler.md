---
name: St. Anthony of Padua and St. Joseph Parishes
website: https://www.saintanthonyparish.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-anthony-of-padua-parish-ambler-pa-19002
publication: ['url:https://www.church-bulletin.org/saint-anthony-of-padua-parish-ambler-pa-19002']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-anthony-of-padua-parish-ambler-pa-19002/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick listing 240, issue of 25 October 2026 (8 pages, image-only: probe pdf reads 0 pages,
    so pages 1-2 were rendered). Page 1 masthead reads ''St. Anthony & St. Joseph Parishes / October 25,
    2026 / Thirtieth Sunday in Ordinary Time'', with both churches'' addresses (St. Anthony of Padua Parish
    259 Forest Avenue; St. Joseph Parish 16 S. Spring Garden Street), one office-hours line, ''Pastor
    - Fr. James Mc Guinn'' and one shared ministry list marked ''SA & SJ''. Page 2 is one combined ''St.
    Anthony & St. Joseph Mass Schedule'' and one Mass-intentions list tagged SA or SJ.'
- url: https://www.church-bulletin.org/bulletin/saint-anthony-of-padua-parish-ambler-pa-19002/2026-03-01.pdf
  seen: 2026-10-28
  quote: St. Anthony & St. Joseph Churches
  note: Text-layer masthead of the 1 March 2026 issue; the 26 October 2025 issue (2025-10-26.pdf) carries
    the same 'St. Anthony & St. Joseph Churches' header and a joint Mass schedule with each Mass tagged
    SA or SJ. The joint bulletin is at least a year old.
- url: https://www.church-bulletin.org/saint-anthony-of-padua-parish-ambler-pa-19002
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 240 'Saint Anthony of Padua Parish', Ambler, PA 19002, 259 Forest Avenue, phone (215)
    646-4742; latest edition October 25, 2026. No other John Patrick listing in the Ambler area names
    St. Joseph (raw/jppc-pa.json search for Ambler finds only 240).
- url: https://saintanthonyparish.org/
  seen: 2026-10-28
  note: 'probe url: HTTP 200; its only bulletin link is http://www.jppc.net/onlinebulletins/240template.pdf
    (the listing 240 template). Other PDFs on the home page are a funeral packet, ministry schedules and
    council lists.'
- url: https://stjosephambler.org/
  seen: 2026-10-28
  quote: Website Outage
  note: St. Joseph's own site (probe url HTTP 200) shows a 'Website Outage' notice with its Mass times
    and no bulletin link or PDF.
- url: https://archphila.org/parish/st-joseph-ambler/
  seen: 2026-10-28
  quote: Rev. James T. McGuinn (Pastor) in residence at Saint Anthony of Padua, Ambler
  note: 'Directory: St. Joseph''s Pastor line; St. Anthony of Padua''s page names Rev. James T. McGuinn
    too.'
bulletin_status: available
---

## Publisher

St. Anthony of Padua (259 Forest Avenue) and St. Joseph (16 S. Spring Garden Street), Ambler, share a pastor, Rev. James T. McGuinn (directory pages of both parishes, read 2026-10-28; he lives at St. Anthony). **One bulletin or two? One.** John Patrick Publishing listing 240 ('Saint Anthony of Padua Parish') carries a single weekly issue whose page-1 masthead reads 'St. Anthony & St. Joseph Parishes' (25 October 2026), with both parishes' addresses, one set of office hours, one clergy list and one ministry list marked 'SA & SJ'; page 2 prints one combined 'St. Anthony & St. Joseph Mass Schedule' and one Mass-intentions list tagged SA or SJ. The 1 March 2026 issue's text layer reads 'St. Anthony & St. Joseph Churches' and the 26 October 2025 issue has the same header and joint schedule, so this is the established arrangement, not a recent merge of covers. St. Joseph has no listing of its own and its site (stjosephambler.org, in an outage) carries no bulletin. This is the only row for both parishes; each church keeps its own church row. It differs from St. Helena/St. Titus (shared content, separate issues) because here one issue has one masthead for both.

## Worship sites

Two churches, both in Ambler, both on the joint Mass schedule (25 October 2026, page 2): St. Anthony of Padua Church (SA: Sunday 9:00 AM, 11:00 AM, 5:00 PM; Spanish 1:00 PM second, fourth and fifth Sunday; weekday 8:15 AM Monday, Wednesday and Friday) and St. Joseph Church (SJ: Saturday vigil 4:00 PM; Sunday 7:30 AM; Spanish 1:00 PM first and third Sunday; weekday 6:30 AM Tuesday and Thursday; 6:30 AM communion services Monday, Wednesday and Friday). The 'Mary Chapel' named for the Anointing of the Sick is a room of St. Anthony's (SA), not another building. Our Lady of Mercy Regional Catholic School appears as a shared ministry only; no Mass is listed there.

## Website and bulletin provider

`other`, reading `page-pdfs` on the listing. saintanthonyparish.org is the site that links listing 240; stjosephambler.org is St. Joseph's own site and is not used, since it hosts no bulletin. The roster entries for St. Anthony and St. Joseph are linked on the two church rows.

## Fetch check

`fetch:check` (2026-10-28) with the `page-pdfs` recipe on the listing picked `https://www.church-bulletin.org/bulletin/saint-anthony-of-padua-parish-ambler-pa-19002/2026-10-25.pdf`: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` because the PDF has no text layer (masthead and Mass schedule read from renders, above). The check printed no separate recipe, and the one in `provider_id` is the one used.

## Not yet confirmed

Pages 3-8 of the issue were not read. Whether St. Joseph will ever get its own listing is unknown; if it does, compare mastheads before splitting.
