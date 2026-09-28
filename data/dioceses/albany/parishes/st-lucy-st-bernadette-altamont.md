---
name: St. Lucy/St. Bernadette Catholic Church
website: https://www.stlstb.org/bulletin
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stlstb.org/bulletin']
group: ''
evidence:
- url: https://drive.google.com/uc?export=download&id=10JOEDCmgct7QoS4BUR83k_CaZ9ntyHNT
  seen: 2026-09-28
  quote: St. Lucy/St. Bernadette Catholic Church Twenty-Third Sunday in Ordinary Time 109 Grand St. Altamont,
    NY 12009
  note: Masthead, page 1 of the 6 September 2026 issue (the newest linked on the parish's Bulletin page
    on 2026-09-28), a PDF in Google Drive; "Rev. Matthew Duclos, Pastor".
- url: https://www.stlstb.org/bulletin
  seen: 2026-09-28
  quote: September 6, 2026
  note: The parish's Google Sites Bulletin page (visit.py, 2026-09-28). It lists one link per Sunday from
    25 January to 6 September 2026, each to a separate Google Drive file (drive.google.com/file/d/<id>/view),
    not to a shared folder.
revisit: Check stlstb.org/bulletin has issues after 6 September 2026, and whether the pipeline's other
  fetcher reads its Drive file links.
revisit_after: 2026-10-26
---

## Publisher

St. Lucy/St. Bernadette, Altamont, publishes its own weekly bulletin as PDFs in Google
Drive, linked from its Google Sites page. The newest listed on 2026-09-28 is 6 September
2026: masthead "St. Lucy/St. Bernadette Catholic Church, 109 Grand St. Altamont, NY 12009",
Rev. Matthew Duclos, Pastor, with one Sunday Mass ("Sunday September 6 9 am Mass" in the
weekly calendar).

Fr. Duclos is also pastor of St. Thomas the Apostle, Delmar, and St. Matthew's,
Voorheesville, lists both with Christ the King (Albany) as its "Network of Parishes". St.
Thomas publishes its own, separate bulletin (eCatholic 16575) and St. Matthew's its own
(ParishesOnline 03/0766), so this is its own row.

## Worship sites

One: `st-lucy-st-bernadette-altamont`. The diocese and GCatholic list one site.

## Website and bulletin provider

The diocese's link (parishes.rcda.org/StLucyStBernadetteChurch/) redirects to stlstb.org, a
Google Sites page, whose Bulletin page lists the issues. Each link is a single Drive file,
not a shared folder, so `google_drive` (which reads a folder) does not fit; the row is
`other`, with the Bulletin page as website and publication. The files download without a
browser through `drive.google.com/uc?export=download&id=<id>`.

## Not yet confirmed

Whether the `other` fetcher follows Drive file-view links (the page has no .pdf links);
flagged in the region notes. The page lagged three weeks behind on 2026-09-28 (newest 6
September), so the parish posts irregularly.
