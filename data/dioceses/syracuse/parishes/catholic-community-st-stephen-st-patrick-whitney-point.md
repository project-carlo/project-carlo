---
name: Catholic Community of St. Stephen, St. Patrick & Our Lady of Perpetual Help
website: https://www.ccsssp.com
bulletin_provider: parishes_online
provider_id: catholic-community-of-st-stephen-st-patrick
publication: ['po-org:catholic-community-of-st-stephen-st-patrick', 'lpi:0018000000Qx7RkAAJ', 'po-container:03/1424']
group: Catholic Community of St. Stephen-St. Patrick (Marathon, Whitney Point, Cincinnatus)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1424/20260927B.pdf
  seen: 2026-09-26
  note: 'Page 1 of the 27 September 2026 issue. The PDF is scanned (no text layer), so this is a transcription
    of the page image, not a findable quote. Masthead: "The Roman Catholic Community of ST. STEPHEN, ST.
    PATRICK & OUR LADY OF PERPETUAL HELP", office "P.O. Box 711, 51 Keibel Road, Whitney Point, NY 13862".
    Mass Schedule: "Saturday Vigil 5:00PM St. Stephen, Marathon; Sunday 8:30AM St. Patrick, Whitney Point;
    11:00AM Our Lady of Perpetual Help, Cincinnatus; Monday 6:00PM St. Patrick; Tuesday 10:00AM St. Patrick;
    First Thursday Weekday Mass 11:00AM Our Lady of Perpetual Help; Thursday 10:00AM St. Patrick".'
- url: https://www.ccsssp.com/
  seen: 2026-09-26
  quote: Saturday Vigil 5:00 PM - St. Stephen Marathon Sunday 8:30 AM - St. Patrick Whitney Point 11:00
    AM - Our Lady of Perpetual Help Cincinnatus
  note: The community's homepage "Mass Times" box, the same schedule as the bulletin masthead.
- url: https://www.ccsssp.com/church-bulletin
  seen: 2026-09-26
  note: The site's Church Bulletin page (read with parish-site-access visit.py; it is a Wix page) links
    the last five issues as parishesonline.com/find/catholic-community-of-st-stephen-st-patrick/bulletin/file/03-1424-<date>B.pdf,
    newest 20260927.
- url: https://parishesonline.com/organization/catholic-community-of-st-stephen-st-patrick
  seen: 2026-09-26
  note: '`probe po catholic-community-of-st-stephen-st-patrick`: LPi id 0018000000Qx7RkAAJ, website ccsssp.com,
    address 59 Keibel Rd, Whitney Point, container 03/1424, weekly issues through 2026-09-27.'
- url: https://www.syracusediocese.org/st-stephens-st-patricks-marathon-whitney-point
  seen: 2026-09-26
  quote: Catholic Community of St. Stephen's-St. Patrick's - Marathon/Whitney Point
  note: 'The diocese''s page for the community (behind Cloudflare; read with visit.py): Marathon church
    at 16 Academy Street, "Church & Office Address - Whitney Point 59 Keibel Road", administrator Rev.
    Malachi F. Clark. Its page for Our Lady of Perpetual Help says "Our Lady of Perpetual Help is a Mission
    of the Catholic Community of St. Stephen - St. Patrick, Marathon/Whitney Point."'
promoted: 2026-09-26
---

## Publisher

The Catholic Community of St. Stephen–St. Patrick (Marathon and Whitney Point) and its mission,
Our Lady of Perpetual Help in Cincinnatus, publish one weekly bulletin through ParishesOnline (LPi),
container 03/1424. I read the 27 September 2026 issue (page 1). Its masthead names all three
("The Roman Catholic Community of St. Stephen, St. Patrick & Our Lady of Perpetual Help") and its Mass
schedule covers all three churches: Saturday 5 pm at St. Stephen, Marathon; Sunday 8:30 am at
St. Patrick, Whitney Point, and 11 am at Our Lady of Perpetual Help, Cincinnatus; weekday Masses at
St. Patrick and a First Thursday Mass at Our Lady of Perpetual Help. The PDF is scanned, so the
evidence item transcribes the page image; the community's homepage carries the same schedule in text.

The diocese lists the community as one entry ("Catholic Community of St. Stephen's-St. Patrick's -
Marathon/Whitney Point") and calls Our Lady of Perpetual Help its mission, so the diocese's grouping
and the bulletin agree: one row, three churches.

## Worship sites

St. Stephen (Marathon), St. Patrick (Whitney Point) and Our Lady of Perpetual Help (Cincinnatus), the
three buildings in the bulletin's Mass schedule. The diocese directory lists the community twice
(directory:33220 at the Marathon address and directory:36284 at Whitney Point) and the mission once;
GCatholic lists the same three churches. Nothing the diocese or GCatholic lists for this community is
left out.

## Website and bulletin provider

ccsssp.com is the community's own site (the diocese and GCatholic both give it). Its "Church Bulletin"
page links each issue through ParishesOnline's `/find/catholic-community-of-st-stephen-st-patrick/`
path; `probe po` on that slug gives LPi id 0018000000Qx7RkAAJ and container 03/1424, weekly through
27 September 2026. All three ids are in `publication`.

## Not yet confirmed

Nothing. The bulletin is image-only, so the pipeline's text extraction will need OCR (or the
homepage schedule) for this row; that is a pipeline concern, not a structure question.
