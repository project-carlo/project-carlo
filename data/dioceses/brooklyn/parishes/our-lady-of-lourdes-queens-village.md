---
name: Our Lady of Lourdes (Queens Village)
website: https://www.ourladyoflourdesqvny.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://www.ourladyoflourdesqvny.org/bulletin/
publication: []
group: Deanery Q7 (Queens East)
evidence:
- url: http://www.ourladyoflourdesqvny.org/wp-content/uploads/2022/04/ollQnsVil11-1.pdf
  seen: 2026-11-06
  note: '1 November 2026 issue (12 pages). Page 1 is an image (read with render.py): masthead ''Our Lady
    of Lourdes Parish'', 92-96 220th Street, Queens Village, New York 11428, www.ourladyoflourdesqvny.org,
    Rev. Josephjude C. Gannon, Pastor; ''Sunday Masses - Main Church: Saturday 5:00 PM; Sunday 7:30 AM,
    9:00 AM Spanish, 11:30 AM''; weekday Masses Monday-Friday 7:30 AM, Monday-Saturday 9:00 AM; Filipino,
    Haitian and Portuguese monthly Masses.'
- url: http://www.ourladyoflourdesqvny.org/wp-content/uploads/2022/04/ollQnsVil11-1.pdf
  seen: 2026-11-06
  quote: M A S S E ST H I SW E E K November 1, 2026
  note: 'Page 2 text: the week''s Mass intentions, Sunday 1 November to Saturday 7 November 2026.'
- url: https://www.ourladyoflourdesqvny.org/bulletin/
  seen: 2026-11-06
  note: WordPress bulletin page with a dFlip flipbook whose inline script source is the fixed file wp-content/uploads/2022/04/ollQnsVil11-1.pdf,
    replaced each week (it held the 1 November 2026 issue on 2026-11-06).
bulletin_status: available
---

## Publisher

Our Lady of Lourdes publishes its own weekly bulletin; no LPi footer or publisher name appears in it. The site's bulletin page (`https://www.ourladyoflourdesqvny.org/bulletin/`) shows it in a dFlip flipbook whose source is one fixed file, `wp-content/uploads/2022/04/ollQnsVil11-1.pdf`, overwritten each week. Read 2026-11-06, that file was the 1 November 2026 issue (12 pages): page 1 (an image, drawn with render.py) has the masthead "Our Lady of Lourdes Parish", 92-96 220th Street, Queens Village, New York 11428, with Rev. Josephjude C. Gannon as pastor; page 2 is headed "MASSES THIS WEEK November 1, 2026".

## Worship sites

One church. Page 1 lists "Sunday Masses - Main Church" (Saturday 5:00 PM; Sunday 7:30 AM, 9:00 AM Spanish, 11:30 AM) and weekday Masses, all at the parish; page 2's "6:00 p.m. Filipino Mass - Chapel" and page 5's "Bethsaida Chapel" are a chapel at the parish, not a separate address. The diocese directory, the deanery list (Q7), GCatholic 16638 and Mass finder 1133 list this one church. The Mass finder's "Our Lady Of Lourdes Chapel" (massfinder:579, 89 Furman Ave., Brooklyn) is a different place in Bushwick, not this parish's.

## Website and bulletin provider

`other`, pinned `page-pdfs https://www.ourladyoflourdesqvny.org/bulletin/` (page-pdfs reads the file address from the flipbook's markup). Unpinned, `fetch:check` (2026-11-06) failed with "No bulletin page link found for other provider"; `linked-issue-page` found no PDF. With the page-pdfs recipe it picked `ollQnsVil11-1.pdf`, issue date inferred 2026-11-01 (freshness `fresh`, 5 days), which is the 1 November 2026 issue read above. The file name never changes, so a week the parish fails to replace it would still be picked; the date check is what catches that. Page 1 is image-only ("First page has no extractable text"), so the Mass schedule there has to be read as an image; page 2's weekly intentions are text.

## Not yet confirmed

Nothing affecting the row.
