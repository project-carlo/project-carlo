---
name: St. Sylvester Parish, Slickville
website: https://www.stsylvester.org
bulletin_provider: other
provider_id: dated-post https://www.stsylvester.org/bulletins/
publication: ['url:https://www.stsylvester.org/bulletins/']
group: 'Partners: St. Ambrose, Avonmore + St. Matthew, Saltsburg + St. Sylvester, Slickville'
evidence:
- url: https://www.stsylvester.org/wp-content/uploads/2026/10/St.-Sylvester-Bulletin-Oct.-25.pdf
  seen: 2026-10-22
  quote: St. Sylvester Parish + 3028 Route 819 + Slickville, PA 15684 Office 5900 Kennedy Avenue, Export,
    PA 15632
  note: 'Page 1 masthead of the 25 Oct 2026 issue ("30th Sunday in Ordinary Time + October 25, 2026",
    "WEBSITE: stsylvester.org"). Names St. Sylvester alone; the office address is St. Mary''s, Export,
    the pastor''s other parish. Page 3 has no text layer.'
- url: https://www.stsylvester.org/wp-content/uploads/2026/10/St.-Sylvester-Bulletin-Oct.-25.pdf
  seen: 2026-10-22
  quote: Sunday Mass 8:30 AM
  note: 'Page 1 Mass list: October 25, November 1 and November 2 (All Souls, 6:30 PM), each with "Monsignor
    Michael Begolly". "CONFESSIONS are Saturdays at noon at St. John''s in Delmont, and 5:00 pm Tuesdays
    at St. Mary''s in Export"; those two are the Delmont/Export parishes'' churches and have no Mass in
    this bulletin.'
- url: https://www.stsylvester.org/bulletins/
  seen: 2026-10-22
  note: 'Read in headed Chrome (parish-site-access visit.py; probe url gets 403). "Read our Weekly Bulletins"
    lists one post per issue, newest first: "October 25, 2026", "October 18, 2026", "October 11, 2026",
    "September 27, 2026" ... "August 23, 2026", "July 19, 2026". The 25 Oct post embeds a dFlip flipbook
    whose source is wp-content/uploads/2026/10/St.-Sylvester-Bulletin-Oct.-25.pdf.'
- url: https://container.parishesonline.com/bulletins/14/0550/20261025B.pdf
  seen: 2026-10-22
  note: The St. John Baptist de La Salle / St. Mary (Delmont, Export) bulletin for 25 Oct 2026, container
    14/0550, the other parishes Msgr. Begolly serves. probe pdf --grep "Sylvester" and "Slickville" finds
    no match. St. Sylvester is not in that bulletin.
- url: https://www.dioceseofgreensburg.org/official-june-20-2026/
  seen: 2026-10-22
  quote: Begolly as Pastor of Saint Sylvester Parish, Slickville
  note: Appointments effective July 7, 2026. The same post makes Fr. Tyler Bandura pastor of St. Matthew,
    Saltsburg and St. Ambrose, Avonmore, ending the three-parish arrangement the directory's partner field
    still shows.
- url: https://parishesonline.com/organization/st-sylvester-church-15684
  seen: 2026-10-22
  note: 'probe po: st-sylvester-church-15684 (lpi:0018000000QxC0iAAF, 3028 State Route 819, Slickville)
    answers "no publications". An empty account, not a live channel; not recorded as a publication id.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=265
  seen: 2026-10-22
  note: 'Directory: St. Sylvester Parish, pastor Msgr. Michael J. Begolly, deacon Michael Orange, "Saturday:
    no Mass; Sunday: 8:30 a.m.", website stsylvester.org, Partner Parishes St. Matthew (253) and St. Ambrose
    (021), mailing address "c/o P.O. Box 617, Avonmore" (the St. Ambrose office, stale since July).'
promoted: 2026-10-23
---

## Publisher

St. Sylvester Parish, Slickville (directory 265) publishes its own weekly bulletin on stsylvester.org. The 25 October 2026 issue (read 2026-10-22 with `probe pdf`) names St. Sylvester alone in its masthead ("St. Sylvester Parish + 3028 Route 819 + Slickville, PA 15684"). It gives the parish office at 5900 Kennedy Avenue, Export (St. Mary's, Export), and lists one Sunday Mass, 8:30 AM, with Msgr. Michael Begolly.

The batch asked whether St. Sylvester is in the St. Ambrose/St. Matthew bulletin or in the Delmont/Export one. It is in neither:
- **St. Ambrose and St. Matthew.** The directory still lists St. Sylvester as a partner of both, with the Avonmore mailing address. But the diocese's 20 June 2026 appointments (effective July 7) split the pastorate: Begolly became pastor of St. Sylvester, and Bandura of St. Matthew and St. Ambrose. The 18 Oct 2026 St. Ambrose/St. Matthew bulletin (row `st-ambrose-and-st-matthew-avonmore`) has no St. Sylvester in its masthead or Mass schedule.
- **Delmont and Export.** Begolly also serves St. John Baptist de La Salle, Delmont and St. Mary, Export (and Mother of Sorrows, Murrysville), and St. Sylvester's office is now at St. Mary's. But their 25 Oct 2026 bulletin (container 14/0550) never mentions "Sylvester" or "Slickville".

Each parish keeps its own live channel, so this is its own row.

## Worship sites

St. Sylvester church, Slickville: the only place with Mass in the 25 Oct issue. The confessions at St. John's (Delmont) and St. Mary's (Export) belong to the Delmont/Export parishes, which have their own rows and bulletin. GCatholic (24165) and the directory list no other site for this parish.

## Website and bulletin provider

stsylvester.org is a diocese-template WordPress site, cloned from partnerparishesmas.org (its menu still has "St. Ambrose Food Pantry"). It answers 403 to `probe url` but opens in headed Chrome, and its PDFs download with a plain fetch. The bulletin page `/bulletins/` links one post per issue, each embedding a dFlip flipbook of a PDF in `wp-content/uploads/<yyyy>/<mm>/`. Provider `other`. The first `fetch:check` (2026-10-22, no recipe) guessed `page-pdfs https://www.stsylvester.org/` and picked the diocese's privacy-policy PDF from the footer, which is wrong. With the recipe pinned to `dated-post https://www.stsylvester.org/bulletins/` it resolved "dated-post on https://www.stsylvester.org/bulletins/: current" and downloaded `St.-Sylvester-Bulletin-Oct.-25.pdf` (url_date 2026-10-25, 883,299 bytes). The LPi organization st-sylvester-church-15684 is empty.

## Not yet confirmed

The pipeline's fetch depends on the headed-browser path working for this host, because the bulletin page answers 403 to plain fetches. `fetch:check` succeeded headed on 2026-10-22. The issue list skips 4 October and has a gap from 19 July to 23 August, so the parish sometimes misses a week.
