---
name: St. Hippolyte Parish
website: https://sainthippolytechurch.com
bulletin_provider: other
provider_id: page-pdfs https://sainthippolytechurch.com/weeklybulletin.php
publication: ['url:https://sainthippolytechurch.com/weeklybulletin.php#st-hippolyte-guys-mills']
group: Partnered under Rev. Jeffrey J. Lucas with The Epiphany of the Lord, Meadville (decree effective
  2023-08-07)
evidence:
- url: https://sainthippolytechurch.com/images/weeklybulletin/6f51b501b29d9690cd73dac174dda7ad.pdf
  seen: 2026-10-23
  quote: IT IS THE MISSION OF SAINT HIPPOLYTE AND OUR LADY OF LOURDES TO FULLY, CONSCIOUSLY, AND
  note: 'Issue ''October 4, 2026'' (Twenty Seventh Sunday in Ordinary Time), 2 pages, Microsoft Publisher,
    md5 4c2f6f8ccbf4bac8e10b91fc352b6599. Masthead names SAINT HIPPOLYTE CHURCH (26012 N. Frenchtown Rd.,
    Guys Mills; ''Sunday 11:00 am - Mass''; ''Monday 8:30am - Adoration and Rosary'') and OUR LADY OF
    LOURDES CHURCH (251 S. Franklin St., Cochranton; ''Friday 8:30am - Adoration and Rosary''); pastor
    Rev. Jeffrey J. Lucas, parochial vicar Rev. Kyle Seyler; parish office 25997 State Highway 27, Guys
    Mills, 814-789-2022. Weekly liturgy schedule: ''8:30am SH Adoration and Rosary'' Monday, ''8:30am
    OLL Adoration and Rosary'' Friday, ''Sunday October 11 ... 11:00am SH''.'
- url: https://sainthippolytechurch.com/images/weeklybulletin/6f51b501b29d9690cd73dac174dda7ad.pdf
  seen: 2026-10-23
  quote: and The Epiphany of the Lord parish bulletin at
  note: 'Page 1 of the same issue: ''Read our parish bulletin online at www.sainthippolytechurch.com and
    The Epiphany of the Lord parish bulletin at www.epiphanymeadville.org''. The two parishes name their
    bulletins as separate documents.'
- url: https://sainthippolytechurch.com/weeklybulletin.php
  seen: 2026-10-23
  note: weeklybulletin_issues.sh lists one PDF per issue, newest 'bulletin for October 4, 2026', then
    Sept 27, 20, 13, 6, August 30 ... back to July 2024 (116 entries). The 11 and 18 October issues were
    not posted on 2026-10-23, so the page lags the current Sunday by two issues (and the 25 October issue
    is not yet due on the page).
- url: https://www.eriercd.org/Parish31006-St-Hippolyte.html
  seen: 2026-10-23
  note: 'Directory record 31006: Sunday 11:00 a.m., Monday 8:30 a.m. Adoration and Rosary, holy day 6
    p.m.; ''Partnered with The Epiphany of the Lord, Meadville''.'
- url: https://www.eriercd.org/images/sections/bishop/pdf/Decree%20partnering%20Epiphany%20and%20St.%20Hippolyte%20Parishes%20and%20altering%20the%20status%20of%20Our%20Lady%20of%20Lourdes%20church.pdf
  seen: 2026-10-23
  quote: St. Hippolyte Parish, Frenchtown, is to be partnered with The Epiphany of the Lord Parish, Meadville
  note: Decree dated 14 July 2023, effective 7 August 2023.
research:
- method: pnpm fetch:check --diocese erie --parish st-hippolyte-guys-mills --expected-identity Hippolyte
    (headed Chrome); recipe is the provider_id (page-pdfs on weeklybulletin.php, first-listed)
  url: https://sainthippolytechurch.com/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for the recipe: it picks the first-listed ''bulletin for October 4, 2026'' PDF, transport
    ok, PDF, identity matched (''Hippolyte'' in first-page text). Issue date reads ''unknown'' (the masthead
    date is split by the layout; the link title gives 2026-10-04) and the page lags the current Sunday
    by two issues (11 and 18 October missing on 2026-10-23), so freshness is unverified.'
  retry_when: 'Recheck freshness after the next fetch run: the 11 October and later issues should be posted
    if the page is kept current'
  revisit_after: 2026-11-13
publication_reviews:
- parish: the-epiphany-of-the-lord-meadville
  decision: separate
  evidence:
  - url: https://sainthippolytechurch.com/images/weeklybulletin/6f51b501b29d9690cd73dac174dda7ad.pdf
    seen: 2026-10-23
    note: St. Hippolyte's 4 October 2026 issue is a 2-page Publisher document (md5 4c2f6f8c...) with its
      own masthead for St. Hippolyte and Our Lady of Lourdes and its own Mass schedule; the Epiphany's
      4 October issue (container 14/1183, md5 c4f13b7c...) is an 8-page LPi bulletin. Page 1 tells readers
      to read The Epiphany of the Lord bulletin at epiphanymeadville.org as a separate document.
---

## Publisher

St. Hippolyte Parish (Frenchtown, mailing Guys Mills) posts its own weekly bulletin on its diocese-hosted site, `sainthippolytechurch.com/weeklybulletin.php`: a two-page Publisher document with the masthead of St. Hippolyte Church and Our Lady of Lourdes Church, Cochranton. It is not the Epiphany's bulletin. Compared on 2026-10-23: the 4 October 2026 issue from each (St. Hippolyte md5 4c2f6f8c..., 2 pages; Epiphany container 14/1183 md5 c4f13b7c..., 8 pages) differ in size, layout, masthead and Mass listing, and the St. Hippolyte issue tells readers to read The Epiphany of the Lord bulletin separately. Same pastor (Rev. Jeffrey J. Lucas) and same vicar, so the two parishes are one partnership but two bulletins: two rows (Settled rule: partnership doesn't make a shared bulletin).

## Worship sites

St. Hippolyte, 26012 N. Frenchtown Rd., Guys Mills (Sunday 11:00 am Mass; Monday 8:30 am Adoration and Rosary). Our Lady of Lourdes, Cochranton is a secondary church without mission status (decree effective 2023-08-07: no Sunday or holy-day Masses; Mass on the solemnity of its title); the bulletin lists only 'Friday 8:30am OLL Adoration and Rosary', not Mass, so it is an `open/` question, not a church row (open/our-lady-of-lourdes-cochranton).

## Website and bulletin provider

Diocese-hosted `weeklybulletin.php` template (see diocese.md), read as `page-pdfs`. The directory and GCatholic give `https://www.sainthippolytechurch.com`, whose certificate does not match the `www.` host (probe url: SSLCertVerificationError), so the bare host `https://sainthippolytechurch.com` is the working website; `http://www...` redirects to it.

## Not yet confirmed

The page runs two issues behind (newest 4 October on 2026-10-23); see research for the fetch check.
