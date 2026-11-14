---
name: Our Lady of Guadalupe (Dyker Heights)
website: https://www.olguadalupe-brooklyn.com/sunday-bulletin
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery B9 (Brooklyn West)
evidence:
- url: https://www.olguadalupe-brooklyn.com/_files/ugd/8a6077_2ff89e8535984cb0aae5647ec568cd95.pdf
  seen: 2026-11-06
  quote: 7201-15th Avenue
  note: '8 November 2026 issue (Thirty-second Sunday in Ordinary Time), 11 pages, text layer. Page 1 masthead:
    OUR LADY OF GUADALUPE Roman Catholic Church, 7201-15th Avenue, Brooklyn, New York 11228; Pastor Monsignor
    Robert J. Romano; Mass schedule Monday to Friday 8:30 am, Saturday 8:30 am, 5:30 pm, 7:00 pm (spanish),
    Sunday 8:00 am, 9:00 am (italian), 11:15 am. No other church is named. No LPi, John Patrick or Church
    Bulletin Inc. footer (grep 03-, LPi): self-made.'
- url: https://www.olguadalupe-brooklyn.com/sunday-bulletin
  seen: 2026-11-06
  note: 'Wix blog index (read with parish-site-access visit.py): ''Our Sunday Bulletin is a weekly publication…'';
    archive November 2026 (1 post), October 2026 (5), September 2026 (6) and back to December 2025; newest
    post ''Thirty-second Sunday in Ordinary Time, November 8, 2026''.'
- url: https://www.olguadalupe-brooklyn.com/post/thirty-second-sunday-in-ordinary-time-2
  seen: 2026-11-06
  quote: OLG Bulletin 11-8-2026
  note: The post holds a file widget 'OLG Bulletin 11-8-2026 .pdf Download PDF • 16.46MB'; clicking it
    (tools/click-requests.py) downloaded download-files.wixmp.com/ugd/8a6077_2ff89e8535984cb0aae5647ec568cd95.pdf.
research:
- method: fetch:check (headed Chrome) on website https://www.olguadalupe-brooklyn.com/sunday-bulletin,
    provider other
  url: https://www.olguadalupe-brooklyn.com/sunday-bulletin
  checked: '2026-11-06'
  outcome: unsupported-format
  next_action: When a collector reads Wix blog file widgets, set provider other with its recipe and rerun
    fetch:check
  retry_when: A collector for fetch_gap kind wix-blog-file-download lands
bulletin_status: unsupported-format
fetch_gap:
  kind: wix-blog-file-download
  seen: 2026-11-06
  note: 'Each issue is a Wix blog post (/post/<slug>) under /sunday-bulletin with a Ricos file widget
    (''OLG Bulletin 11-8-2026.pdf, Download PDF''). The page HTML has no PDF link: the file URL comes
    from /_api/communities-blog-node-api/v2/media/download-url on click (download-files.wixmp.com/ugd/<id>.pdf?token=...).
    The same file is public at /_files/ugd/<id>.pdf once the id is known. fetch:check: ''No PDF links
    found on bulletin page''.'
  url: https://www.olguadalupe-brooklyn.com/post/thirty-second-sunday-in-ordinary-time-2
---

## Publisher

Our Lady of Guadalupe, Dyker Heights publishes its own weekly bulletin (no LPi, John Patrick or Church Bulletin Inc. footer), posted as a PDF attached to a Wix blog post each week. The 8 November 2026 issue (read 2026-11-06, 11 pages) has on page 1 "OUR LADY OF GUADALUPE Roman Catholic Church, 7201-15th Avenue, Brooklyn, New York 11228", with Monsignor Robert J. Romano, Pastor.

## Worship sites

One. The page 1 Mass schedule gives Monday to Friday 8:30 am; Saturday 8:30 am, 5:30 pm and 7:00 pm (Spanish); Sunday 8:00 am, 9:00 am (Italian) and 11:15 am, with no other church. A grep of the issue for "Rosalia" found nothing. The directory, the deanery list, GCatholic 16634 and Mass finder 1130 all give the one church at 7201 15th Avenue.

## Website and bulletin provider

`unsupported`, `fetch_gap` kind `wix-blog-file-download`. The website is the Wix blog index `/sunday-bulletin`; each issue is a post whose file widget gets its download URL from a Wix API only on click, so `fetch:check` finds no PDF links (2026-11-06). Once the file id is known, `/_files/ugd/<id>.pdf` serves it publicly. No publication id: the bulletin is self-made.

## Not yet confirmed

Nothing about the bulletin or church; only a collector is missing (see research).
