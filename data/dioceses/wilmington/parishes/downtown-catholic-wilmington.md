---
name: Downtown Catholic (Cathedral of St. Peter, St. Mary of the Immaculate Conception, St. Patrick)
website: https://www.downtowncatholic.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-cathedral-parish-of-downtown-catholic-wilmington-de-19801
publication: ['url:https://www.church-bulletin.org/the-cathedral-parish-of-downtown-catholic-wilmington-de-19801']
group: City Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/the-cathedral-parish-of-downtown-catholic-wilmington-de-19801/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 of the 25 October 2026 issue (4 pages, scanned image, so no text layer; read from a rendering).
    Masthead ''Downtown Catholic'' with ''Very Reverend Joseph W. McQuaide, IV, Rector-Pastor'', Deacons
    Anthony J. Gallo and Roberto Ortiz. ''Scheduled Masses'' in three columns: Saint Patrick (Sunday *8
    am, 9:30 am, *11 am, 5 pm; Mon & Wed *5:30 pm; Tue & Thu 5:30 pm; First Fridays 5 pm Adoration, *6
    pm; First Saturdays *9 am; * = Latin), Cathedral of Saint Peter (Sunday 9:30 am; Mon, Wed, Fri 12:10
    pm; Saturday 4 pm), Saint Mary (Sunday 8 am; First Saturdays 11 am). The cover drawings caption the
    three churches: Saint Patrick, 15th and King Streets, founded 1880; Cathedral of Saint Peter, 6th
    and West Streets, 1816; Saint Mary of the Immaculate Conception, 6th and Pine Streets, 1858. One office:
    1414 N. King Street, (302) 652-0743.'
- url: https://www.downtowncatholic.com/
  seen: 2026-10-27
  quote: The Downtown Catholic Churches are individual parishes administered by the one pastoral team.
  note: 'Home page ''About Us''. Its giving form names three separate parish funds: ''ST MARY-WILMINGTON
    (34) ST PATRICK (44) ST PETERS CATHEDRAL (1)''.'
- url: https://www.downtowncatholic.com/bulletin.html
  seen: 2026-10-27
  quote: Bulletin - Downtown Catholic - Wilmington, DE
  note: Page title. The page's only bulletin link is the href https://www.jppc.net/onlinebulletins/309template.pdf
    (John Patrick Publishing no. 309; not visible text), which covers all three churches. No separate
    bulletin page for St. Mary or St. Patrick.
- url: https://jppc.net/onlinebulletins/309template.pdf
  seen: 2026-10-27
  note: 'probe url: redirects to https://www.church-bulletin.org/the-cathedral-parish-of-downtown-catholic-wilmington-de-19801
    (''The Cathedral Parish of Downtown Catholic Bulletin'', 500 North West Street, Wilmington, DE 19801),
    which lists dated PDFs newest first (2026-10-25, 10-18, 10-11, 10-04, 09-27 ...).'
research:
- method: 'Compared The Dialog''s 2026-03-26 ''United in Christ'' deanery realignment (City Deanery listed
    as Cathedral of Saint Peter, Saint Ann, Saint Anthony of Padua, Saint Elizabeth, Saint Hedwig, Saint
    Joseph, Saint Paul, Saint Thomas the Apostle) with cdow.org/deaneries (modified 2026-05-26: also lists
    Saint Mary of the Immaculate Conception and Saint Patrick), downtowncatholic.com, the 25 October 2026
    bulletin and a Dialog title/content search for ''downtown catholic'''
  url: https://thedialog.org/featured/bishop-koenigs-united-in-christ-update-going-beyond-pre-established-boundaries-experimenting-with-joint-pastoral-initiatives/
  checked: '2026-10-27'
  outcome: not-found
  next_action: 'None for row structure: the bulletin decides it. If the owner wants the canonical status,
    ask the diocese or read a decree; the Dialog list may simply name the cathedral for the whole Downtown
    Catholic team.'
  retry_when: A diocesan decree, Dialog article or revised deaneries page says St. Mary or St. Patrick
    was merged or suppressed
---

## Publisher

The three Downtown Catholic churches publish one weekly bulletin, John Patrick Publishing no. 309, 'The Cathedral Parish of Downtown Catholic'. downtowncatholic.com's only Bulletin page links `jppc.net/onlinebulletins/309template.pdf`, which redirects to the church-bulletin.org listing. The 25 October 2026 issue (page 1, an image; read from a rendering) has one masthead, 'Downtown Catholic', with one Rector-Pastor, Very Reverend Joseph W. McQuaide, IV, and one 'Scheduled Masses' box covering Saint Patrick, the Cathedral of Saint Peter and Saint Mary. So this is **one row** with three churches, the row the batch plan expected.

## Worship sites

Three churches, each with its own Mass in the same bulletin: the Cathedral of St. Peter (6th and West Streets), St. Mary of the Immaculate Conception (6th and Pine Streets; Sunday 8 am, First Saturday 11 am) and St. Patrick (15th and King Streets; the busiest, with Latin Masses). Each has its own church record. The diocese map lists all three; GCatholic lists St. Mary and St. Patrick and omits the cathedral.

## Is each still a parish? (the deanery disagreement)

The Dialog's 2026-03-26 realignment lists the City Deanery without St. Mary and St. Patrick; cdow.org/deaneries (modified 2026-05-26) still names both. Nothing found says either was merged or suppressed: the Downtown Catholic home page (read 2026-10-27) still calls them 'individual parishes administered by the one pastoral team' and its giving form still lists three funds. The likeliest reading is that the Dialog list names the cathedral for the whole team, but that is an inference. It does not change the row: canonical mergers don't merge rows, and the bulletin is one either way.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing as the playbook records for John Patrick bulletins. The cover is a scanned image, so `probe pdf` finds no text; the fetch check still passes. The old GCatholic site, smspwilmington.com, is not used. The diocese map's websites are `downtowncatholic.com` pages for the cathedral and St. Patrick and a catholicmasses.org listing for St. Mary, which is not a parish site.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish downtown-catholic-wilmington` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf; transport ok, document type PDF, freshness fresh (2 days). Identity is `unverified` to the tool (the cover is an image); the masthead read above settles it. The pinned recipe is already in `provider_id`.

## Not yet confirmed

The canonical status of St. Mary and St. Patrick (research above).
