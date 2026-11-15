---
name: Immaculate Heart of Mary
website: https://discovermass.com/church/immaculate-heart-of-mary-danbury-ct/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['discovermass:immaculate-heart-of-mary-danbury-ct']
group: ''
evidence:
- url: https://discovermass.com/church/immaculate-heart-of-mary-danbury-ct/
  seen: 2026-11-12
  quote: There are currently no bulletins available for Immaculate Heart of Mary.
  note: 'The diocese''s directory gives this Discover Mass page as IHM''s website. It lists no bulletin
    issues (issues.py discovermass: ''no bulletins listed''); its ''Visit Website'' link is the Facebook
    page facebook.com/immaculateheartdanbury; Mass times ''Powered by MassTimes.org''.'
- url: https://parishesonline.com/organization/immaculate-heart-of-mary-church-06810
  seen: 2026-11-12
  note: 'probe po: ParishesOnline org ''Immaculate Heart of Mary Church'', 149 Deer Hill Ave, Danbury
    (LPi id 0018000000Qbz4qAAB), with no publications (''this organization does not publish a bulletin
    here now'').'
- url: https://www.facebook.com/immaculateheartdanbury/
  seen: 2026-11-12
  note: 'Read logged out with visit.py: ''Immaculate Heart of Mary Church, Danbury, Connecticut'', 706
    followers; the visible posts are two from 23 December 2025, no bulletin.'
- url: https://www.bridgeportdiocese.org/parishes/immaculate-heart-of-mary-parish-danbury/
  seen: 2026-11-12
  note: 'Directory entry (directory:1352): 149 Deer Hill Avenue, Danbury; ''Reverend Leonel Medeiros,
    Administrator''; Mass times (wp-json custom/v1/mass-times?parish_id=1352) Saturday 17:00 English,
    18:30 Portuguese; Sunday 09:00 Portuguese, 11:00 English, 18:00 Portuguese; Monday-Friday 19:00 Portuguese,
    Wednesday 09:00 Portuguese.'
revisit: 'Look again for an IHM bulletin: the Discover Mass page''s Bulletins tab, ParishesOnline org
  immaculate-heart-of-mary-church-06810, the Facebook page''s posts, and Our Lady of Aparecida''s site
  (same pastor); if one turns up, set the provider and run fetch:check'
revisit_after: 2027-02-01
research:
- method: issues.py discovermass; probe po on the IHM org; visit.py on the Facebook page; probe url on
    guessed domains ihmdanbury.org, immaculateheartdanbury.org (no parish words), ihmdanbury.com (no DNS);
    church-bulletin.org guessed slugs (no issues); Our Lady of Aparecida's site (no bulletin, no mention
    of IHM)
  checked: '2026-11-12'
  outcome: not-found
  next_action: 'Ask through a later check whether IHM posts a bulletin anywhere: recheck the Discover
    Mass and ParishesOnline listings and the Facebook posts, and search the web for ''Immaculate Heart
    of Mary Danbury bulletin'''
  retry_when: A web search is available, or the diocese's directory lists a new IHM website
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No bulletin found for Immaculate Heart of Mary, Danbury (checked 2026-11-12). The diocese's directory gives as its website the Discover Mass page, which says "There are currently no bulletins available for Immaculate Heart of Mary." Its ParishesOnline organisation (`immaculate-heart-of-mary-church-06810`) has no publications, and its Facebook page, the "Visit Website" link on Discover Mass, shows no bulletin. The administrator, Rev. Leonel Medeiros, is also pastor of Our Lady of Aparecida in Bethel; Aparecida's own site posts no bulletin either and does not mention IHM, so no shared bulletin was found. St. Peter's bulletin (1 November 2026) doesn't mention either parish.

## Worship sites

- `immaculate-heart-of-mary-danbury`: the diocese's directory (read 2026-11-12) lists Saturday 5:00pm English and 6:30pm Portuguese, Sunday 9:00am Portuguese, 11:00am English and 6:00pm Portuguese, weekdays 7:00pm Portuguese and Wednesday 9:00am. GCatholic (22022) lists the church at 149 Deer Hill Ave.

The Discover Mass page's schedule (from MassTimes.org, under a stale COVID-19 notice) places the Monday, Tuesday, Thursday and Friday 7:00pm Portuguese Masses "In chapel Santo Cristo inside Portuguese Community Center". The directory gives no place for them. That chapel is kept in `open/santo-cristo-chapel-danbury` until a current source settles it.

## Website and bulletin provider

Provider `no_bulletin`: no bulletin was found anywhere checked (see research). The website stays the directory's Discover Mass page, where an IHM bulletin would most likely appear; `publication` keeps its Discover Mass id.

## Not yet confirmed

Whether IHM publishes a bulletin anywhere, and whether the Santo Cristo chapel still holds Mass. See research and `revisit`.
