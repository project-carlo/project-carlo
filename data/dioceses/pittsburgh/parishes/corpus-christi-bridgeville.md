---
name: Corpus Christi Parish (Bridgeville)
website: https://www.corpuschristipgh.org
bulletin_provider: parishes_online
provider_id: corpus-christi-parish-15017
publication: ['po-org:corpus-christi-parish-15017', 'lpi:0018000000Qbz01AAB', 'po-container:14/0673',
  'po-org:st-barbara-parish-15017', 'lpi:0018000000Qx7roAAB', 'ecatholic:21066']
group: Corpus Christi Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/0673/20261025B.pdf
  seen: 2026-10-23
  quote: WEEKEND MASSES
  note: 'Page 1 of the 25 October 2026 issue (container 14/0673, 16 pages, text layer readable): masthead
    ''CORPUS CHRISTI PARISH'', office 212 Station Street, Bridgeville; one Mass schedule box for all three
    churches (Sat 4:00 PM St. Mary, 5:00 PM Holy Child; Sun 8:00 AM Holy Child, 9:00 AM St. Barbara, 10:00
    AM St. Mary, 11:00 AM Holy Child, 5:00 PM St. Barbara) with their three addresses.'
- url: https://container.parishesonline.com/bulletins/14/0673/20261018B.pdf
  seen: 2026-10-23
  quote: OCTOBER 18, 2026
  note: Same masthead and Mass box in the 18 October issue; identical page 1 text to the parish site's
    own copy files.ecatholic.com/21066/bulletins/20261018.pdf (both 16 pages).
- url: https://www.corpuschristipgh.org/bulletins
  seen: 2026-10-23
  quote: Corpus Christi Parish
  note: Rendered in headed Chrome (Cloudflare blocks plain fetches). The eCatholic site 21066 archive
    lists weekly PDFs files.ecatholic.com/21066/bulletins/<yyyymmdd>.pdf, latest 20261018; the ParishesOnline
    container carries the same issue a week earlier.
- url: https://parishesonline.com/organization/corpus-christi-parish-15017
  seen: 2026-10-23
  note: 'probe po: org ''Holy Child Church - Corpus Christi Parish'', 212 Station St, Bridgeville; container
    14/0673, latest issue 2026-10-25. Sibling org st-barbara-parish-15017 (45 Prestley Rd) points at the
    same container.'
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

Corpus Christi Parish (Bridgeville and Cecil; formed from St. Barbara, Holy Child and St. Mary, per the diocese's predecessor list) publishes one weekly bulletin for all three churches. The 25 October 2026 ParishesOnline issue (container 14/0673) is headed "CORPUS CHRISTI PARISH", gives the office at 212 Station Street, Bridgeville, and prints one Mass schedule covering the three churches. Pastor Rev. Dennis P. Yurochko (diocese page and bulletin page 2).

## Worship sites

Three churches, all in the Mass box on page 1 of the 25 Oct issue: Holy Child (212 Station St, Bridgeville), St. Barbara (45 Prestley Rd, Bridgeville), St. Mary (10 St. Mary's Lane, Cecil). The diocese directory lists the same three with the same weekend times. Predecessor list (https://diopitt.org/alphabetical-list-of-current-and-predecessor-parishes) shows no other predecessor church for this parish. The other Corpus Christi in the diocese (McKeesport, listed with no Masses) is a different parish and belongs to another batch.

## Website and bulletin provider

The site www.corpuschristipgh.org is diocese-provided eCatholic (site 21066) behind Cloudflare: `probe url` is blocked, headed Chrome reads it. It hosts the bulletin archive as PDFs at files.ecatholic.com/21066/bulletins/<yyyymmdd>.pdf, and the 18 October file has the same page 1 text as ParishesOnline container 14/0673's 20261018B.pdf, so the two are one bulletin. Row uses ParishesOnline (container 14/0673) because it posts the issue first (25 Oct was live on 23 Oct) and is read by org slug. Three ParishesOnline orgs exist for this parish: corpus-christi-parish-15017 (Holy Child) and st-barbara-parish-15017 both resolve to 14/0673; no org found for St. Mary, Cecil. Publication ids for both orgs are recorded here since they are the same bulletin. The eCatholic fallback is the website's /bulletins page if ParishesOnline ever stops.

## Not yet confirmed

Nothing outstanding for the row. Weekday Masses (Mon-Wed-Fri 7:00 AM St. Barbara, Tue-Thu-Sat 7:00 AM St. Mary, Mon-Fri noon Holy Child) are read from the same box but are not modelled here.
