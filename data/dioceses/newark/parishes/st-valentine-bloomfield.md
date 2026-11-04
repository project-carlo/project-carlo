---
name: St. Valentine, Bloomfield
website: https://www.stvalentinechurch.com/
bulletin_provider: other
provider_id: page-pdfs https://www.stvalentinechurch.com/ filename=*_-_*.pdf
publication: ['url:https://www.stvalentinechurch.com/']
group: Planning Area G
evidence:
- url: https://www.stvalentinechurch.com/uploads/4/9/1/6/4916586/allsaintsday_-_2026.pdf
  seen: 2026-11-03
  quote: CHURCH OF SAINT VALENTINE
  note: '1 November 2026 issue (5 pages, text), file allsaintsday_-_2026.pdf. Page 1 masthead: ''CHURCH
    OF SAINT VALENTINE … 125 North Spring Street Bloomfield, NJ 07003 ALL SAINTS DAY NOVEMBER 1, 2026'';
    Masses Saturday Evening 5:30 pm; Sunday 8:00 am, 10:00 am & 12:00 pm; Monday to Saturday in the Chapel
    12:00 pm; pastor Fr. Andrew N. Onyemaobi. No other church is named; no printer''s code or publisher
    footer (self-produced).'
- url: https://www.stvalentinechurch.com/uploads/4/9/1/6/4916586/oct_25_2026_-_30th_wk__sunday_in_ordinary_time.pdf
  seen: 2026-11-03
  quote: 'Parish Website: ----------- www.stvalentinechurch.com'
  note: '25 October 2026 issue, same masthead and layout: the parish posts one PDF a week.'
- url: https://www.stvalentinechurch.com/
  seen: 2026-11-03
  note: The parish homepage (Weebly, editmysite.com) links the weekly bulletins newest first (allsaintsday_-_2026.pdf,
    oct_25_2026_-_30th_wk__sunday_in_ordinary_time.pdf, oct_18…, oct_11…, oct_04…, sep_20…) and, before
    them in the page, a 'Liturgical Ministry Monthly Schedule' PDF (liturgical_ministers_november_2026_schedule.pdf).
    There is no separate bulletin page.
research:
- method: fetch:check with filename=*_-_*.pdf on the homepage
  url: https://www.stvalentinechurch.com/
  checked: '2026-11-03'
  outcome: found
  next_action: If fetch picks an old issue, read the homepage's newest bulletin file name and change the
    filename glob
  retry_when: A fetch picks an issue older than two weeks
bulletin_status: available
---

## Publisher

The parish produces its own bulletin (no printer's code or publisher footer) and posts it on its Weebly site. I read the 1 November 2026 issue (allsaintsday_-_2026.pdf, 5 pages, text): page 1 reads "CHURCH OF SAINT VALENTINE", "125 North Spring Street Bloomfield, NJ 07003 ALL SAINTS DAY NOVEMBER 1, 2026", pastor Fr. Andrew N. Onyemaobi. The 25 October issue has the same masthead.

## Worship sites

One church, `st-valentine-bloomfield`: the page-1 schedule gives Saturday evening 5:30pm, Sunday 8:00am, 10:00am and 12:00pm, and "Monday to Saturday in the Chapel … 12:00 pm". The chapel is the rectory chapel (page 1: confession "after the 12:00pm mass in the Rectory Chapel"), on the parish's own property, so it is not recorded as a separate place; the Neocatechumenal Eucharist listed "[Chapel]" on page 4 is a community celebration in the same chapel. The directory (11) and GCatholic (18368) list only this church.

## Website and bulletin provider

The directory's http://www.stvalentinechurch.com/ redirects to https. Its homepage lists the weekly bulletin PDFs newest first, after a monthly 'Liturgical Ministry' schedule PDF, so the recipe filters on the file names: `page-pdfs https://www.stvalentinechurch.com/ filename=*_-_*.pdf`. Every bulletin file seen so far has "_-_" in its name (`oct_25_2026_-_30th_wk__sunday_in_ordinary_time.pdf`, `allsaintsday_-_2026.pdf`) and the ministers' schedule does not; the names are typed by hand, so the glob can miss a future issue (see research).

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://www.stvalentinechurch.com/: current` and picked allsaintsday_-_2026.pdf, the 1 November 2026 issue read above. Issue date and freshness `unknown`: the file name carries no full date and the masthead date is in capitals ("NOVEMBER 1, 2026"). Identity `unverified` only because no expected identity is supplied. The recipe is the one in `provider_id`.

## Not yet confirmed

Whether the hand-typed file names keep the "_-_" pattern; see research.
