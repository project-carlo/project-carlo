---
name: St. Jude
website: https://www.stjuderc.org/recent-calendars-and-newsletters
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stjuderc.org/recent-calendars-and-newsletters']
group: ''
evidence:
- url: https://myemail.constantcontact.com/New-Beginnings---11-06-2026-.html?soid=1133232330998&aid=nVNZMjepV0g
  seen: 2026-11-12
  quote: St. Jude Parish | 707 Monroe Turnpike | Monroe, CT 06468 US
  note: '''New Beginnings - 11/06/2026'', the parish''s weekly email newsletter (HTML, no PDF): ''Reflection
    from Fr. Joseph'', ''Mass Intentions for November 7 – November 15'', and a Mass Schedule: weekday
    Masses Monday thru Friday 9 am in the main Church; weekend Saturday 4:30 pm, Sunday 7:30, 9:30 and
    11:30. It names St. Jude alone.'
- url: https://www.stjuderc.org/recent-calendars-and-newsletters
  seen: 2026-11-12
  note: 'visit.py (the page builds its links in JavaScript): the site''s ''Weekly Newsletters'' page links
    ''Current Weekly Newsletter'' to the 11-06-2026 Constant Contact email and ''October 30'' to the previous
    week''s; no bulletin PDF, ParishesOnline or other publisher link anywhere on the Duda site (homepage
    links checked).'
- url: https://www.stjuderc.org/mass-schedule
  seen: 2026-11-12
  quote: Sunday - 7:30 AM, 9:30 AM, 11:30 AM
  note: 'The site''s Mass Schedule page: Monday-Thursday 9:00 AM; Saturday 4:30 PM; Sunday 7:30, 9:30,
    11:30 AM.'
research:
- method: probe po on guessed ParishesOnline slugs st-jude-church-06468 and st-jude-parish-06468
  checked: '2026-11-12'
  outcome: not-found
  next_action: Check the parish site for a PDF bulletin or publisher link
  retry_when: The parish site adds a Bulletin link or a printed bulletin is seen
bulletin_status: unsupported-format
fetch_gap:
  kind: constant-contact-html-newsletter
  seen: 2026-11-12
  note: St. Jude's weekly bulletin is an HTML Constant Contact email ('New Beginnings - <date>'), linked
    from the site's Newsletters page as 'Current Weekly Newsletter' plus an archive of earlier weeks (myemail.constantcontact.com
    pages, soid 1133232330998); no PDF. The 6 November 2026 issue carries the Mass schedule and weekly
    Mass intentions.
  url: https://myemail.constantcontact.com/New-Beginnings---11-06-2026-.html?soid=1133232330998&aid=nVNZMjepV0g
---

## Publisher

St. Jude, Monroe publishes no PDF bulletin that was found; its weekly bulletin is an HTML email newsletter sent with Constant Contact. The site's Newsletters page (`https://www.stjuderc.org/recent-calendars-and-newsletters`, read 2026-11-12 with visit.py because its links are built in JavaScript) links "Current Weekly Newsletter" to "New Beginnings - 11/06/2026" and the previous week's as "October 30". That issue (read 2026-11-12 with probe get) opens with "Reflection from Fr. Joseph", lists "Mass Intentions for November 7 – November 15" and gives the Mass Schedule: weekday Masses Monday thru Friday 9 am in the main Church; Saturday 4:30 pm; Sunday 7:30, 9:30 and 11:30. Its footer reads "St. Jude Parish | 707 Monroe Turnpike | Monroe, CT 06468 US". It names no other church.

## Worship sites

One church, `st-jude-monroe`. The diocese directory (1395) and GCatholic (22016) list only this church. The newsletter mentions the Sisters of Nazareth in Monroe only as a caroling visit, not a Mass site.

## Website and bulletin provider

`unsupported`, with `fetch_gap` `constant-contact-html-newsletter`: the bulletin is HTML email pages on myemail.constantcontact.com, not a PDF, so no collector reads it. The website is the Newsletters page that links each week's issue. `probe po` found no ParishesOnline org under the guessed slugs `st-jude-church-06468` or `st-jude-parish-06468`. The Duda site's homepage links no bulletin PDF or publisher.

The site's Mass Schedule page gives weekdays Monday-Thursday 9:00 AM, while the 6 November newsletter says Monday thru Friday; the weekend times agree.

## Not yet confirmed

Whether a printed bulletin exists that is not posted online; see `research`.
