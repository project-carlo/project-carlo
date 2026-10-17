---
name: Holy Name of Mary Parish and St. Brigid Parish
website: https://holynameofmary.com/bulletins
bulletin_provider: other
provider_id: ''
publication: ['url:https://holynameofmary.com/bulletins']
group: Holy Name of Mary Parish; Saint Brigid Parish
evidence:
- url: https://img1.wsimg.com/blobby/go/05fa032b-63a4-434f-9af9-1ca3c845125d/10.11.26.pdf
  seen: 2026-10-16
  quote: Holy Name of Mary Church
  note: Page 1 of the 11 October 2026 issue (28th Sunday in Ordinary Time), bilingual; masthead names
    Holy Name of Mary Church, 278 South Main Street, Montrose, and "Pastor ... Father Kevin Miller".
- url: https://img1.wsimg.com/blobby/go/05fa032b-63a4-434f-9af9-1ca3c845125d/10.11.26.pdf
  seen: 2026-10-16
  quote: MASS TIMES until OCTOBER 31/NOVEMBER 1, 2026
  note: 'Page 2: the schedule covers three churches: Holy Name of Mary Montrose (Sat 4:00pm bilingual,
    Sun 12:30pm, Mon and Thu 12:00pm), St. Francis Xavier Friendsville (Sat 6:30pm, Sun 7:30am, Fri 12:00pm)
    and St. Augustine Silver Lake (Sun 10:00am, Tue, Wed and Sat 8:30am).'
- url: https://img1.wsimg.com/blobby/go/05fa032b-63a4-434f-9af9-1ca3c845125d/10.11.26.pdf
  seen: 2026-10-16
  quote: Beginning on October 31 and November 1, our NEW Mass Schedule will start!
  note: 'Page 7: from 31 October HNM moves to Sat 6:30pm, Sun 8:00am (English) and Sun 1:00pm (Spanish);
    the date list keeps St. Francis Xavier Friendsville (Sat 4:00pm) and St. Augustine Silver Lake (Sun
    10:00am).'
- url: http://www.tiogaweb.com/church/
  seen: 2026-10-16
  quote: The St. Brigid bulletins are online CLICK ABOVE FOR BULLETINS
  note: St. Brigid Parish site (finder homepage). Its bulletin link goes to issuu.com/search?q=st+brigid+parish;
    the uploader (issuu.com/tiogaweb, read in a browser 2026-10-16) has no St. Brigid bulletin after "AUGUST
    3, 2025 BULLETIN"; its later uploads are a monthly "CommunityPress". The older link issuu.com/stbrigid
    answers 404.
- url: https://www.dioceseofscranton.org/find-a-parish/saint-brigid-parish-friendsville
  seen: 2026-10-16
  quote: Reverend Kevin M. Miller – Pastor
  note: 'Diocese finder page for St. Brigid Parish: the same pastor as Holy Name of Mary.'
- url: https://discovermass.com/church/st-francis-xavier-friendsville-pa/
  seen: 2026-10-16
  note: Discover Mass page "St. Brigid (St. Francis Xavier)" lists no bulletins (issues.py, 2026-10-16).
promoted: 2026-10-17
---

## Publisher

Holy Name of Mary Parish, Montrose publishes a weekly bilingual (English/Spanish) bulletin
on its own site. The 11 October 2026 issue's page 1 names "Holy Name of Mary Church", 278
South Main Street, with "Pastor ... Father Kevin Miller". Father Miller is also pastor of
Saint Brigid Parish, Friendsville (diocese finder), and this bulletin carries St. Brigid's
whole Mass schedule: page 2's "MASS TIMES until OCTOBER 31/NOVEMBER 1, 2026" lists Holy
Name of Mary, St. Francis Xavier (Friendsville) and St. Augustine (Silver Lake) side by
side, and page 7 lists the new schedule from 31 October for all three.

St. Brigid has no bulletin of its own now. Its site (tiogaweb.com/church, the finder's
homepage) says "The St. Brigid bulletins are online" and links an Issuu search; the
uploader's newest St. Brigid bulletin there is 3 August 2025 (read 2026-10-16), the old
issuu.com/stbrigid account is gone, and its Discover Mass page lists no issues. So the
member's own channel is silent and the shared pastor's current bulletin carries its
schedule: one row for both canonical parishes (`group` names both). What I did not see is a
masthead naming St. Brigid; the evidence for the fold-in is the schedule, not a title.

## Worship sites

Three, all in the 11 October 2026 schedule:

- Holy Name of Mary, Montrose (`holy-name-of-mary-montrose`).
- St. Francis Xavier, Friendsville (`st-francis-xavier-friendsville`), St. Brigid Parish.
- St. Augustine, Silver Lake / Brackney (`st-augustine-brackney`), St. Brigid Parish.

St. Brigid's own "Our Churches" page (dated 2013) lists three more churches as closed and
merged into St. Brigid: St. Joseph (St. Joseph, Choconut Twp., final Mass 18 July 2010),
St. Patrick (Middletown Twp., 21 June 2009) and St. Thomas the Apostle (Little Meadows, 19
June 2010). None is in the finder or in this diocese's GCatholic roster, so no records were
made for them.

## Website and bulletin provider

holynameofmary.com/bulletins (GoDaddy Website Builder) shows a "CURRENT BULLETIN" with a
"Download PDF" link to `img1.wsimg.com/blobby/go/<site id>/<M>.<D>.<YY>.pdf` (10.11.26.pdf
on 2026-10-16), plus older issues as .docx downloads. The page loaded in a browser
(parish-site-access visit.py); plain curl through the proxy was cut off twice. The PDF has a
text layer. No publisher id, so `other`, with the bulletin page as publication. No
`fetch:check` recipe pinned: after promotion (2026-10-17) it could not load the page
(`ERR_CONNECTION_RESET` from the sandbox, twice). `page-pdfs` on the bulletin page should
find the one PDF, whose name (`10.11.26.pdf`) the resolver dates.

## Not yet confirmed

That St. Brigid has no other current channel (its Facebook page "St Brigid Parish" was not
readable here). If it resumes a bulletin of its own, its two churches move to a row of
their own.
