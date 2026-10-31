---
name: Saint Elizabeth Ann Seton Parish, Windber
website: https://webparish.com/aj/SEAS/
bulletin_provider: other
provider_id: page-pdfs http://www.webparish.com/aj/SEAS/index.php?PG=ourschool
publication: ['url:https://webparish.com/aj/SEAS/index.php?PG=ourschool']
group: ''
evidence:
- url: http://www.webparish.com/pdfs/SEAS2026-10-25Bulletin.pdf
  seen: 2026-10-21
  quote: Rev. Roderick N. Soha, T.O.R.
  note: 'The 25 October 2026 bulletin (2 pages), already posted on 21 October. Page 1 masthead: "St. Elizabeth
    Ann Seton Church 605 Graham Avenue Windber, PA 15963 www.stelizabethannsetonwindber.com", "Pastor:
    Rev. Roderick N. Soha, T.O.R.", "In Residence Rev. Lawrence Lacovic", "Fr. Soha 467-7292", "Church
    Office: 467-7191". Under WEEKLY MASS SCHEDULE it lists the week 26 Oct-1 Nov for all three Windber
    churches, with the code (SA) St. Anthony, (SEAS), (SSCM) Sts. Cyril and Methodius, and (SEAS at SSCM)
    for SEAS intentions said at the SSCM building. The abbreviations are not expanded in the bulletin:
    read from the site Mass page and the directory times (see the church records).'
- url: http://www.webparish.com/pdfs/SEAS2026-10-25Bulletin.pdf
  seen: 2026-10-21
  quote: 12:00 PM (SSCM) Kay Paulochik by George & Eileen Maruschok
  note: 'Thursday 29 Oct. Sunday 1 Nov in the same issue: "8:00 AM (SEAS)", "10:00 AM (SA)", "12:00 PM
    (SSCM)".'
- url: https://www.webparish.com/aj/SEAS/index.php?PG=ourschool
  seen: 2026-10-21
  quote: October 25, 2026 Bulletin
  note: 'The parish site''s "Our Bulletins" page (rendered in Chrome; the home page stelizabethannsetonwindber.com
    redirects into www.webparish.com/aj/SEAS/ and curl gets Mod_Security 406): issues of 25, 18, 11 and
    4 October and 27 and 20 September 2026, linked to webparish.com/pdfs/SEAS2026-MM-DD-Bulletin.pdf.'
- url: https://www.webparish.com/aj/SEAS/index.php?PG=masstimeschedule
  seen: 2026-10-21
  quote: Wednesday - 9:00 AM at Sts. Cyril & Methodius
  note: 'The parish''s Mass Time Schedule page: "Monday - 9:00 AM at St. Anthony of Padua", "Tuesday -
    12:00 PM at St. Anthony of Padua", "Thursday - (SEAS mass intentions) 12:00 PM at Sts. Cyril & Methodius",
    "Friday - (SEAS mass intentions) 9:00 AM at Sts. Cyril & Methodius", "Sunday - 8:00 a.m.", confession
    "Sundays at St. Elizabeth Ann Seton 7:45 am". Confirms SA and SSCM are the other two buildings.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory entries for the three Windber parishes, all with pastor Rev. Roderick Soha, TOR and
    no homepage. Saint Elizabeth Ann Seton: Sunday 8:00 AM; Saints Cyril and Methodius: Sun 12:00 PM,
    Wed 9:00 AM, Thu 12:00 PM, Fri 9:00 AM (matches the bulletin).'
- url: https://discovermass.com/church/st-elizabeth-ann-seton-windber-pa/
  seen: 2026-10-21
  quote: no bulletins available for St. Elizabeth Ann Seton
  note: Discover Mass pages for this church and for saints-cyril-and-methodius-windber-pa both say the
    same; empty, not a live channel.
promoted: 2026-10-21
---

## Publisher

St. Elizabeth Ann Seton publishes its own weekly bulletin, `SEAS<YYYY-MM-DD>Bulletin.pdf` on webparish.com, listed on its "Our Bulletins" page (`webparish.com/aj/SEAS/index.php?PG=ourschool`). On 2026-10-21 the newest issue was dated 25 October 2026 (posted ahead of the Sunday). The masthead names St. Elizabeth Ann Seton Church, 605 Graham Avenue, and the pastor Rev. Roderick N. Soha, T.O.R. The same three Windber parishes share Fr. Soha, a common Mass rota and a shared schedule, but St. Anthony of Padua publishes a different weekly PDF from its own site, so it is a separate row (`saint-anthony-of-padua-windber`).

## Worship sites

Two churches: St. Elizabeth Ann Seton (605 Graham Ave, Sunday 8:00 AM) and Sts. Cyril and Methodius (604 Graham Ave, across the street; Sunday 12:00 PM and weekdays Wed/Thu/Fri). Sts. Cyril and Methodius has no bulletin of its own: its Discover Mass page says "no bulletins available", its old Web Parish page (`webparish.com/aj/CyrilandMethodius/`) is a stub still naming Rev. Matthew Misurda as pastor with no Mass times or bulletins, and its only live channel is Facebook (`facebook.com/SSCMWindber`, posts of Sept 2026, not read). Its Masses appear in both St. Elizabeth Ann Seton's and St. Anthony's bulletins; I filed the church here because this parish's own weekday intentions are said there ("SEAS at SSCM" on Thursdays and Fridays), a judgement, since either row's bulletin lists it. St. Anthony of Padua's church, 2201 Graham Ave, is in the other row, though the Mass list here covers it too. GCatholic's St. Mary, Windber (gcatholic:17326) is a Ruthenian church: other jurisdiction, not recorded.

## Website and bulletin provider

`other`, read by `page-pdfs` on the "Our Bulletins" page (Web Parish). The directory gives no homepage; the parish's own site `stelizabethannsetonwindber.com` (printed in the masthead) redirects into the Web Parish page. Same Web Parish host and 406 behaviour as St. Thomas, Bedford.

## Not yet confirmed

Whether the two weekly PDFs will stay separate: the SA and SEAS bulletins carry the same Mass list, and if one stops being posted the rows should be merged (`pnpm diocese merge`). Neither is silent today.
