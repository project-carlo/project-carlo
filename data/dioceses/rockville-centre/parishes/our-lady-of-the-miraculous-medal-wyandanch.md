---
name: Our Lady of the Miraculous Medal
website: https://www.wyandanch-olmm.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.wyandanch-olmm.org/_files/ugd/922c78_4e2c83aea5694f6a9d564894d5b0e3c6.pdf
  seen: 2026-11-13
  quote: November 17, 2024
  note: 'The PDF the home page''s ''Weekly Bulletin'' link opens: the Our Lady of the Miraculous Medal
    Roman Catholic Church bulletin, 1434 Straight Path, Wyandanch, for November 17, 2024, two years old.
    The other home-page PDF (922c78_7cc0c985...) is the July 14th, 2024 issue.'
- url: https://www.wyandanch-olmm.org/
  seen: 2026-11-13
  quote: During renovations, Spanish mass will change to the follow times
  note: Wix home page read with visit.py; its sitemap lists no bulletin page, only the two PDFs linked
    from the home page.
- url: https://discovermass.com/church/our-lady-of-the-miraculous-medal-wyandanch-ny/
  seen: 2026-11-13
  note: 'Discover Mass church page exists but lists no bulletins (issues.py: ''no bulletins listed'').'
- url: https://www.olmm-wyandanch.org/
  seen: 2026-11-13
  quote: has expired and is parked free, courtesy of GoDaddy.com
  note: The domain GCatholic and the 2024 bulletins give is parked; the locator's wyandanch-olmm.org is
    the live site.
revisit: Check the Wix home page's Weekly Bulletin link for an issue dated within the last month, and
  Discover Mass; if one is current, set provider other with a pinned page-pdfs recipe on the home page
  and run fetch:check
revisit_after: 2027-02-01
research:
- method: visit.py on the Wix site and its sitemap (pages-sitemap.xml); read both linked PDFs
  url: https://www.wyandanch-olmm.org/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Reopen the home page's Weekly Bulletin link and check the issue date
  retry_when: The home page links a newer PDF, or a bulletin page appears in the sitemap
  revisit_after: 2027-02-01
- method: issues.py discovermass and probe po on the slug our-lady-of-the-miraculous-medal-church-11798
  url: https://discovermass.com/church/our-lady-of-the-miraculous-medal-wyandanch-ny/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Recheck Discover Mass; look for an LPi id or printer on any new issue
  retry_when: A new issue names a printer or the Discover Mass page lists bulletins
bulletin_status: not-found
---

## Publisher

No current bulletin found. Our Lady of the Miraculous Medal, 1434 Straight Path, Wyandanch did publish one: the PDF behind its home page's "Weekly Bulletin" link (`https://www.wyandanch-olmm.org/_files/ugd/922c78_4e2c83aea5694f6a9d564894d5b0e3c6.pdf`, read 2026-11-13) is the November 17, 2024 issue (masthead "Our Lady of the Miraculous Medal Roman Catholic Church", Microsoft Publisher), and the only other PDF linked is the July 14th, 2024 issue. Nothing newer was found on the site (its Wix sitemap has no bulletin page), on Discover Mass (church page with no bulletins) or ParishesOnline.

## Worship sites

One: the church at 1434 Straight Path (`our-lady-of-the-miraculous-medal-wyandanch-church`). The diocesan locator (directory:88), GCatholic (16937) and the Mass-times page list only this building. The parish's home page (2026-11-13) announces changed Spanish Mass times "During renovations" without naming another place.

## Website and bulletin provider

`no_bulletin`: the newest issue is two years old. The website is the live Wix site the locator links, www.wyandanch-olmm.org. GCatholic's and the old bulletins' olmm-wyandanch.org is a parked GoDaddy domain. Under Settled policy 4 this row and its church stay in the records but off the site until a current bulletin appears.

## Not yet confirmed

Whether the parish still prints a bulletin at all (on paper, or on Facebook, which was not read). See `research` and `revisit`.
