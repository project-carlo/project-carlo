---
name: St. Andrew Kim Korean Catholic Church, Maplewood
website: https://www.ilovesak.org/v2/jubo/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.ilovesak.org/v2/jubo/']
group: ''
evidence:
- url: https://www.ilovesak.org/v2/jubo/
  seen: 2026-11-04
  quote: November 1 Weekly Bulletin (English)
  note: 'The parish''s bulletin board (주보), newest first: posts 602 ''[2026] 11월 1일 주보 (한글)'', 601 ''November
    1 Weekly Bulletin (English)'', 600 ''10월 25일 주보 (한글)'', 599 ''October 25 Weekly Bulletin (English)''
    … one Korean and (most weeks) one English post per Sunday.'
- url: https://www.ilovesak.org/v2/jubo/?vid=601
  seen: 2026-11-04
  note: The English post for 1 November 2026 shows three JPEGs, uploads/mangboard/2026/10/29/F3673_Slide1.jpeg,
    F3674_Slide2.jpeg and an advertising page; no PDF. Post 602 (Korean) shows '2026.11.01 한국어 주보-1…3'
    JPEGs.
- url: https://www.ilovesak.org/v2/wp-content/uploads/mangboard/2026/10/29/F3673_Slide1.jpeg
  seen: 2026-11-04
  note: 'Page 1 of the English 1 November 2026 issue (an image; recheck can''t find text): masthead ''SAINT
    ANDREW KIM KOREAN CATHOLIC CHURCH, 280 Parker Ave. Maplewood, NJ 07040, www.ilovesak.org'', ''November
    1, 2026: SOLEMNITY OF ALL SAINTS'', pastor Rev. Paul Kyung Lee, and one MASS SCHEDULE (Main Church,
    Augustine Chapel, Small Chapel) naming no other parish or address.'
- url: https://www.ilovesak.org/v2/
  seen: 2026-11-04
  note: 'probe url: WordPress site, no publisher links; its one PDF is a 50th-anniversary booklet (50anniversary/WWJ.pdf).
    The media API lists no PDFs (wp-json/wp/v2/media?mime_type=application/pdf returned []).'
research:
- method: visit of the jubo board and its newest posts; fetch:check with page-images on the board page
  url: https://www.ilovesak.org/v2/jubo/
  checked: '2026-11-04'
  outcome: unsupported-format
  next_action: Pin a collector that opens the newest English post on the board and keeps its Slide JPEGs,
    then run fetch:check
  retry_when: A collector for image bulletins inside board posts lands (fetch_gap board-post-images)
bulletin_status: unsupported-format
fetch_gap:
  kind: board-post-images
  seen: 2026-11-04
  note: 'Each week''s bulletin is a post on the site''s MangBoard board (/v2/jubo/?vid=<n>), one in English
    and one in Korean, whose pages are JPEG images (wp-content/uploads/mangboard/<yyyy>/<mm>/<dd>/F<n>_Slide1.jpeg).
    The board page links only the posts; page-images on it finds nothing (fetch:check 2026-11-04: ''No
    PDF links found on bulletin page''), and no collector follows the newest post to its images.'
  url: https://www.ilovesak.org/v2/jubo/?vid=601
---

## Publisher

The parish makes its own bulletin (주보) each week and posts it on its WordPress site's MangBoard board, https://www.ilovesak.org/v2/jubo/: one post in Korean ('11월 1일 주보 (한글)') and, most weeks, one in English ('November 1 Weekly Bulletin (English)'), both editions of the one parish bulletin. Each post shows its pages as JPEG images, not a PDF. I read page 1 of the English issue for 1 November 2026 (an image): 'SAINT ANDREW KIM KOREAN CATHOLIC CHURCH, 280 Parker Ave. Maplewood, NJ 07040 … www.ilovesak.org', 'November 1, 2026: SOLEMNITY OF ALL SAINTS', and a Mass schedule for the Main Church and Augustine Chapel. No printer appears.

## Worship sites

One church, `st-andrew-kim-maplewood` (directory 113, GCatholic 18477). The schedule's Main Church, Augustine Chapel and Small Chapel are, I infer, on the parish's one property: the bulletin gives no other address, and neither roster lists another place.

## Website and bulletin provider

The website is the bulletin board page. The bulletin is published but no collector reads it: the board links only posts, and each post holds the issue as JPEGs (`page-images` on the board page found nothing; fetch:check 2026-11-04 'No PDF links found on bulletin page'). So the row is `unsupported`, with fetch_gap `board-post-images`, and stays off the site until a collector can open the newest post and keep its images. The English edition is the one to pin then (its Slide images carry the full Mass schedule in English). GCatholic's older website (catholicmaplewood.com) is not used.

## Not yet confirmed

- A collector for this format: see `research` and `fetch_gap`.
