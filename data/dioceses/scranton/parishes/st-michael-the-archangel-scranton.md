---
name: St. Michael the Archangel Parish (FSSP)
website: https://fsspscranton.wordpress.com
bulletin_provider: other
provider_id: page-pdfs https://fsspscranton.wordpress.com/sunday-bulletin/
publication: ['url:https://fsspscranton.wordpress.com/sunday-bulletin/']
group: Saint Michael the Archangel Parish
evidence:
- url: https://fsspscranton.wordpress.com/wp-content/uploads/2026/10/bulletin_october_11_2026.pdf
  seen: 2026-10-16
  quote: St. Michael the Archangel Roman Catholic Parish At St. Lucy’s Church 949 Scranton, St. Scranton,
    PA 18504
  note: 'Page 1 (masthead) of the 11 October 2026 issue: "THE PRIESTLY FRATERNITY OF ST. PETER", pastor
    Rev. Edgar Ramirez, FSSP. Page 2 lists the week''s Mass intentions: Sunday 8:00 AM & 10:30 AM, Monday-Thursday
    7:30 AM, Friday 6:00 PM, Saturday 9:00 AM.'
- url: https://fsspscranton.wordpress.com/sunday-bulletin/
  seen: 2026-10-16
  quote: 'Most Recent Issue Pictured: Sunday, October 11, 2026 See below for archived Bulletins'
  note: The parish's Bulletins page, with each week's PDF in wp-content/uploads (bulletin_october_11_2026.pdf,
    bulletin_october_4_2026.pdf, ...) and archives back to 2021.
- url: https://fsspscranton.wordpress.com/mass-devotions/
  seen: 2026-10-16
  quote: 'Mass Times: Sunday: 8:00 am (Low), 10:30 am (High) Monday – Thursday: 7:30 am Friday: 6:00 pm
    Saturday: 9:00 am'
---

## Publisher

St. Michael the Archangel Parish, the diocese's personal parish for the Traditional Latin
Mass, entrusted to the Priestly Fraternity of St. Peter, publishes its own weekly bulletin as
a PDF on its WordPress site. The 11 October 2026 issue (the newest on 16 October) has the
masthead "St. Michael the Archangel Roman Catholic Parish At St. Lucy’s Church, 949 Scranton
St." and lists the week's Masses (Sunday 8 and 10:30 am, Monday-Thursday 7:30 am, Friday
6 pm, Saturday 9 am). No other parish shares it.

## Worship sites

One: St. Lucy's Church, 949 Scranton Street (`st-lucy-scranton`), the finder's only worship
site for this parish. The parish's former church, St. Michael's at 1703 Jackson Street (still
in GCatholic), had its last Mass on 28 September 2025, when the parish moved to St. Lucy's; it is
`excluded/st-michael-scranton.md`.

## Website and bulletin provider

The finder's website, saintmichaelsrcc.org, redirects to fsspscranton.wordpress.com, and the
bulletin's own address, fsspscranton.org, redirects there too (`curl -I`, 2026-10-16). The
WordPress site is used as `website`. Its "Bulletins" page (/sunday-bulletin/) links every
issue as a PDF named by date (`wp-content/uploads/<YYYY>/<MM>/bulletin_<month>_<d>_<yyyy>.pdf`),
so the row is `other` with the recipe `page-pdfs https://fsspscranton.wordpress.com/sunday-bulletin/`,
written by hand (`fetch:check` reads only promoted rows). The PDF has a text layer.

## Not yet confirmed

Whether `fetch:check` picks the newest issue from the dated file names after promotion.
