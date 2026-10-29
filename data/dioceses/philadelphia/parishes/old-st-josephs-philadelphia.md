---
name: Old St. Joseph Parish
website: https://www.oldstjoseph.org
bulletin_provider: ecatholic
provider_id: '37776'
publication: ['ecatholic:37776']
group: Philadelphia South and East
evidence:
- url: https://files.ecatholic.com/37776/bulletins/20261025.pdf
  seen: 2026-10-29
  quote: 'Sunday: 7:30, 9:30, and 11:30 AM / Holy Days: 12:05 PM'
  note: '25 October 2026 issue (6 pages, text layer; md5 7b6ab1b8e393a84d9a6710a209b3eb62): page 1 masthead
    ''Old St. Joseph’s Church Est. 1733 | Philadelphia’s Jesuit Parish, 321 Willings Alley, Philadelphia
    PA 19106, 215-923-1733, www.oldstjoseph.org'', ''October 25, 2026 | The 30th Sunday in Ordinary Time
    (A)''; page 4 ''Mass Times'': Tuesday, Wednesday, Thursday 12:05 PM; Sunday 7:30, 9:30 and 11:30 AM;
    Holy Days 12:05 PM; pastor Fr. Francis Hannafey SJ. Only Old St. Joseph''s is named.'
- url: https://www.oldstjoseph.org/bulletins
  seen: 2026-10-29
  note: Opened with the stealth browser (plain `probe url` gets HTTP 403). The page source links files.ecatholic.com/37776/bulletins/20261025.pdf
    first, then 20261018, 20261011 ... newest first. The home page embeds eCatholic id 37776 and its 'Current
    Bulletin' still pointed at 20261018 (cached), so /bulletins is the fresher listing.
- url: https://archphila.org/parish/old-st-josephs-philadelphia/
  seen: 2026-10-28
  note: 'Directory: Rev. Francis T. Hannafey, S.J.; 4th and Walnut Sts.; rectory 321 Willings Alley 19106;
    Mass ''Sundays: 7:30, 9:30, & 11:30 AM. Holydays: 12:05 PM, Daily: Tuesdays, Wednesdays, & Thursdays,
    12:05 PM.'' (page updated 2 years earlier); same times as the bulletin.'
---

## Publisher

Old St. Joseph Parish (the Jesuit parish in Old City) publishes its own weekly bulletin on its eCatholic site, id 37776: `files.ecatholic.com/37776/bulletins/<yyyymmdd>.pdf`, listed newest first on `/bulletins`. No John Patrick listing for Old St. Joseph's was found among the 19106 listings in the scan (only 62, the cathedral; 167, Old St. Mary; 210, St. Augustine).

**One bulletin or several?** One, for this parish alone. The masthead and the Mass box name Old St. Joseph's only, and the directory names no shared pastor.

## Worship sites

One: Old St. Joseph's Church (`churches/old-st-josephs-philadelphia.md`), a shrine-status church GCatholic lists as 'St. Joseph, Old St. Joseph's Church'.

## Website and bulletin provider

oldstjoseph.org answers HTTP 403 to `probe url` and loads in the stealth browser (`visit.py`).
