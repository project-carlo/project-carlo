---
name: Christ the Redeemer Parish
website: https://www.christtheredeemer.us
bulletin_provider: parishes_online
provider_id: christ-the-redeemer
publication: ['po-org:christ-the-redeemer', 'lpi:0018000000QbyuvAAB', 'po-container:03/1431']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1431/20261025B.pdf
  seen: 2026-10-29
  quote: 318 Carl Hasselhan Drive, Atco, NJ 08004
  note: 'Page 1 masthead of the 24-25 October 2026 issue (16 pages, text layer): ''CHRIST THE REDEEMER
    ... CATHOLIC CHURCH'', pastor Rev. Joseph D. Wallace. Names this parish alone and gives one address.'
- url: https://container.parishesonline.com/bulletins/03/1431/20261025B.pdf
  seen: 2026-10-29
  quote: Saturday Vigil | 4:00pm
  note: 'Page 1 MASS SCHEDULE: Sunday 9:00am & 11:00am; Monday through Friday 8:00am. Page 8 lists every
    Mass intention at those times only (Sat 4:00 PM, Sun 9:00 and 11:00 AM, weekdays 8:00 AM).'
- url: https://www.christtheredeemer.us/bulletins
  seen: 2026-10-29
  note: 'Rendered in the browser: the page embeds the ParishesOnline publicationWidget with id=0018000000QbyuvAAB
    (probe: lpi:0018000000QbyuvAAB, po-container:03/1431) and links the 2026-10-11 to 2026-11-01 issues
    in container 03/1431; footer ''WeConnect | By LPi''.'
- url: https://parishesonline.com/organization/christ-the-redeemer
  seen: 2026-10-29
  note: 'probe po christ-the-redeemer: organization ''Christ the Redeemer'', 318 Carl Hasselhan Dr, Atco,
    NJ 08004-1939, website christtheredeemer.us, latest issue 2026-11-01.'
- url: https://www.church-bulletin.org/christ-the-redeemer-catholic-church-atco-nj-08004
  seen: 2026-10-29
  note: 'John Patrick listing (id 683, from jppc.net/onlinebulletins/683template.pdf) for the same parish:
    no bulletin editions, only USCCB readings and a link to christtheredeemer.us. John Patrick hosts the
    listing but the bulletin is the LPi one.'
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese camden --parish christ-the-redeemer
  url: https://container.parishesonline.com/bulletins/03/1431/20261101B.pdf
  checked: '2026-10-29'
  outcome: found
  next_action: None; the pick is the 2026-11-01 issue (posted early, so freshness reads 'future'); the
    2026-10-25 issue's masthead was read in full.
- method: 'Searched for Mass at St. Anthony (Waterford) and Sacred Heart (Cedar Brook): the parish bulletin,
    site pages, Catholic Star Herald search for both names'
  url: https://www.christtheredeemer.us/general-information
  checked: '2026-10-29'
  outcome: not-found
  next_action: Ask the parish office or read a later bulletin for any Mass at either church; search for
    a sale or relegation decree
  retry_when: A bulletin lists Mass at either church, or a source dates a closure
  revisit_after: 2027-01-31
---

## Publisher

The parish publishes through LPi / ParishesOnline (organization `christ-the-redeemer`, LPi id 0018000000QbyuvAAB, container 03/1431). The 24-25 October 2026 issue (page 1, read 2026-10-29) is headed "Christ the Redeemer ... Catholic Church", Rev. Joseph D. Wallace pastor, 318 Carl Hasselhan Drive, Atco, with Saturday vigil 4:00 pm, Sunday 9:00 am and 11:00 am, Monday to Friday 8:00 am. It names no other parish. The parish was formed on 10 November 2010 from Assumption (Atco), Blessed John XXIII (St. Lucy, Blue Anchor, and Sacred Heart, Cedar Brook) and St. Anthony (Waterford); "the seat of the parish will be Assumption Church" (diocese news, 2010-10-08).

## Worship sites

One church: Assumption, 318 Carl Hasselhan Drive, Atco, which the parish's own "The Parish Story" calls "the parish's principal worship space" and which houses St. Lucy's Chapel. The roster lists two more of the 2010 churches under this parish, St. Anthony (436 Pennington Ave., Waterford) and Sacred Heart (Route 73, Cedar Brook). The current bulletin and the site's Mass schedule give times at one site only, and every Mass intention and minister schedule in the 25 October issue fits Atco alone, but no source says those two are closed (a 2015 Catholic Star Herald article says St. Anthony was "re-evaluated and kept opened as an active worship site" in 2010, and the parish's General Information page still lists addresses for both). They are in `open/` with a revisit, per the rule that a church is closed only on a source that says so. St. Lucy, Blue Anchor, closed with a final Mass on 7 November 2010 and has an `excluded/` record.

## Website and bulletin provider

`parishes_online` with provider_id `christ-the-redeemer`; the parish's own site embeds the widget, and its old domain ctratco.com (the directory's, GCatholic's) no longer resolves. The site christtheredeemerparish.org, found by guessing, is a Catholic parish in Lusaka, Zambia, and is not this one. John Patrick's listing for the parish (id 683) carries no issues.

## Not yet confirmed

Whether Mass is ever held at St. Anthony or Sacred Heart (see their open records).
