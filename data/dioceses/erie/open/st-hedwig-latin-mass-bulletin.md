---
name: St. Hedwig Latin Mass Community bulletin (latinmasserie.org)
revisit: Split St. Hedwig into its own row once the pipeline can read Wix blog attachments (latinmasserie.org
  posts; wixlinks.py method)
revisit_after: null
roster: []
evidence:
- url: https://www.latinmasserie.org/post/bulletin-for-october-18-2026
  seen: 2026-10-23
  quote: Bulletin for Sunday, October 18, 2026 - External Solemnity of Saint Hedwig
  note: Wix blog post on latinmasserie.org, published 2026-10-17 (blog-feed.xml pubDate), carrying one
    attached PDF 'Bulletin for 10_18_2026-2.pdf' (262 KB, Download PDF button). The PDF is delivered only
    by clicking the button (headed Chrome download, wixmp token URL for ugd/071fae_2a693066c86147398046c9bff426fe80.pdf);
    the page HTML and the blog feed contain no PDF link, so the pipeline's 'other' resolver finds none.
- url: https://www.latinmasserie.org/post/bulletin-for-october-18-2026
  seen: 2026-10-23
  quote: Please note that all email addresses and phone numbers are removed from the online bulletin
  note: 'Post text above the attachment. The downloaded PDF (2 pages, read with pdftotext) is headed ''St.
    Hedwig Church / Latin Mass Community'', ''October 18, 2026 / External Solemnity of St. Hedwig'', MASS
    TIMES ''Sunday: 9:30am, Tuesday: 5:30pm'', CONFESSIONS Sunday 8:45-9:15am and Tuesday 5:00-5:20pm,
    MASS INTENTIONS for 18 and 20 October and 25 October (Christ the King), clergy Fr. Ian McElrath, Fr.
    James Power, Fr. Joseph Petrone, a weekly collection (''October 11 $ 1,918.00'', checks to ''St. Hedwig
    Church''), and ''To schedule a Mass or the sanctuary lamp, please contact Fr. Glover at St. Stanislaus
    Church at (814) 452-6606''. Page 2 is a chaplain''s column. Its calendar is the traditional one (Seventeenth
    Sunday After Pentecost etc.), unlike the St. Stanislaus bulletin.'
- url: https://www.latinmasserie.org/blog-feed.xml
  seen: 2026-10-23
  note: 'curl of the Wix blog feed (the quote was in a CDATA title and the recheck fetcher does not find
    it): Blog feed lists one post per issue: 18 Oct (posted 17 Oct), 20 Sep (posted 20 Sep), ''Bulletin
    for September 9, 2026'' (posted 5 Sep; the title date is off, the post text says ''Fifteenth Sunday
    After Pentecost''), 30 Aug, 23 Aug, 16 Aug, 9 Aug, 2 Aug, 26 Jul. So the weekly series has gaps (13
    and 27 Sep, 4 and 11 Oct have no post in the feed) and the 25 Oct issue was not yet posted on 2026-10-23.'
- url: https://container.parishesonline.com/bulletins/14/1710/20261025B.pdf
  seen: 2026-10-23
  quote: TRADITIONAL LATIN MASS APOSTOLATE
  note: 'The St. Stanislaus / Our Mother of Sorrows bulletin heads page 1 ''TRADITIONAL LATIN MASS APOSTOLATE
    AT ST. HEDWIG''S - LATIN MASS: Sunday at 9:30AM, Tuesday at 5:30PM'' but its Mass intentions and sanctuary
    candles omit St. Hedwig; the Latin Mass Community''s own bulletin carries those.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: 'Daily: Latin Mass on Tuesday at 5:30 p.m.'
  note: 'Printable directory dated Oct. 6, 2026: St. Hedwig Church, ''Secondary Church'' under St. Stanislaus
    Parish, 521 E. 3rd St., ''Sunday: Latin Mass at 9:30 a.m.''; website listed as http://www.ststanserie.org
    (the web record 10217 gives http://latinmasserie.org).'
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE_MergingSt.HedwigandSt.Stans.pdf
  seen: 2026-10-23
  quote: Saint Hedwig Parish in Erie shall be merged and subsumed into Saint Stanislaus Parish
  note: 'Merger decree (Presbyteral Council support dated June 28, 2016; the effective date is not in
    the text layer I read, which ends mid-sentence): St. Hedwig Parish merged into St. Stanislaus, with
    the Polish-heritage pastoral care ''provided instead by an apostolate assigned to Saint Stanislaus
    Parish''. A merger decree closes nothing: the church stays open for the Latin Mass.'
parish: st-stanislaus-erie
line1: 521 E 3rd St.
city: Erie
state: PA
postal_code: '16507'
research:
- method: probe url; blog-feed.xml; browser download of the Oct 18 post's attachment; pnpm fetch:check
    --diocese erie --parish st-hedwig-erie
  url: https://www.latinmasserie.org/post/bulletin-for-october-18-2026
  checked: '2026-10-23'
  outcome: unsupported-format
  next_action: 'Split St. Hedwig into its own parish row once the pipeline can read Wix blog attachments
    (latinmasserie.org posts; scratch/map-erie/tools/wixlinks.py method: click the file-upload-viewer
    button and capture the download).'
  retry_when: The fetch pipeline gains a Wix blog-attachment collector, or the community posts the PDF
    as a plain link
---

## What is known

The Traditional Latin Mass apostolate at St. Hedwig Church (521 E. 3rd St., Erie) posts its own weekly bulletin on latinmasserie.org (Wix blog, one post per issue, PDF attached). I read the 18 October 2026 issue on 2026-10-23: a two-page PDF headed 'St. Hedwig Church / Latin Mass Community' with Mass times (Sunday 9:30 AM, Tuesday 5:30 PM), St. Hedwig-only Mass intentions, a weekly collection, its own clergy (Fr. Ian McElrath, Fr. James Power, Fr. Joseph Petrone) and 'please contact Fr. Glover at St. Stanislaus Church' for Mass scheduling. It is a different document from the St. Stanislaus / Our Mother of Sorrows bulletin (container 14/1710; comparing the 18 Oct issues: different masthead, traditional calendar, own intentions and collection). Under the diocese rule (an apostolate with its own regular bulletin is its own row) this would be a separate parish row.

The pipeline cannot fetch it: `fetch:check` on 2026-10-23 found 'No PDF links found on bulletin post page' because the attachment is a Wix file viewer whose download URL is minted on click (the file itself is public at https://www.latinmasserie.org/_files/ugd/071fae_2a693066c86147398046c9bff426fe80.pdf once the id is known). Posting is irregular (no post for 13 or 27 Sep, 4 or 11 Oct; the 25 Oct issue was not up on 2026-10-23). The draft parish record (website https://www.latinmasserie.org/blog, provider other, publication url:https://www.latinmasserie.org/blog#st-hedwig-latin-mass-community, bulletin_status unsupported-format) was removed unpromoted.

## Why it is not decided

Orchestrator decision 2026-10-23: no Wix collector in this PR. Because the St. Stanislaus bulletin prints St. Hedwig's Latin Mass times on page 1 every week, its schedule covers the church, so church st-hedwig-erie sits under parish st-stanislaus-erie for now. The separate row is deferred until the pipeline can read Wix blog attachments; at that point restore the parish row from the evidence above, move the church to it, and add a 'separate' publication review against st-stanislaus-erie.
