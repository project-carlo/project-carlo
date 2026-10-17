---
name: Most Holy Trinity Parish
website: https://sites.google.com/view/mostholytrinitynepa/bulletin
bulletin_provider: other
provider_id: ''
publication: ['url:https://sites.google.com/view/mostholytrinitynepa/bulletin']
group: Most Holy Trinity Parish Susquehanna
evidence:
- url: https://sites.google.com/view/mostholytrinitynepa/bulletin
  seen: 2026-10-16
  quote: October 18, 2026 Bulletin
  note: The parish's Google Sites "Bulletin" page, which links the current issue as a shared Google Doc
    (https://docs.google.com/document/d/18ujWxlm2oDDbN16oYTV8bTVI-l6ncVaqohnf9IWN50s/edit?usp=sharing).
- url: https://docs.google.com/document/d/18ujWxlm2oDDbN16oYTV8bTVI-l6ncVaqohnf9IWN50s/edit?usp=sharing
  seen: 2026-10-16
  note: '18 October 2026 issue, page 1 masthead: "Most Holy Trinity Parish, October 17-18, 2026—29th Sunday
    in Ordinary Time—Year A", the three churches with addresses (St. John the Evangelist, 15 E. Church
    Street, Susquehanna; St. Lawrence, 380 Franklin Street, Great Bend; St. Martin of Tours, 8175 State
    Route 492, Jackson), "Weekend Mass Schedule: Saturday St. Lawrence''s 4 PM, Sunday St. John''s 8:30
    AM and St. Martin''s 10:30 AM", "Daily Mass 8 AM: Mon.–St. Martin''s, Tues.–IHM Chapel, Wed.–St. Lawrence''s,
    Thurs.–IHM Chapel", Fr. Sudhir Toppo, Administrator. Read by exporting the Google Doc as PDF (docs.google.com/document/d/18ujWxlm2oDDbN16oYTV8bTVI-l6ncVaqohnf9IWN50s/export?format=pdf)
    and rendering it (parish-site-access render.py): the export has no text layer, so recheck cannot find
    this.'
- url: https://discovermass.com/church/st-john-the-evangelist-susquehanna-pa/
  seen: 2026-10-16
  note: Discover Mass page for St. John the Evangelist, Susquehanna lists no bulletins (issues.py).
promoted: 2026-10-17
---

## Publisher

Most Holy Trinity Parish, Susquehanna (one canonical parish, three churches) writes its
weekly bulletin as a Google Doc and links it from its Google Sites page. The 18 October
2026 issue's masthead names the parish and pictures all three churches with their
addresses, gives the weekend and daily Mass schedule for them, and names Fr. Sudhir
Toppo, administrator. The diocese groups it with no other parish. (A 2022 diocesan
posting paired St. Brigid, Friendsville with Most Holy Trinity under one pastor; that has
since changed: St. Brigid is now with Holy Name of Mary, Montrose, and the two bulletins
are separate.)

## Worship sites

Three, all on the 18 October 2026 masthead:

- St. John the Evangelist, Susquehanna (`st-john-the-evangelist-susquehanna`), including
  the "IHM Chapel at St. John's" used for Tuesday and Thursday daily Mass (page 2: "Daily
  Masses: ... Tuesday and Thursday in the IHM Chapel at St. John's"), not a separate row.
- St. Lawrence, Great Bend (`st-lawrence-great-bend`).
- St. Martin of Tours, Jackson (`saint-martin-of-tours-jackson`).

The finder and GCatholic list the same three.

## Website and bulletin provider

The website is the Google Sites "Bulletin" page, which links one Google Doc
(`docs.google.com/document/d/<id>/edit`) titled with the issue date. The Doc exports as PDF
(`/export?format=pdf`, 4 pages) **with no text layer** (the content is images), so the
pipeline has to read it as images; the plain-text export is empty. Not a shared Drive
folder, so `other` rather than `google_drive`; whether the `other` resolver follows a
Google Doc link has not been checked (`fetch:check` after promotion). Discover Mass has an
empty page for St. John's.

## Not yet confirmed

Whether each week's issue is a new Doc or the same Doc overwritten (the page showed one
link on 2026-10-16). The `other` resolver's handling of a Google Doc link.
