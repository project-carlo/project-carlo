---
name: St. Leo Magnus Parish
website: https://stleomagnus.org/weeklybulletin.php
bulletin_provider: other
provider_id: page-pdfs https://stleomagnus.org/weeklybulletin.php
publication: ['url:https://stleomagnus.org/weeklybulletin.php#st-leo-magnus']
group: ''
evidence:
- url: https://stleomagnus.org/images/weeklybulletin/bc046e30bf4816d78d3840fc43046e99.pdf
  seen: 2026-10-23
  note: 'Bulletin for 25 October 2026, the newest on the parish''s Weekly Bulletin page (link text ''October
    25, 2026 Bulletin''; 5 pages, scanned images with no text layer, ''Microsoft: Print To PDF''). Page
    1 rendered: masthead ''St. Leo Magnus Roman Catholic Church ... Faithful Witnesses of Christ''s Gospel
    since 1874'', ''THE THIRTIETH SUNDAY IN ORDINARY TIME OCTOBER 25, 2026'', Pastor ''The Very Reverend
    Justin P. Pino, VF'', and a Mass Schedule box: Saturday Vigil 5:15 pm; Sunday 8:00 am & 10:00 am;
    Daily Tuesday 6:00 pm, Wednesday-Saturday 8:30 am; Holy Day evening before 6:00 pm, on the day 8:30
    am & 12:05 pm. It names this parish alone.'
- url: https://stleomagnus.org/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted template site (weeklybulletin.php). Lists two issues, ''October 25, 2026 Bulletin''
    and ''October 18, 2026 Bulletin'', both scanned-image PDFs (18 Oct created 2026-10-13, 25 Oct created
    2026-10-20). Current: 25 October is the Sunday after the check date.'
- url: https://stleomagnus.org/
  seen: 2026-10-23
  quote: Tuesday 6 p.m.; Wednesday through Saturday 8:30 a.m.
  note: Home page Mass Times box (Saturday 5:15 p.m.; Sunday 8, 10 a.m.), matching the bulletin box and
    the diocese directory.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pino, VF, Very Rev. Justin P.
  note: 'Clergy PDF (8/7/2026): pastor of St. Leo Magnus, Ridgway; his only assignment.'
research:
- method: probe url on the directory website; weeklybulletin_issues.sh; pdftotext (no text layer), pdftoppm
    render of page 1; fetch:check with recipe page-pdfs https://stleomagnus.org/weeklybulletin.php
  url: https://stleomagnus.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: None. The fetch picks the 25 October 2026 issue (transport ok, PDF). Identity and date
    can't be read automatically because every issue is image-only; the pipeline needs image reading for
    this parish.
---

## Publisher

St. Leo Magnus, Ridgway publishes its own weekly bulletin on its diocese-hosted site, stleomagnus.org/weeklybulletin.php, one PDF per issue. The 25 October 2026 issue (rendered page 1) has the masthead 'St. Leo Magnus Roman Catholic Church', the date 'OCTOBER 25, 2026', pastor Very Rev. Justin P. Pino and a Mass Schedule box. It names this parish alone. The PDFs are scanned images (no text layer), so identity and date came from reading the rendered page, not from `fetch:check`.

## Worship sites

One church, St. Leo Magnus at 111 Depot St. The diocese directory lists no mission or secondary church for it and the bulletin's schedule names no other building. Fr. Pino's only assignment in the clergy PDF is this parish.

## Website and bulletin provider

Provider `other` with the recipe `page-pdfs https://stleomagnus.org/weeklybulletin.php`. `fetch:check` picked the 25 October 2026 issue (transport ok, document type PDF, identity and issue date unknown because the PDF has no text layer; freshness is by the link text, which the page lists newest first). The site is not on ParishesOnline or Discover Mass as far as probe url shows (no publications embedded).

## Not yet confirmed

The bulletin's `publication` id is the page URL with a publisher fragment (no ParishesOnline or similar id exists). Whether Discover Mass carries a page for this parish was not checked.
