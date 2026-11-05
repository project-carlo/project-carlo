---
name: St. Mary
website: https://stmarysdover.org/
bulletin_provider: parishes_online
provider_id: st-mary-church-07801
publication: ['po-org:st-mary-church-07801', 'lpi:0018000000QxAXOAA3', 'po-container:03/1188']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1188/20261101B.pdf
  seen: 2026-11-04
  note: 'Page 1 (image only; rendered with render.py) masthead: ST. MARY''S CHURCH, www.StMarysDover.org,
    973-366-0184, NOVEMBER 01, 2026; Weekend Masses Saturday 5:00 PM Vigil, Sunday 7:30 AM, 9:30 AM, 11:30
    AM; Weekday Monday - Friday 7:00 AM; Mailing Address 425 West Blackwell St., Dover, NJ 07801; GPS
    Address 371 South Main St., Wharton, NJ 07885; Pastor Rev. Lemmuel Camacho. Page 8 text: ''St. Mary
    Church | 03-1188''.'
- url: https://parishesonline.com/organization/st-mary-church-07801
  seen: 2026-11-04
  note: 'probe po: St. Mary Church, 425 W Blackwell St, Dover 07801, website stmarysdover.org, LPi id
    0018000000QxAXOAA3, container 03/1188, latest issue 8 November 2026.'
- url: https://stmarysdover.org/bulletins-1
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic page (site id 6893) linking
    parishesonline.com/publication-page/st-mary-church-07801 issues 03/1188/20261108B.pdf back to 20261018B.pdf
    and 'View Past Bulletins' at the organization page.
bulletin_status: available
---

## Publisher

St. Mary's Church, Wharton/Dover publishes its own weekly bulletin through LPi's ParishesOnline (org `st-mary-church-07801`, container 03/1188). The 1 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1188/20261101B.pdf`) has no text layer except page 8's ad footer "St. Mary Church | 03-1188"; page 1, rendered with render.py on 2026-11-04, is headed "ST. MARY'S CHURCH", "www.StMarysDover.org | 973-366-0184", "NOVEMBER 01, 2026 | ALL SAINTS DAY", with "Pastor | Rev. Lemmuel Camacho".

## Worship sites

- `st-mary-dover`: the only church. Page 1's Mass schedule (Saturday 5:00 PM Vigil; Sunday 7:30 AM, 9:30 AM, 11:30 AM; Monday - Friday 7:00 AM) names no other place, and gives "Mailing Address 425 West Blackwell St., Dover, NJ 07801" and "GPS Address 371 South Main St., Wharton, NJ 07885".

The diocese's finder (directory:6893) and GCatholic (18978) list this one church.

## Website and bulletin provider

`stmarysdover.org` is the parish's eCatholic site (site id 6893), behind Cloudflare (probe url: 403). visit.py read its /bulletins-1 page on 2026-11-04: it embeds the ParishesOnline issues of `st-mary-church-07801` (newest 8 November 2026). Provider `parishes_online`, provider_id the org slug; publication ids from probe po (`po-org`, `lpi`, `po-container`), not the eCatholic site id, since the eCatholic site carries no bulletins of its own. `fetch:check` on 2026-11-04 picked `https://container.parishesonline.com/bulletins/03/1188/20261108B.pdf`, the 8 November 2026 issue posted ahead of that Sunday (freshness "future", age -4 days): the newest issue, which is what fetch should take. Identity is unverified (image-only pages, no expected identity supplied); the masthead was read by hand above.

## Not yet confirmed

Nothing open.
