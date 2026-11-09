---
name: St. Joseph of the Holy Family
website: https://stjosephsharlem.com/bulletin/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://stjosephsharlem.com/bulletin/', 'po-org:st-joseph-of-the-holy-family-church',
  'lpi:0018000000QxALhAAN']
group: ''
evidence:
- url: https://stjosephsharlem.com/wp-content/uploads/2026/02/Bulletin-2026-Week-5-OT-PRINT.pdf
  seen: 2026-11-08
  quote: February 8th, 2026
  note: The newest bulletin PDF in the site's media library (uploaded 2026-02-09), page 3; the only other
    bulletin uploads are the Week 3 issues of January 2026.
- url: https://stjosephsharlem.com/bulletin/
  seen: 2026-11-08
  note: The site's Bulletin page links no PDF and lists no issues; the October 2026 uploads are All Saints
    flyers, not bulletins.
- url: https://stjosephsharlem.com/mass-schedule/
  seen: 2026-11-08
  quote: French Mass, 2:00 PM
  note: 'Current Mass schedule: Monday-Saturday 9:00 AM; Sunday Children''s Mass 8:30 AM, Gospel 10:00
    AM, Spanish 12:00 PM, French 2:00 PM; Saturday vigil 5:30 PM.'
- url: https://parishesonline.com/organization/st-joseph-of-the-holy-family-church
  seen: 2026-11-08
  note: 'probe po: LPi 0018000000QxALhAAN, no publications.'
revisit: Check https://stjosephsharlem.com/bulletin/ and the WordPress media library (wp-json/wp/v2/media?mime_type=application/pdf)
  for a bulletin newer than February 2026.
revisit_after: 2027-01-08
research:
- method: probe get of /bulletin/ and the WordPress media and search APIs; probe po of the ParishesOnline
    org
  url: https://stjosephsharlem.com/wp-json/wp/v2/media?mime_type=application/pdf
  checked: '2026-11-08'
  outcome: not-found
  next_action: Recheck the Bulletin page and the media library for a current issue
  retry_when: A bulletin PDF newer than February 2026 is uploaded or linked
  revisit_after: 2027-01-08
bulletin_status: not-found
---

## Publisher

St. Joseph of the Holy Family, 405 West 125th Street in Harlem, has posted bulletins only occasionally: the site's media library (read November 8, 2026) holds Week 3 and Week 5 of Ordinary Time 2026 (the latter dated February 8th, 2026, uploaded February 9), and nothing later, while its Bulletin page lists no issue. ParishesOnline has an organization for it with no publications. No current bulletin was found, so the row is `no_bulletin`, kept in the records and off the site.

## Worship sites

One: St. Joseph of the Holy Family, 405 West 125th Street (`churches/st-joseph-of-the-holy-family-new-york-city.md`). The Mass schedule page (November 8) gives Monday-Saturday 9:00 AM; Saturday vigil 5:30 PM; Sunday 8:30 AM (children's), 10:00 AM (Gospel), 12:00 PM (Spanish) and 2:00 PM (French). This is not the St. Joseph on Monroe Street.

## Website and bulletin provider

The website is the parish's Bulletin page. The February 2026 PDFs were never linked from it in a form a collector could follow week by week.

## Not yet confirmed

Whether the parish prints a weekly bulletin it doesn't post.
