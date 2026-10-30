---
name: The Parish of the Holy Cross
website: https://parishholycross.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://parishholycross.org/bulletin
publication: ['url:https://parishholycross.org/bulletin#holy-cross-bridgeton']
group: ''
evidence:
- url: https://parishholycross.org/bulletin
  seen: 2026-10-29
  quote: November 1, 2026 New
  note: 'Parish site (Solutio CMS), read in the browser with visit.py: the Bulletin | Boletín page lists
    one PDF per Sunday from ''November 1, 2026 New'' back to August 30, 2026 on page 1 (20 pages), each
    linked as /bulletin/<n>-<month>-<d>-<year>/file (213 is 1 November, 212 is 25 October). The PDFs answer
    HTTP 403 to probe get and render.py, and fetch:check cannot resolve them, so no masthead was read.'
- url: https://parishholycross.org/about-us/parish-staff-clergy
  seen: 2026-10-29
  quote: "Rev. Schned Bruno\tAdministrator / Administrador"
  note: 'Staff page: Rev. Schned Bruno, Administrator; Rev. Ruben D. Valdes Arias, Parochial Vicar; three
    deacons. One administrator for the whole parish.'
- url: https://catholicstarherald.org/83106-2/
  seen: 2026-10-29
  quote: Rev. Schned Bruno , from Outside the Diocese to Administrator, Holy Cross, Bridgeton.
  note: 2026 priest assignments (effective 2026-07-01). The same post moves Rev. Matthew Weber from Pastor,
    Holy Cross to an interval of rest in view of an assignment as Parochial Vicar, Holy Cross. Rev. Vince
    Guest, the 2015 directory's pastor, is not named for Holy Cross.
- url: https://parishholycross.org/our-churches
  seen: 2026-10-29
  quote: Saint Anthony | San Antonio
  note: 'Our Churches page lists the five churches with addresses: Immaculate Conception, 312 N. Pearl
    St.; Saint Teresa of Avila, 46 Central Ave.; Saint Mary, 732 Morton Ave.; Saint Michael, 367 Main
    St., Cedarville; Saint Anthony, 1560A Main St., Port Norris. Each church page lists Mass times (see
    the church records).'
- url: https://www.camdendiocese.org/bishop-galante-issues-decree-establishing-the-parish-of-the-holy-cross-on-sept10/
  seen: 2026-10-29
  quote: The seat of the parish will be St. Teresa of Avila Church. The other churches will be open as
    worship sites on some basis.
  note: '2010-09-09 decree post: Immaculate Conception and St. Teresa of Avila (Bridgeton), St. Michael
    (Cedarville) and its mission St. Anthony (Port Norris) and St. Mary (Rosenhayn) unite as The Parish
    of the Holy Cross, established 2010-10-13.'
research:
- method: probe url, probe get and probe get --out on parishholycross.org and its /bulletin/213-november-1-2026/file
    link
  url: https://parishholycross.org/bulletin/213-november-1-2026/file
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read a bulletin's masthead and Mass schedule once a fetch method the site allows works
    (the pipeline's own fetch or a browser run the sandbox permits); then pin the recipe and run fetch:check
  retry_when: fetch:check resolves the Bulletin page's /file links, a collector for Solutio /file links
    exists, or the site stops answering 403 to non-browser clients
  revisit_after: 2026-11-30
- method: fetch:check --diocese camden --parish holy-cross-bridgeton with page-pdfs recipe on the Bulletin
    page (PLAYWRIGHT_BROWSER_CHANNEL=chrome), and render.py on the 1 November issue
  url: https://parishholycross.org/bulletin
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: 'None with this recipe: fetch:check reports ''resolve_failed NoBulletin: No PDF links found
    on bulletin post page'', since Solutio links end in /file with no .pdf; render.py gets HTTP 403'
  retry_when: A collector for Solutio /file links exists, or the bulletin is found on another host
- method: 'church-bulletin.org: curl -sIL of church-bulletin.org/<id> for ids 6000-6110 and 701-730, plus
    five guessed listing slugs (holy-cross-parish-bridgeton-nj-08302 and variants); probe po for four
    ParishesOnline slugs'
  checked: '2026-10-29'
  outcome: not-found
  next_action: 'None: no John Patrick listing or ParishesOnline organization for this parish was found
    in those ranges and names (the one hit, 6018, is Holy Cross, Harrison)'
  retry_when: A search for the parish's bulletin on another host finds a listing (the DuckDuckGo search
    answered a bot challenge)
bulletin_status: access-blocked
---

## Publisher

The Parish of the Holy Cross, Bridgeton (46 Central Ave., 08302; (856) 455-2323) is one parish with one administrator, Rev. Schned Bruno (parish staff page and the 2026 assignments, both read 2026-10-29), and one bulletin page, parishholycross.org/bulletin, which lists one PDF per Sunday (newest 'November 1, 2026 New', 2026-10-29). The site is built by Solutio and answers 403 to `probe url`, `probe get` and `render.py`; it loads in the browser. **No bulletin issue was read**, so the masthead and the bulletin's own Mass schedule are unconfirmed. The parish is mapped from its website's church pages, the 2010 establishment decree and GCatholic.

The 2015 directory names Rev. Vince Guest pastor of Holy Cross (and of Sacred Heart, Camden). That is stale: the 2026 assignments name Rev. Schned Bruno administrator here, and the parish's own staff page lists no Guest. It does not mean a shared bulletin with Sacred Heart, which publishes its own (John Patrick 6039).

## Worship sites

All five churches in GCatholic's group 'Holy Cross Parish' still list Mass on the parish's church pages (read 2026-10-29): Immaculate Conception and St. Teresa of Avila (Bridgeton), St. Mary (Rosenhayn, mailing address Bridgeton), St. Michael (Cedarville) and St. Anthony (Port Norris), church records `immaculate-conception-bridgeton`, `st-teresa-of-avila-bridgeton`, `st-mary-bridgeton`, `st-michael-cedarville` and `st-anthony-port-norris`. St. Michael and St. Anthony have a weekend Mass only on some Sundays. Nothing read says any of them has closed. The parish's other places are not worship sites: the Good Shepherd Dining Room (lower level of St. Teresa), the Pope Francis Food Pantry (Immaculate Conception convent, 64 North St.) and cemeteries.

## Website and bulletin provider

The directory and GCatholic give parishholycross.org. `other`, with the Bulletin page as a `page-pdfs` recipe (`bulletin_status: access-blocked`). `fetch:check` (2026-10-29) returns `resolve_failed NoBulletin: No PDF links found on bulletin post page`: Solutio links each issue as `/bulletin/<n>-<date>/file` (no `.pdf`) and the site answers 403 to plain fetches. The recipe is therefore not confirmed to pick a bulletin, and no pick was checked for identity or freshness. No John Patrick listing or ParishesOnline organization was found; see `research`.

## Not yet confirmed

- The bulletin masthead, its Mass schedule and its list of churches (does it agree with the church pages, and does it name Rosenhayn for St. Mary?).
- Whether the recipe or another collector can read the `/file` links from the pipeline's environment.
- That the church pages are current: they are the only Mass-time source read; they carry no date.
