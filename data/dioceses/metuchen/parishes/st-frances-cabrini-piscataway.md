---
name: St. Frances Cabrini
website: https://stfrancab.com/
bulletin_provider: other
provider_id: page-pdfs https://stfrancab.com/parish-bulletin/ filename=Bulletin-template*.pdf
publication: ['url:https://stfrancab.com/parish-bulletin/']
group: ''
evidence:
- url: https://stfrancab.com/wp-content/uploads/2026/10/Bulletin-template-11-01-26.pdf
  seen: 2026-11-02
  quote: Rev. Jim Considine, Pastor
  note: '1 November 2026 issue (3 text pages). Page 1 masthead: ''St. FRANCES CABRINI CHURCH, Piscataway,
    New Jersey 08854'', parish office 208 Bound Brook Ave., website stfrancab.com; Mass Schedule ''Saturday
    Vigil 4:30 PM'', ''Sunday 7:30, 9:30, 11:30 AM'', weekdays Monday/Wednesday/Friday 12:10, Tuesday
    & Thursday 7:00 AM, Saturday 8:00 AM. Page 2 lists the Mass intentions for 2-8 November.'
- url: https://stfrancab.com/parish-bulletin/
  seen: 2026-11-02
  note: 'Parish WordPress ''BULLETIN'' page: embeds and links Bulletin-template-11-01-26.pdf, plus two
    non-bulletin PDFs (Breakfast-Flyer-2026.pdf, a scanned doc0273…pdf), hence the filename filter. ''Previous
    Bulletins'' (/previous-bulletins/) lists Bulletin-template-10-04-26 through 10-25-26.'
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

St. Frances Cabrini, Piscataway, posts its own weekly bulletin on its WordPress site as `wp-content/uploads/<yyyy>/<mm>/Bulletin-template-<MM-DD-YY>.pdf` (the 1 November issue sits in the 2026/10 upload folder). The 1 November 2026 issue (read 2026-11-02) names 'St. FRANCES CABRINI CHURCH, Piscataway, New Jersey 08854' and 'Rev. Jim Considine, Pastor' with its own Mass schedule; the finder lists Rev. James F. Considine. The parish finder gives no website; I found the site by a web search on 2026-11-02, and the bulletin prints it ('Website: stfrancab.com').

## Worship sites

One church, 208 Bound Brook Avenue (directory:24529, gcatholic:18651). The bulletin's Mass schedule names no other place. GCatholic's phone for this church (+1 732 968-5555) is Our Lady of Fatima's; the bulletin and the finder give 732-885-5313, and nothing I read makes Cabrini part of Fatima: Fatima's 1 November bulletin lists only its own church.

## Website and bulletin provider

Website https://stfrancab.com/ (`probe url` reported DEAD-DNS; `probe get` fetched it). Provider `other`, recipe `page-pdfs https://stfrancab.com/parish-bulletin/ filename=Bulletin-template*.pdf`, because the Bulletin page also carries flyers.

## Not yet confirmed

Nothing about the publisher.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs https://stfrancab.com/parish-bulletin/ filename=Bulletin-template*.pdf` and picked Bulletin-template-11-01-26.pdf: transport ok, PDF, issue date observed from the file name, freshness `fresh`, identity unverified by the tool. That is the 1 November 2026 issue whose masthead I read (above). No `recipe` line was printed, so the provider settings stay as set.
