---
name: Holy Rosary Parish
website: https://dioceseoferie.org/HolyRosary/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Holy Rosary Parish, Johnsonburg (merged with St. Anne, Wilcox, 2017)
evidence:
- url: https://dioceseoferie.org/HolyRosary/weeklybulletin.php
  seen: 2026-10-23
  quote: No Bulletin found.
  note: 'The parish''s diocese-hosted Weekly Bulletin page (same template as stleomagnus.org and stjosephforce.org,
    which list PDFs) lists no issue. Read with curl and in headed Chrome. Note the path is case-sensitive:
    /HolyRosary/ answers 200 (probe url says ok, bulletin link weeklybulletin.php); the lowercase /holyrosary/
    gives 404.'
- url: https://discovermass.com/church/holy-rosary-johnsonburg-pa/
  seen: 2026-10-23
  quote: There are currently no bulletins available for Holy Rosary.
  note: 'Discover Mass page for Holy Rosary lists Mass Times ''Saturday 5:30pm Sunday 10:00am Monday 7:45am
    ... Thursday 7:45am ... Friday 7:45am''; no bulletin posted. The St. Anne page (st-anne-wilcox-pa)
    is the same: ''no bulletins available for St Anne'', Mass Times Sunday 8:30am.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: 'Sunday: 10 a.m.; 8:30 a.m. - St. Anne'
  note: 'Printable diocese directory dated Oct. 6, 2026, Johnsonburg: Holy Rosary Parish, 210 Bridge St.;
    pastor Reverend David Wilson; Daily Monday, Thursday and Friday 7:45 a.m. (Subject to change, check
    bulletin.); Saturday 5:30 p.m.; St. Anne Church, Wilcox, ''Secondary Mission''. No Holy Cross, Rasselas
    entry.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ..........................................................................................
    Holy Rosary, Johnsonburg
  note: 'Clergy PDF (8/7/2026): Wilson, Rev. David J., pastor of Holy Rosary, Johnsonburg (606 Penn Street);
    his only assignment.'
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE_MergingSt.AnneWilcoxintoHolyRosaryJohnsonburg.pdf
  seen: 2026-10-23
  quote: This decree is effective February 13, 2017, anything to the contrary notwithstanding.
  note: 'Merger decree: St. Anne Parish, Wilcox merged by extinctive union into Holy Rosary, Johnsonburg;
    St. Anne church became a secondary mission church of Holy Rosary. A merger closes nothing; the bulletin
    question is separate.'
- url: https://www.ferraginefuneralhome.com/obituaries/ann-farr
  seen: 2026-10-23
  quote: Mass of Christian Burial for Ann Marie Farr to be conducted at Holy Rosary Church, Johnsonburg,
    on Wednesday May 6, 2026, at 10 AM with Fr. David Wilson, Pastor, as celebrant.
  note: Obituary snippet from a web search, evidence that Holy Rosary is open with Fr. Wilson in 2026;
    one of several (Pennington, 16 April 2026; Zuraski, 5 Aug 2026).
revisit: Re-read https://dioceseoferie.org/HolyRosary/weeklybulletin.php for posted PDFs; also check Discover
  Mass slugs holy-rosary-johnsonburg-pa and st-anne-wilcox-pa for a first bulletin.
revisit_after: 2026-12-01
research:
- method: probe url dioceseoferie.org/HolyRosary/ (ok, bulletin link weeklybulletin.php); curl and headed-Chrome
    read of weeklybulletin.php; 17 site pages' links scanned (home, About, Join Us, St. Anne); Discover
    Mass pages for Holy Rosary, St. Anne, Holy Cross (all 'no bulletins available'); ParishesOnline search
    API at 41.488,-78.674 (distance 15 and 40) returned only a senior center and a Methodist church; DuckDuckGo
    searches for the parish bulletin
  url: https://dioceseoferie.org/HolyRosary/weeklybulletin.php
  checked: '2026-10-23'
  outcome: not-found
  next_action: Re-read the Weekly Bulletin page and the two Discover Mass pages; the parish's Facebook
    page says 'Weekly bulletins are available on our website' (profile pages need login, so not read)
    and the site advertises a MyParish app, whose contents were not read.
  retry_when: A PDF appears on weeklybulletin.php, a Discover Mass page gains a current bulletin, or a
    ParishesOnline organization for Johnsonburg turns up
  revisit_after: 2026-12-01
bulletin_status: not-found
---

## Publisher

No bulletin could be read. Holy Rosary, Johnsonburg (with its mission St. Anne, Wilcox) has a diocese-hosted site whose Weekly Bulletin page says 'No Bulletin found.' (read 2026-10-23, curl and headed Chrome). Discover Mass has pages for the parish and for St. Anne, both 'no bulletins available'. The ParishesOnline search API near the parish returned no Catholic organization. The row is therefore `no_bulletin` (kept in the records, left off the site) with `bulletin_status: not-found`: the check covered those sources only, and the parish may publish through the MyParish app or Facebook, neither of which was readable.

The parish is open: the pastor is Rev. David J. Wilson (clergy PDF, 8/7/2026), the Oct. 6, 2026 printable directory gives Mass times, and 2026 obituaries (16 April, 6 May, 5 August) have funeral Masses at Holy Rosary Church with Fr. Wilson as celebrant.

## Worship sites

Two churches: Holy Rosary, 210 Bridge St., Johnsonburg (parish church) and St. Anne, 75 Buchanan St., Wilcox (secondary mission church since the merger decree effective 2017-02-13). Holy Cross, Rasselas (4672 Rasselas Rd., Wilcox) was a secondary church of this parish; it was relegated by decree effective 2017-09-07 and is in `excluded/holy-cross-wilcox`. The directory lists no other church for this parish.

## Website and bulletin provider

website is https://dioceseoferie.org/HolyRosary/ (the weeklybulletin.php page is empty). The survey recorded HTTP 403 for the lowercase path https://dioceseoferie.org/holyrosary; on 2026-10-23 that path returns 404 (curl and `probe url`), while the directory's own capital-H URL /HolyRosary/ returns 200 to both, so the site is not blocked, only case-sensitive. Provider `no_bulletin`.

## Not yet confirmed

A bulletin. Retry when the Weekly Bulletin page lists a PDF or a Discover Mass page gains a bulletin (see `revisit` and research). The MyParish app and the Facebook page were not read.
