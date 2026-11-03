---
name: Our Lady of Fatima
website: https://www.olfparish.org
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2127
publication: ['url:http://sponsors.bonventure.net/?page=2127']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/2127/2026-11-01.pdf
  seen: 2026-11-02
  quote: 'Physical Address/Church: 501 New Market Road, Piscataway, New Jersey 08854'
  note: '1 November 2026 issue (16 text pages). The page 1 masthead names Our Lady of Fatima Church, ''The
    Home of the Shrine of the Three Little Shepherds of Fatima'', alone: Saturday 5:00 pm; Sunday 7:00,
    9:00, 11:00 am, 1:00 & 5:00 pm; weekdays 7:00 & 9:00 am (Tue/Thu 7:00 am & 7:00 pm); ''Mailing Address/Parish
    Center: 50 Van Winkle Place''. Page 2 Parish Directory lists ''Pastor Very Rev. Arlindo Paul Da Silva''.'
- url: http://sponsors.bonventure.net/?page=2127
  seen: 2026-11-02
  quote: Our Lady of Fatima Church 50 Van Winkle Place • Piscataway, NJ 08854
  note: 'Bon Venture sponsor page 2127 for this parish only: ''Click to View Current Bulletin'' and weekly
    previous issues through November 01, 2026.'
- url: https://www.olfparish.org/about-masstimes
  seen: 2026-11-02
  quote: Sunday 7:00am, 9:00am, 11:00am, 1:00pm, 5:00pm
  note: Parish site (Catholic Web Company) Divine Worship Times page; it agrees with the bulletin. The
    site's 'Bulletin' menu item goes to an HTML 'Bulletin Events & Announcements' page (/event) and links
    no PDF or Bon Venture page.
bulletin_status: available
---

## Publisher

Our Lady of Fatima, Piscataway, publishes its own weekly bulletin through Bon Venture (sponsor page 2127; files at `sponsors.bonventure.net/pdfs/2127/<YYYY-MM-DD>.pdf`). I found the listing by a web search on 2026-11-02; the parish site does not link it. The 1 November 2026 issue (read 2026-11-02) has a text page 1 masthead naming 'Our Lady of Fatima Church … Physical Address/Church: 501 New Market Road, Piscataway' with its own Mass schedule, and page 2 lists 'Pastor Very Rev. Arlindo Paul Da Silva', matching the parish finder.

## Worship sites

One church, 501 New Market Road (directory:24528, gcatholic:18617). The masthead's Mass schedule names no other place. The 'Shrine of the Three Little Shepherds of Fatima' is at the parish ('The Home of the Shrine'); no separate Mass is listed there. The finder's 'Filipino Mass: 4th Sunday of every month in the church' is in the same church. 50 Van Winkle Place is the parish center and mailing address.

## Website and bulletin provider

Website https://www.olfparish.org (`probe url` reported DEAD-DNS; `probe get` fetched it). Its 'Bulletin' item is an HTML events page, not the printed bulletin. Provider `other`, recipe `page-pdfs http://sponsors.bonventure.net/?page=2127`, as for the other Bon Venture parishes here.

## Not yet confirmed

Nothing about the publisher.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs http://sponsors.bonventure.net/?page=2127` and picked pdfs/2127/2026-11-01.pdf: transport ok, PDF, issue date inferred from the file name, freshness `fresh`, identity unverified by the tool. That is the 1 November 2026 issue whose masthead I read (above). No `recipe` line was printed, so the provider settings stay as set.
