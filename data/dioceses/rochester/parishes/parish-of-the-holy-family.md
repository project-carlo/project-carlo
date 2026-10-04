---
name: The Parish of the Holy Family
website: https://theparishoftheholyfamily.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:32186']
group: ''
evidence:
- url: https://files.ecatholic.com/32186/bulletins/20260927.pdf
  seen: 2026-10-02
  quote: 'Address: 4100 Lyell Road, Rochester, New York, 14606'
  note: 'Page 2 of the 27 September 2026 issue (the 4 October issue, 20261004.pdf, is also posted). The
    bulletin has a single "Location Key" (CH- Church, PLC- Parish Life Center, LIB, MH- Office Building):
    one campus, no second church.'
- url: https://files.ecatholic.com/32186/bulletins/20260927.pdf
  seen: 2026-10-02
  quote: Location Key CH- Church PLC– Parish Life Center
- url: https://theparishoftheholyfamily.org/bulletins
  seen: 2026-10-02
  note: 'Behind Cloudflare to curl (403), read with visit.py: the page embeds ecatholic site id 32186
    (eCatholic-hosted site on the custom domain). Home page: "Weekend MASSES: Saturday: 4:00PM Sunday:
    9:00AM-Live Streamed Sunday: 5:00PM", "Saturday: 8:00AM Vietnamese Mass Sunday: 11:30AM Vietnamese
    Mass".'
- url: https://ps.dor.org/directory/parish-of-the-holy-family/
  seen: 2026-10-02
  quote: Sunday 9AM, 11:30AM (Vietnamese/Bilingual Mass) 5PM
  note: 'Diocesan Directory of Parishes (updated 1/27/25): one address, 4100 Lyell Road, one Mass schedule.'
promoted: 2026-10-02
---

## Publisher

The Parish of the Holy Family (Gates) publishes one weekly bulletin on eCatholic, site id 32186 (`files.ecatholic.com/32186/bulletins/YYYYMMDD.pdf`). I read the 27 September 2026 issue: it gives the office address as 4100 Lyell Road, Rochester 14606, with Masses on Saturday 4:00 PM (and 8:00 AM Vietnamese), Sunday 9:00 AM, 11:30 AM (Vietnamese) and 5:00 PM, weekdays 9:00 AM and the Vietnamese 6:00 PM. Its Location Key lists only a church, a Parish Life Center, a library and an office building, i.e. one campus.

## Worship sites

One: `churches/holy-family.md`, the church at 4100 Lyell Road. The building is St. Jude the Apostle (GCatholic 17809, the Parish Locator's "St. Jude", OpenStreetMap). The parish was formed from the "Gates Catholic Community" cluster of St. Jude, Holy Ghost and St. Helen. The other two are closed: `excluded/holy-ghost-gates.md` (250 Coldwater Rd) and `excluded/st-helen-gates.md` (310 Hinchey Rd). Both appear in the Locator with "Mass: closed" and in GCatholic with the old cluster website; the parish announced their closing for 30 June 2020. The parish site's "Holy Ghost Cemetery" page is a cemetery page, not a worship site.

## Website and bulletin provider

`theparishoftheholyfamily.org` answers curl with 403 (Cloudflare) but loads in a real browser: an eCatholic-hosted site (footer "powered by eCatholic®"), and its page embeds site id 32186, so `bulletin_provider: ecatholic` with the website is right. `provider_id` stays empty (eCatholic reads from the website). `issues.py ecatholic ecatholic:32186` finds the issues of 27 September and 4 October 2026.

## Not yet confirmed

Nothing.
