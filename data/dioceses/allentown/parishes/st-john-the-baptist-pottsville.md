---
name: St. John the Baptist
website: http://www.saintjohnpottsville.org/Bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:http://www.saintjohnpottsville.org/Bulletins/', 'po-org:st-john-the-baptist-church-longinus',
  'lpi:0018000000QxAimAAF']
group: ''
evidence:
- url: http://www.saintjohnpottsville.org/Resources/Bulletin%2010-18-26.pdf
  seen: 2026-10-18
  quote: St. John the Baptist Roman Catholic Parish Family 10th & Mahantongo Sts.
  note: 'Page 1 of the 18 October 2026 issue (a cover page; its only text is the masthead and the date). Page 2:
    "Pastor ... Rev. Kevin J. Bobbin". The PDF''s "tt"/"ti" ligatures extract as U+FFFD, e.g. "Po�sville".'
- url: http://www.saintjohnpottsville.org/Resources/Bulletin%2010-18-26.pdf
  seen: 2026-10-18
  quote: Sunday, October 18 8:15 a.m. R.J. Post
  note: 'Page 3 Mass intentions: Saturday 5:00 p.m., Sunday 8:15 a.m. and 10:30 a.m., weekdays 9:00 a.m. (Monday
    6:30 p.m.), no place named but the one church. Page 4 has "October 25 - 8:15 a.m. Mass" and "10:30 a.m." in
    the parish calendar.'
- url: http://www.saintjohnpottsville.org/Bulletins/
  seen: 2026-10-18
  note: 'probe url: the "Bulletins" page links one PDF per Sunday, "Resources/Bulletin 10-18-26.pdf" back to
    "Bulletin 09-13-26.pdf" (the 4 October file is "Bulletin 10-04-26 .pdf", with a stray space).'
- url: https://parishesonline.com/organization/st-john-the-baptist-church-longinus
  seen: 2026-10-18
  note: 'probe po: an old ParishesOnline org, "St. John the Baptist Church Longinus" (lpi 0018000000QxAimAAF, 913
    Mahantongo St), with no publications. "Longinus Hall" is the parish hall named in the bulletin.'
---

## Publisher

St. John the Baptist, Pottsville, publishes its own weekly bulletin as PDFs on its website.
I read the 18 October 2026 issue. The page-1 masthead is "St. John the Baptist Roman
Catholic Parish Family, 10th & Mahantongo Sts., Pottsville", and page 2 names the pastor,
Rev. Kevin J. Bobbin. The page-3 Mass intentions list Saturday 5:00 p.m., Sunday 8:15 a.m.
and 10:30 a.m., and weekday Masses, all at the one church. It covers one church and nothing
groups it with another parish. Its neighbour St. Patrick, three blocks down Mahantongo
Street, publishes its own bulletin (`st-patrick-pottsville`).

## Worship sites

- St. John the Baptist, 913 Mahantongo St. (`st-john-the-baptist-pottsville`).

GCatholic and the diocesan parish map list this one church. Nothing ruled out.

## Website and bulletin provider

`other`: the "Bulletins" page at saintjohnpottsville.org/Bulletins/ links one PDF per Sunday
under /Resources/, named "Bulletin MM-DD-YY.pdf" (with spaces, and once with a stray space
before ".pdf"). The current issue was up on the Sunday itself. The text extracts, but the
"tt" and "ti" ligatures come out as U+FFFD. The old ParishesOnline org (no publications) is
recorded among the publication ids so that no other row claims it.

Fetch check (2026-10-18, `fetch_check_rows.py`): the resolver read the Bulletins page
("page-pdfs ... current") and picked "Resources/Bulletin 10-18-26.pdf", dated 2026-10-18,
which is this week's issue. Its recipe, `page-pdfs`, is recorded as `provider_id`.

## Not yet confirmed

Nothing.
