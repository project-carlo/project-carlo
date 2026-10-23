---
name: Saint Paul Cathedral Parish
website: https://www.ghocatholics.org
bulletin_provider: parishes_online
provider_id: st-paul-cathedral-parish
publication: ['po-org:st-paul-cathedral-parish', 'lpi:0018000000Qx7sGAAR', 'po-container:14/1180', 'po-org:st-rosalia-church',
  'lpi:0018000000Qx7qHAAR', 'po-org:st-stephen-church-15207', 'lpi:0018000000Qx7s9AAB']
group: Saint Paul Cathedral Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1180/20261025B.pdf
  seen: 2026-10-23
  quote: SAINT PAUL CATHEDRAL PARISH
  note: 'Page 1 masthead of the 25 October 2026 issue (container 14/1180, 20 pages, text layer readable):
    ''SERVING GREENFIELD • HAZELWOOD • OAKLAND'', ''PARISH WORSHIP SITES'' naming Saint Paul Cathedral
    (Fifth Avenue & Craig Street), Saint Rosalia (411 Greenfield Avenue) and Saint Stephen (5115 Second
    Avenue). One bulletin for all three.'
- url: https://container.parishesonline.com/bulletins/14/1180/20261025B.pdf
  seen: 2026-10-23
  quote: Saturday Anticipated | 4pm
  note: 'Page 2 Mass times box: Saint Paul Cathedral ''Saturday Anticipated | 6pm; Sunday | 6:30am, 10am,
    12pm, 6pm; Mon - Sat | 8:15am & 12:05pm''; Saint Rosalia ''Saturday Anticipated | 4pm; Sunday | 9am
    & 12pm (Spanish)''. The Mass-intentions list (26 Oct-1 Nov) names only Saint Paul Cathedral and Saint
    Rosalia. No Mass times are printed for Saint Stephen.'
- url: https://container.parishesonline.com/bulletins/14/1180/20260906B.pdf
  seen: 2026-10-23
  quote: place on Tuesday, September 15 at 6:00 pm at Saint Stephen Church, Hazelwood
  note: 'Page 7 ''Special events on the horizon'': the annual Mass celebrating the dedication of Saint
    Stephen Church, ''All are welcome''. Same page 1 masthead lists the three worship sites.'
- url: https://parishesonline.com/organization/st-paul-cathedral-parish
  seen: 2026-10-23
  note: 'probe po: three LPi orgs resolve to container 14/1180 with the 2026-10-25 issue as latest: st-paul-cathedral-parish
    (lpi 0018000000Qx7sGAAR, 108 N Dithridge St, website ghocatholics.org), st-rosalia-church (lpi 0018000000Qx7qHAAR,
    411 Greenfield Ave) and st-stephen-church-15207 (lpi 0018000000Qx7s9AAB, 5115 2nd Ave). All recorded
    as this one bulletin''s ids. Container walked 2025-10-05 to 2026-10-25: every Sunday returned 200.'
- url: https://www.ghocatholics.org/bulletins-1
  seen: 2026-10-23
  note: 'Rendered in headed Chrome (probe url gets 403): diocese-provided eCatholic site (ecatholic:22378,
    plus the diocese''s 16469 which is not recorded). The Bulletins page links to an online viewer (the
    ParishesOnline widget) and lists no PDF files, so ecatholic:22378 is not a publication id. Its footer
    names only two worship sites (St. Paul Cathedral, St. Rosalia).'
- url: https://diopitt.org/saint-paul-cathedral-parish
  seen: 2026-10-23
  note: 'Diocese parish page (read in headed Chrome for the directory roster; diopitt.org answers 403
    to recheck): one entry with three churches (Saint Paul Cathedral, Saint Rosalia, Saint Stephen), website
    www.saintpaulcathedral.org, phone 412-621-4951, pastor Very Rev. Kris D. Stubna. Saint Stephen is
    listed ''No Masses Scheduled''.'
promoted: 2026-10-23
research:
- method: Grepped monthly issues of container 14/1180 (2025-10-05 to 2026-10-25) for 'Saint Stephen' and
    'Hazelwood'
  url: https://container.parishesonline.com/bulletins/14/1180/20260906B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: Re-grep for Saint Stephen Masses around 15 September 2027 or if the parish site lists a
    Stephen schedule
  retry_when: A new bulletin prints a Mass at Saint Stephen
bulletin_status: available
---

## Publisher

Saint Paul Cathedral Parish (the 2020-07-01 merger of St. Paul Cathedral, St. Regis, St. Rosalia and St. Stephen, per the diocese's predecessor list and the St. Regis decree) publishes one weekly bulletin on ParishesOnline container 14/1180. Read 2026-10-23: the 25 October 2026 page 1 is headed "SAINT PAUL CATHEDRAL PARISH / SERVING GREENFIELD • HAZELWOOD • OAKLAND" and lists three worship sites; page 2 gives one Mass-times box and one intentions list. Three LPi orgs (the parish's and the two former-church accounts for St. Rosalia and St. Stephen) list the same issues and resolve to the one container, so they are one bulletin and all their ids are recorded. The LPi ad-page footer reads "St. Paul Cathedral, Pittsburgh, PA 14-1180". One row for the whole parish (Rules settled 3 does not apply: there is no second publisher).

## Worship sites

Three churches have records: Saint Paul Cathedral (Oakland; daily and weekend Masses), Saint Rosalia (Greenfield; Saturday 4pm, Sunday 9am and 12pm Spanish) and Saint Stephen (Hazelwood). The directory lists Saint Stephen as 'No Masses Scheduled' and the 25 October bulletin prints no Mass there, but the 6 September 2026 issue announces the annual dedication-anniversary Mass there on 15 September ('All are welcome'), so by Rules settled 2 it is a church row (occasional public Mass), not an exclusion.

Ruled out: St. Regis Church (3256 Parkview Ave, Oakland), the fourth predecessor parish's church. The bishop's decree of 30 August 2025 closed it for worship effective 29 September 2025 (see excluded/saint-regis-oakland). The parish's own eCatholic site footer lists only two worship sites (Cathedral and St. Rosalia): a lag against the bulletin, which prints three.

Campus Masses: the 25 October 2026 issue prints no Pitt, CMU, Carlow or Duquesne campus Mass (grepped Newman, Oratory, Chapel, Carnegie). Nothing recorded; campus leads go to batch 33 in the manifest.

## Website and bulletin provider

www.ghocatholics.org (the bulletin masthead's own address; the diocese lists www.saintpaulcathedral.org, the same eCatholic site) is behind Cloudflare. It embeds the ParishesOnline org, so the provider is parishes_online with provider_id st-paul-cathedral-parish. The fetch check result is in scratch/map-pittsburgh/scouts/19/manifest.json.

## Not yet confirmed

How often Mass is celebrated at Saint Stephen beyond the annual dedication Mass: only the 6 September 2026 announcement was found in the sampled issues (2025-10-05 to 2026-10-18). Retry when the next September issue appears or if a weekday/occasional Mass is printed.
