---
name: Sacred Heart Parish & St. Cecilia Parish
website: https://saintcecilia.net
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://saintcecilia.net/']
group: 'Partners: St. Cecilia, Whitney + Sacred Heart, Youngstown'
evidence:
- url: https://saintcecilia.net/wp-content/uploads/2026/10/bulletin-2026-10-21.pdf
  seen: 2026-10-22
  quote: Sacred Heart Parish & St. Cecilia Parish
  note: 'Page 1 of the 25 Oct 2026 issue: "October 25, 2026 Thirtieth Sunday in Ordinary Time", "Pastor: Fr.
    James F. Podlesny, O.S.B.", both churches'' addresses ("421 Main St. Youngstown, PA 15696", "220 St. Cecilia
    Rd. Latrobe, PA 15650"), "Partner Parishes of the Catholic Diocese of Greensburg", "Parish Office & Mailing
    Address: 222 St. Cecilia Road, Latrobe, PA 15650", www.saintcecilia.net.'
- url: https://saintcecilia.net/wp-content/uploads/2026/10/bulletin-2026-10-21.pdf
  seen: 2026-10-22
  quote: Saturday 6:00pm at Sacred Heart Church
  note: 'Page 1 "MASS TIMES": "Tues. & Thurs. Mass 8am at Sacred Heart; Wed. & Fri. Mass 8am at Saint Cecilia;
    Saturday 4:00pm at St Cecilia Church; Saturday 6:00pm at Sacred Heart Church; Sunday 8:00am at St Cecilia
    Church; Sunday 10:30am at Sacred Heart Church". No other place.'
- url: https://saintcecilia.net/
  seen: 2026-10-22
  note: 'Home page ("Saint Cecilia & Sacred Heart Church") links the bulletins directly as uploads:
    wp-content/uploads/2026/10/bulletin-2026-10-21.pdf and bulletin-2026-10-12.pdf (file names carry the upload
    date, not the Sunday: the 10-21 file is the 25 Oct issue). No ParishesOnline, eCatholic or Discover Mass id
    on the page.'
- url: https://parishesonline.com/organization/st-cecilia-church-15693
  seen: 2026-10-22
  note: 'probe po: LPi organizations st-cecilia-church-15693 (lpi:0018000000QxC0FAAV) and sacred-heart-church-15696
    (lpi:0018000000QxC0GAAV) both answer "no publications". Old, empty accounts, not a live channel.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=301
  seen: 2026-10-22
  note: 'Directory: St. Cecilia Parish, Whitney, pastor Father James F. Podlesny, OSB, "Saturday: 4:00 p.m.; Sunday:
    8:00 a.m.", Partner Parishes "Sacred Heart Parish, Youngstown (307)", website saintcecilia.net. LocationID=307
    (Sacred Heart): same pastor, "Saturday: 6:00 p.m.; Sunday: 10:30 a.m.", partner St. Cecilia, same website,
    mailing address c/o St. Cecilia Church.'
---

## Publisher

St. Cecilia Parish, Whitney (directory 301) and Sacred Heart Parish, Youngstown (directory 307) are two canonical parishes in a diocesan partnership with one pastor (Fr. James F. Podlesny, O.S.B.), one office (222 St. Cecilia Road) and one website, saintcecilia.net. They publish one weekly bulletin, self-hosted on that site. The 25 October 2026 issue (read 2026-10-22 with `probe pdf`) is headed "Sacred Heart Parish & St. Cecilia Parish ... Partner Parishes of the Catholic Diocese of Greensburg", gives both church addresses and one combined Mass schedule (page 1). It also says "Every family should be registered at either St. Cecilia or at Sacred Heart Parish [one or the other]. Of course you can go to Mass at either parish": two canonical parishes, one bulletin, so one row.

## Worship sites

St. Cecilia (Whitney) and Sacred Heart (Youngstown): the only two places in the bulletin's "MASS TIMES". GCatholic and the diocesan directory list no other site for either parish.

## Website and bulletin provider

saintcecilia.net is a WordPress site (not the diocese template) whose home page links the latest bulletins as uploaded PDFs (`wp-content/uploads/<yyyy>/<mm>/bulletin-<upload date>.pdf`); `probe url` reads it without a browser. Provider `other`; `fetch:check` on 2026-10-22 resolved "page-pdfs on https://saintcecilia.net: current", downloaded `bulletin-2026-10-21.pdf` (the 25 Oct issue, 8,043,781 bytes) and printed the recipe `page-pdfs`, recorded as `provider_id`. The two LPi organizations (st-cecilia-church-15693, sacred-heart-church-15696) have no publications and are not recorded as publication ids. The row is named after the masthead, which lists Sacred Heart first; the slug carries Youngstown for that reason, though the office is at St. Cecilia.

## Not yet confirmed

The file name carries the upload date (Wednesday 21 Oct for the 25 Oct issue), not the Sunday; `fetch:check` treated it as current, but an upload made more than a few days before the Sunday could be judged stale. Recheck that the next issue is picked up. Nothing else.
