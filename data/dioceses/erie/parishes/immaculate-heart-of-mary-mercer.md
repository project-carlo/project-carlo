---
name: Immaculate Heart of Mary Parish
website: https://ihmercer.org
bulletin_provider: discover_mass
provider_id: immaculate-heart-of-mary-mercer-pa
publication: ['discovermass:immaculate-heart-of-mary-mercer-pa']
group: Pastor Very Rev. Andrew Boyd serves Immaculate Heart of Mary, Mercer and St. Columbkille, Stoneboro
  (clergy list 8/7/2026); one joint bulletin
evidence:
- url: https://discovermass.com/church/immaculate-heart-of-mary-mercer-pa/
  seen: 2026-10-23
  quote: Immaculate Heart of Mary | Discover Mass
  note: 'Church page: current bulletin ''Oct 25, 2026'' (cover class carries bulletin number 3536), archive
    back to Aug 9, 2026. ihmercer.org/bulletin/ is a 301 to this page''s #bulletins anchor, so Discover
    Mass is the parish''s bulletin channel. The 25 Oct 2026 PDF (2,036,514 bytes, downloaded 2026-10-23
    and read with pdftotext) opens: ''Immaculate Heart of Mary Parish | St. Columbkille Parish'', two
    columns, each ''A Roman Catholic Parish in the Diocese of Erie'', IHM ''100 Penn Ave | Mercer, PA
    | 16137'' and St. Columbkille ''Physical Address: 70 Franklin St | Stoneboro, PA | 16153'', then ''THIRTIETH
    SUNDAY IN ORDINARY TIME | OCTOBER 25, 2026'' and ''Very Rev. Fr. Andrew M. Boyd, V.F. - Pastor & Dean
    of Greenville Deanery''.'
- url: https://discovermass.com/church/immaculate-heart-of-mary-mercer-pa/
  seen: 2026-10-23
  note: 'Same PDF, Sacraments column: ''Daily Mass Tuesday - Friday: 8 AM'', ''Saturday Vigil Mass: 4
    PM - Immaculate Heart, 6 PM - St. Columbkille'', ''Sunday Mass at IHM: May - Aug - 8 AM & 10 AM, Sept
    - April - 8 AM & 11 AM''. The Mass Intentions column says ''Services in Red are at St. Columbkille''
    and lists Saturday 6pm only for Stoneboro. The same schedule block appears in the 9 Aug and 4 Oct
    2026 issues I downloaded (ten of the twelve listed issues, 9 Aug - 25 Oct 2026 minus 6 and 13 Sept,
    were downloaded and read; see excluded/st-hermenegild-mercer).'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  note: 'Clergy list updated 8/7/2026 (via diocese.md Sources): Boyd is pastor of both Immaculate Heart
    of Mary, Mercer and St. Columbkille, Stoneboro. The bulletin masthead states the pastor for the joint
    bulletin; the clergy list is the source for the shared-pastor association.'
- url: https://www.eriercd.org/Parish31104-Immaculate-Heart-of-Mary.html
  seen: 2026-10-23
  quote: 'Saturday: 4 p.m.'
  note: 'Directory record 31104: 100 Penn Ave., Mercer PA 16137; Saturday 4 p.m.; Sunday May-August 8,
    10 a.m., September-April 8, 11 a.m.; Tuesday-Friday 8 a.m.; website https://ihmercer.org. Record 31112
    (St. Columbkille Parish, Stoneboro) and 31120 (St. Hermenegild Church, secondary church) both name
    Immaculate Heart of Mary as parent (locator GroupID 31104) and give ihmercer.org as website.'
research:
- method: pnpm fetch:check --diocese erie --parish immaculate-heart-of-mary-mercer --expected-identity
    Columbkille --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://discovermass.com/church/immaculate-heart-of-mary-mercer-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for the pick: transport ok, PDF, identity matched (''Expected phrase found in first-page
    text'', Columbkille: the joint masthead). The issue date read ''unknown'' (''No unambiguous issue
    date in inspected masthead'') although the masthead prints ''THIRTIETH SUNDAY IN ORDINARY TIME | OCTOBER
    25, 2026''; the pick is 2,036,514 bytes, byte-identical in size to the 25 Oct 2026 issue I downloaded
    and read with pdftotext, so it is the current issue. Re-run on a later week to confirm it follows
    the newest link.'
---

## Publisher

Immaculate Heart of Mary (IHM), Mercer publishes one weekly bulletin through Discover Mass (church slug `immaculate-heart-of-mary-mercer-pa`; ihmercer.org/bulletin/ redirects there). The 25 October 2026 issue (bulletin number 3536, read 2026-10-23) is a joint bulletin for **two canonical parishes**: its masthead puts 'Immaculate Heart of Mary Parish' and 'St. Columbkille Parish' side by side with each address, it names one pastor (Very Rev. Fr. Andrew M. Boyd, V.F.), and its Mass Intentions list both churches' Masses, marking Stoneboro's in red. So the directory's separate St. Columbkille Parish record (31112) is not a separate bulletin: one row, with St. Columbkille as a worship site. Stoneboro's own site (stcolumbkillechurch.org) has a Bulletin page with no bulletin on it (read 2026-10-23: only the heading and contact block, office@ihmercer.org), and its Discover Mass page (st-columbkille-stoneboro-pa) says 'Shucks! There are no bulletins available.' and carries stale Mass times (Saturday 4:30pm, Tuesday-Friday 9:00am), so it is not a live channel.

## Worship sites

- Immaculate Heart of Mary, 100 Penn Ave., Mercer: Saturday 4 PM, Sunday 8 AM and 10 AM (May-Aug) or 11 AM (Sept-April), Tuesday-Friday 8 AM.
- St. Columbkille, 70 Franklin St., Stoneboro: Saturday vigil 6 PM (bulletin, 25 Oct 2026). No other Stoneboro Mass is in the bulletin.
- Not a worship site here: St. Hermenegild, 28 Church Road, Mercer (Pardoe), a secondary church of IHM. Its only public Mass is the annual August Mass and picnic (9 Aug 2026 bulletin; parish posts for 2022, 2024, 2025), so it is excluded as `no-public-mass` (`excluded/st-hermenegild-mercer`); a recurring schedule would make it a church row under this parish again.

Nothing else in the bulletin: no campus or institutional Mass.

## Website and bulletin provider

Discover Mass, `discover_mass` with the church slug. ihmercer.org is a WordPress site that redirects its bulletin page to Discover Mass. The page lists twelve issues (9 Aug - 25 Oct 2026). Downloads are capped per IP per day; 6 and 13 Sept returned HTML when I fetched all twelve.

## Not yet confirmed

St. Columbkille's weekday Masses: the directory and the bulletin give none, while the stale Discover Mass page lists weekday 9am. Left at Saturday 6 PM only on the strength of the current bulletin.
