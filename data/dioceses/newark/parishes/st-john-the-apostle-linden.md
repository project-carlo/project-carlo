---
name: St. John the Apostle, Linden
website: https://www.sjanj.net/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://www.sjanj.net/bulletin/ filename=20??????-*.pdf
publication: ['url:https://www.sjanj.net/bulletin/']
group: ''
evidence:
- url: https://www.sjanj.net/wp-content/uploads/2026/11/20261108-Thirty-Second-Sunday-in-Ordinary-Time.pdf
  seen: 2026-11-05
  note: '8 November 2026 issue, 6 pages, read as browser screenshots (parish-site-access visit.py; the
    probe proxy gets ''Remote end closed connection''). Page 1 cover: ''Saint John the Apostle Roman Catholic
    Church'', ''THIRTY SECOND SUNDAY IN ORDINARY TIME NOVEMBER 08, 2026'', ''1805 PENBROOK TERRACE, LINDEN
    NJ 07036 (908) 486-6363 | SJANJ.NET''. Page 2: ''Pastor Rev. Mauro Primavera''; ''Sunday Mass Schedule
    Saturday 5:30pm Sunday 8:00am, 10:00am, 12:00pm''; ''Daily Mass Schedule Monday - Friday 7:00am &
    8:30am''. One church; no printer''s footer (a parish-made bulletin).'
- url: https://www.sjanj.net/bulletin/
  seen: 2026-11-05
  note: 'Bulletin page (visit.py): newest first, 20261108-Thirty-Second-Sunday-in-Ordinary-Time.pdf, 20261101-…,
    20261025-…, 20261018-… under wp-content/uploads/2026/; the only other PDFs are the footer''s Harassment
    and Whistleblower policies (2024/02).'
- url: https://www.sjanj.net/
  seen: 2026-11-05
  quote: Saturday 5:30p || Sunday 8a | 10a | 12p
  note: 'Homepage: ''Daily Mass Schedule Monday – Friday 7a | 8:30a || Saturday 8:30a''; ''Address: 1805
    Penbrook Terrace, Linden, NJ 07036''; ''Adoration Chapel … Open 24/7''. probe url reports UNREACHABLE
    (proxy EOF, possibly IPv6-only); visit.py reads it.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. John the Apostle, Linden, makes its own weekly bulletin and posts it on its WordPress site's bulletin page, one dated PDF per Sunday (`20261108-Thirty-Second-Sunday-in-Ordinary-Time.pdf`, newest first). I read the 8 November 2026 issue (6 pages) as browser screenshots: page 1 is 'Saint John the Apostle Roman Catholic Church … November 08, 2026, 1805 Penbrook Terrace, Linden NJ 07036'; page 2 names pastor Rev. Mauro Primavera and one Mass schedule. No publisher's footer.

## Worship sites

- St. John the Apostle Church (`st-john-the-apostle-linden`): Saturday 5:30 PM; Sunday 8:00, 10:00 AM, 12:00 PM; Monday-Friday 7:00 and 8:30 AM; Saturday 8:30 AM (bulletin page 2 and homepage, 2026-11-05). The 24/7 Adoration Chapel is on the parish grounds, not a separate Mass site.

The directory (102) and GCatholic (18465) list only this church. The homepage also links www.sjanj.org (not read; presumably the parish school, inferred from the menu).

## Website and bulletin provider

`other`, reading `page-pdfs` on the bulletin page with a filter on the issues' `YYYYMMDD-` names so the policy PDFs in the footer are never picked. The probe proxy can't reach sjanj.net (UNREACHABLE / RemoteDisconnected, 2026-11-05); the browser can.

Fetch check (2026-11-05, headed): resolved 'page-pdfs on https://www.sjanj.net/bulletin/: current', transport ok, PDF (16 MB), picked `20261108-Thirty-Second-Sunday-in-Ordinary-Time.pdf`, the issue read above; freshness `future` (age -3 days). Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Nothing open. Page 1 is an image; I did not check how much of the issue has a text layer (the probe proxy cannot download it).
