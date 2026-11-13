---
name: St. Mary Star of the Sea and St. Gertrude (Far Rockaway)
website: https://saintsmaryandgertrude.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://saintsmaryandgertrude.org/bulletins
publication: []
group: Deanery Q10 (Queens East)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjQvOTlsMG9vbmtsYl9CdWxsZXRpbi4yMDI2LjEwLjI1LnBkZiJdXQ/Bulletin.2026.10.25.pdf
  seen: 2026-11-06
  quote: St. Mary Star of the Sea and St. Gertrude
  note: '25 October 2026 issue (2 pages; page 1 rendered with render.py because its text uses a shifted
    font encoding that drops digits). Page 1 masthead ''St. Mary Star of the Sea and St. Gertrude Roman
    Catholic Church'', phone (718) 327-1133, www.saintsmaryandgertrude.org, with two church photos and
    addresses: ''1920 New Haven Ave. Far Rockaway, N.Y. 11691'' and ''336 Beach 38th Street Far Rockaway,
    N.Y. 11691''. Mass intentions Sat 24 Oct 7:30 pm; Sun 25 Oct 8:15, 9:30, 11:00, 11:30 am, 1:15 pm;
    weekdays 12:10 pm and 7:00 pm (Fri 7:30 pm). No publisher footer.'
- url: https://saintsmaryandgertrude.org/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, Oct 25, 2026
  note: 'Tilma bulletins page, newest first: Oct 25, Oct 18, Oct 11, Oct 04, Sep 27, Sep 20, Sep 13, Sep
    06, Aug 30, Jul 26 … files Bulletin.YYYY.MM.DD.pdf on files.tilmaplatform.com. No 1 November card
    yet on 6 November.'
- url: https://saintsmaryandgertrude.org/mass-times
  seen: 2026-11-06
  quote: 'St. Gertrude: 9:30am (Spanish), 11:00am'
  note: 'Mass times page: Saturday Vigil St. Mary 7:30pm (Spanish); Sunday St. Mary 8:15am, 11:30am (Spanish),
    1:15pm; St. Gertrude 9:30am (Spanish), 11:00am; weekdays Mon-Fri 12:10pm, Mon-Thu 7:00pm, Fri 7:30pm
    (Spanish). Footer: St. Mary Star of the Sea Church, 1920 New Haven Ave.; St. Gertrude''s Church, 336
    Beach 38th St.'
- url: https://parishesonline.com/organization/st-gertrude-church-11691
  seen: 2026-11-06
  note: 'probe po: org ''St. Gertrude Church'', 1920 New Haven Avenue, Far Rockaway, lists no issues,
    so it is not a publication id. No org at st-mary-star-of-the-sea-church-11691, st-mary-star-of-the-sea-st-gertrude-11691
    or st-mary-star-of-the-sea-and-st-gertrude-church-11691.'
- url: https://dioceseofbrooklyn.org/priests/
  seen: 2026-11-06
  note: 'Priests'' directory as read by the survey (2026-11-05): Very Rev. Francis T. Shannon, ''Pastor,
    St. Mary Star of the Sea and St. Gertrude, Far Rockaway''; Rev. David P. Bertolotti, Parochial Vicar
    of the same.'
promoted: 2026-11-12
research:
- method: fetch:check with page-pdfs https://saintsmaryandgertrude.org/bulletins
  url: https://saintsmaryandgertrude.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-run fetch:check and confirm it picks the 8 November 2026 (or later) issue; the 1 November
    issue was not posted by 6 November
  retry_when: After the weekend of 7-8 November 2026
  revisit_after: 2026-11-10
- method: 'Reconcile: headed fetch:check of every Brooklyn row'
  url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTEvMDcvNHY1aXVoamRpNF9CdWxsZXRpbi4yMDI2LjExLjA4LnBkZiJdXQ/Bulletin.2026.11.08.pdf
  checked: '2026-11-12'
  outcome: found
  next_action: 'None: the pick is the 8 November 2026 issue (Bulletin.2026.11.08.pdf; issue date ''conflict''
    in fetch:check, the file name is dated).'
bulletin_status: available
---

## Publisher

The parish makes its own bulletin (no publisher footer, files named `Bulletin.YYYY.MM.DD.pdf`) and posts it on its Tilma site's `/bulletins` page. The issue read is 25 October 2026 (read 2026-11-06): its page 1 masthead (an image-like text layer; rendered with render.py) reads "St. Mary Star of the Sea and St. Gertrude Roman Catholic Church" and shows both churches with their addresses, 1920 New Haven Ave. and 336 Beach 38th Street, Far Rockaway. The ParishesOnline org `st-gertrude-church-11691` exists but has no issues, so the row has no publication id, like the diocese's other self-posted Tilma rows.

## Worship sites

Two churches: St. Mary Star of the Sea, 1920 New Haven Ave., and St. Gertrude, 336 Beach 38th St. The bulletin masthead shows both; the parish's Mass times page assigns the Masses: St. Mary has the Saturday 7:30pm Vigil (Spanish) and Sunday 8:15am, 11:30am (Spanish) and 1:15pm; St. Gertrude has Sunday 9:30am (Spanish) and 11:00am. The bulletin's Mass intentions list the same Sunday times without the church. The diocese directory and deanery list (Q10) list the parish once at 1920 New Haven Avenue; GCatholic 16748 is the parish at 1920 New Haven Ave; the Mass finder lists St. Gertrude's Church separately (place 932) and has no place for St. Mary.

## Website and bulletin provider

`other` with the recipe `page-pdfs https://saintsmaryandgertrude.org/bulletins`. `fetch:check` (2026-11-06) picked the first-listed card, the 25 October 2026 issue, transport ok, freshness unknown (its date check saw the week's Mass-intention dates as a conflict). That was the newest posted on 6 November: the 1 November card was not yet up. Issues are mostly weekly, with occasional skipped weeks (no cards for 2-23 August or 28 June-12 July). The PDF's text uses a shifted font encoding that loses digits and much of the English text, so the Mass schedule is best read from rendered pages.

## Not yet confirmed

That fetch picks the current week's issue once it is posted (see research; recheck after 10 November 2026).
