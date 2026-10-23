---
name: The Pittsburgh Oratory and Catholic Newman Center
website: https://pittsburghoratory.org/publications
bulletin_provider: other
provider_id: page-pdfs https://pittsburghoratory.org/publications#bulletin
publication: ['url:https://pittsburghoratory.org/publications#bulletin']
group: ''
evidence:
- url: https://d945e594-8657-47e2-9cd9-e9033c3d8da0.usrfiles.com/ugd/5299f8_39c2fc664b0a4d238e038df1fa77f459.pdf
  seen: 2026-10-23
  quote: The Pittsburgh Oratory
  note: Page 1 masthead of the weekly bulletin the Oratory's site links as 'Read This Week's Bulletin'
    (4 pages; page 1 is the cover 'The Pittsburgh Oratory of Saint Philip Neri, Catholic Newman Center';
    page 2 is headed 'October 25 | Thirtieth Sunday in Ordinary Time' with the Mass intentions). Own publisher,
    not carried in any parish bulletin.
- url: https://d945e594-8657-47e2-9cd9-e9033c3d8da0.usrfiles.com/ugd/5299f8_39c2fc664b0a4d238e038df1fa77f459.pdf
  seen: 2026-10-23
  quote: '**During the academic year, the 11:00am Mass on Sunday is celebrated at'
  note: 'Page 2, MASS AND CONFESSIONS box: ''Sunday: 9:00am, 11:00am, 4:00pm, 9:00pm; Monday-Thursday:
    7:00am, 5:15pm, *9:00pm; Friday: 7:00am, 5:15pm; Saturday: 10:00am, 4:00pm''; continues ''Heinz Chapel
    on the University of Pittsburgh campus, not in the Oratory Chapel.'' Sunday intentions list ''11:00am
    (Heinz Chapel) Newman Center Students''.'
- url: https://pittsburghoratory.org/publications
  seen: 2026-10-23
  quote: The weekly bulletin carries the week's Mass intentions, announcements, and schedule notes. A
    new edition is published every weekend.
  note: Publications page of the Oratory's own site (Next.js, 200 to curl). The 'Read This Week's Bulletin'
    button links the hashed usrfiles.com PDF above; a second button links the quarterly newsletter The
    Oratory Times (August 2026, vol. 10 no. 2), which is not the weekly bulletin.
- url: https://parishesonline.com/organization/catholic-newman-center
  seen: 2026-10-23
  note: 'probe po: LPi org ''Catholic Newman Center'' (0018000000Qx7qXAAR, 4450 Bayard St, website thepittsburghoratory.org)
    exists but has no publications. Not a channel; ids not recorded as publication.'
research:
- method: fetch:check --diocese pittsburgh --parish pittsburgh-oratory (headed Chrome), 2026-10-23
  url: https://pittsburghoratory.org/publications
  checked: '2026-10-23'
  outcome: found
  next_action: 'Re-run fetch:check after the next weekend issue: the file name is a hash with no date,
    so check the pick''s page 2 heading shows the new Sunday'
  retry_when: The Oratory redesigns /publications or lists the quarterly Oratory Times ahead of the weekly
    bulletin
---

## Publisher

The Pittsburgh Oratory (Oratory of St. Philip Neri, GCatholic 60863) is the Catholic Newman Center for Pitt, CMU and Chatham. It is not a diocesan parish and appears in no parish bulletin or the diocese's Mass Finder, but it publishes its own weekly bulletin: the 25 October 2026 issue (read 2026-10-23) is a 4-page PDF whose cover reads 'The Pittsburgh Oratory of Saint Philip Neri, Catholic Newman Center' and whose page 2 carries the Mass intentions and the full Mass and confession schedule. Under Rules settled 1 a place whose public Mass schedule is printed in a bulletin is a church row; here the publisher is the Oratory itself, so it is a parish-like publisher row (README: one parish row = one bulletin). Batch 19's parish bulletins printed no campus Mass, as the lead said; none was expected, because this bulletin is separate.

## Worship sites

Two places: the Oratory chapel at 4450 Bayard Street (churches/st-philip-neri-pittsburgh, daily Masses) and, in the academic year, Heinz Chapel on the Pitt campus (churches/heinz-memorial-chapel-pittsburgh, Sunday 11:00 am), both from the bulletin's schedule box. The Oratory's site (https://pittsburghoratory.org/liturgy) says the same: 'We celebrate Mass every day in the Oratory Chapel and on campus. All are welcome at any Mass.' Nothing else is named. CMU and Chatham have no Mass in the schedule.

## Website and bulletin provider

The Oratory's own site, https://pittsburghoratory.org (the old thepittsburghoratory.org, GCatholic's website, redirects to it), links the current bulletin from /publications and from /liturgy as a hashed usrfiles.com PDF (the file name carries no date). Provider `other`, recipe `page-pdfs https://pittsburghoratory.org/publications#bulletin`. `fetch:check` on 2026-10-23 picked 5299f8_39c2fc664b0a4d238e038df1fa77f459.pdf ('first-listed'), the 25 October weekly bulletin: transport ok, a PDF, 9.2 MB. The same page lists a second PDF (5299f8_3814e108..., The Oratory Times, 15 August 2026, 8 pages) after it; the pick depends on the weekly bulletin staying first. ParishesOnline has an empty org `catholic-newman-center` for this address: not a channel, not recorded as a publication id.

## Not yet confirmed

Publication identity and freshness read 'unverified/unknown' in fetch:check because the file name has no date and no expected identity was supplied; I checked them by hand (masthead and the 25 October heading above). Whether next week's file replaces the first-listed link was not observable in one session.
