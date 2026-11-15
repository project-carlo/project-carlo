---
name: Resurrection Coptic Catholic Church (Park Slope)
reason: no-bulletin
line1: 328 14th St.
city: Brooklyn
state: NY
postal_code: '11215'
decided: 2026-11-14
roster: ['gcatholic:16803']
evidence:
- url: https://gcatholic.org/churches/usa-02/16803
  seen: 2026-11-12
  quote: 'Jurisdiction: Diocese of Brooklyn'
  note: 'GCatholic 16803, ''Chapel of the Resurrection (Coptic)'', rite Coptic (Alexandrian), history
    1985, Plus Code 87G8M277+WH, 328 14th St., Brooklyn, New York 11215, telephone +1 (718) 499-6946.
    No eparchy: the Coptic Catholic Church has none in the US.'
- url: https://nominatim.openstreetmap.org/search?q=328+14th+Street,+Brooklyn,+NY&format=jsonv2
  seen: 2026-11-12
  quote: Resurrection Coptic Catholic Church, 328, 14th Street, Park Slope, Brooklyn
  note: OSM way 250424858, amenity place_of_worship, denomination catholic, at 40.66461, -73.98618.
- url: https://html.duckduckgo.com/html/?q=%22Resurrection+Coptic+Catholic%22+Brooklyn+Sunday+mass+time
  seen: 2026-11-14
  quote: MASS SCHEDULE 📅 Sunday, November 16, 2025 - 10:00 a.m. ⛪ Resurrection Coptic Catholic Church
    - Brooklyn, NY 328 14th Street, Brooklyn, NY 11215
  note: DuckDuckGo result snippet for the parish's own Facebook page (https://www.facebook.com/people/Resurrection-Coptic-Catholic-Church/100064995902629/,
    'Resurrection Coptic Catholic Church كنيسة القيامة للأقباط الكاثوليك'). Logged out, the page itself
    shows only its newest post (4 October 2026, a hymn video), so the post was not read on Facebook.
- url: https://www.facebook.com/people/Resurrection-Coptic-Catholic-Church/100064995902629/
  seen: 2026-11-14
  note: 'Read with parish-site-access visit.py: intro ''Msgr. Francis Fayez · Page · Religious organization
    · 328 14th St, New York, NY · (718) 499-6946 · contact@francisfayez.com · francisfayez.com''; newest
    post 4 October 2026. No bulletin or schedule visible logged out.'
- url: https://thetablet.org/brooklyn-coptic-catholics-rejoice-as-pastor-is-appointed-monsignor/
  seen: 2026-11-14
  quote: His website (francisfayez.com) is a portal to social media channels that stream the Mass and
    post his homilies
  note: 'The Tablet, 2022-11-15: solemn Mass at Resurrection Coptic Catholic Church, Park Slope, for its
    pastor Msgr. Francis Fayez, pastor since 2013.'
- url: https://www.francisfayez.com/pdf/
  seen: 2026-11-14
  note: 'Read with visit.py (probe url and probe get get no answer from the host). The pastor''s site
    menu: Home, About, Books, Announcements, Videos, Hymns, Audio, Photos, Iconography, PDF, Powerpoint.
    /pdf/ lists teaching booklets (newest ''Pentecost and the Descent of the Holy Spirit – 2025'', 20
    pages, uploaded 2025/06; then a 2024 Immaculate Conception text, ''Lenten Issue 2015'', ''Palm Sunday
    2017''...), not a weekly bulletin. /announcements/ and /church-services/ have no content beyond the
    menu; /videos/masses-2/ lists old Mass videos (2012, 2016).'
- url: https://www.facebook.com/francisfayez.org/about_contact_and_basic_info
  seen: 2026-11-14
  note: 'The pastor''s second page, ''The Lord''s Banquet'' (intro ''The Resurrection Coptic Catholic
    Church 328 14th Street Brooklyn NY 11215''): contact info and an ''Hours'' field with no times shown
    logged out; newest post 11 November 2026, a hymn video. No bulletin.'
revisit: 'Confirm a 2026 Mass schedule (the newest one found is the parish Facebook page''s post for Sunday
  16 November 2025, read only as a search snippet) and look again for a bulletin: the pastor''s site francisfayez.com
  (Announcements, Church Services, PDF) and the two Facebook pages.'
revisit_after: 2027-05-01
research:
- method: DuckDuckGo html search (church name, francisfayez.com, Sunday Mass time); The Tablet wp-json
    search 'Coptic'; church directory listings (churchdirectoryusa, thechurchmap, findachurchnearme);
    visit.py on francisfayez.com (home timed out; /about/, /announcements/, /church-services/, /pdf/,
    /videos/, /videos/masses-2/) and both Facebook pages; Yahoo search answered HTTP 500
  url: https://www.francisfayez.com/pdf/
  checked: '2026-11-14'
  outcome: not-found
  next_action: Look for a bulletin or a posted weekly schedule on francisfayez.com (Announcements, Church
    Services) and the Facebook pages; if one appears, make a parish row (website where it is posted) and
    link the church to it.
  retry_when: francisfayez.com posts announcements or a schedule, or a later search finds a bulletin
  revisit_after: 2027-05-01
---

## Why it is excluded

The owner decided (answer to the eastern-catholic batch's flag, 2026-11) that this Coptic Catholic church, which GCatholic 16803 places under "Jurisdiction: Diocese of Brooklyn" rather than an eparchy, is mapped under Brooklyn like any chapel with public Mass: a parish row if it has a bulletin, otherwise a no-bulletin exclusion. It is not an other-jurisdiction exclusion.

**It holds public Mass.** The parish's own Facebook page ('Resurrection Coptic Catholic Church كنيسة القيامة للأقباط الكاثوليك') posted "MASS SCHEDULE 📅 Sunday, November 16, 2025 - 10:00 a.m. ⛪ Resurrection Coptic Catholic Church - Brooklyn, NY 328 14th Street", inviting "your friends, youth, and families". I read that post only as DuckDuckGo's snippet on 2026-11-14; logged out, Facebook shows just the newest post (4 October 2026, a hymn video), so the post itself was not opened. The Tablet (2022-11-15) reports a solemn public Mass there and calls Msgr. Francis Fayez pastor since 2013; both of the pastor's Facebook pages were posting in October and November 2026. No 2026 schedule was found: that Mass is still held is inferred from the 2025 post and the active pages, not read.

**It publishes no bulletin found.** The pastor's site, francisfayez.com, which both Facebook pages give as the church's website, has a 'PDF' section of occasional teaching booklets (newest Pentecost 2025, 20 pages), not a weekly bulletin, and its Announcements and Church Services pages are empty. The Facebook pages post hymn videos. Neither carries a bulletin or a weekly schedule the pipeline could read (read 2026-11-14 with visit.py; the host doesn't answer `probe url`).

Address: 328 14th St., Brooklyn NY 11215 per GCatholic, OSM (way 250424858, 'Resurrection Coptic Catholic Church', 40.66461, -73.98618) and both Facebook pages; the parish page's '328 14th St, New York, NY' is the same street address with the city given as New York. Not in the Brooklyn Mass finder or directory rosters.

## What would change this

A bulletin or a regularly posted weekly schedule on francisfayez.com or a Facebook page would make it a parish row with this church. A source saying Masses stopped (the pastor leaving with no successor, the building sold) would make it `closed`. See `revisit`: a 2026 schedule has not been read yet.
