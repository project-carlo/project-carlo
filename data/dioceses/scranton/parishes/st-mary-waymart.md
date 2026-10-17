---
name: St. Mary Parish
website: https://stmaryswaymart.com/newbulletin
bulletin_provider: other
provider_id: page-images
publication: ['url:https://stmaryswaymart.com/newbulletin']
group: Saint Mary Parish
evidence:
- url: https://stmaryswaymart.com/newbulletin
  seen: 2026-10-16
  quote: October 10-11, 2026
  note: 'The parish site''s Bulletins page (Squarespace), listing one captioned image per weekend from
    June to 10-11 October 2026. The page also gives "Parish Life Coordinator: Deacon Edward T. Kelly"
    and "Sacramental Minister: Reverend Joseph S. Sitko".'
- url: https://images.squarespace-cdn.com/content/v1/56b29d4a2eeb817ddb26b146/ff6824bd-b761-4165-b283-9a0a57d84349/Bulletin+2026+October+10-11.jpg?format=1500w
  seen: 2026-10-16
  note: 'The 11 October 2026 issue: a single JPEG (1500x911) of one bulletin spread, read by viewing the
    image. Headed "Sunday, October 11, 2026, Twenty-Eighth Sunday in Ordinary Time"; "Mass Schedule for
    the Week": 10/10 Saturday 4:00 PM, 10/11 Sunday 8:00 AM and 9:45 AM, 10/12-10/16 Monday to Friday
    9:00 AM, 10/17 4:00 PM, 10/18 8:00 AM and 9:45 AM, no church named (one church). Image only, so recheck
    cannot find any quote in it.'
- url: https://discovermass.com/church/st-mary-of-the-assumption-waymart-pa/
  seen: 2026-10-16
  note: Discover Mass pages "St. Mary of the Assumption" and "St. Patrick" (st-patrick-waymart-pa), Waymart,
    list no bulletins (issues.py).
promoted: 2026-10-17
---

## Publisher

St. Mary Parish, Waymart, led by a parish life coordinator (Deacon Edward T. Kelly) with a
sacramental minister, posts its weekly bulletin on its own Squarespace site as an image.
The 10-11 October 2026 issue's "Mass Schedule for the Week" lists Saturday 4:00 PM, Sunday
8:00 AM and 9:45 AM and Monday to Friday 9:00 AM, with no church named: one church, as on
the site's Mass schedule and in the finder. The diocese does not group it with another
parish.

## Worship sites

One: St. Mary, 242 Carbondale Road (`st-mary-waymart`). Discover Mass also has an empty
page for a "St. Patrick, Waymart"; no current source (finder, GCatholic roster, the
parish's site or bulletin) lists a St. Patrick church in Waymart, so it is not recorded.

## Website and bulletin provider

stmaryswaymart.com/newbulletin (reached from the "Bulletins" page's "Click here for
bulletin") lists each weekend's bulletin as a captioned image on images.squarespace-cdn.com
(the caption is the date, e.g. "October 10-11, 2026"); the full-size image is the whole
bulletin spread. **There is no PDF and no text: the pipeline has to read an image.** Plain
curl reads the page. No publisher id, so `other`, with recipe `page-images`: a collector that reads a page's
images only when a recipe names it, taking those dated or labelled "bulletin" (the
gallery's undated "2026 BULLETIN COVER TEMPLATE" image is dropped once dated ones are
found). `fetch` stores the image as a one-page PDF. `fetch:check` after promotion
(2026-10-17) picked `Bulletin+2026+October+10-11.jpg` (`current`) and downloaded it as a
PDF. The cover template (a fixed front page, not fetched) is not part of the stored issue;
the weekly image carries the week's Mass schedule.

## Not yet confirmed

How well the extractor reads a 1500-pixel spread of small type, once fetched.
