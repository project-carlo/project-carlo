---
name: Visitation Parish
website: https://visitationrcchurch.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:6597', 'url:https://www.church-bulletin.org/church-of-the-visitation-brick-nj-08723']
group: Cohort 22 (Brick and Lakewood)
evidence:
- url: https://files.ecatholic.com/6597/bulletins/20261101.pdf
  seen: 2026-10-30
  quote: Church of the Visitation
  note: 'The 1 November 2026 issue (12 pages, 11 with text) is a bulletin for the Church of the Visitation
    alone: page 2 gives Very Rev. Edward H. Blanchett, pastor; Church Address 755 Mantoloking Rd., Rectory
    Address 730 Lynnwood Ave., Brick, NJ; and the Liturgy of the Eucharist block Weekend Saturday 4:00,
    Sunday 9:00 & 11:00 AM; Daily Monday-Friday 7:30 (Church), Saturday 8:15 AM (Church).'
- url: https://www.church-bulletin.org/bulletin/church-of-the-visitation-brick-nj-08723/2026-11-01.pdf
  seen: 2026-10-30
  note: John Patrick listing 574 (Church of the Visitation, Brick 08723; latest edition November 1, 2026)
    serves the same 5,251,571-byte file as the parish's eCatholic bulletins page (identical md5 f68b04e0949c9ec8edae1470a7392b33).
- url: https://visitationrcchurch.org/bulletins
  seen: 2026-10-30
  quote: November 1 , 2026
  note: The eCatholic Bulletin Archive lists issues weekly from 1 November 2026; the home page also links
    jppc.net/onlinebulletins/574template.pdf. visitationchurch.com (GCatholic's site) is a parked domain-sale
    page; the finder's visitationrcchurch.org is the parish.
research:
- method: issues.py ecatholic:6597; probe get of the eCatholic and John Patrick files for the same Sunday,
    md5 compared
  url: https://visitationrcchurch.org/bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: both channels carry the same current issue.'
- method: pnpm fetch:check --diocese trenton --parish visitation-brick (headed Chrome); eCatholic resolver
    on visitationrcchurch.org
  url: https://files.ecatholic.com/6597/bulletins/20261101.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue (coming Sunday, ''future'' freshness). The cover
    page has no extractable text, so identity shows unverified; page 2 names the Church of the Visitation.'
bulletin_status: available
publication_reviews:
- parish: st-dominic-brick
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/6597/bulletins/20261101.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is a bulletin for the Church of the Visitation alone (page 2: pastor
      Very Rev. Edward H. Blanchett, 755 Mantoloking Road), with its own Mass times. (eCatholic 6597 =
      John Patrick 574)'
  - url: http://sponsors.bonventure.net/pdfs/4139/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead (page 1) names the Church of Saint Dominic and Diocesan Shrine
      of Saint Carlo Acutis, 250 Old Squan Road, Brick, alone, with pastor Rev. Brian Patrick Woodrow
      and its own Mass times. (Bon Venture 4139)
- parish: our-lady-of-guadalupe-lakewood
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/6597/bulletins/20261101.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is a bulletin for the Church of the Visitation alone (page 2: pastor
      Very Rev. Edward H. Blanchett, 755 Mantoloking Road), with its own Mass times. (eCatholic 6597 =
      John Patrick 574)'
  - url: http://sponsors.bonventure.net/pdfs/2195/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 1) names Our Lady of Guadalupe, Lakewood, alone, with pastor
      Rev. Guilherme Andrino, S.V.D. and the Mass times of its three churches. (Bon Venture 2195)
---

## Publisher

Visitation Parish, Brick (Cohort 22). It publishes one bulletin, printed by John Patrick Publishing (listing 574) and posted on the parish's eCatholic site (id 6597). The 1 November 2026 issue is the same file on both (identical md5), a bulletin for the Church of the Visitation alone: page 2 names the pastor Very Rev. Edward H. Blanchett and the parish's own Mass schedule.

## Worship sites

One church, the Church of the Visitation. The bulletin's page 2 gives two addresses: Church 755 Mantoloking Rd. and Rectory 730 Lynnwood Ave. (the finder, GCatholic and the John Patrick listing give 730 Lynnwood, the rectory). The "Daily Chapel" (confession Saturday 3:00 PM, adoration, weekday Masses "will resume in the Daily Chapel beginning Monday, November 9th at 7:30 AM" after the auction setup) is part of the church campus with no address of its own, so no second church row.

## Website and bulletin provider

visitationrcchurch.org is the eCatholic site. GCatholic's visitationchurch.com is parked (domain sale). The row reads the eCatholic archive; the John Patrick listing is kept in `publication`.

## Not yet confirmed

Nothing outstanding.
