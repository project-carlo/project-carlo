---
name: St. Rose of Lima Parish
website: https://strosenj.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-rose-of-lima-roman-catholic-church-haddon-heights-nj-08035
publication: ['ecatholic:35649', 'url:https://www.church-bulletin.org/saint-rose-of-lima-roman-catholic-church-haddon-heights-nj-08035#john-patrick-646']
group: ''
evidence:
- url: https://files.ecatholic.com/35649/bulletins/20261025.pdf
  seen: 2026-10-29
  quote: 300 KINGS HIGHWAY, HADDON HEIGHTS, NEW JERSEY 08035
  note: 'Page 1 of the 25 October 2026 issue (12 pages, text layer): ''SAINT ROSE OF LIMA ROMAN CATHOLIC
    CHURCH''; Saturday vigil 5:30 pm; Sunday 8:00am, 9:30am, 11:00am, 5:30pm (no Sunday 5:30pm from Memorial
    Day to Labor Day); weekdays Mon-Fri 6:30am and 8:30am (CHAPEL), Saturday 8:30am (CHURCH). Page 3 calendar
    and page 10 Mass intentions name Church and Chapel only. A grep for Sacred Heart, Maternity, Francis,
    Ephraim, Barrington and Audubon finds no church or Mass there (Mount Ephraim and Audubon appear only
    in a parish-area line and advertisements). The page 11 footer prints ''John Patrick Publishing Company''
    code 646.'
- url: https://strosenj.org/bulletins
  seen: 2026-10-29
  note: 'probe url: eCatholic site 35649; lists files.ecatholic.com/35649/bulletins/ PDFs weekly, newest
    20261025, then 20261018 and 20261011.'
- url: https://strosenj.org/
  seen: 2026-10-29
  quote: Mon Fri
  note: 'Home page Mass Times: Saturday 5:30 PM; Sunday 8:00, 9:30, 11:00 AM and 5:30 PM; Monday-Friday
    6:30 AM (Chapel) and 8:30 AM (Church); Saturday 8:30 AM (Church); address 300 Kings Highway Suite
    B, Haddon Heights. No other church. The directory''s strosenj.com redirects here; Its Staff page lists
    Fr. Dave Grover, Pastor, and Fr. Francis Kim and Rev. Joseph Cuong M. Pham, Parochial Vicars.'
- url: https://www.church-bulletin.org/saint-rose-of-lima-roman-catholic-church-haddon-heights-nj-08035
  seen: 2026-10-29
  note: The John Patrick listing for code 646 carries the same issues weekly (2026-11-01 posted ahead,
    then 2026-10-25 and 2026-10-18). The parish's own eCatholic copy is the same printed bulletin and
    is on the parish's site, so the eCatholic id is recorded; the listing is a fallback if the eCatholic
    copy lags.
research:
- method: fetch:check --diocese camden --parish st-rose-of-lima-haddon-heights (recipe page-pdfs on the
    John Patrick listing)
  url: https://www.church-bulletin.org/saint-rose-of-lima-roman-catholic-church-haddon-heights-nj-08035
  checked: '2026-10-29'
  outcome: found
  next_action: 'None: picked bulletin/.../2026-11-01.pdf (transport ok, PDF, issue date observed 2026-11-01,
    freshness future: posted before its Sunday); its page 1 masthead names Saint Rose of Lima Roman Catholic
    Church, 300 Kings Highway, Haddon Heights.'
---

## Publisher

St. Rose of Lima Parish publishes its own weekly bulletin, printed by John Patrick Publishing (code 646; the page 11 footer says so) and posted both on the printer's church-bulletin.org listing and on the parish's eCatholic site (id 35649; /bulletins lists files.ecatholic.com/35649/bulletins/ PDFs). The 25 October 2026 eCatholic issue (read 2026-10-29) is headed 'SAINT ROSE OF LIMA ROMAN CATHOLIC CHURCH, 300 Kings Highway, Haddon Heights' and names this parish alone; the listing's 1 November 2026 issue (read 2026-10-29, text layer) has the same masthead, address and Mass schedule. It is not shared with St. Mary, Gloucester City (John Patrick 6049) or St. Joachim, Bellmawr, which publish separately.

## Worship sites

The Haddon Heights church (`st-rose-of-lima-haddon-heights`), with its chapel on the same campus, holds the weekly Masses in the bulletin and on the home page. The 2014 consolidation (Catholic Star Herald and camdendiocese.org, 2014-05-08, effective 2014-06-30) joined the Emmaus Catholic Community of Mount Ephraim (Sacred Heart and Holy Maternity, Audubon) and the parishioners of St. Francis de Sales, Barrington to this parish. Of those three churches:

- `st-francis-de-sales-barrington` is a church of the parish with a monthly Mass (the Igbo Catholic Apostolate, third Sunday at noon; Catholic Star Herald, 2026-07-23, which calls it 'Saint Rose of Lima Parish's Saint Francis de Sales Church'). The weekly bulletin doesn't list it.
- `open/sacred-heart-mount-ephraim` and `open/holy-maternity-audubon` are undecided: the bulletin and the parish site name no Mass there, and no source read says either closed.

GCatholic still groups them under the pre-2014 'Community of Emmaus' (and Barrington under 'St. Rita of Cascia Parish').

## Website and bulletin provider

`other`, `page-pdfs https://www.church-bulletin.org/saint-rose-of-lima-roman-catholic-church-haddon-heights-nj-08035` (reconcile, 2026-10-29). The row was first on the eCatholic copy (`ecatholic`, strosenj.org; the directory's strosenj.com redirects to it), whose `fetch:check` pick on 2026-10-29 was 20261025.pdf, while the listing already carried 2026-11-01 (posted ahead). It is the same printed bulletin a week later, not a different one, so reconcile moved the row to the listing, as the playbook prefers for a parish copy that runs behind the printer's (Notre Dame de la Mer, Holy Child) and for the listing's uniform dated file names; `ecatholic:35649` stays in `publication` as another form of the same bulletin, and the eCatholic site is the fallback if the listing stops. `fetch:check` on the listing recipe: see research.

## Not yet confirmed

The pastor is Rev. David A. Grover (second six-year term from 2026-07-01, Catholic Star Herald 2026-05-02; the parish's Staff page). The directory's 'Rev. David Grover' is current. Nothing else open for this row.
