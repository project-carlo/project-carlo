---
name: Our Lady of Mount Carmel Parish, Altoona
website: https://mountcarmelaltoona.weebly.com
bulletin_provider: discover_mass
provider_id: our-lady-of-mount-carmel-altoona-pa
publication: ['discovermass:our-lady-of-mount-carmel-altoona-pa', 'discovermass:our-lady-of-assumption-altoona-pa']
group: ''
evidence:
- url: https://discovermass.com/church/our-lady-of-mount-carmel-altoona-pa/
  seen: 2026-10-21
  quote: Current Bulletin
  note: 'The church page lists a "Current Bulletin" dated 2026-10-18 (cover class "bulletin-current ...
    2026-10-18") and about a dozen back issues. Its download link (tokenised, not cited) returned a 4-page
    PDF whose page 2 is headed "OUR LADY OF MOUNT CARMEL CHURCH ALTOONA, PENNSYLVANIA  OCTOBER 18, 2026"
    and whose page 1 gives "LITURGYS CHEDULE: Eucharist: Saturday 4:00 p.m. Sunday 8:00 a.m. and1 1:00
    a.m." (text layer garbled; quotes keep the garble). Page 3 prints a Mass-intentions list headed "SUNDAY—MT.
    CARMEL  8 :00 A.M. ... 11:00 A.M." and then "ASSUMPTION CHAPEL  9 :30 A.M. M ary Jane Feigh (Husband,
    John)".'
- url: https://discovermass.com/church/our-lady-of-assumption-altoona-pa/
  seen: 2026-10-21
  quote: Our Lady of Assumption Chapel
  note: 'A second Discover Mass church page, "Our Lady of Assumption Chapel", whose Visit Website link
    is https://mountcarmelaltoona.weebly.com/. Its "Current Bulletin" (cover dated 2026-10-18) downloaded
    as a PDF whose page 1 text is identical to Mount Carmel''s (same 4 pages, same masthead block: "Served
    by theF ranciscans T.O.R. Since1 909 806 11thS treetA ltoona,P A1 6602"). One bulletin under two Discover
    Mass slugs.'
- url: http://mountcarmelaltoona.weebly.com/
  seen: 2026-10-21
  note: http://www.mountcarmelaltoona.com (the directory and GCatholic homepage) 301-redirects here ("Our
    Lady of Mount Carmel - Home"). Weebly answers 429 to curl and probe url; headed Chrome loads it. It
    embeds no bulletin id and no bulletin link, so the bulletin is read from Discover Mass.
promoted: 2026-10-21
---

## Publisher

Our Lady of Mount Carmel Parish, Altoona (Franciscans T.O.R.; pastor Fr. Frank A. Scornaienchi,
TOR) publishes one weekly bulletin on Discover Mass, and Discover Mass carries it under **two
church pages**: `our-lady-of-mount-carmel-altoona-pa` and `our-lady-of-assumption-altoona-pa`
("Our Lady of Assumption Chapel"). On 2026-10-21 both pages listed the issue dated 2026-10-18
(cover id suffix `1792603220` / `1792603221`, one number apart) and the downloaded PDFs had
identical page-1 text (4 pages): the parish masthead block "Served by the Franciscans T.O.R.,
Since 1909, 806 11th Street Altoona, PA 16602, PARISH WEBSITE: www.mountcarmelaltoona.com",
then the pastoral staff and "LITURGY SCHEDULE: Eucharist: Saturday 4:00 p.m., Sunday 8:00 a.m.
and 11:00 a.m." Page 2 is headed "OUR LADY OF MOUNT CARMEL CHURCH ALTOONA, PENNSYLVANIA OCTOBER
18, 2026". Both slugs are recorded as `publication`. One row.

## Worship sites

Two churches, both covered by the one bulletin:

- **Our Lady of Mount Carmel**, 806 11th St (churches/our-lady-of-mount-carmel-altoona).
- **Assumption Chapel**, Hileman St & Adams Ave (churches/assumption-chapel-altoona). The
  bulletin's intentions list for the week of 17-25 October gives "SUNDAY—MT. CARMEL 8:00 A.M.
  ... 11:00 A.M." and then, as its own heading, "ASSUMPTION CHAPEL 9:30 A.M. Mary Jane Feigh",
  matching the directory's Sunday 9:30 AM for the chapel. Page 2 also mentions "collection
  barrels located at the entrances of the Church/Chapel".

The diocese directory lists exactly these two churches for the parish. Nothing else in the
bulletin is a separate worship site.

## Website and bulletin provider

`bulletin_provider: discover_mass`, `provider_id: our-lady-of-mount-carmel-altoona-pa`.
`website` is https://mountcarmelaltoona.weebly.com (the target of the old
mountcarmelaltoona.com that the directory and GCatholic give, and the "Visit Website" link on
the Assumption Chapel Discover Mass page). The Mount Carmel Discover Mass page's own "Visit
Website" link still says http://www.mountcarmelaltoona.com, which redirects to the Weebly site.
The Weebly site (429 to curl) shows no bulletin, so Discover Mass is the channel.

## Not yet confirmed

Nothing about the grouping. Discover Mass caps downloads per IP per day, so `fetch:check` may
report `not_pdf` if the cap has been hit; rerun the next day.
