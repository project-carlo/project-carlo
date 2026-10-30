---
name: St. Peter Church
website: https://stpetersbytheshore.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2097
publication: ['url:http://sponsors.bonventure.net/?page=2097']
group: Cohort 20 (Point Pleasant, Brick)
evidence:
- url: http://sponsors.bonventure.net/pdfs/2097/2026-11-01.pdf
  seen: 2026-10-30
  quote: Saint Peter Catholic Church
  note: 'Page 1 of the 1 November 2026 issue (12 pages; text on 10, pages 6-7 image-only): ''The Solemnity
    of All Saints, St. Peter Church, November 1, 2026, Saint Peter Catholic Church, 406 Forman Avenue,
    Point Pleasant Beach, New Jersey 08742, (732) 892-0049''. Page 2: Sunday Masses 7:30, 9:00 and 11:00
    a.m.; weekday 8:30 a.m.; Saturday 5:00 p.m. It names St. Peter alone.'
- url: http://sponsors.bonventure.net/?page=2097
  seen: 2026-10-30
  quote: Saint Peter Roman Catholic Church
  note: 'Bon Venture sponsor page 2097, headed ''406 Forman Avenue • Point Pleasant Beach, NJ 08742'':
    ''Click to View Current Bulletin'', previous bulletins listed weekly from 1 November 2026 back to
    2025 and earlier.'
- url: https://stpetersbytheshore.org/
  seen: 2026-10-30
  note: Read in the browser (probe url answers 403). The homepage links 'Bulletins' to https://sponsors.bonventure.net/?page=2097
    and embeds eCatholic site 35377. The site's Mass block (#massModeAll) was not read; Mass times come
    from the bulletin.
research:
- method: pnpm fetch:check --diocese trenton --parish st-peter-point-pleasant-beach (headed Chrome); page-pdfs
    on Bon Venture page 2097
  url: http://sponsors.bonventure.net/?page=2097
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: transport ok, document_type pdf, picks 2026-11-01.pdf (''current''; issue date observed
    in the text; freshness ''future'', the coming Sunday''s issue).'
bulletin_status: available
---

## Publisher

St. Peter Church, Point Pleasant Beach publishes its own weekly bulletin through Bon Venture (sponsor page 2097), which its website's 'Bulletins' link goes to. The 25 October and 1 November 2026 issues (page 1, read 2026-10-30) name St. Peter Catholic Church, 406 Forman Avenue, alone, and the Mass schedule and intentions on page 2 cover only that church. The parish is run by friars ('Our Friars' on its site; the bulletin says 'a Friar'), but no other parish is named in the issues read.

## Worship sites

One: St. Peter Church (see `st-peter-point-pleasant-beach`). The wreath-sale notice in St. Martha's bulletin lists St. Peter's as a venue; that is cohort cooperation, not a shared bulletin.

## Website and bulletin provider

The directory's website is stpetersbytheshore.org (GCatholic's saintpetersonline.org is the older domain, JavaScript-rendered in the survey). The site is hosted by eCatholic (id 35377) but its Bulletins link goes to Bon Venture, so the eCatholic id is only the host and is not recorded as a publication. `probe url` answers 403 on stpetersbytheshore.org; the browser reads it.

## Not yet confirmed

Nothing outstanding.
