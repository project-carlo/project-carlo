---
name: The Catholic Community of Hopewell Valley
website: https://thecatholiccommunityofhopewellvalley.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-catholic-community-of-hopewell-valley-hopewell-nj-08525
publication: ['url:https://www.church-bulletin.org/the-catholic-community-of-hopewell-valley-hopewell-nj-08525',
  'ecatholic:22670']
group: Cohort 8 (Catholic Community of Hopewell Valley)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-catholic-community-of-hopewell-valley-hopewell-nj-08525/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (Solemnity of All Saints), image-only (probe pdf: no extractable
    text; md5 93e32e254591af4c3108e932b6f52393); read from renders of pages 1-4. Page 1 masthead: "THE
    CATHOLIC COMMUNITY OF HOPEWELL VALLEY", tagline "THREE PARISH FAMILIES; ONE FAITH COMMUNITY", thecatholiccommunityofhopewellvalley.org,
    with the addresses of St. Alphonsus Parish (54 E. Prospect Street, Hopewell), St. George Parish (1370
    River Road, Titusville), St. James Parish (115 E. Delaware Avenue, Pennington) and St. James Chapel
    (6 Eglantine Avenue, Pennington). Page 2 directory: one pastor, Fr. Stephen Sansevere ("Pastor of
    St. Alphonsus in Hopewell, St. George in Titusville, and St. James in Pennington"), one parochial
    vicar and shared deacons and staff, with a parish office line for each. Page 4 gives each church its
    own Mass times and Mass intentions.'
- url: https://www.church-bulletin.org/bulletin/the-catholic-community-of-hopewell-valley-hopewell-nj-08525/2026-10-25.pdf
  seen: 2026-10-30
  note: The listing's 25 October 2026 issue (12 pages, image-only, md5 062e0b0403bc4451622087c675b82562)
    is byte-identical to the same Sunday's file on the community's own eCatholic site, https://files.ecatholic.com/22670/bulletins/20261025.pdf.
    The listing already carries 1 November; the eCatholic Bulletins page ended at 20261025 when read.
- url: https://stjamespennington.org/mass-and-confession
  seen: 2026-10-30
  quote: Weekday Mass (Mondays, Tuesdays, Thursdays, Fridays), 9:00am Chapel
  note: 'One eCatholic site (id 22670) answers on the three parishes'' own domains: stalphonsushopewell.org,
    stgeorgetitusville.org and stjamespennington.org all return the title "The Catholic Community of Hopewell
    Valley - NJ", link jppc.net/onlinebulletins/547template.pdf (listing 547) and carry ecatholic:22670
    (probe url, 2026-10-30). Its Mass & Confession page lists all three churches with their addresses.'
promoted: 2026-10-30
research:
- method: 'pnpm fetch:check --diocese trenton --parish catholic-community-of-hopewell-valley (headed Chrome):
    picked .../2026-11-01.pdf, transport ok, document_type pdf, freshness future (the coming Sunday, posted
    early), identity unverified by the tool because the issue is image-only; identity and parish were
    read from renders of pages 1-4 instead.'
  url: https://www.church-bulletin.org/the-catholic-community-of-hopewell-valley-hopewell-nj-08525
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
---

## Publisher

One bulletin serves all three canonical parishes. John Patrick Publishing's listing 547, "The Catholic Community of Hopewell Valley" (Hopewell, NJ 08525), posts dated PDFs on church-bulletin.org. The newest, 1 November 2026, is a 12-page image-only issue (read from renders of pages 1-4). Its masthead is the community's name and the line "Three parish families; one faith community", not any one parish, and gives the addresses of St. Alphonsus, St. George and St. James (see `evidence`). The page 2 directory has one pastor, Fr. Stephen Sansevere, "Pastor of St. Alphonsus in Hopewell, St. George in Titusville, and St. James in Pennington", one parochial vicar and shared deacons and staff. Page 4 gives each church its own Mass times and intentions, so this is one row with three churches, the rule for a current masthead that names parishes together (see `diocese.md`, *Rules settled*).

## Structure

The 2017 *Faith in Our Future* decisions linked St. James, St. Alphonsus and St. George under one pastor (Linkage Model) and the July 2024 cohort list puts them in Cohort 8 ("Cath Community of Hopewell Valley"); neither says one bulletin. The masthead above does. The three canonical parishes are kept as the three churches' homes; no merger is claimed.

## Website and bulletin provider

The directory's three sites (stalphonsushopewell.org, stgeorgetitusville.org, stjamespennington.org) are one eCatholic site (id 22670) under three domains, as is thecatholiccommunityofhopewellvalley.org, the domain printed on the masthead; the row uses the masthead's. Its `/bulletins` page lists `files.ecatholic.com/22670/bulletins/<yyyymmdd>.pdf` and was one issue behind (25 October) when read, while the listing had 1 November, so the row reads the listing (`other`, `page-pdfs`) and keeps `ecatholic:22670` in `publication`. The 25 October issue is byte-identical on both channels.

## Worship sites

Three churches and a chapel: St. Alphonsus (Hopewell), St. George (Titusville), St. James (Pennington) and St. James Chapel; see `st-alphonsus-hopewell`, `st-george-titusville`, `st-james-pennington`, `st-james-chapel-pennington`. The masthead also names "St. James Chapel, 6 Eglantine Avenue, Pennington", where St. James's weekday Masses are said; reconcile (2026-10-30) gave it a church row, `st-james-chapel-pennington`, under the settled chapel rule.
