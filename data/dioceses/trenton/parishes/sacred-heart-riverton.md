---
name: Church of the Sacred Heart
website: https://www.shcriverton.org
bulletin_provider: parishes_online
provider_id: church-of-the-sacred-heart-08077
publication: ['po-org:church-of-the-sacred-heart-08077', 'lpi:0018000000Qx8obAAB', 'po-container:03/1347']
group: Cohort 2 (Cinnaminson, Riverton, Maple Shade, Delran)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1347/20261101B.pdf
  seen: 2026-10-30
  quote: Church of The Sacred Heart
  note: 'Page 1 of the 1 November 2026 issue (12 pages, text layer): ''Sunday, November 1, All Saints
    Day  Church of The Sacred Heart''. Page 2 staff list: ''Pastor Rev. Charles M. Schwartz 856-829-0090'',
    and ''Mass Schedule Weekend Mass Saturday Vigil | 4:00 pm Sunday | 7:30 am, 9:30 am & 11:30 am Weekday
    Mass Monday | 8:00 am ... Sacred Heart Catholic Church 103 Fourth Street; Riverton, NJ 08077''. It
    names this parish alone.'
- url: https://www.shcriverton.org/bulletin
  seen: 2026-10-30
  quote: View Past Bulletins
  note: The parish's own Bulletin page (plain fetch works) links the container.parishesonline.com/bulletins/03/1347/
    PDFs for 25 Oct, 18 Oct, 11 Oct and 1 Nov 2026 and 'View Past Bulletins' to parishesonline.com/organization/church-of-the-sacred-heart-08077.
- url: https://parishesonline.com/organization/church-of-the-sacred-heart-08077
  seen: 2026-10-30
  note: 'probe po church-of-the-sacred-heart-08077: lpi 0018000000Qx8obAAB, address ''103 4th Street,
    Riverton, New Jersey, 08077'', container 03/1347, latest issue 2026-11-01.'
research:
- method: pnpm fetch:check --diocese trenton --parish sacred-heart-riverton (headed Chrome); ParishesOnline
    container 03/1347 by org slug
  url: https://parishesonline.com/organization/church-of-the-sacred-heart-08077
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 2026-11-01 issue (freshness future: the
    coming Sunday''s issue, posted early)'
bulletin_status: available
publication_reviews:
- parish: st-charles-borromeo-cinnaminson
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1347/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Church of the Sacred Heart, Riverton alone (pastor Rev. Charles
      M. Schwartz, 103 Fourth Street), with its own Mass times.
  - url: http://sponsors.bonventure.net/pdfs/2203/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Saint Charles Borromeo, Cinnaminson alone (pastor Rev. Daniel
      E. Kirk, 2500 Branch Pike), with its own Mass times. (Bon Venture 2203)
- parish: our-lady-of-perpetual-help-maple-shade
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1347/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Church of the Sacred Heart, Riverton alone (pastor Rev. Charles
      M. Schwartz, 103 Fourth Street), with its own Mass times.
  - url: http://sponsors.bonventure.net/pdfs/2214/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 issue is a bulletin for Our Lady of Perpetual Help, Maple Shade alone (pastor
      Fr. Fernando Monsalve, 236 E. Main St), with its own Mass times; its footer shows the Maple Shade
      account. (Bon Venture 2214)
- parish: resurrection-delran
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1347/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Church of the Sacred Heart, Riverton alone (pastor Rev. Charles
      M. Schwartz, 103 Fourth Street), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Resurrection Parish alone (pastor Rev.
      Michael A. Gentile Jr., 260 Conrow Road), with Mass at Holy Name and St. Casimir only. (John Patrick
      542)
---

## Publisher

The Church of the Sacred Heart, Riverton publishes its own weekly bulletin through ParishesOnline (organization church-of-the-sacred-heart-08077, container 03/1347). The 1 November 2026 issue (read from its text layer) is headed 'Church of The Sacred Heart' with Rev. Charles M. Schwartz as pastor and one Mass schedule at 103 Fourth Street. It names no other parish; Cohort 2's other three parishes publish elsewhere (Bon Venture 2203 and 2214, John Patrick 542), so the cohort is not one bulletin.

## Worship sites

One church, 103 Fourth Street, Riverton (see `sacred-heart-riverton`). The bulletin lists Mass at no other place. GCatholic (18727) and the finder (14548) list the same one site.

## Website and bulletin provider

The parish's own site (shcriverton.org, Cloudflare-free) embeds the container's PDFs on its /bulletin page; probe url finds lpi:0018000000Qx8obAAB and po-container:03/1347 there. The row reads ParishesOnline by the org slug.
