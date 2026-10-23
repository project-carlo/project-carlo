---
name: Holy Spirit Parish of Lawrence County
website: https://www.hsplc.org
bulletin_provider: parishes_online
provider_id: holy-spirit-parish-of-lawrence-county
publication: ['po-org:holy-spirit-parish-of-lawrence-county', 'lpi:0018000000Qc1FgAAJ', 'po-container:14/1181',
  'ecatholic:20843', 'po-org:st-vitus-church-16101', 'lpi:0018000000Qx7rfAAB', 'po-org:st-marys-church',
  'lpi:0018000000Qbz5nAAB', 'po-org:st-joseph-the-worker-church-16101', 'lpi:0018000000Qc1VFAAZ', 'po-org:st-vincent-de-paul-church-16102',
  'lpi:0018000000Qx7reAAB']
group: Holy Spirit Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1181/20261025B.pdf
  seen: 2026-10-23
  quote: OF LAWRENCE COUNTY, PENNSYLVANIA
  note: 'Page 1 of the 25 October 2026 issue (container 14/1181, 20 pages, text layer readable): masthead
    ''HOLY SPIRIT PARISH OF LAWRENCE COUNTY, PENNSYLVANIA'', office 910 S. Mercer Street, New Castle,
    724-652-3422, www.hsplc.org. No other parish is named in the masthead.'
- url: https://container.parishesonline.com/bulletins/14/1181/20261025B.pdf
  seen: 2026-10-23
  quote: 7:00am | St. Vitus | People of the Parish
  note: Page 5 'Mass Schedule and Intentions' lists Masses for 24 Oct to 1 Nov at St. Camillus (Sat 4:00pm,
    Sun 11:00am), St. Vitus (Sat 4:00pm, Sun 7:00am and 9:00am) and St. Mary (Sun 8:00am, weekdays 9:00am).
    Page 3 (rendered, the Mass box is partly an image layout) adds 'Sunday Mass ... 7:00pm Westminster
    College (when classes are in session)'; page 1 says the 9:00am daily Mass has moved from St. Vitus
    to St. Mary 'Due to roof construction at St. Vitus Church'.
- url: https://www.hsplc.org/mass
  seen: 2026-10-23
  quote: 7:00 PM Westminster College (when classes are in session)
  note: 'Parish Mass Schedule page (diocese-provided eCatholic site 20843, read in headed Chrome): Saturday
    4:00 PM St. Vitus and St. Camillus; Sunday 7:00 AM and 9:00 AM St. Vitus, 8:00 AM St. Mary, 11:00
    AM St. Camillus, 7:00 PM Westminster College; daily 9:00 AM. No other building is listed.'
- url: https://www.hsplc.org/bulletins-1
  seen: 2026-10-23
  quote: Our Bulletin is published weekly - current and past Bulletins can be found below.
  note: The parish's own Bulletins page embeds the ParishesOnline widget for container 14/1181 (page lists
    issues of 5, 12, 19, 26 Oct 2026 and links organization/holy-spirit-parish-of-lawrence-county); rendered
    by visit.py, which reports lpi:0018000000Qc1FgAAJ, ecatholic:20843 and po-container:14/1181.
- url: https://parishesonline.com/organization/holy-spirit-parish-of-lawrence-county
  seen: 2026-10-23
  note: 'probe po on 2026-10-23: orgs holy-spirit-parish-of-lawrence-county, st-vitus-church-16101, st-marys-church,
    st-joseph-the-worker-church-16101 and st-vincent-de-paul-church-16102 each list the same latest issue
    (2026-10-25) in container 14/1181: one bulletin carried under five org names (old predecessor orgs).
    The orgs holy-trinity-church-16102 (1708 S Jefferson St) and st-john-maronite-church (2 W Reynolds
    St) have no issues and are not this parish''s.'
- url: https://diopitt.org/holy-spirit-new-castle
  seen: 2026-10-23
  quote: On July 1, 2019, the seven parishes were formally merged to create the new Holy Spirit Parish.
  note: 'Diocese parish-history page (read with visit.py; diopitt.org answers 403 to recheck). Also dates
    the closures of St. Lawrence (2020-02-21) and St. Anthony, St. James, St. Joseph the Worker and St.
    Vincent de Paul (2023-10-02): see excluded/ records.'
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

Holy Spirit Parish of Lawrence County (Pastor Rev. Benjamin E. Barr per the diocese page and bulletin) publishes one weekly bulletin through ParishesOnline, container 14/1181. The 25 October 2026 issue (read 2026-10-23) is headed 'Holy Spirit Parish of Lawrence County, Pennsylvania' and prints one Mass schedule and one intentions list for all of the parish's churches. No sibling parish prints in this container. The parish was formed on 2019-07-01 from seven parishes (Christ the King, Bessemer/Hillsville; St. James, Pulaski; Mary, Mother of Hope; St. Joseph the Worker; St. Vincent de Paul; St. Vitus; plus St. Camillus, Neshannock) per the diocese page.

## Worship sites

Three churches, each with Masses in the 25 October bulletin and on hsplc.org/mass: St. Camillus (Neshannock Twp.), St. Mary (New Castle) and St. Vitus (New Castle). A fourth place, the Wallace Memorial Chapel at Westminster College (New Wilmington), has a Sunday 7:00pm Mass printed in the bulletin's schedule (see churches/wallace-memorial-chapel-new-wilmington). Ruled out: five former churches the diocese's parish history says were closed (St. Lawrence, Hillsville, 2020-02-21; St. Anthony, Bessemer; St. James the Apostle, Pulaski; St. Joseph the Worker and St. Vincent de Paul, New Castle, 2023-10-02): none appears in the Mass schedule or intentions of the 25 Oct, 27 Sep, 30 Aug or 5 Jul 2026 issues (grepped for the church names, towns and street names), each has its own record in excluded/. Settled under the diocese rule 2: they are closed on a dated diocese source, not just the directory's silence.

## Website and bulletin provider

hsplc.org is diocese-provided eCatholic (site 20843) behind Cloudflare: `probe url` gets 403, headed Chrome reads it. The Bulletins page embeds the ParishesOnline container, and eCatholic's own bulletin files are not used (issues.py ecatholic:20843 found no files, 403 for 2026-10-25 and 10-18). The row therefore reads ParishesOnline by org slug. Old predecessor orgs (St. Vitus, St. Mary's, St. Joseph the Worker, St. Vincent de Paul) all point at the same container and are recorded in publication.

## Not yet confirmed

The St. Vitus daily Mass is temporarily at St. Mary during roof work (bulletin p. 1, hsplc.org/mass 'until further notice'); weekday Masses are not modelled. The Westminster Mass runs only while classes are in session.
