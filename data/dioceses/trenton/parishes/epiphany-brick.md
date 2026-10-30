---
name: Church of Epiphany
website: https://churchofepiphanynj.org/
bulletin_provider: no_bulletin
provider_id: page-pdfs https://churchofepiphanynj.org/index.php/sunday-bulletins filename=bulletin*.pdf
publication: ['url:https://churchofepiphanynj.org/index.php/sunday-bulletins#epiphany']
group: Cohort 20 (Point Pleasant, Brick)
evidence:
- url: https://churchofepiphanynj.org/images/pdf/bulletin/2026/bulletin102526.pdf
  seen: 2026-10-30
  quote: 615 Thiele Road  ~  Brick,  New Jersey  08724
  note: 'Page 1 of the 25 October 2026 issue (12 pages, text layer on 8): ''The Church of Epiphany ROMAN
    CATHOLIC CHURCH'', ''REV. MICHAEL SANTANGELO ---- Pastor'', Masses ''Saturday Vigil 4:00 pm; Sunday
    8:00 am & 10:30 am''; page 2 lists daily Mass 9:00 AM Monday-Saturday. It names Epiphany alone.'
- url: https://churchofepiphanynj.org/images/pdf/bulletin/2026/bulletin110126.pdf
  seen: 2026-10-30
  quote: REV. MICHAEL SANTANGELO ---------------------------Pastor
  note: 'Page 2 of the 1 November 2026 issue (12 pages; the cover, page 1, is a Bon Venture design: ''©2012
    Bon Venture Services, LLC The Church Of Epiphany Brick Township, New Jersey''). Same staff and Mass
    schedule. The issue is on the server, but the Sunday Bulletins page did not yet list it on 2026-10-30.'
- url: https://churchofepiphanynj.org/index.php/sunday-bulletins
  seen: 2026-10-30
  quote: October 25 - 30th Sunday in Ordinary Time
  note: 'Joomla weblinks list, 2025 and 2026 issues in date order, oldest first; the newest entry on 2026-10-30
    is 25 October. Each entry is a weblink.go redirect: entry 252 answers 301 to http://www.churchofepiphanynj.org/images/pdf/bulletin/2026/bulletin102526.pdf.'
revisit: 'Restore bulletin_provider to other with a working recipe once a collector follows Joomla weblink.go
  redirects (owner decision 2026-10-30: add the collector, keep the row off the live CSVs until then).'
revisit_after: 2026-12-01
research:
- method: pnpm fetch:check --diocese trenton --parish epiphany-brick (headed Chrome), unpinned
  url: https://churchofepiphanynj.org/index.php/sunday-bulletins
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Add a collector for Joomla weblinks lists (each entry is a task=weblink.go link that answers
    301 to /images/pdf/bulletin/<yyyy>/bulletin<mmddyy>.pdf), or have the owner decide how to carry this
    row.
  retry_when: A collector that follows weblink.go redirects exists, or Epiphany links its PDFs directly
- method: fetch:check with recipes page-pdfs (filename=bulletin*.pdf), dated-post, linked-issue-page and
    redirected-pdf on the Sunday Bulletins page
  url: https://churchofepiphanynj.org/index.php/sunday-bulletins
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: None of the four recipes resolves a bulletin (resolve_failed); the unpinned pick is /images/pdf/ministers.pdf
    (a staff list, not a bulletin). Do not promote with the unpinned recipe.
  retry_when: A weblinks collector exists
- method: 'tools/epiphany_latest.sh: last weblink.go href on the page, curl -I for its Location'
  url: https://churchofepiphanynj.org/index.php/component/weblinks/weblink/252-october-25-30th-sunday-in-ordinary-time?catid=20&Itemid=101&task=weblink.go
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: this reads the current bulletin by hand (25 October 2026); the homepage''s only
    PDF link is ministers.pdf, so there is no direct current-bulletin link.'
bulletin_status: unsupported-format
---

## Publisher

The Church of Epiphany, Brick publishes its own weekly bulletin on its Joomla site, https://churchofepiphanynj.org (the directory's and GCatholic's churchofepiphany.org redirects there). Masthead of the 25 October 2026 issue (page 1) and of the 1 November issue (page 2): The Church of Epiphany, 615 Thiele Road, Brick; Rev. Michael Santangelo, pastor; Saturday vigil 4:00 pm, Sunday 8:00 am and 10:30 am; daily Mass 9:00 am. No other parish is named. Bon Venture's copyright on the 1 November cover shows the printer, not a shared account; the John Patrick listing 584 ('Epiphany Church', Brick 08724) has no edition and is dead.

## Worship sites

One: Church of Epiphany, 615 Thiele Road (see `epiphany-brick`). The 2017 *Faith in Our Future* decisions put Epiphany's status under review by 2018; the 2024 cohort list and the current bulletin show it still a parish with its own pastor and schedule. No other building appears in either issue's Mass schedule.

## Website and bulletin provider

The bulletin is real and current, but the current resolver can't collect it, so the row is `no_bulletin` for now: the records keep it, `promote` leaves it off the live CSVs (README, Settled policy 4), and this is not a claim that Epiphany publishes no bulletin. The Sunday Bulletins page is a Joomla weblinks list, oldest first: each entry is a `task=weblink.go` link that redirects (301) to `/images/pdf/bulletin/<yyyy>/bulletin<mmddyy>.pdf`, so the page contains no PDF href. `fetch:check` unpinned picks `/images/pdf/ministers.pdf?refresh=yes` (a staff list) as 'first-listed'; the recipes `page-pdfs` (with `filename=bulletin*.pdf`), `dated-post`, `linked-issue-page` and `redirected-pdf` all fail to resolve. The list lags the server by a week: the 1 November issue (bulletin110126.pdf) is on the server while the page's newest entry is 25 October.

## Owner decision and what remains

The owner answered (2026-10-30): add a collector that follows weblink.go 301s and picks the newest, and keep the row off the live CSVs until then. The collector is a change to `src/pdf_extract/parish_sites/collectors.py`, which a map job may not edit; a sketch is in `scratch/trenton-map-1/037-map/weblinks_collector.md` (untested). When it lands, set `bulletin_provider: other`, pin `page-pdfs https://churchofepiphanynj.org/index.php/sunday-bulletins` (or the new collector's recipe name), run `fetch:check`, and confirm it picks the newest bulletin<mmddyy>.pdf.
