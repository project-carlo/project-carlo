---
name: St. Joseph the Carpenter, Roselle
website: https://parishesonline.com/organization/st-joseph-the-carpenter
bulletin_provider: parishes_online
provider_id: st-joseph-the-carpenter
publication: ['po-org:st-joseph-the-carpenter', 'lpi:0018000000Qc1V7AAJ', 'po-container:04/0041']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0041/20261108B.pdf
  seen: 2026-11-05
  quote: 160 East 3rd Avenue
  note: '8 November 2026 issue (5 pages, text). Page 1: ''Parish Office 157 East 4th Ave. • Roselle, NJ'';
    ''Rev. Leandro N. Torres Mas—Pastor''; ''Website: www.stjosephroselle.com''; Mass Schedule: daily
    (Mon-Sat) 7:30 AM; Saturday Vigil 5:00 PM, 7:00 PM in Spanish; Sunday 7:30 AM, 9:00 AM in Spanish,
    10:30 AM & 12:00 PM; ''Church Location St. Joseph the Carpenter Church 160 East 3rd Avenue Roselle,
    New Jersey 07203''. One church.'
- url: https://parishesonline.com/organization/st-joseph-the-carpenter
  seen: 2026-11-05
  note: 'probe po: St. Joseph the Carpenter, 157 E 4th Ave, Roselle, New Jersey, 07203-2004; lpi 0018000000Qc1V7AAJ;
    container 04/0041; website https://www.stjosephroselle.com; latest issues 2026-11-08, 11-01, 10-25,
    10-18.'
- url: https://www.stjosephroselle.com/
  seen: 2026-11-05
  note: 'Directory website. probe url and visit.py: HTTP 200, title ''Temporarily Unavailable'', text
    ''Unfortunately, this site is temporarily unavailable.'' (the LPi WeConnect lapse page).'
- url: http://web.archive.org/web/20260617232044id_/https://www.stjosephroselle.com/
  seen: 2026-11-05
  note: 'Last Wayback capture in the CDX (2026-06-17): a WeConnect site titled ''Church of Saint Joseph
    the Carpenter'' linking https://parishesonline.com/publication-page/st-joseph-the-carpenter and container
    04/0041 issues to 20260614B.pdf.'
research:
- method: probe url and visit.py on the directory website; Wayback CDX for its homepage
  url: https://www.stjosephroselle.com/
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reopen the site; if it is back and links the PO org, set it as the website
  retry_when: stjosephroselle.com no longer shows the 'Temporarily Unavailable' page, or a later masthead
    names a different website
  revisit_after: 2027-02-01
bulletin_status: available
---

## Publisher

St. Joseph the Carpenter, Roselle, publishes a weekly bulletin with LPi (ParishesOnline org `st-joseph-the-carpenter`, container 04/0041). I read the 8 November 2026 issue (5 pages, text): page 1 gives the parish office at 157 East 4th Ave., pastor Rev. Leandro N. Torres Mas, one Mass schedule in English and Spanish, and 'Church Location St. Joseph the Carpenter Church 160 East 3rd Avenue'. No other church is named.

## Worship sites

- St. Joseph the Carpenter Church (`st-joseph-the-carpenter-roselle`): daily (Monday-Saturday) 7:30 AM; Saturday vigil 5:00 PM and 7:00 PM in Spanish; Sunday 7:30 AM, 9:00 AM in Spanish, 10:30 AM and 12:00 PM (page 1, 8 November 2026).

The directory (180) and GCatholic (18548) list only this church. The parish school (St. Joseph the Carpenter School, principal on page 1) is not a worship site.

## Website and bulletin provider

The directory and the masthead give www.stjosephroselle.com, and the PO org gives the same. It now shows LPi WeConnect's 'Temporarily Unavailable' page (probe url and visit.py, 2026-11-05); its last Wayback capture (2026-06-17) was the WeConnect site linking this container's issues. GCatholic's stjosephsroselle.org does not resolve (probe url DEAD-DNS, 2026-11-05). The bulletin itself is current on ParishesOnline, so `website` is the PO org page and the provider is `parishes_online` with the org slug as `provider_id`.

Fetch check (2026-11-05, headed): transport ok, PDF, picked container 04/0041's `20261108B.pdf`, the 8 November 2026 issue read above; freshness `future` (age -3 days) because the issue is dated the coming Sunday. Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Whether stjosephroselle.com comes back (structured research holds the retry trigger). It does not affect the bulletin.
