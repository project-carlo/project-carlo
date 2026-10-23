---
name: Church of the Good Shepherd
website: https://www.goodshepherdwm.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://www.goodshepherdwm.org/bulletins
publication: ['url:https://www.goodshepherdwm.org/bulletins#good-shepherd-west-middlesex']
group: Pastor Rev. Glenn Whitman also serves Our Lady of Fatima, Farrell (clergy list 8/7/2026); separate
  bulletin
evidence:
- url: https://www.goodshepherdwm.org/_files/ugd/fb8de7_6e224fbb65434d848be2f24128dad1bd.pdf
  seen: 2026-10-23
  note: 'The ''Oct. 25th, 2026'' issue linked from the Bulletins page (8 pages; image-only scans, no text
    layer, rendered with pdftoppm). Page 1 is a photo; page 2 reads: ''THIRTIETH SUNDAY IN ORDINARY TIME
    - OCTOBER 25TH, 2026'', ''Church of the Good Shepherd'', ''Office Address: 3613 Sharon Road (PO Box
    226) West Middlesex, PA 16159'', ''PASTOR - Fr. Glenn Whitman'', ''SACRAMENTAL ASSISTANT - Fr. William
    Barron'', and a Mass-intention table: Monday 26 Oct and Tuesday 27 Oct ''NO MASS, COMMUNION SERVICE'',
    Thursday 29 and Friday 30 Oct 8:30am, Saturday 31 Oct 6:00pm, Sunday 1 Nov 9:00am and 11:30am.'
- url: https://www.goodshepherdwm.org/bulletins
  seen: 2026-10-23
  quote: WEEKLY BULLETINS
  note: 'Wix page read in headed Chrome (visit.py): ''Search the most recent three months of bulletins
    below'', ''CURRENT BULLETIN'', archive by month; issue links ''Oct. 4th, 2026'' ... ''Oct. 25th, 2026''
    then Sept. and Aug., each a `usrfiles.com/ugd/fb8de7_<hash>.pdf` link. Plain curl of the page shows
    only the current one, `/_files/ugd/fb8de7_6e224fbb65434d848be2f24128dad1bd.pdf` (which redirects to
    filesusr.com).'
- url: https://www.eriercd.org/Parish31102-Good-Shepherd.html
  seen: 2026-10-23
  quote: Good Shepherd
  note: 'Directory record 31102: 3613 Sharon Road, West Middlesex PA 16159; ''Priest-in-Residence: Rev.
    William Barron; Pastor: Rev. Glenn Whitman''; Saturday 6 p.m. (in person and online), Sunday 9 and
    11:30 a.m., Monday/Tuesday/Thursday/Friday 8:30 a.m.; holy days 8:30 a.m. and 7 p.m.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Good Shepherd
  note: 'Clergy list updated 8/7/2026: Whitman, Rev. Glenn: pastor of Good Shepherd, West Middlesex and
    Our Lady of Fatima, Farrell.'
research:
- method: pnpm fetch:check --diocese erie --parish good-shepherd-west-middlesex --expected-identity Shepherd
    (headed Chrome)
  url: https://www.goodshepherdwm.org/bulletins
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for the pick: it resolved the ''Oct. 25th, 2026'' file (fb8de7_6e224fbb65434d848be2f24128dad1bd.pdf
    on usrfiles.com, 3,145,953 bytes, a PDF), the current issue I read by rendering. Identity and issue
    date read ''unknown'' only because every page is a scan with no text layer; the identity was confirmed
    by eye on page 2. Re-run on a later week to confirm it follows the newest link.'
publication_reviews:
- parish: our-lady-of-fatima-farrell
  decision: separate
  evidence:
  - url: https://www.goodshepherdwm.org/_files/ugd/fb8de7_6e224fbb65434d848be2f24128dad1bd.pdf
    seen: 2026-10-23
    note: Good Shepherd's 25 Oct 2026 issue is headed 'Church of the Good Shepherd' with Saturday 6:00
      pm and Sunday 9:00/11:30 am Masses and no Fatima Mass; Fatima's 24 Oct issue is a different four-page
      bulletin on fatimafarrell.org whose only Mass is Saturday 4:00 pm.
---

## Publisher

Good Shepherd, West Middlesex publishes its own weekly bulletin on its Wix site, goodshepherdwm.org, Bulletins page (three months of issues, newest 'Oct. 25th, 2026'). The issue is an eight-page scan with no text layer; page 2 (rendered and read 2026-10-23) carries the masthead block 'Church of the Good Shepherd, 3613 Sharon Road, West Middlesex, PA 16159, PASTOR - Fr. Glenn Whitman' and the Mass-intention table (Saturday 6:00 pm, Sunday 9:00 and 11:30 am, Thursday and Friday 8:30 am; 'NO MASS, COMMUNION SERVICE' Monday and Tuesday that week).

Fr. Whitman is also the pastor of Our Lady of Fatima, Farrell (clergy list), but Fatima publishes a different bulletin (see its record and the two `separate` peer reviews), so Good Shepherd is its own row.

## Worship sites

One church, Good Shepherd at 3613 Sharon Road (GCatholic 24434 and directory 31102). No mission or secondary church is attached in the directory.

## Website and bulletin provider

Provider `other`, `page-pdfs` on the Bulletins page. Wix serves the current issue in static HTML, but the full list only after JavaScript; the outcome of `fetch:check` is recorded in `research`. Because the PDFs are image-only, `fetch:check` identity reading will be `unknown`; the issue's page 2 is what identifies the parish.

## Not yet confirmed

Nothing about the parish's identity; see `research` for the fetch result.
