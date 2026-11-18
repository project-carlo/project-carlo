---
name: St. Anthony of Padua
website: https://www.stanthony.nyc/
bulletin_provider: other
provider_id: page-pdfs https://www.stanthony.nyc/bulletins/ filename=[!b]*[0-9].pdf
publication: ['url:https://www.stanthony.nyc/bulletins/']
group: ''
evidence:
- url: https://www.stanthony.nyc/wp-content/uploads/2026/07/October25.pdf
  seen: 2026-10-31
  note: 'Image-only two-page issue, rendered and read: page 1 masthead names St. Anthony of Padua Church,
    ''Thirtieth Sunday in Ordinary Time | October 25, 2026'', church 155 Sullivan Street, parish office
    154 Sullivan Street. It was the DearFlip source on /bulletins/ that day.'
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/november-1.pdf
  seen: 2026-11-08
  note: 'Image-only issue, page 1 rendered and read: masthead names St. Anthony of Padua Church, ''All
    Saints | November 1, 2026''; Saturday 5:00 pm, Sunday 9:00 and 11:00 am, 1:00 pm Spanish, Tuesday-Friday
    8:00 am and 12:10 pm. Picked by the pinned recipe on 2026-11-08.'
- url: https://www.stanthony.nyc/bulletins/
  seen: 2026-11-08
  quote: Latest Bulletin
  note: The 'Latest Bulletin' and 'Bulletins' headings still link August-16-Bulletin.pdf and the other
    anchors link June/July BULLETIN*.pdf files; the DearFlip script source is november-1.pdf.
revisit: If a weekly fetch fails with no matching PDF, read the DearFlip source on https://www.stanthony.nyc/bulletins/
  (window.option_df_ script) and widen the filename glob to the new naming; if the parish fixes its Latest
  Bulletin anchor, drop the glob.
revisit_after: 2026-12-08
promoted: 2026-11-09
research:
- method: page-pdfs https://www.stanthony.nyc/bulletins/ filename=[!b]*[0-9].pdf (check_fetch on a hypothetical
    row)
  url: https://www.stanthony.nyc/wp-content/uploads/2026/07/October25.pdf
  checked: '2026-10-31'
  outcome: found
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese new-york --parish st-anthony-of-padua-new-york-city
  url: https://www.stanthony.nyc/wp-content/uploads/2026/10/november-1.pdf
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Anthony of Padua (Franciscan friars, Sullivan Street) publishes its own weekly bulletin, a two-page image-only PDF. Issues read: October 4, 2026 (`2026/10/october4.pdf`, read October 8), October 25, 2026 (`2026/07/October25.pdf`, rendered October 31) and November 1, 2026 (`2026/10/november-1.pdf`, rendered November 8). Each front page is headed "St. Anthony of Padua Church" with the Sunday and date, and its footer gives the church at 155 Sullivan Street and the parish office at 154 Sullivan Street. No other church appears in the schedule.

## Worship sites

One: St. Anthony of Padua Church, 155 Sullivan Street (`churches/st-anthony-of-padua-new-york-city.md`). The November 1 issue prints Saturday 5:00 pm; Sunday 9:00 and 11:00 am and 1:00 pm Spanish; Tuesday-Friday 8:00 am and 12:10 pm; no Masses on Mondays (October 4 issue, page 2). The homepage gives 154 (the office) and a 1:30 pm Spanish Mass in its menu; the bulletins say 155 for the church and 1:00 pm, and the bulletin is followed.

## Website and bulletin provider

https://www.stanthony.nyc/bulletins/ shows the current issue in a DearFlip viewer whose PDF address is only in a script (`window.option_df_10804 = {... "source": ".../november-1.pdf"}`), while the page's ordinary links are stale: "Latest Bulletin" and "Bulletins" still link `2026/08/August-16-Bulletin.pdf`, and the others `BULLETIN-6.21.pdf`, `BULLETIN-6.28-BACK-combined.pdf`, `BULLETIN-7.5.2026-BACK-combined.pdf`, `BULLETIN.pdf`. Unpinned, page-pdfs takes the August 16 anchor (October 8 and October 31), because it reads the script source only when the page's links give nothing.

The pinned recipe `page-pdfs https://www.stanthony.nyc/bulletins/ filename=[!b]*[0-9].pdf` removes every stale anchor (they start with "BULLETIN" or end in "Bulletin") and keeps the viewer's files, which the parish has named month plus day (`october4`, `October25`, `november-1`). With it the resolver picked October25.pdf on October 31 and november-1.pdf on November 8, each the newest issue on the site. The November 8 issue was not yet posted that day.

The glob depends on that naming habit. If the parish names a file `Bulletin-...`, or one ending in a letter, the pick fails loudly (no matching PDF) rather than taking a stale issue; then read the script source and adjust the glob. The publication id is the bulletin page.

## Not yet confirmed

Nothing that changes the row. Whether a week's issue is posted on time is up to the parish: on November 8 the newest was November 1.
