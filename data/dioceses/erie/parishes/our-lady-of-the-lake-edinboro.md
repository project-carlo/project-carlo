---
name: Our Lady of the Lake Parish
website: https://ololake.com
bulletin_provider: discover_mass
provider_id: our-lady-of-the-lake-edinboro-pa
publication: ['discovermass:our-lady-of-the-lake-edinboro-pa']
group: Our Lady of the Lake, Edinboro, with St. Anthony of Padua (Cambridge Springs) and St. Bernadette
  (Saegertown), merged into it by decree (St. Anthony Parish and its mission St. Bernadette subsumed;
  2024)
evidence:
- url: https://discovermass.com/church/our-lady-of-the-lake-edinboro-pa/
  seen: 2026-10-23
  quote: Twenty-Ninth Sunday in Ordinary Time
  note: 'Discover Mass church page, bulletin-current for the 18 October 2026 issue (cover class ''bulletin-cover
    X-|2026-10-18|...|3527'', bulletin number 3527); I downloaded the PDF once and read it. Page 1 cover:
    ''Our Lady of the Lake Parish / With a Mother''s Embrace for the Families of'', then three blocks:
    ''Our Lady of the Lake Church, Edinboro, Pennsylvania''; ''St. Anthony of Padua Mission Church, Cambridge
    Springs, Pennsylvania''; ''St. Bernadette Church, Saegertown, Pennsylvania''; ''Sunday October 18,
    2026 - Twenty-Ninth Sunday in Ordinary Time''. Every inside-page footer reads ''Our Lady of the Lake
    Parish - Serving Edinboro, Cambridge Springs & Saegertown PA''. So one bulletin covers all three churches.
    (Quote is the page-1 cover line; the footer line quoted in this note is on the inside pages.)'
- url: https://discovermass.com/church/our-lady-of-the-lake-edinboro-pa/
  seen: 2026-10-23
  note: 'Page 9 of the same issue: ''Our Lady of the Lake Parish Office, 128 Sunset Drive, Edinboro, Pennsylvania
    16412, Phone: 814-734-3113''; Pastor Rev. Mark A. Hoffman. Clergy PDF (8/7/2026) is the pastor source
    for the other rows; this row has one pastor. Pages beyond the first few are not reached by recheck,
    so this item has no quote.'
- url: https://ololake.com/bulletin
  seen: 2026-10-23
  quote: Diocesan Bulletin Publication
  note: The parish's own bulletin page (GoDaddy site builder) carries no PDF; it says 'We are pleased
    to announce that our parish has migrated to Diocesan Bulletin Publication' and links https://discovermass.com/church/our-lady-of-the-lake-edinboro-pa/#bulletins.
    probe url finds no ParishesOnline or LPi id on the site.
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE%20-%20Merging%20St.%20Anthony%20(Cambridge%20Springs)%20into%20Our%20Lady%20of%20the%20Lake%20(Edinboro).pdf
  seen: 2026-10-23
  quote: secondary mission church (i.e. with Mass on Saturday evening or on Sunday); and Saint Bernadette
  note: 'Merger decree (hearings dated 2023 and 28 Feb 2024; PDF text layer): St. Anthony of Padua Parish,
    Cambridge Springs ''shall be merged and subsumed into Our Lady of the Lake Parish, Edinboro''; Our
    Lady of the Lake stays the parish church, St. Anthony becomes a secondary mission church and St. Bernadette
    ''a secondary church without mission status (i.e. no Mass on Saturday evening or on Sundays)''. The
    decree gives no effective date in the text I searched; the deanery plan and directory treat it as
    2024.'
research:
- method: probe url ololake.com; curl of ololake.com/bulletin; one read of the Discover Mass church page
    and its current PDF
  url: https://discovermass.com/church/our-lady-of-the-lake-edinboro-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: Discover Mass is the parish''s declared bulletin channel. Check that the 25 October
    issue replaces 3527 once posted.'
- method: pnpm fetch:check --diocese erie --parish our-lady-of-the-lake-edinboro --expected-identity Edinboro
    (headed Chrome)
  url: https://discovermass.com/church/our-lady-of-the-lake-edinboro-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Resolver discover_mass downloaded the current PDF (4,045,694 bytes, the same size
    as the file I read, bulletin 3527 dated 18 October); transport ok, PDF, identity matched (Edinboro
    in first-page text; Hoffman is not on page 1). Issue date reads unknown (masthead date split by layout),
    so overall unverified for that reason only.
---

## Publisher

Our Lady of the Lake Parish, Edinboro publishes one weekly bulletin through the diocesan publisher (J.S. Paluch / Discover Mass). The issue for Sunday 18 October 2026 (Discover Mass bulletin number 3527, read 2026-10-23) has a cover naming three churches: Our Lady of the Lake Church (Edinboro), St. Anthony of Padua Mission Church (Cambridge Springs) and St. Bernadette Church (Saegertown), and its inside footers read 'Our Lady of the Lake Parish - Serving Edinboro, Cambridge Springs & Saegertown PA'. Its first page lists the week's Masses at all three: Mon/Wed/Fri 8:00am at Our Lady of the Lake, Tue 12:10pm at St. Anthony, Thu 12:10pm at St. Bernadette, Sat 4:00pm at St. Anthony, Sun 8:00am and 10:30am at Our Lady of the Lake.

The pastor is Rev. Mark A. Hoffman (page 9 of the issue; the directory's locator field names a different priest, Rev. Daniel R. Hoffman / Rev. Mark A. Nowak for the missions, which the bulletin and the printable directory (Oct. 6, 2026: 'Pastor: Reverend Mark A. Hoffman') contradict).

## Worship sites

Three churches, each with its own church record: Our Lady of the Lake (128 Sunset Drive, Edinboro), St. Anthony of Padua (Cambridge Springs) and St. Bernadette (Saegertown). St. Anthony and St. Bernadette were a separate parish and its mission until the merger decree (see evidence). The diocese's locator still groups St. Anthony and St. Bernadette under 'St. Stephen of Hungary Parish (10314)'; that is a data error (St. Stephen is an Erie city parish) and the directory's mailing address, the bulletin and the decree all put both under Our Lady of the Lake. Their Discover Mass pages (st-anthony-of-padua-cambridge-springs-pa, st-bernadette-saegertown-pa) say 'no bulletins available' (read 2026-10-23), so they are not separate channels.

## Website and bulletin provider

`discover_mass` with the church slug `our-lady-of-the-lake-edinboro-pa`. The parish site ololake.com only links to Discover Mass. Website is https://ololake.com (the directory's http://www.ololake.com redirects there).

## Not yet confirmed

The 18 October issue was the current one on Discover Mass on 2026-10-23 (before the 25 October weekend), so freshness should be confirmed by `fetch:check`, see research.
