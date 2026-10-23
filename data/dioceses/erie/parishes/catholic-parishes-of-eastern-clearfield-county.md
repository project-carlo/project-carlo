---
name: Catholic Parishes of Eastern Clearfield County
website: https://cpoecc.org
bulletin_provider: other
provider_id: page-pdfs https://cpoecc.org/weeklybulletin.php
publication: ['url:https://cpoecc.org/weeklybulletin.php#catholic-parishes-of-eastern-clearfield-county']
group: 'Partnership: Christ the King (Houtzdale), St. Agnes (Morrisdale), St. Basil the Great (Coalport);
  one pastor, Rev. Johnathan P. Schmolt, per clergy PDF 8/7/2026'
evidence:
- url: https://cpoecc.org/images/weeklybulletin/2cdf15148eaa8fa3e95ef57e5163d9de.pdf
  seen: 2026-10-23
  quote: Rev. Johnathan Schmolt, Pastor; Rev. Cory Pius, Parochial Vicar, Deacon Eugene J.
  note: Page 2 of the issue dated October 25, 2026 (first listed on weeklybulletin.php, posted early).
    The masthead on page 1 reads 'Catholic Parishes of Eastern Clearfield County'; page 2 gives one office
    (123 Good Street, Houtzdale PA 16651, (814) 378-7653, office@cpoecc.org) and one pastor for all churches.
    Seven churches carry Mass times on pages 4-6 (Christ the King, Immaculate Conception, St. Agnes, St.
    Mary of the Assumption, St. Severin, St. Basil the Great, Holy Trinity) and a 'Church Name Key' on
    page 3 lists nine codes. Separate stewardship and 'make checks payable to' boxes per canonical parish
    (St. Agnes p. 4, St. Basil p. 5, Christ the King p. 6) show it is one bulletin for three canonical
    parishes.
- url: https://cpoecc.org/images/weeklybulletin/2cdf15148eaa8fa3e95ef57e5163d9de.pdf
  seen: 2026-10-23
  quote: Ss. Peter & Paul Church
  note: Page 4 Mass-times box for St. Agnes, with Hawk Run (120 Sixth St.) and Grassflat (130 Indiana
    St.) each followed by 'No regular Masses'. Those two churches are not church rows (see open/ss-peter-and-paul-hawk-run
    and open/ss-peter-and-paul-grassflat).
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: 3) St. Basil the Great, Coalport
  note: 'Clergy list updated 8/7/2026: Schmolt, Rev. Johnathan P., ''Pastor ... 1) Christ the King, Houtzdale;
    2) St. Agnes, Morrisdale 3) St. Basil the Great, Coalport''. Pius, Rev. Cory L., ''Parochial Vicar
    ... 1) Christ the King, Houtzdale; 2) St. Agnes, Morrisdale; 3) St. Basil the Great, Coalport''. The
    directory''s own pastor fields on the web detail pages for these records name other people (Horgas,
    Perry, Amar, Solomon) and are unreliable.'
- url: https://www.eriercd.org/images/pdf/Final-Clearfield-Deanery2023B.pdf
  seen: 2026-10-23
  quote: will not have a weekend Mass
  note: 'Oct 2023 Clearfield Deanery final plan (effective 2023-12-01): Immaculate Conception, Osceola
    Mills merges into Christ the King, Houtzdale; St. Mary of the Assumption, Frenchville merges into
    St. Agnes, Morrisdale and becomes a secondary mission church; St. Severin remains a secondary mission
    church of St. Agnes; Ss. Peter and Paul, Grassflat and Hawk Run remain secondary churches ''now without
    mission status'' with no weekend Mass. The printable directory (Oct 6 2026) says Christ the King,
    St. Agnes and St. Basil are each ''Partnered with'' the other two. A plan; the bulletin decides.'
- url: https://discovermass.com/church/christ-the-king-houtzdale-pa/
  seen: 2026-10-23
  note: 'Cover image class on the church page reads ''bulletin-cover X-|2026-10-25|1792781902|3444'' (bulletin
    number 3444). Discover Mass carries the same 25 October 2026 issue (bulletin number 3444; downloaded
    file is a re-export of the same text, 2.5 MB vs 6.8 MB on the parish site). The St. Agnes (st-agnes-morrisdale-pa)
    and St. Basil (st-basil-the-great-coalport-pa) pages say ''no bulletins available''. Not used as the
    source: the parish site''s weeklybulletin.php is the primary channel and also lists inserts.'
research:
- method: pnpm fetch:check --diocese erie --parish catholic-parishes-of-eastern-clearfield-county --expected-identity
    'Eastern Clearfield County' (headed Chrome)
  url: https://cpoecc.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver page-pdfs on weeklybulletin.php picked the first-listed file (2cdf1514...pdf,
    25 Oct 2026 bulletin, 6.8 MB, 7 pages): transport ok, PDF, identity matched (''catholic parishes of
    eastern clearfield county'' in first-page text), issue date 2026-10-25 observed, freshness ''future''
    (posted 2 days early; not a failure), overall unverified only because of the early date. No separate
    recipe line was printed; provider_id pins the same page-pdfs recipe. Weeks when inserts are posted
    above the main bulletin (the 18 October week lists Insert 1, Insert 3, Insert 2 before ''Bulletin'')
    could make the first-listed file an insert; recheck on the next Sunday''s posting.'
- method: Listed all 24 files on weeklybulletin.php (2 Aug to 25 Oct 2026), downloaded all, text-grepped
    the 13 main issues for each church code; compared with the Discover Mass listing for Christ the King
    (bulletin 3444, same 25 Oct issue)
  url: https://cpoecc.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for structure: one bulletin. Three Discover Mass pages exist for CTK (live, same
    issue), St. Agnes and St. Basil (no bulletins); none is a distinct channel.'
---

## Publisher

One weekly bulletin, "Catholic Parishes of Eastern Clearfield County", covers three canonical parishes under one pastor, Rev. Johnathan P. Schmolt (clergy PDF 8/7/2026: pastor of Christ the King, Houtzdale; St. Agnes, Morrisdale; St. Basil the Great, Coalport; Rev. Cory L. Pius is parochial vicar of all three). The issue dated 25 October 2026, read on 2026-10-23, has a single office, a single set of announcements and one Mass-intentions list tagging each Mass with its building (CTK, IC, AG, MA, SEV, BA, HT; see the Church Name Key on page 3). The three canonical parishes appear only as separate stewardship and donation boxes. That is one bulletin, so one parish row. The row sits under Christ the King (the administrative office, 123 Good St., Houtzdale) with the masthead name.

## Worship sites

Seven churches hold Mass now, from the October 2026 bulletins' Mass-times boxes and Mass-intentions lines: Christ the King (Houtzdale), Immaculate Conception (Osceola Mills), St. Agnes (Morrisdale), St. Mary of the Assumption (Frenchville), St. Severin (Drifting; the directory files it under Morrisdale), St. Basil the Great (Coalport) and Holy Trinity (Ramey). Ss. Peter and Paul, Grassflat and Ss. Peter and Paul, Hawk Run are listed in the bulletin as "No regular Masses" and are in `open/` with a revisit at their patronal feast (29 June 2027). The two Eastern Catholic churches in the same area (St. John the Baptist Byzantine, Hawk Run; Annunciation of the BVM, Ukrainian, Ramey) are other-jurisdiction and belong to another batch; they are not linked here.

## Website and bulletin provider

`other`, read from cpoecc.org/weeklybulletin.php: a diocese-hosted template page with one PDF per issue under images/weeklybulletin/<md5>.pdf, newest first. The page also lists inserts and side flyers ("Bulletin Insert 1 Fr. Pius Letter", "Fundraising Minutes") that have no text layer or only a flyer; the file names are hashes, so a filename filter cannot separate them. See the fetch check in `research` for which file the resolver picked. clearfieldcatholic.org, which the printable directory still gives as these churches' website, is a different site (probe url: 'Clearfield Catholic', own weeklybulletin.php) and was not read here; the directory's current detail pages and the bulletin both give cpoecc.org.

## Not yet confirmed

Whether the resolver picks the main bulletin in weeks when inserts are listed first (see research). Whether Grassflat and Hawk Run ever have a patronal-feast or other occasional Mass (open/ records). Whether Discover Mass's Christ the King listing will stay in step with the parish site (not needed: the site is the source).
