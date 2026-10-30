---
name: St. Benedict Parish
website: https://parish.stbenedictholmdel.org/
bulletin_provider: parishes_online
provider_id: st-benedict-church-and-school
publication: ['po-org:st-benedict-church-and-school', 'lpi:0018000000Qx8o7AAB', 'po-container:03/1050']
group: Cohort 14 (Keyport, Matawan, Union Beach, Holmdel)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1050/20261025B.pdf
  seen: 2026-10-30
  quote: Very Rev. Garry R. Koch, V.F.
  note: '25 October 2026 issue (16 pages, text layer), page 1: parish office voice 732/264-4712, Pastor
    Very Rev. Garry R. Koch, V.F., Parochial Vicar Rev. Adam Midor; Mass Schedule block: Saturday Vigil
    5:00 p.m., Sunday 8:00, 9:30, 11:00 am and 5:00 pm, Monday-Friday 9:00 am. It names St. Benedict alone
    ("St. Benedict School" in the staff list). Page 3 mentions "Our Lady of Victory Adoration Chapel".'
- url: https://container.parishesonline.com/bulletins/03/1050/20261025B.pdf
  seen: 2026-10-30
  quote: ': 8:00, 9:30, 11:00 am and 5:00 pm'
  note: The Sunday line of the page 1 Mass Schedule block (labels and times extract as separate lines).
- url: https://parish.stbenedictholmdel.org/bulletins-1
  seen: 2026-10-30
  note: Read in the browser (probe url answers 403). The Bulletins page lists parishesonline.com publication-page
    links to container.parishesonline.com/bulletins/03/1050/20261025B.pdf, 20261018B, 20261011B and 20261004B;
    its embedded ids are lpi:0018000000Qx8o7AAB, ecatholic:15175 and po-container:03/1050. `probe po st-benedict-church-and-school`
    gives address 165 Bethany Rd, Holmdel 07733-1654, website parish.stbenedictholmdel.org, latest issue
    2026-10-25.
- url: https://stbenedictholmdel.org/
  seen: 2026-10-30
  note: Read in the browser (403 to probe url). The older eCatholic site 39277, "St. Benedict Parish &
    School", copyright 2016, with no bulletin link; GCatholic lists it as the website. The finder lists
    parish.stbenedictholmdel.org (eCatholic 15175).
- url: https://parish.stbenedictholmdel.org/
  seen: 2026-10-30
  note: 'Homepage Mass times read in the browser: Saturday 5:00 PM; Sunday 8:00 AM, 9:30 AM, 11:00 AM,
    5:00 PM; Monday-Friday 9:00 AM; perpetual adoration in the Our Lady of Victory Adoration Chapel. Pastor
    Father Garry Koch.'
research:
- method: issues.py ecatholic 15175 and 39277 (files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf, Sundays
    30 Aug-1 Nov 2026)
  url: https://parish.stbenedictholmdel.org/bulletins-1
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None: neither eCatholic id serves bulletin files (403 for every Sunday probed); the Bulletins
    page links ParishesOnline, which is the bulletin.'
  retry_when: The Bulletins page stops linking container.parishesonline.com issues.
- method: pnpm fetch:check --diocese trenton --parish st-benedict-holmdel (headed Chrome)
  url: https://container.parishesonline.com/bulletins/03/1050/
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: see the fetch check result in the Website and bulletin provider section.'
bulletin_status: available
publication_reviews:
- parish: st-clement-matawan
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1050/20261025B.pdf
    seen: 2026-10-30
    quote: Very Rev. Garry R. Koch, V.F.
    note: 'Bulletin for St. Benedict Parish (row st-benedict-holmdel), read by its map batch: 25 October
      2026 issue (16 pages, text layer), page 1: parish office voice 732/264-4712, Pastor Very Rev. Garry
      R. Koch, V.F., Parochial Vicar Rev. Adam Midor; Mass Schedule block: Saturday Vigil 5:00 p.m., Sunday
      8:00, 9:30, 11:00 am and 5:00 pm, Monday-Friday 9:00 am. It names St. Benedict alone ("St. Benedict
      School" in the staff list). Page 3 mentions "Our Lady of Victory Adoration Chapel".'
  - url: https://www.church-bulletin.org/bulletin/church-of-saint-clement-matawan-nj-07747/2026-10-25.pdf
    seen: 2026-10-30
    quote: 'Mass Schedule: Saturday: 5:00PM | Sunday 8:00, & 11:00AM Daily Mass: Mon, Tues, Wed, Fri 8:00AM'
    note: 'Bulletin for St. Clement Parish (row st-clement-matawan), read by its map batch: 25 October
      2026 issue (8 pages, text layer). Page 1 masthead: "Church of ST. CLEMENT, 172 Freneau Avenue Matawan,
      NJ 07747 (732)-566-3616 www.stclementmatawan.org"; staff list names "REV. THOMAS VALA, PASTOR".
      It names St. Clement alone, with no other church or parish. The 18 October and 1 November issues
      on the same listing are image-only (no text layer).'
- parish: st-john-neumann-mount-laurel
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1050/20261025B.pdf
    seen: 2026-10-30
    quote: Very Rev. Garry R. Koch, V.F.
    note: 'Bulletin for St. Benedict Parish (row st-benedict-holmdel), read by its map batch: 25 October
      2026 issue (16 pages, text layer), page 1: parish office voice 732/264-4712, Pastor Very Rev. Garry
      R. Koch, V.F., Parochial Vicar Rev. Adam Midor; Mass Schedule block: Saturday Vigil 5:00 p.m., Sunday
      8:00, 9:30, 11:00 am and 5:00 pm, Monday-Friday 9:00 am. It names St. Benedict alone ("St. Benedict
      School" in the staff list). Page 3 mentions "Our Lady of Victory Adoration Chapel".'
  - url: https://files.ecatholic.com/2914/bulletins/20261101.pdf
    seen: 2026-10-30
    quote: 560 WALTON AVE., MT. LAUREL, NJ 08054
    note: 'Bulletin for St. John Neumann Roman Catholic Church (row st-john-neumann-mount-laurel), read
      by its map batch: The eCatholic issue dated 1 November 2026 (10 pages, text layer; md5 4671b2a3802925bddc66b5f8e417e639):
      ''St. John Neumann Roman Catholic Church'', ''Pastor - Rev. Fr. Michael Dunn'', ''1 November 2026
      - Solemnity of All Saints''. Page 2 ''Weekly Liturgical Schedule'': Monday 9:00am, Wednesday 7:00pm,
      Thursday 9:00am, Friday 9:00am (Tuesday no Masses), Saturday 4:00pm, Sunday 8:00am and 10:00am.
      It names this parish alone.'
---

## Publisher

St. Benedict Parish, Holmdel (Cohort 14). It publishes its own weekly bulletin through ParishesOnline (org `st-benedict-church-and-school`, container 03/1050, 16 pages in the 25 October 2026 issue). Page 1 names pastor Very Rev. Garry R. Koch, V.F. and parochial vicar Rev. Adam Midor, and the Mass schedule; no other parish is named. A different pastor from the other three Cohort 14 parishes, so the cohort is not a shared bulletin.

## Worship sites

One church, St. Benedict, 165 Bethany Road. Our Lady of Victory Adoration Chapel is the parish's perpetual adoration chapel on the same campus (no street address of its own; the schedule lists no Mass there), so no second church row. GCatholic (18740) and the finder (14604) list the one place. Weekday Masses that other parishes' bulletins list at a cohort neighbour (St. Mary, Colts Neck's at St. Catharine, Holmdel) are another batch's business.

## Website and bulletin provider

The diocese's task note says St. Benedict shows two eCatholic ids. 39277 is the old site `stbenedictholmdel.org` (copyright 2016, no bulletin link); 15175 is the current `parish.stbenedictholmdel.org`, which GCatholic does not list and the finder does. Both are 403 to plain fetch and load in the browser. Neither id serves `files.ecatholic.com/<id>/bulletins/` PDFs (403 for every Sunday probed), and the current site's Bulletins page links ParishesOnline issues, so ParishesOnline is the bulletin and the eCatholic ids stay out of `publication`. 15175 also appears on St. John Neumann, Mount Laurel's homepage; it was not identified as a St. Benedict file store there and is not recorded. Row: `parishes_online`.

`fetch:check` (2026-10-30, headed Chrome) picked the 25 October 2026 issue (the latest on ParishesOnline) from the publication page: status ok, PDF, fresh; identity unverified because the check had no expected identity.
