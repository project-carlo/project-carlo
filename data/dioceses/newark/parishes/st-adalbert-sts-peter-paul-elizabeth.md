---
name: St. Adalbert and Sts. Peter & Paul, Elizabeth
website: https://www.stadalbert.us/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:12332']
group: ''
evidence:
- url: https://files.ecatholic.com/12332/bulletins/20261108.pdf
  seen: 2026-11-05
  note: 'Text layer is an unreadable font encoding; pages 1, 2 and 4 rendered. Every page is headed ''St.
    Adalbert and Ss. Peter & Paul Parish'' with the footer ''November 8th, 2026 Thirty-Second Sunday in
    Ordinary Time''. Page 4 (Mass Intentions) has two columns: ''Ss. Peter & Paul Church Week of November
    8th, 2026'' with ''November 8th, 2026 9:30 AM'' and ''November 15th, 2026 9:30 AM'', and ''St. Adalbert
    Church'' with Saturday 5:30 PM, Sunday 8:00 AM, 10:00 AM, 12:00 PM and Monday-Saturday 8:00 AM.'
- url: https://www.stadalbert.us/
  seen: 2026-11-05
  note: 'eCatholic site (visit.py; probe url gets 403). MASS TIMES: Monday to Saturday 8:00 am (English/Polish);
    Sunday 5:30 pm Saturday Vigil (English), 8:00 am (Polish), 10:00 am (Polish), 12:00 pm (English).
    Administrative office 250 East Jersey Street, Elizabeth, NJ 07206. Menu links a ''Peter&Paul Church''
    page (https://www.stadalbert.us/sts-peter-paul-church) and a Sts. Peter & Paul office contact page;
    Bulletins page https://www.stadalbert.us/bulletins.'
- url: https://rcan.org/parishes/
  seen: 2026-11-05
  note: 'Archdiocese directory entry 37: St. Adalbert/Ss. Peter & Paul Parish, 250 E Jersey Street, Elizabeth,
    website https://www.stadalbert.us/st-adalbert.'
bulletin_status: available
---

## Publisher

The parish posts its own bulletin on eCatholic (site id 12332, `files.ecatholic.com/12332/bulletins/<yyyymmdd>.pdf`). I read the 8 November 2026 issue (4 pages). Its text layer is an unreadable font encoding, so I rendered pages 1, 2 and 4: each is headed "St. Adalbert and Ss. Peter & Paul Parish" with the footer "November 8th, 2026 Thirty-Second Sunday in Ordinary Time". The bulletin is in English and Polish.

## Worship sites

Two churches, both in the page-4 Mass intentions of the 8 November 2026 issue:

- `st-adalbert-elizabeth`: "St. Adalbert Church", Saturday 5:30 PM, Sunday 8:00, 10:00 AM and 12:00 PM, Monday-Saturday 8:00 AM (the parish site gives the same times).
- `sts-peter-paul-elizabeth`: "Ss. Peter & Paul Church", Sunday 9:30 AM (8 and 15 November).

St. Adalbert (Polish) and Sts. Peter and Paul (Lithuanian) are one canonical parish. The directory (37) lists them as one parish and GCatholic lists both churches (18391, 18397). The site's own page for Sts. Peter & Paul Church tells its Lithuanian founding history and gives only the 250 East Jersey Street office address.

## Website and bulletin provider

https://www.stadalbert.us/ is the eCatholic site (Cloudflare: `probe url` gets 403, `visit.py` reads it). The directory links its `/st-adalbert` subpage and GCatholic links http://www.stadalbert.us; I recorded the homepage. Provider `ecatholic`, publication `ecatholic:12332`. The site also posts weekly Mass-intention PDFs under `files.ecatholic.com/12332/documents/`, which are not the bulletin.

Fetch check (2026-11-05, headed): transport ok, PDF; the eCatholic resolver read https://www.stadalbert.us/bulletins and picked `files.ecatholic.com/12332/bulletins/20261108.pdf`, the 8 November 2026 issue read above (date inferred from the URL); freshness `future` (the coming Sunday). Identity `unverified` only because no expected identity is supplied; the rendered pages confirm it.

## Not yet confirmed

The bulletin's text layer can't be read, so the pipeline has to read it as images. Nothing else is open.
