---
name: Our Lady of the Immaculate Conception of Aparecida
website: https://ourladyofaparecida.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://ourladyofaparecida.org/
  seen: 2026-11-12
  quote: Established as an independent parish in 2020 after nearly two decades as a quasi-parish under
    St. Peter's, the community has expanded to a new location in Bethel
  note: 'The parish''s own bilingual site (probe get): ''42 Vail Road, Bethel, CT 06801''; Fr. Leonel
    Medeiros, ''Episcopal Vicar for Brazilian Catholics''; Mass schedule Saturday 5:00 PM and 7:00 PM
    Portuguese, Sunday 7:30 AM, 9:30 AM Portuguese, 11:30 AM English, 6:00 PM Portuguese, daily Mon-Wed
    & Fri 7:00 PM, Thu 6:45 AM; events listed through October 2026. No bulletin link; /bulletin and /boletim
    answer 404. No mention of St. Peter as a Mass site, nor of Immaculate Heart of Mary.'
- url: https://www.bridgeportdiocese.org/parishes/our-lady-of-the-immaculate-conception-of-aparecida-parish-bridgeport/
  seen: 2026-11-12
  note: 'Directory entry (directory:1167): 42 Vail Road, Bethel; ''Reverend Leonel Medeiros, Pastor''.
    Its Mass times (wp-json custom/v1/mass-times?parish_id=1167) include Saturday 17:00 and Sunday 16:00
    and 18:00 Portuguese ''At St. Peter Parish, Danbury'' besides Masses with no place given.'
revisit: 'Look again for an Aparecida bulletin (boletim): the parish site, its Facebook/Instagram pages,
  ParishesOnline, Discover Mass; if one turns up, set the provider and run fetch:check'
revisit_after: 2027-02-01
research:
- method: probe get on the parish site (home page, /bulletin, /boletim); church-bulletin.org guessed slug;
    probe po guessed org slugs our-lady-of-aparecida-06801 and our-lady-of-aparecida-parish-06801 (no
    such organisation)
  url: https://ourladyofaparecida.org/
  checked: '2026-11-12'
  outcome: not-found
  next_action: Search the web for 'Nossa Senhora Aparecida Bethel boletim'; open the parish's Facebook
    and Instagram pages in the browser (the site's links to them are script-rendered)
  retry_when: A web search is available, or the parish site adds a bulletin page
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No bulletin found for Our Lady of the Immaculate Conception of Aparecida, Bethel (checked 2026-11-12). Its own site (`ourladyofaparecida.org`), a bilingual Portuguese-English one-page site, gives the Mass schedule, ministries and events through October 2026 but links no bulletin, and `/bulletin` and `/boletim` answer 404. No ParishesOnline organisation or church-bulletin.org page was found under the slugs tried. Its pastor, Fr. Leonel Medeiros, also administers Immaculate Heart of Mary, Danbury, which has no bulletin either; St. Peter, Danbury's bulletin (1 November 2026) mentions neither. So no shared bulletin was found among the three.

## Worship sites

- `our-lady-of-aparecida-bethel`: the parish site gives "42 Vail Road, Bethel CT" with Saturday 5:00pm and 7:00pm, Sunday 7:30am, 9:30am, 6:00pm (Portuguese) and 11:30am (English), and daily Masses (Mon-Wed and Fri 7:00pm, Thu 6:45am).

The diocese's directory still lists some Aparecida Masses "At St. Peter Parish, Danbury" (mass-times:1167-st-peter-church-aparecida-masses). The parish site says the community was a quasi-parish under St. Peter's before 2020 and "has expanded to a new location in Bethel", and lists no Mass at St. Peter; St. Peter's 1 November 2026 bulletin lists no Portuguese Mass. I took the directory's note as out of date and linked that roster entry to St. Peter's church (`st-peter-danbury`), the building it names, not to this row. The directory's Aparecida schedule (Sunday 9:00 Portuguese and 11:00 English) also differs from the site's; I followed the parish's own site.

## Website and bulletin provider

Provider `no_bulletin`: no bulletin was found (see research). Website: the parish's own site, where a bulletin would appear.

## Not yet confirmed

Whether the parish publishes a bulletin anywhere (its Facebook and Instagram pages were not read). See research and `revisit`.
