---
name: Our Lady of Victories and the Shrine of St. Jude
website: https://olvjude.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://olvjude.org/bulletins
  seen: 2026-11-05
  note: 'Read with parish-site-access visit.py (probe url gets 403; eCatholic site 11314). The page shows
    the heading ''Bulletin'' and ''ARCHIVE'' and no bulletin files: its links are menu, Mass-time anchors
    and social media only.'
- url: https://olvjude.org/
  seen: 2026-11-05
  quote: 'LOCATION: Church address: 169 Broadway (corner of Paterson St. & Memorial Dr.) in Paterson,
    NJ 07501'
  note: Home page (visit.py), header 'OUR LADY OF VICTORIES CHURCH & The Shrine of St. Jude'; next line
    'Entrance to our two parking lots by 100 Fair St. (back of the Church)'. Its calendar lists Misa and
    'Mass in Honor to St. Jude English' this week. The /mass-times path is 404 on this site.
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:11314 'Our Lady of Victories, Paterson', 100 Fair Street, Paterson 07501,
    website https://olvjude.org/; Saturday 7:00 PM Spanish; Sunday 8:00 AM Spanish, 10:30 AM English,
    1:00 PM Spanish; weekday Masses Tuesday-Saturday.
revisit: Reload https://olvjude.org/bulletins with visit.py and probe files.ecatholic.com/11314/bulletins/<Sunday>.pdf;
  if issues appear, set provider ecatholic, publication ecatholic:11314, and run fetch:check.
revisit_after: 2027-02-01
research:
- method: parish-site-access visit.py on /bulletins (text and link list) and the home page (--bulletin,
    link list)
  url: https://olvjude.org/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reload the /bulletins page and its Archive
  retry_when: On the revisit date, or when the site or finder links a bulletin
- method: 'issues.py ecatholic ecatholic:11314: every Sunday 4 Oct - 8 Nov 2026, Saturdays 17 Oct - 7
    Nov 2026, and 2 Aug, 30 Aug, 27 Sep 2026 (all 403, not posted)'
  url: https://files.ecatholic.com/11314/bulletins/20261108.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Probe the coming Sundays' file names again
  retry_when: On the revisit date
bulletin_status: not-found
---

## Publisher

No bulletin found. Our Lady of Victories runs an eCatholic site (site id 11314, the finder pin id) whose Bulletin page, read 2026-11-05 with parish-site-access visit.py, shows a heading and "ARCHIVE" and no issues. `files.ecatholic.com/11314/bulletins/<YYYYMMDD>.pdf` answered 403 (not posted) for every Sunday 4 October - 8 November 2026, Saturday-dated names, and three Sundays August-September 2026. See `research`.

## Worship sites

One church, `our-lady-of-victories-paterson`. The home page (2026-11-05) gives "Church address: 169 Broadway (corner of Paterson St. & Memorial Dr.)" with parking by 100 Fair St. at the back, and its calendar lists Masses and the Thursday St. Jude Mass; the finder (directory:11314) gives Saturday 7:00 PM, Sunday 8:00 AM, 10:30 AM and 1:00 PM and weekday Masses. The Shrine of St. Jude is in this church, not a separate place. The finder and GCatholic (19050) list this one church.

Its administrator, Rev. Angel J. Torres, is also a parochial vicar of the cathedral (rcdop.org priest directory, per the survey); that is not a shared pastorate, and neither parish posts a bulletin, so nothing suggests one bulletin.

## Website and bulletin provider

`https://olvjude.org/` (the finder's website; eCatholic behind Cloudflare). Provider `no_bulletin`: public Mass but no bulletin posted, so promote keeps the row and its church off the site until one turns up. If issues appear they will be `ecatholic:11314`.

## Not yet confirmed

Whether the parish prints a bulletin it doesn't post (the office, (973) 279-0487, could say), and the current Mass schedule, which the home page announces ("NEW SCHEDULE OF MASSES") without readable text. The revisit on 2027-02-01 rereads the Bulletin page and the eCatholic file names.
