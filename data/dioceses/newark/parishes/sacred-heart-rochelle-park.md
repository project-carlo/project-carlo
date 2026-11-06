---
name: Sacred Heart, Rochelle Park
website: https://www.wearesacredheart.org/
bulletin_provider: parishes_online
provider_id: sacred-heart-church-07662
publication: ['po-org:sacred-heart-church-07662', 'lpi:0018000000Qc04XAAR', 'po-container:04/0961']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0961/20261101B.pdf
  seen: 2026-11-03
  quote: Sacred Heart Church  |  04-0961
  note: The page-5 and page-6 ad-page footer of the 1 November 2026 issue (6 pages, text layer) names
    the container.
- url: https://container.parishesonline.com/bulletins/04/0961/20261101B.pdf
  seen: 2026-11-03
  quote: Saturday 4PM & 5:30PM
  note: 'Page 1 (NOVEMBER 1, 2026, ALL SAINTS): ''Weekend Masses Saturday 4PM & 5:30PM, Sunday 10AM &
    12PM; Weekday Masses (In Chapel) Monday-Friday 8AM''; Church 12 Terrace Ave, Rochelle Park; Parish
    Center 15 Forest Place; Web: Wearesacredheart.org. No other worship site is named.'
- url: https://parishesonline.com/organization/sacred-heart-church-07662
  seen: 2026-11-03
  note: 'probe po: org ''Sacred Heart Church'', 12 Terrace Ave, Rochelle Park, NJ 07662-3715, website
    wearesacredheart.org, lpi 0018000000Qc04XAAR, container 04/0961. Latest issue 2026-11-08, weekly back
    to 2026-10-04.'
- url: https://www.wearesacredheart.org/
  seen: 2026-11-03
  note: The parish's Weebly site has no bulletin page or bulletin link (its menu lists Home, Livestream
    Masses, Calendar, Sacraments, Ministries, Online Giving and others; the only PDF is a 4 March 2026
    letter from Cardinal Tobin). Checked with probe get and visit.py --bulletin.
bulletin_status: available
---

## Publisher

LPi / ParishesOnline publishes Sacred Heart's bulletin (org sacred-heart-church-07662, container 04/0961). I read the 1 November 2026 issue (6 pages, text). Page 1 is headed "NOVEMBER 1, 2026 ALL SAINTS" and gives the church at 12 Terrace Ave, Rochelle Park, the parish center at 15 Forest Place, and Wearesacredheart.org; the page-5 and page-6 footers read "Sacred Heart Church | 04-0961". (The page-1 text layer also carries a stray "March 15, 2026 4th Sunday of Lent" from the template; the issue's own date line is November 1.)

## Worship sites

There is one church, `sacred-heart-rochelle-park`. Page 1 gives weekend Masses Saturday 4 PM and 5:30 PM and Sunday 10 AM and 12 PM, and weekday Masses "In Chapel" Monday to Friday 8 AM. I take the chapel to be at the parish (the bulletin gives no other address for it); no other place is named. The archdiocese directory (178) and GCatholic (18546) each list only this church.

## Website and bulletin provider

The website is the directory's https://www.wearesacredheart.org/, which the ParishesOnline org also names. The site itself has no bulletin link (see evidence), so the bulletin was found through the ParishesOnline org. GCatholic's http://www.sacredheartrp.org answered HTTP 5xx in visit.py (2026-11-03). The provider is `parishes_online`, read by the org slug.

Fetch check (2026-11-03, headed): transport ok, PDF. Through the ParishesOnline provider id it picked container 04/0961's 8 November 2026 issue (20261108B.pdf, posted ahead of the Sunday), the newest the org lists. Its issue date reads `conflict` and freshness `unknown` because the text layer carries both "NOVEMBER 8, 2026" and the stray template date "March 15, 2026" (the same stray line is on page 1 of the 1 November issue); the file name and the issue's own date line agree on 8 November, so the pick is the current bulletin. Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Nothing open.
