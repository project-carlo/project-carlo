---
name: St. Ambrose and St. Matthew Partner Parishes, Avonmore
website: https://www.partnerparishesmas.org
bulletin_provider: other
provider_id: dated-post https://www.partnerparishesmas.org/bulletins/
publication: ['url:https://www.partnerparishesmas.org/bulletins/']
group: 'Partners: St. Ambrose, Avonmore + St. Matthew, Saltsburg + St. Sylvester, Slickville'
evidence:
- url: https://www.partnerparishesmas.org/wp-content/uploads/2026/10/St-A-bulletin-10.18.26.pdf
  seen: 2026-10-22
  quote: ST. AMBROSE CHURCH ST. MATTHEW CHURCH Parishes of the Diocese of Greensburg October 18, 2026
  note: 'Page 1 masthead of the 18 Oct 2026 issue (the newest posted on 2026-10-22). Lists "St. Ambrose
    Church & Main Office 505 Cambria Avenue P O Box 617 Avonmore, PA 15618" and "St. Matthew Church: 501
    Cathedral Street Saltsburg, PA 15681", pastor "The Very Reverend Tyler Bandura, VF, Pastor". No St.
    Sylvester in the masthead or staff.'
- url: https://www.partnerparishesmas.org/wp-content/uploads/2026/10/St-A-bulletin-10.18.26.pdf
  seen: 2026-10-22
  quote: 'Saturday Vigil: 5:00 pm at St. Ambrose Sunday Mass: 11:00 am at St. Matthew Weekday Masses:
    to be announced'
  note: 'Page 1 Mass schedule. The week''s Mass intentions use only "St A" and "St M" (Sat 5:00 pm St
    A, Sun 11:00 am St M, Mon 8:30 am St A, Fri 8:30 am St M). Page 2 keeps separate collection and attendance
    figures for the two churches. St. Sylvester appears only in a page-2 notice ("St. Sylvester, Slickville:
    is holding an apple ..."), as a neighbour.'
- url: https://www.partnerparishesmas.org/bulletins/
  seen: 2026-10-22
  quote: Read our Weekly Bulletins October 18, 2026 October 11, 2026 October 4, 2026
  note: Plain fetch works. One child post per issue, newest first, back to "August 16, 2026"; the 18 Oct
    post (/october-18-2026/) embeds a dFlip flipbook whose source is wp-content/uploads/2026/10/St-A-bulletin-10.18.26.pdf.
    Footer contact block names St. Ambrose Parish and St. Matthew Parish only ("Mailing address same as
    St. Ambrose").
- url: https://parishesonline.com/organization/st-ambrose-church-15618
  seen: 2026-10-22
  note: 'probe po: st-ambrose-church-15618 (lpi:0018000000QxC0ZAAV, website partnerparishesmas.org) and
    st-matthew (lpi:0018000000QxC0wAAF, 501 Cathedral St, Saltsburg) both answer "no publications". Old,
    empty accounts, not live channels; not recorded as publication ids.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=021
  seen: 2026-10-22
  note: 'Directory: St. Ambrose Parish, pastor Father Tyler J. Bandura, "Saturday: 5:00 p.m.; Sunday:
    no Mass", website partnerparishesmas.org, Partner Parishes St. Sylvester (265) and St. Matthew (253).
    LocationID=253 (St. Matthew): same pastor and website, "Saturday: no Mass; Sunday: 11:00 a.m.", mailing
    c/o P.O. Box 617, Avonmore.'
- url: https://www.dioceseofgreensburg.org/official-june-20-2026/
  seen: 2026-10-22
  quote: Bandura, VF as Pastor at Saint Matthew Parish, Saltsburg and Saint Ambrose Parish, Avonmore
  note: 'Same post: Begolly "as Pastor of Saint Sylvester Parish, Slickville", and Frescura "resigns as
    Administrator of Saint Sylvester Parish, Slickville, Saint Matthew Parish Saltsburg and Saint Ambrose
    Parish, Avonmore". The post gives July 7, 2026 as the effective date. This is the source of the St.
    Sylvester split; the directory''s partner field predates it.'
promoted: 2026-10-23
---

## Publisher

St. Ambrose Parish, Avonmore (directory 021) and St. Matthew Parish, Saltsburg (directory 253) are two canonical parishes with one pastor (Very Rev. Tyler Bandura, who is also pastor of St. James, New Alexandria, a separate row), one office (505 Cambria Ave., Avonmore) and one website, partnerparishesmas.org. They publish one weekly bulletin, self-hosted there. The 18 October 2026 issue (read 2026-10-22 with `probe pdf`) has both churches in its page-1 masthead ("ST. AMBROSE CHURCH / ST. MATTHEW CHURCH / Parishes of the Diocese of Greensburg"), one staff list, one Mass schedule and one week of intentions covering both. One bulletin, so one row.

The diocesan directory lists St. Sylvester, Slickville (265) as a third partner of both, and the partner site's menu still has a "St. Sylvester Minister Schedule" page. That three-way arrangement ended with the diocese's "Official" appointments of 20 June 2026 (effective July 7, 2026): Deacon Daniel Frescura "resigns as Administrator of Saint Sylvester Parish, Slickville, Saint Matthew Parish Saltsburg and Saint Ambrose Parish, Avonmore", Msgr. Michael Begolly became "Pastor of Saint Sylvester Parish, Slickville" and Fr. Bandura "Pastor at Saint Matthew Parish, Saltsburg and Saint Ambrose Parish, Avonmore". The 18 Oct bulletin names St. Sylvester only in a page-2 parish-news notice, not in its masthead, staff or Mass schedule. St. Sylvester publishes its own bulletin on stsylvester.org (row `st-sylvester-slickville`). So the group has two rows, each with its own live channel.

## Worship sites

St. Ambrose (Avonmore) and St. Matthew (Saltsburg). They are the only places in the 18 Oct Mass schedule and intentions, and the only sites GCatholic (24118, 24155) and the directory list for these two parishes. The site's "St. Matthew Cemetery" page is a cemetery, not a worship site, and was not recorded.

## Website and bulletin provider

partnerparishesmas.org is a diocese-template WordPress site that answers plain fetches. Its bulletin page `/bulletins/` links one post per issue (e.g. `/october-18-2026/`), and each post embeds a dFlip flipbook of a PDF in `wp-content/uploads/<yyyy>/<mm>/` (file names like `St-A-bulletin-10.18.26.pdf`). Provider `other`. The first `fetch:check` (2026-10-22, no recipe) guessed `page-pdfs https://www.partnerparishesmas.org/` and picked the diocese's privacy-policy PDF from the footer, which is wrong. With the recipe pinned to `dated-post https://www.partnerparishesmas.org/bulletins/` it resolved "dated-post on https://www.partnerparishesmas.org/bulletins/: current" and downloaded `St-A-bulletin-10.18.26.pdf` (url_date 2026-10-18, 436,937 bytes), the newest issue posted on 2026-10-22, a Thursday. The LPi geo-search within 6 miles of each church found only the empty organizations st-ambrose-church-15618 and st-matthew; neither is a publication id.

## Not yet confirmed

The 25 Oct issue was not yet posted on 2026-10-22, so this row's uploads may lag the weekend by a few days. That is a timing matter, not a structural one.
