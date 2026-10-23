---
name: St. Mary, Mother of God Parish, Freeport
website: https://www.stmaryfreeport.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-mother-of-god-church-freeport-pa-16229
publication: ['url:https://www.church-bulletin.org/saint-mary-mother-of-god-church-freeport-pa-16229',
  'ecatholic:5138']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-mary-mother-of-god-church-freeport-pa-16229
  seen: 2026-10-22
  quote: Latest Edition October 25, 2026
  note: 'John Patrick Publishing (jppc.net) listing "Saint Mary, Mother of God Church Freeport, PA 16229",
    608 High Street. The parish site''s "Current Bulletin" link (https://www.jppc.net/onlinebulletins/280template.pdf)
    redirects here via church-bulletin.org/?id=280 (John Patrick id 280). The archive lists weekly PDFs
    /bulletin/saint-mary-mother-of-god-church-freeport-pa-16229/<yyyy-mm-dd>.pdf from 2024-10-27 to 2026-10-25.
    The 25 Oct 2026 PDF (8 pages) has no text layer; rendered page 1 has the masthead "St. Mary, Mother
    of God Church ... 608 High Street ~ Freeport, PA 16229 ... October 25th, 2026", "Rev. Vincent A. Yee
    Concepcion, Administrator", "Saturday (Vigil): 4:00 P.M. Sunday: 8:30 & 11:00 A.M.".'
- url: https://www.church-bulletin.org/bulletin/saint-mary-mother-of-god-church-freeport-pa-16229/2026-10-18.pdf
  seen: 2026-10-22
  quote: 608 High Street ~ Freeport, PA 16229
  note: 'Page 1 of the 18 Oct 2026 issue (text layer present): "St. Mary, Mother of God Church Roman Catholic
    Church ... 29th Sunday in Ordinary Time October 18th, 2026 ... Saturday (Vigil): 4:00 P.M. Sunday:
    8:30 & 11:00 A.M. Weekday Masses: Monday, Tuesday, Thursday and Friday—8:00 A.M.; Wednesday—7:00 P.M.".
    Names no other parish or church. Byte-identical (MD5 9c2feccfa757130751fc0aef92036beb, 9,221,162 bytes)
    to the parish site''s eCatholic copy files.ecatholic.com/5138/bulletins/20261018.pdf.'
- url: https://www.stmaryfreeport.com/bulletins
  seen: 2026-10-22
  note: eCatholic site 5138 (files.ecatholic.com/5138/...). Plain fetches get a Cloudflare challenge ("Just
    a moment...", 403); opened headed (tools/headed_open.py). Its archive lists weekly issues to "October
    18, 2026" (files.ecatholic.com/5138/bulletins/20261018.pdf). On 2026-10-22 it had not posted Oct 25,
    which John Patrick already had. The homepage title is "St. Mary Mother of God Parish - Freeport, PA".
- url: https://parishesonline.com/organization/st-mary-mother-of-god-church
  seen: 2026-10-22
  note: 'LPi organization "St. Mary, Mother of God Church", 608 High St, Freeport (lpi 0018000000QxC0rAAF):
    `probe po` lists no publications. Empty, not a channel; ids not recorded. The Discover Mass page st-mary-mother-of-god-freeport-pa
    says "Shucks! There are no bulletins available": not a channel either.'
promoted: 2026-10-23
---

## Publisher

St. Mary, Mother of God Parish, Freeport (directory 117 "St. Mary Parish"; GCatholic 24152) publishes its own weekly bulletin, printed by John Patrick Publishing. The issues sit on JPPC's listing https://www.church-bulletin.org/saint-mary-mother-of-god-church-freeport-pa-16229 (id 280), and the parish reposts the same file on its eCatholic site (5138). The 18 Oct 2026 copies on both are byte-identical. The 25 Oct 2026 issue (John Patrick, read 2026-10-22, page 1 rendered because it has no text layer) and the 18 Oct issue both have the masthead "St. Mary, Mother of God Church ... 608 High Street ~ Freeport, PA 16229" under administrator Father Vincent A. Yee Concepcion, and name no other parish. The directory lists no partner parish.

## Worship sites

One church: St. Mary, Mother of God, 608 High Street (`st-mary-freeport`). The 18 and 25 Oct 2026 issues list Saturday Vigil 4:00 P.M., Sunday 8:30 & 11:00 A.M. and weekday Masses Monday, Tuesday, Thursday and Friday at 8:00 A.M. and Wednesday at 7:00 P.M. A grep of the 18 Oct text for "chapel" and "Mass at" found no other place. GCatholic and the directory list no other site.

## Website and bulletin provider

`other`, recipe `page-pdfs https://www.church-bulletin.org/saint-mary-mother-of-god-church-freeport-pa-16229`. `fetch:check` on 2026-10-23 picked `.../2026-10-25.pdf` (url_date 2026-10-25, 9,155,817 bytes, "page-pdfs ... current"), which is this week's issue. John Patrick is a week ahead of the eCatholic page, so it is preferred over an `ecatholic` row on the parish site. That site would also need a headed browser to get past Cloudflare. The website is the parish's own site (directory homepage), which links the John Patrick listing as "Current Bulletin". Publications: the John Patrick listing and `ecatholic:5138`, which are one bulletin.

## Not yet confirmed

Recent John Patrick issues can have no text layer (25 Oct 2026). Whether the pipeline reads them is a processing question, not a fetch one. If it can't, the eCatholic copy is the same file a week later.
