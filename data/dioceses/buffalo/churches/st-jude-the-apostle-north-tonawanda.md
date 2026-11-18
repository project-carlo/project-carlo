---
parish: tonawanda-catholic
name: St. Jude the Apostle Church
line1: 800 Niagara Falls Boulevard
line2: ''
city: North Tonawanda
state: NY
postal_code: '14120'
latitude: 43.0591875
longitude: -78.8394375
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: true
roster: ['directory:7781', 'gcatholic:17697']
evidence:
- url: https://container.parishesonline.com/bulletins/14/1840/20260920B.pdf
  seen: 2026-09-26
  note: 'This part of the bulletin is an image; OCR reads: ''*5:00 pm First Sunday St. Jude the Apostle
    … First Friday (beginning August) 12:00 pm St. Jude the Apostle''.'
- url: https://www.buffalodiocese.org/parish-finder/
  seen: 2026-09-26
  note: 'Diocesan parish finder (fetched 2026-09-26): ''St. Jude the Apostle [2008]'', 800 Niagara Falls
    Blvd., North Tonawanda; homepage https://stjudetheapostleparish.org/.'
- url: https://gcatholic.org/churches/usa-02/17697
  seen: 2026-09-26
  quote: 800 Niagara Falls Blvd., North Tonawanda, New York 14120-2063
  note: GCatholic's address for the building.
- url: https://container.parishesonline.com/bulletins/14/1840/20261122B.pdf
  seen: 2026-11-17
  note: 'Page 1 is an image (rendered and read): the Mass schedule box still prints "*5:00 pm First Sunday
    St. Jude the Apostle" and "**First Friday 12:00 pm St. Jude the Apostle", and the Worship Sites box
    lists "St. Jude the Apostle Church, 800 Niagara Falls Blvd., North Tonawanda". Page 2 reports St. Jude''s
    collection for the month to 8 November. The 25 October issue (page 7) lists "St. Jude the Apostle Sunday,
    Nov 1 at 5:00 pm" for All Souls intentions.'
- url: https://container.parishesonline.com/bulletins/14/1840/20250504B.pdf
  seen: 2026-11-17
  quote: this weekend is the final Mass at St. Jude the Apostle in North Tonawanda.
  note: Pastor's letter, 4 May 2025. The church's regular Masses ended with the 12:00 noon Mass of Thanksgiving
    that day, when St. Jude the Apostle Parish was to merge into St. Christopher.
- url: https://container.parishesonline.com/bulletins/14/1840/20251005B.pdf
  seen: 2026-11-17
  quote: St. Jude the Apostle Parish remains in limbo as we await further instruction from the Vatican.
  note: Pastor's report, 5 October 2025. The merger was under appeal in Rome.
- url: https://container.parishesonline.com/bulletins/14/1840/20260628B.pdf
  seen: 2026-11-17
  note: 'Page 1 is an image (rendered and read): the first issue whose Mass schedule has "*5:00 pm First
    Sunday St. Jude the Apostle" and "**First Friday (beginning August) 12:00 pm St. Jude the Apostle".
    The 7, 14 and 21 June 2026 issues have no Mass at St. Jude. Page 2 also gives "5:00pm St. Jude the
    Apostle" in the adjusted schedule for the 2 August 2026 Family Reunion.'
- url: https://en.wikipedia.org/wiki/List_of_churches_in_the_Diocese_of_Buffalo
  seen: 2026-11-17
  quote: St. Jude the Apostle was merged into St. Christopher Parish in Tonawanda and held its last mass
    in 2025.
  note: Wikipedia's St. Albert the Great row, North Tonawanda. Out of date; the bulletins above show monthly
    Masses here again from July 2026.
promoted: 2026-09-26
---

## Holds Mass

The Roman Catholic Community of the Tonawandas bulletin lists Mass here: a First Sunday Mass at 5:00 p.m. and a First Friday Mass at 12:00 noon. The 22 November 2026 issue still prints both and lists the church among the family's worship sites.

## History of the closure question

Checked on 17 November 2026 because the bulletin of 13 April 2025 announced "the final Mass on Sunday, May 4th at 12:00 noon" here, and Wikipedia says St. Jude "held its last mass in 2025". Both are true of 2025 but no longer current:

- **4 May 2025**: the parish's regular Masses ended ("this weekend is the final Mass at St. Jude the Apostle in North Tonawanda"), ahead of its merger into St. Christopher.
- **October 2025**: the merger was appealed; the pastor wrote that the parish "remains in limbo as we await further instruction from the Vatican".
- **28 June 2026**: the bulletin's schedule first adds the First Sunday 5:00 p.m. Mass and the First Friday 12:00 p.m. Mass "(beginning August)". They are absent from the 7, 14 and 21 June issues.
- **6 August 2026**: local news (WKBW, Niagara Gazette) reported a decree merging St. Jude into St. Christopher. The monthly Masses continued after it, and the church is still a worship site of the family.

So the church stays live with the two monthly Masses, which is what the seed has (`data/seeds/tonawanda-catholic.json`, weeks-of-month slots). If the bulletin drops them, close the church with the last dated Mass.

## Name and address

Name and address come from PR 14's row. On the house number, the modelled address agrees with GCatholic, the diocesan parish finder. Coordinates are from GCatholic's Plus Code, decoded.
