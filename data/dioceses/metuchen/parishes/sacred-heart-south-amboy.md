---
name: Sacred Heart
website: https://sacredheartsa.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:12058']
group: ''
evidence:
- url: https://files.ecatholic.com/12058/bulletins/20261025.pdf
  seen: 2026-10-30
  quote: Rev. Stanley G. Gromadzki, Pastor
  note: 'Page 1 of the 25 October 2026 issue on the parish''s own eCatholic site: staff block names Rev.
    Stanley G. Gromadzki, Pastor, Rev. Lukasz Blicharski, Parochial Vicar and Jose R. Diaz, Deacon, beside
    the parish office at 531 Washington Ave., South Amboy and ''MASS SCHEDULE: Saturday evening 4:00 pm
    (English); Sunday 7:00 am, 9:00 am (Polish), 10:30am, 12:00 noon, 2:00pm (Spanish); Weekdays 8:00
    am (Monday through Saturday)''. It names no other parish church.'
- url: https://sacredheartsa.org/bulletins
  seen: 2026-10-30
  note: 'Read with the browser (visit.py --links): the parish''s Bulletins page links one files.ecatholic.com/12058/bulletins/<YYYYMMDD>.pdf
    per Sunday, newest 20261101, back to 20260726 in the first 15 links.'
- url: https://www.church-bulletin.org/church-of-the-sacred-heart-south-amboy-nj-08879
  seen: 2026-10-30
  note: John Patrick Publishing also lists this parish (newest issue 2026-11-01). Its 2026-10-25.pdf has
    the same page-1 text as the eCatholic 20261025.pdf (same Mass schedule and staff block) with extra
    advertising pages, so it is a second copy of the same bulletin, not a second publisher; only the parish-hosted
    copy is recorded.
research:
- method: probe url on the finder/GCatholic website http://www.sacredheartchurchsa.com
  url: http://www.sacredheartchurchsa.com
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None: the domain does not resolve (checked with and without www). The live site was found
    by web search and confirmed from the bulletin masthead.'
  retry_when: The diocese's finder is updated to sacredheartsa.org
bulletin_status: available
---

## Publisher

Sacred Heart (Church of the Sacred Heart, 531 Washington Avenue, South Amboy) publishes its own weekly bulletin on its own eCatholic site (id 12058). The 25 October 2026 issue (`files.ecatholic.com/12058/bulletins/20261025.pdf`, page 1) gives Rev. Stanley G. Gromadzki, Pastor, Rev. Lukasz Blicharski, Parochial Vicar and Jose R. Diaz, Deacon, the parish office address and one Mass schedule: Saturday evening 4:00 pm (English); Sunday 7:00 am, 9:00 am (Polish), 10:30 am, 12:00 noon, 2:00 pm (Spanish); weekdays 8:00 am Monday to Saturday. The finder names the same pastor and parochial vicar, so the finder's clergy line is current for this parish.

**Not shared with St. Mary.** South Amboy's other parish, St. Mary, Star of the Sea, has a different pastor in its bulletin (Rev. Guy W. Selvester) and publishes through John Patrick Publishing (id 537). A grep of St. Mary's 25 October 2026 issue (8 pages) for 'Sacred Heart' and 'Gromadzki' found nothing, and a grep of this bulletin for 'St. Mary' and 'Selvester' found nothing. They are separate bulletins.

## Worship sites

One church, 531 Washington Avenue (`sacred-heart-south-amboy`; directory:24541, gcatholic:18632). The bulletin's Mass schedule names no other place. The bulletin mentions Memorial Hall, Sacred Heart Cemetery and a Knights of Columbus hall, which are parish function spaces, not Mass sites.

## Website and bulletin provider

The finder and GCatholic both give http://www.sacredheartchurchsa.com, which does not resolve (probe url, 2026-10-30: DEAD-DNS, checked with and without www). A web search found https://sacredheartsa.org, which is the parish's live eCatholic site; the bulletin masthead prints 'www.sacredheartsa.org', and the contact page gives 531 Washington Avenue, (732) 721-0040, the finder's phone. Provider `ecatholic`, site id 12058. The same bulletin is also posted on church-bulletin.org (see evidence); that copy is not recorded as a publication.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved the eCatholic site and picked `files.ecatholic.com/12058/bulletins/20261101.pdf` (5 pages, 1.1 MB): transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `future` (two days ahead). Publication identity was not machine-checked; a grep of that issue finds 'Gromadzki' and I read the 25 October masthead myself. No recipe is needed for `ecatholic`.

## Not yet confirmed

Nothing open. The only gap is the freshness status `future`, which is the publisher posting the next Sunday's issue early.
