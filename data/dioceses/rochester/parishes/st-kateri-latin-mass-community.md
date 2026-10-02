---
name: St. Kateri Tekakwitha Latin Mass Community
website: https://www.skt-lmc.org
bulletin_provider: other
provider_id: ''
publication:
- url:https://www.skt-lmc.org/our-parish/latest-bulletins-and-notices/
group: Saint Kateri Tekakwitha
evidence:
- url: https://www.skt-lmc.org/wp-content/uploads/2026/09/2026-09-27_18thSun_Web.pdf
  seen: '2026-10-02'
  quote: "ST. KATERI TEKAKWITHA \nLATIN MASS COMMUNITY \nST. THOMAS THE APOSTLE CHURCH"
  note: 'Masthead, page 1 of the issue filed as 2026-09-27_18thSun_Web.pdf (12 pages). Its page 1 date
    line reads "SEPTEMBER 20, 2026" over "Twenty-sixth Sunday in Ordinary Time", which is 27 September:
    a typo carried over from the previous week. The 4 October issue (2026-10-04_19thaftPent_Web.pdf) is
    up and reads "OCTOBER 4, 2026".'
- url: https://www.skt-lmc.org/wp-content/uploads/2026/09/2026-09-27_18thSun_Web.pdf
  seen: '2026-10-02'
  quote: MASS TIMES Sundays 9:00am-English, 11:15am-Latin
  note: 'Page 9 (contact page): "LOCATION 4536 St. Paul Boulevard, Rochester NY 14617", "MAILING ADDRESS
    / OFFICE St. Kateri Parish, 445 Kings Highway South", "CONFESSION Sundays before & after 11:15 am
    Mass".'
- url: https://www.skt-lmc.org/our-parish/latest-bulletins-and-notices/
  seen: '2026-10-02'
  note: 'Bulletins page (WordPress): one PDF per Sunday under /wp-content/uploads/<year>/<month>/, newest
    "2026-10-04_19thaftPent_Web.pdf" then 2026-09-27_18thSun_Web.pdf, 2026-09-20_17th_Web.pdf. Read with
    visit.py --bulletin ("bulletin PDFs but no publisher id: looks self-hosted").'
- url: https://www.skt-lmc.org/
  seen: '2026-10-02'
  quote: Sunday Mass | English 9:00 AM | Latin 11:15 AM
  note: 'Home page: "Latin Mass Community at St. Thomas the Apostle Church in Irondequoit on St. Paul
    Boulevard ... Ordinary Form of the Mass at 9am and the Extraordinary Form at 11:15 every Sunday";
    Adoration Chapel open Monday to Friday 9 am to 10 pm.'
---

## Publisher

The St. Kateri Tekakwitha Latin Mass Community, which worships at St. Thomas the Apostle Church on St. Paul Boulevard in Irondequoit, publishes its own 12-page weekly bulletin on its own website (skt-lmc.org). The masthead is "St. Kateri Tekakwitha Latin Mass Community, St. Thomas the Apostle Church" and the contact page gives the Mass times (Sundays 9:00 am English, 11:15 am Latin) and the location. The community is part of St. Kateri Tekakwitha parish (its office is the parish's, 445 Kings Highway South; it appears in the parish's directory listing and in a box on the parish bulletin), but the parish's ParishesOnline bulletin (`st-kateri-tekakwitha`, container 06/0078) prints none of St. Thomas's Mass times, only "Visit: www.skt-lmc.org". The two bulletins are different publications (different host, masthead, content), so by the one-row-one-bulletin rule this is its own row, with `group: Saint Kateri Tekakwitha`. It is not a merge: the parish's own channel is alive.

## Worship sites

One: `churches/st-thomas-apostle.md` (4536 St. Paul Boulevard), moved here from `st-kateri-tekakwitha`. The locator's "Latin Mass Community" entry (`directory:357-latin-mass-community`, "Mass: Sun, 9:00am Mass (in English) | 11:15am Mass (in Latin) at St. Thomas the Apostle Church", skt-lmc.org) is linked to it. The `skt-lmc.org` site's address (4536 St. Paul Blvd) is the same building as the church record, so lead hypothesis confirmed: the community's church and the roster's St. Thomas the Apostle are one place.

## Website and bulletin provider

`www.skt-lmc.org` (WordPress, no Cloudflare) is alive. The "Bulletins" page lists one PDF per Sunday, so `other` reading the website's bulletin link works; the publication id is the bulletins page.

## Not yet confirmed

Nothing; I read the 27 September issue's text and the 4 October masthead.
