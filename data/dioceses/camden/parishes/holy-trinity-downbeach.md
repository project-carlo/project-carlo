---
name: Holy Trinity Parish
website: https://www.holytrinitydownbeach.org/news/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.holytrinitydownbeach.org/news/bulletin
publication: ['url:https://www.holytrinitydownbeach.org/news/bulletin#holy-trinity-downbeach']
group: ''
evidence:
- url: https://www.holytrinitydownbeach.org/news/bulletin
  seen: 2026-10-29
  quote: November 1, 2026 New
  note: 'Parish site (Solutio CMS), read in the browser with visit.py: the Bulletin page lists one PDF
    per Sunday from ''November 1, 2026 New'' back to April 2026, each linked as /news/bulletin/<n>-<month>-<d>-<year>/file
    (197 is 1 November). Its footer names the parish ''Holy Trinity Parish of Downbeach, NJ'' with the
    office at 11 N Kenyon Ave and four sites. The PDFs themselves answer HTTP 403 to probe pdf, so no
    masthead was read.'
- url: https://www.holytrinitydownbeach.org/
  seen: 2026-10-29
  quote: Come Join Us at our Community of Catholic Churches
  note: 'Home page, read in the browser: one schedule block each for St. James Church, Blessed Sacrament
    Church and Church of the Epiphany, and a Trinity Chapel entry (12 N Jerome Ave) with no Mass line.
    Details are in the church records.'
- url: https://www.holytrinitydownbeach.org/about-us/our-priests-staff
  seen: 2026-10-29
  quote: Fr. Pawel Kryszkiewicz
  note: 'Staff page: Fr. Pawel Kryszkiewicz, Pastor; Fr. Christuraj Gnanapragasam, Parochial Vicar. One
    pastor for the whole parish.'
research:
- method: probe url on holytrinitydownbeach.org and probe pdf on the /news/bulletin/197-november-1-2026/file
    link
  url: https://www.holytrinitydownbeach.org/news/bulletin
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read a bulletin's masthead and Mass schedule once a fetch method that the site allows works
    (the pipeline's own fetch, or a browser run the sandbox permits); then pin a recipe and run fetch:check
  retry_when: fetch:check resolves the Bulletin page's /file links, or the site stops answering 403 to
    non-browser clients
  revisit_after: 2026-11-30
- method: fetch:check --diocese camden --parish holy-trinity-downbeach with page-pdfs recipe on the Bulletin
    page (PLAYWRIGHT_BROWSER_CHANNEL=chrome)
  url: https://www.holytrinitydownbeach.org/news/bulletin
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: 'None with this recipe: it reports ''resolve_failed NoBulletin: No PDF links found on bulletin
    page'', because Solutio links end in /file with no .pdf and the page answers 403 to plain fetches'
  retry_when: A collector for Solutio /file links exists, or the site's bulletin is found on another host
- method: church-bulletin.org listings for the pre-merger John Patrick codes 501 (Holy Trinity, Ventnor),
    504 (Blessed Sacrament, Margate) and 529 (Epiphany, Longport)
  url: https://www.church-bulletin.org/holy-trinity-parish-ventnor-nj-08406
  checked: '2026-10-29'
  outcome: not-found
  next_action: 'None: the three listings carry no /bulletin/ editions, so the parish does not publish
    through them any more'
  retry_when: A merged-parish listing appears on church-bulletin.org
- method: one duckduckgo.com/html search for the parish name, towns and 'bulletin' through probe get
  checked: '2026-10-29'
  outcome: not-found
  next_action: Search again only with a changed query, such as the parish name and a ParishesOnline or
    Bon Venture host
  retry_when: A new publisher is suspected
bulletin_status: access-blocked
---

## Publisher

Holy Trinity Parish ('Holy Trinity Parish of Downbeach, NJ' in its site footer) is one parish with one pastor, Fr. Pawel Kryszkiewicz (staff page, 2026-10-29), and one bulletin page: holytrinitydownbeach.org/news/bulletin, which lists one PDF per Sunday (newest 'November 1, 2026 New', 2026-10-29). The site is built by Solutio and answers 403 to `probe url` and `probe pdf`; it loads in the browser. **No bulletin issue was read**, so the masthead and the bulletin's own Mass schedule are unconfirmed. The parish is mapped from its website's home page and church list, which name one parish and four sites.

## Worship sites

Three churches take Mass by the parish's home page (read 2026-10-29): St. James, Ventnor; Blessed Sacrament, Margate; and the Church of the Epiphany, Longport (church records `st-james-ventnor`, `blessed-sacrament-margate`, `epiphany-longport`). The site's fourth site, **Trinity Chapel**, 12 N Jerome Ave., Margate (GCatholic's 'Chapel of the Holy Trinity', 100 N Jerome Ave., 'Mission of' Blessed Sacrament), has no Mass line anywhere read, so it is in `open/holy-trinity-chapel-margate`. The parish office, 11 N Kenyon Ave., Margate, is the directory's and GCatholic's address for Blessed Sacrament; it is an office, not a separate site. The summer guide (Catholic Star Herald, 2026-05-22) lists the same three churches and no chapel.

## Website and bulletin provider

The directory and GCatholic give holytrinitydownbeach.org. `other`, with the Bulletin page as a `page-pdfs` recipe (`bulletin_status: access-blocked`). `fetch:check` (2026-10-29) with that recipe returns `resolve_failed NoBulletin: No PDF links found on bulletin page`: Solutio links each issue as `/news/bulletin/<n>-<date>/file` (no `.pdf`), and the plain fetch is refused. The recipe is therefore not confirmed to pick a bulletin, and no pick was checked for identity or freshness. The playbook's other route for blocked parishes, a John Patrick listing, has nothing: the old per-church listings (501 Ventnor, 504 Margate, 529 Longport) carry no editions. See `research` for the checks and their retry triggers.

## Not yet confirmed

- The bulletin masthead, its Mass schedule and its listing of churches (does it name Trinity Chapel, or Mass there?).
- Whether the recipe or another collector can read the `/file` links from the pipeline's environment.
- The home page's schedule against the bulletin: it shows only the off-season times; see the church records.
