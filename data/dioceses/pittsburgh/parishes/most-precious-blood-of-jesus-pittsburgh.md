---
name: Most Precious Blood of Jesus Parish (Institute of Christ the King)
website: https://institute-christ-king.org/pittsburgh-home
bulletin_provider: other
provider_id: page-pdfs https://institute-christ-king.org/pittsburgh-bulletins
publication: ['url:https://institute-christ-king.org/pittsburgh-bulletins']
group: ''
evidence:
- url: https://institute-christ-king.org/images/pittsburgh/bulletins/2026-10-18.pdf
  seen: 2026-10-23
  note: 'Bulletin of 18 October 2026 (4 pages, image only, no text layer; the server answers 406 to a
    bare curl, 200 with a browser User-Agent). Rendered page 1 reads ''MOST PRECIOUS BLOOD of JESUS PARISH
    / A Roman Catholic Personal Parish for the Extraordinary Form in the Diocese of Pittsburgh / 21st
    Sunday after Pentecost, October 18, A.D. 2026 / Mass Schedule: Sundays: 8am, 11am; Monday: 12 Noon;
    Tuesday: 12 Noon & 7pm; Wednesday through Friday: 12 Noon; 1st Friday of Month: 12 Noon & 7pm; Saturday:
    9am / Parish Office 3250 California Avenue, Pittsburgh, PA 15212, 412-761-1508 / Canon William Avis,
    Pastor''. recheck cannot find the image text.'
- url: https://institute-christ-king.org/pittsburgh-home
  seen: 2026-10-23
  quote: Most Precious Blood of Jesus Parish celebrates Mass daily in the "Extraordinary form" of the
    Roman Rite
  note: 'Rendered in headed Chrome (visit.py --bulletin): verdict ok, no publisher id embedded. Home page
    lists Sunday Masses 8:00 AM Low Mass and 11:00 AM High Mass; Daily Masses Monday - Friday 12:00 Noon,
    Saturday 9:00 AM, also Tuesday 7:00 PM and First Fridays 7:00 PM; address 3250 California Avenue.
    ''Latest Bulletin'' links to images/pittsburgh/bulletins/2026-10-18.pdf.'
- url: https://institute-christ-king.org/pittsburgh-bulletins
  seen: 2026-10-23
  note: 'Bulletins page (visit.py --bulletin): bulletin PDFs with no publisher id, self-hosted. Fifteen
    dated weekly files from 2026-07-12 to 2026-10-18 (images/pittsburgh/bulletins/<yyyy-mm-dd>.pdf; one
    named -wFinRept, one 09-06... all Sunday dates), newest 2026-10-18.'
- url: https://parishesonline.com/organization/most-precious-blood-of-jesus-parish
  seen: 2026-10-23
  note: 'probe po: LPi org 0018000000Qx7sEAAR ''Most Precious Blood of Jesus - Latin Mass Community''
    (3250 California Ave; website institute-christ-king.org) resolves to container 14/1701, the Christ
    Our Savior bulletin (footer ''Christ Our Savior, Pittsburgh, PA 14-1701''). Not this parish''s bulletin,
    so no po-org/lpi/po-container id is recorded here.'
- url: https://diopitt.org/risen-lord
  seen: 2026-10-23
  quote: Instead it became the church of the newly established Most Precious Blood of Jesus Parish, North
    Side, where the traditional Latin Mass is celebrated.
  note: 'Diocese history page (headed Chrome; 403 to recheck): the church at 3250 California Ave is the
    former Risen Lord Church (the former St. Francis Xavier), transferred to this personal parish in 2019.
    The directory lists the Mass Finder parish at the same address with ''Sunday 8:00 a.m. (Low Mass)
    | 11:00 a.m. (High Mass)''.'
promoted: 2026-10-23
bulletin_status: available
publication_reviews:
- parish: christ-our-savior-pittsburgh
  decision: separate
  evidence:
  - url: https://institute-christ-king.org/images/pittsburgh/bulletins/2026-10-18.pdf
    seen: 2026-10-23
    note: 'Masthead comparison of the two 18 October 2026 bulletins: the Institute''s PDF (rendered) has
      the masthead ''Most Precious Blood of Jesus Parish ... Personal Parish for the Extraordinary Form'',
      Canon William Avis, and serves one church, 3250 California Avenue; the Christ Our Savior masthead
      (ParishesOnline 14/1701) names Fr. Michael Caridi and serves three other churches (St. Peter, St.
      Boniface, St. Cyril of Alexandria). Different publishers, mastheads, clergy and member churches;
      a stale LPi org named for Most Precious Blood merely points at 14/1701.'
---

## Publisher

Most Precious Blood of Jesus Parish is a personal parish for the Extraordinary Form (traditional Latin Mass) staffed by the Institute of Christ the King Sovereign Priest; it was established 2019-07-01 and took over the former Risen Lord Church at 3250 California Avenue, Brighton Heights. It publishes its own weekly bulletin as a PDF on the Institute's Pittsburgh site (institute-christ-king.org/pittsburgh-bulletins). The 18 October 2026 issue (read 2026-10-23) is headed "Most Precious Blood of Jesus Parish ... A Roman Catholic Personal Parish for the Extraordinary Form in the Diocese of Pittsburgh" and lists the Mass schedule for the one church. It is a different bulletin from Christ Our Savior's (container 14/1701), although a stale LPi org named for this parish points at that container (see evidence).

## Worship sites

One church: 3250 California Avenue (former Risen Lord / St. Francis Xavier). Sunday 8am (Low Mass) and 11am (High Mass) plus daily weekday Masses per the bulletin and the Institute page.

## Website and bulletin provider

The diocese directory gives www.mostpreciousbloodparish.org, which redirects to institute-christ-king.org/pittsburgh-home (a Joomla site, not Cloudflare-blocked in the browser). Provider is `other`, pinned to the bulletin listing page (`page-pdfs`). **The bulletin PDF is image-only** (no text layer), so the pipeline must read the Mass schedule from the rendered pages. The server rejects clients without a browser User-Agent (406).

## Not yet confirmed

The fetch check result is recorded in the manifest; the Institute site's PDFs have no text layer, so recheck cannot verify the bulletin text.
