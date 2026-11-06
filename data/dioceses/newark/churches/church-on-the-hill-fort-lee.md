---
parish: madonna-fort-lee
name: Church on the Hill (historic Church of the Madonna)
line1: Hoefley's Lane
line2: ''
city: Fort Lee
state: NJ
postal_code: '07024'
latitude: 40.86027778
longitude: -73.97888889
coordinates_from: manual
name_verified: false
address_verified: false
roster: []
evidence:
- url: https://container.parishesonline.com/bulletins/03/1309/20261101B.pdf
  seen: 2026-11-03
  note: '1 November 2026 bulletin, page 1 (image, read with render.py): Mass Schedule ''Sundays: 7:30AM,
    10:30AM, 12PM & 11AM at Church on the Hill''. Page 1 also lists ''Cemetery Office 2070 Hoefley''s
    Lane''.'
- url: https://container.parishesonline.com/bulletins/03/1309/20261101B.pdf
  seen: 2026-11-03
  quote: 12 noon Church on the Hill - English
  note: 'Page 4, All Souls Day Masses, 2 November 2026: 10 am Church on the Hill (Korean) and 12 noon
    (English). Page 3 Mass intentions also list Sanctuary Lamps for ''CHURCH ON THE HILL''.'
- url: https://www.madonnachurch.org/
  seen: 2026-11-03
  quote: 11AM (English)- Church on the Hill
  note: Homepage Weekend Masses box (probe get). The site's 'small-chapel-location' popup gives no address.
- url: https://en.wikipedia.org/wiki/Madonna_Church_(Fort_Lee,_New_Jersey)
  seen: 2026-11-03
  quote: The Church of the Madonna is a Catholic church located on Hoefley's Lane in the borough of Fort
    Lee
  note: Gothic Revival church completed 1854, NRHP 1976; article coordinates 40.86028, -73.97889, next
    to the Cemetery of the Madonna (OSM way 41914950).
research:
- method: probe get of the parish homepage and its 'small-chapel-location' page for an address of the
    Church on the Hill
  url: https://www.madonnachurch.org/small-chapel-location
  checked: '2026-11-05'
  outcome: not-found
  next_action: Ask for or find a parish notice (bulletin page 1 or a Christmas/Easter schedule) that gives
    the Church on the Hill's street address; the chapel-location page shows only the parish logo and the
    340 Main Street office
  retry_when: A bulletin or parish page names the building's address
  revisit_after: 2026-12-20
---

## Holds Mass

Yes. The 1 November 2026 bulletin's page 1 schedule lists Sunday '11AM at Church on the Hill', and page 4 lists All Souls Masses there on 2 November at 10 am (Korean) and 12 noon (English). The parish homepage's Weekend Masses box says '11AM (English)- Church on the Hill'.

## Name and address

No parish source gives this building's address, and neither the directory nor GCatholic lists it. I identified it as the parish's original church, the 1854 Church of the Madonna on Hoefley's Lane (Wikipedia; NRHP-listed 1976), which stands on a rise beside the parish's Cemetery of the Madonna (cemetery office '2070 Hoefley's Lane' on page 1 of the bulletin). That 'Church on the Hill' is this building is my inference from the name and the parish's only other property, not a statement in the bulletin. Coordinates are Wikipedia's for the church (40.86028, -73.97889), entered by hand; Nominatim reverse-geocodes them to Church Lane, Fort Lee 07024, inside the cemetery grounds. The name is what the bulletin calls it, with the historic name in brackets. Neither name nor address is verified by two sources.

## Not yet confirmed

The street address and the identification above. A parish page or bulletin notice giving the Church on the Hill's address, or the archdiocese's listing of it, would settle both.
