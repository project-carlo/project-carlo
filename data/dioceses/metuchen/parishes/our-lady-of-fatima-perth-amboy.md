---
name: Our Lady of Fatima
website: https://www.ourladyoffatimaperthamboy.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.ourladyoffatimaperthamboy.com/fatima-sample']
group: ''
evidence:
- url: https://www.ourladyoffatimaperthamboy.com/s/Sunday-September-6-2026.pdf
  seen: 2026-11-03
  quote: OUR LADY OF FATIMA PARISH
  note: 'Page 1 of the 6 September 2026 issue (6 pages, text, no publisher ad pages): ''Septiembre 06,
    2026 / September 06, 2026'', ''OUR LADY OF FATIMA PARISH 380 Smith St. Perth Amboy, NJ 08861'', ''Web
    Page: www.ourladyoffatimaperthamboy.com'', ''Claretian Missionaries / Misioneros Claretianos: Rev.
    Gilles D. Njobam, CMF'', ''Rev. Patrick Ekong, CMF'', ''Rev. Hector Navalo, CMF''; Masses ''Diariamente
    / Daily: 7:00 am (S) & 6:30 pm (S)'', ''Domingo / Sunday: * 9:00 am (S), * 11:00 am (E) * 1:00 pm
    (S), 5:30 pm (S), 7:30 pm (Bilingual)''. One church only.'
- url: https://www.ourladyoffatimaperthamboy.com/fatima-sample
  seen: 2026-11-03
  note: 'The site''s ''Bulletin'' menu item opens /fatima-sample, which (rendered with visit.py and fetched
    with probe get) links one PDF, labelled ''Bulletin'': /s/Sunday-September-6-2026.pdf. The home page
    links the same file. Its header repeats the schedule ''Domingo/Sunday: * 9:00 am (S), * 11:00 am (E),*
    1:00 pm (S), 5:30 pm (S), 7:30 pm (Bilingual)''.'
- url: https://discovermass.com/church/our-lady-of-fatima-perth-amboy-nj/
  seen: 2026-11-03
  quote: There are currently no bulletins available for Our Lady of Fatima.
  note: Discover Mass church page for 380 Smith St. carries no bulletins.
revisit: Check whether /fatima-sample links an issue newer than 6 September 2026; if so run fetch:check
  and record its recipe.
revisit_after: 2026-11-17
promoted: 2026-11-03
research:
- method: Read the Bulletin page /fatima-sample and the home page (probe get and visit.py); tried /s/Sunday-<Month>-<d>-2026.pdf
    for every Sunday 13 September-1 November 2026 and variants (Bulletin-Sunday-…, -01-, -1 suffix), all
    404; read the sitemap; Discover Mass church page; Facebook page needs a login; old Weebly olfperthamboy.weebly.com/weekly-bulletin.html
    lists only years-old issues
  url: https://www.ourladyoffatimaperthamboy.com/fatima-sample
  checked: '2026-11-03'
  outcome: not-found
  next_action: Reload /fatima-sample and check whether its Bulletin link has moved past Sunday-September-6-2026.pdf;
    if it has, run fetch:check and record its page-pdfs recipe
  retry_when: The parish posts a newer issue, or by 2026-11-17
  revisit_after: 2026-11-17
bulletin_status: available
---

## Publisher

Our Lady of Fatima Parish, Perth Amboy (Claretian Missionaries) writes its own bilingual bulletin and posts it on its Squarespace site. The newest issue posted, read 2026-11-03, is 6 September 2026 ('Septiembre 06, 2026 / September 06, 2026'): 'OUR LADY OF FATIMA PARISH 380 Smith St. Perth Amboy, NJ 08861', pastor 'Rev. Gilles D. Njobam, CMF' (as in the finder), one church, no publisher ad pages.

## Worship sites

One church, Our Lady of Fatima, 380 Smith Street (directory:24525, gcatholic:18616), with daily 7:00 am and 6:30 pm and Sunday 9:00 am, 11:00 am (English), 1:00 pm, 5:30 pm and 7:30 pm (bilingual) Masses (6 September masthead; same on the site header, 2026-11-03). Neither source names another church. It is not the same place as Our Lady of the Rosary of Fatima, a church of St. John Paul II Parish (Discover Mass lists both separately).

## Website and bulletin provider

The finder gives no website; the masthead gives www.ourladyoffatimaperthamboy.com, found by a search and confirmed by the masthead's address. The 'Bulletin' menu item opens /fatima-sample, which links a single PDF at a time (/s/<name>.pdf); on 2026-11-03 that was still the 6 September 2026 issue, eight weeks old. Provider `other`, read from the site; no recipe is recorded because the newest posted issue is not current.

## Fetch check

`pnpm fetch:check` on 2026-11-03 (recipe `page-pdfs` on the home page) picked https://www.ourladyoffatimaperthamboy.com/s/Sunday-September-6-2026.pdf: transport ok, PDF, issue date 2026-09-06 (inferred), freshness stale (58 days), overall failed. The transport works; the issue is not current, which is why no recipe is recorded.

## Not yet confirmed

Whether the parish still posts its bulletin weekly. The site's one bulletin link was eight weeks stale on 2026-11-03 and no newer issue could be found (see `research`). Recheck after 2026-11-17: if /fatima-sample links a current issue, run fetch:check and pin its recipe; if it is still stale, look for another channel (Facebook posts, a publisher).
