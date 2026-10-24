---
name: St. Joseph Parish
website: https://stjosephforce.org/weeklybulletin.php
bulletin_provider: other
provider_id: page-pdfs https://stjosephforce.org/weeklybulletin.php
publication: ['url:https://stjosephforce.org/weeklybulletin.php#st-joseph-force']
group: ''
evidence:
- url: https://stjosephforce.org/images/weeklybulletin/3f830e12b64271575839a283e62ce4ee.pdf
  seen: 2026-10-23
  quote: St. Joseph Parish  Force, PA    Bringing Eucharistic Life to Bennetts Valley since 1872
  note: 'Page 1 of the 18 October 2026 bulletin (4 pages; link text ''October 18 2026'', newest on the
    Weekly Bulletin page; the 25 October issue was not yet posted on 2026-10-23). A footer box reads ''ST.
    JOSEPH CHURCH, PO Box 124 Force, PA 15841, Rev. Mark J. Mastrian Pastor, MASS TIMES: Saturday Vigil:
    5:30 pm Sunday: 9:15 am, DAILY MASS: Monday, Tuesday, Thursday, and Friday 8:30 am, HOLY DAYS: 9:00
    am & 7:00 pm''. Names this parish alone.'
- url: https://stjosephforce.org/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted template site. Lists weekly PDFs newest first: October 18 2026, October 11, October
    04, September 27, ... back to August 30 2026 and earlier.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ........................................................................................................
    St. Joseph, Force
  note: 'Clergy PDF (8/7/2026): Mastrian, Rev. Mark J., pastor of St. Joseph, Force, 17764 Bennetts Valley
    Highway; his only assignment.'
- url: https://www.eriercd.org/Parish20607-St-Joseph.html
  seen: 2026-10-23
  note: 'Diocese directory record 20607: St. Joseph Parish, Force; no mission or secondary church.'
promoted: 2026-10-23
research:
- method: probe url on the directory website; weeklybulletin_issues.sh; probe pdf and pdftotext of the
    18 October issue; fetch:check with recipe page-pdfs https://stjosephforce.org/weeklybulletin.php
  url: https://stjosephforce.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: None. fetch:check picked the 18 October 2026 issue (transport ok, PDF, identity matched
    'Joseph'); the issue date has no unambiguous masthead date, so it is read from the link text.
---

## Publisher

St. Joseph, Force publishes its own weekly bulletin on its diocese-hosted site, stjosephforce.org/weeklybulletin.php, one PDF per Sunday. The 18 October 2026 issue (page 1 'St. Joseph Parish Force, PA'; schedule table for 18 to 25 October; Mass Times box naming Rev. Mark J. Mastrian, pastor) is the newest posted on 23 October. It names this parish alone.

## Worship sites

One church, St. Joseph on Bennetts Valley Highway, Force. The diocese directory lists no mission or secondary church, and the bulletin's schedule lists one building's Masses. Fr. Mastrian's only assignment in the clergy PDF is this parish.

## Website and bulletin provider

Provider `other`, recipe `page-pdfs https://stjosephforce.org/weeklybulletin.php`. `fetch:check` picked the 18 October 2026 issue: transport ok, PDF, identity matched, freshness taken from the page's link text (the masthead has no date in the first-page text).

## Not yet confirmed

Nothing outstanding for the bulletin. The 25 October issue was not yet posted on 2026-10-23.
