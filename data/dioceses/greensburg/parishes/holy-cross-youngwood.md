---
name: Holy Cross Parish, Youngwood
website: https://www.holycrossyoungwood.org
bulletin_provider: other
provider_id: dated-post https://www.holycrossyoungwood.org/bulletin/read-our-weekly-bulletin/ filename=[0-9]*.pdf
publication: ['url:https://www.holycrossyoungwood.org/bulletin/read-our-weekly-bulletin/']
group: ''
evidence:
- url: https://www.holycrossyoungwood.org/wp-content/uploads/2026/10/10-25-26-30OT.pdf
  seen: 2026-10-22
  quote: HOLY CROSS CHURCH
  note: 'Page 1 of the 25 Oct 2026 issue (6 pages; post https://www.holycrossyoungwood.org/weekly-bulletin-october-25-2026/):
    "THIRTIETH SUNDAY IN ORDINARY TIME// OCTOBER 25, 2026 //YEAR A", "HOLY CROSS CHURCH", "A word from
    Fr. Rod..."; Mass Times "Saturday (Vigil): 5pm", "Sunday: 8am & 10am", "Monday - Thursday: 8am", "Friday:
    No mass"; "Contact: 711 Depot St. Youngwood, PA 15697 724-925-7811". Names Holy Cross alone.'
- url: https://www.holycrossyoungwood.org/wp-content/uploads/2026/10/10-25-26-30OT.pdf
  seen: 2026-10-22
  quote: Living & Deceased Parishioners of Holy Cross
  note: 'Page 2 MASS INTENTIONS for 24-31 October: Sat 5PM, Sun 8AM and 10AM, Mon-Thu 8AM, "Fri Oct 30
    ***NO MASS***"; no other church or chapel named. Parish Directory column: "Rev. Rogelio Rodriguez,
    Pastor and Trust Administrator".'
- url: https://www.holycrossyoungwood.org/bulletin/read-our-weekly-bulletin/
  seen: 2026-10-22
  note: Diocese-template WordPress page (403 to probe url; curl with a browser User-Agent reads it) listing
    one post per issue, weekly-bulletin-october-25-2026 back to weekly-bulletin-august-23-2026. Each post
    embeds one PDF named MM-DD-YY-<week>OT.pdf (10-25-26-30OT, 10-18-26-29OT, 10-11-26-28OT, 09-27-26-26OT,
    08-23-26-21OT) and the footer links the diocese privacy-policy PDF.
- url: https://parishesonline.com/organization/holy-cross-church-15697
  seen: 2026-10-22
  note: 'probe po: LPi org "Holy Cross Church", 711 Depot St, Youngwood (LPi 0018000000QxC0HAAV) has no
    publications and no container: not a live channel, not recorded.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=309
  seen: 2026-10-22
  note: 'Directory: Holy Cross Parish, 711 Depot Street, Youngwood; pastor Father Rogelio I. Rodriguez;
    "Saturday: 5:00 p.m.; Sunday: 8:00 a.m., 10:00 a.m."; no Partner Parishes listed. Fr. Rodriguez is
    not in the tools'' list of priests serving two or more parishes.'
promoted: 2026-10-23
---

## Publisher

Holy Cross Parish, Youngwood publishes its own weekly bulletin on its diocese-template WordPress site. The
25 October 2026 issue (read 2026-10-22, already posted, `10-25-26-30OT.pdf`) is headed "HOLY CROSS CHURCH",
with a letter from the pastor, Fr. Rogelio ("Rod") Rodriguez, and a Mass schedule and intentions for Holy
Cross alone. The diocese lists no partner parish and Fr. Rodriguez serves no other parish.

## Worship sites

One: Holy Cross church, 711 Depot Street, Youngwood. The bulletin's Mass times (Saturday 5 p.m., Sunday 8 and
10 a.m., Monday to Thursday 8 a.m.) and its intentions name no other place, and neither the diocese nor
GCatholic lists another building for this parish.

## Website and bulletin provider

`website` is the parish's own site. Provider `other`, recipe `dated-post
https://www.holycrossyoungwood.org/bulletin/read-our-weekly-bulletin/ filename=[0-9]*.pdf`: the page lists one
post per issue, each embedding the issue PDF (`MM-DD-YY-<n>OT.pdf`); the filter keeps the footer's
diocese privacy-policy PDF out. `fetch:check` on 2026-10-22 resolved it as "current" and picked
`wp-content/uploads/2026/10/10-25-26-30OT.pdf`, the 25 October issue. The LPi organization
`holy-cross-church-15697` is empty and not recorded.

## Not yet confirmed

Nothing.
