---
name: Most Holy Name of Jesus
website: https://www.mostholynameofjesus.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22505']
group: ''
evidence:
- url: https://files.ecatholic.com/22505/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: La Asuncion Church (LA)
  note: 'Page 1 of the 1 November 2026 issue (8 pages, text): ''Sunday, November 1 , 2026 / Domingo, 1
    de noviembre, 2026'', ''Most Holy Name of Jesus Parish'', and the masthead lists three churches: ''La
    Asuncion Church (LA) 777 Cortland Street Parish Office/Oficina Principal'', ''Our Lady of Hungary
    Church (OLH) 697 Cortlandt St'', ''Holy Trinity Church (HT) 315 Lawrie Street''. Page 3 signs the
    pastor''s letter ''Rev. Ron Machado''. Page 7''s schedule: ''7:30am Spanish Mass La Asuncion'', ''9am
    English Mass Holy Trinity'', ''10:30am Spanish Mass La Asuncion'', ''12pm Spanish Mass Holy Trinity'',
    ''1:30pm Spanish Mass La Asuncion'', ''6pm Spanish Mass La Asuncion'', weekday ''7p.m. Spanish Mass
    Our Lady of Hungary''. No St. Mary and no Fatima church is named.'
- url: https://www.mostholynameofjesus.org/bulletins
  seen: 2026-11-03
  quote: November 1, 2026
  note: eCatholic site 22505, loaded with visit.py (probe url said DEAD-DNS, probe get answered 403).
    The 'Bulletins | Boletines' page lists files.ecatholic.com/22505/bulletins/<YYYYMMDD>.pdf weekly,
    newest 20261101.pdf.
- url: https://www.mostholynameofjesus.org/mass-schedule
  seen: 2026-11-03
  quote: 9:00 AM Holy Trinity Church
  note: 'Mass Schedule page (visit.py): Saturday 6:00 PM Spanish La Asuncion; Sunday 7:30 AM, 10:30 AM,
    1:30 PM and 6:00 PM Spanish La Asuncion Church, 9:00 AM Holy Trinity Church, 12:00 PM Spanish Holy
    Trinity Church; Monday-Wednesday 7:00 PM La Asuncion; Thursday and Friday 7:00 PM Our Lady of Hungary;
    Saturday 8:00 AM OLH. Footer: ''Most Holy Name of Jesus Parish 777 Cortlandt St., Perth Amboy, NJ
    08861''.'
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

Most Holy Name of Jesus Parish, Perth Amboy publishes its own weekly bilingual bulletin on its eCatholic site (22505). The 1 November 2026 issue (read 2026-11-03) is headed 'Most Holy Name of Jesus Parish / Parroquia Santo Nombre de Jesus' and lists three churches on page 1: La Asuncion Church (777 Cortland Street, also the parish office), Our Lady of Hungary Church (697 Cortlandt St) and Holy Trinity Church (315 Lawrie Street). The pastor's letter on page 3 is signed 'Rev. Ron Machado'; the parish finder still names Msgr. John B. Gordon as pastor, which I did not follow (the playbook takes the pastor from the masthead).

## Worship sites

Three churches, each with Mass in the 1 November 2026 bulletin (page 7) and on the parish's Mass Schedule page (2026-11-03): La Asuncion (directory:24524's address, gcatholic:18610, worship-sites:most-holy-name-of-jesus-la-asuncion), Holy Trinity (gcatholic:18609, worship-sites:most-holy-name-of-jesus-holy-trinity-church) and Our Lady of Hungary (gcatholic:18611, worship-sites:most-holy-name-of-jesus-our-lady-of-hungary-church). These are exactly GCatholic's three churches for the Parish of the Most Holy Name of Jesus. The finder's Worship Sites line names Holy Trinity and Our Lady of Hungary only, but its own Mass list places Masses at 'La Asuncion', which the bulletin locates at 777 Cortlandt Street.

GCatholic's St. Mary, 104 Center St (gcatholic:18591) is grouped under the Parish of St. John Paul II, and this bulletin does not name it (a grep of the 1 November issue for 'Mary' finds only 'Legion of Mary' and a contributions line); it is left to the St. John Paul II batch. Our Lady of Fatima, 380 Smith St is a separate parish with its own bulletin (our-lady-of-fatima-perth-amboy).

## Website and bulletin provider

Website https://www.mostholynameofjesus.org (finder and bulletin masthead), an eCatholic site (22505) behind a bot check: `probe url` reported DEAD-DNS and `probe get` 403, but visit.py loaded it. GCatholic's website for Holy Trinity, mostholynamejesus.org, does not answer. The Bulletins page links only eCatholic files; no other publisher was found.

## Fetch check

`pnpm fetch:check` on 2026-11-03 picked https://files.ecatholic.com/22505/bulletins/20261101.pdf (the 1 November 2026 issue): transport ok, PDF, issue date 2026-11-01 (inferred), freshness fresh, identity unverified by the tool; I read that issue myself (evidence above).

## Not yet confirmed

Nothing open for this row.
