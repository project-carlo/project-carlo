---
name: St. John the Baptist, St. Peter's and Holy Family
website: https://stjohnthebaptistwalton.com/schedule-of-services/
bulletin_provider: google_drive
provider_id: drive-folder https://drive.google.com/drive/folders/1TGq51SjI0RD7HGKSlS8PkKW3ZbPZUV_w
publication: ['url:https://stjohnthebaptistwalton.com/schedule-of-services/', 'url:https://drive.google.com/drive/folders/1TGq51SjI0RD7HGKSlS8PkKW3ZbPZUV_w']
group: St. John the Baptist; St. Peter's Church; Church of the Holy Family
evidence:
- url: https://drive.google.com/uc?export=download&id=1SkwVr1m6FWsl6cTmyFL0oYTphD2YXk5d
  seen: 2026-09-28
  quote: St. John the Baptist, Holy Family, St. Peter
  note: 'The 20 September 2026 issue (Google Drive file linked from the parish site as "September 20,
    2026 Bulletin.pdf"), page 2, under "Roman Catholic Churches of": "Father Joseph Arockiasamy, Pastor";
    Mass schedule "Saturday Vigil 4:00 pm at St. John''s, 5:30 pm at St. Peter''s; Sunday 8:00 am at Holy
    Family, 9:30 am at St. Peter''s, 11:15 am at St. John''s"; Tuesday, Wednesday and First Friday 8:00
    am at St. Peter''s and 9:30 am at St. John''s.'
- url: https://stjohnthebaptistwalton.com/schedule-of-services/
  seen: 2026-09-28
  quote: 11:00AM at St. John the Baptist.
  note: 'Behind a SiteGround "Robot Challenge Screen" (sgcaptcha): plain fetches get a 202 challenge;
    read in headed Chrome after waiting for the challenge to clear. Lists Mass times for all three churches
    and a BULLETINS list of Google Drive links, newest "September 20, 2026 Bulletin.pdf" back to May 31,
    2026. The same page''s lower Mass Schedule block says 11:15 at St. John the Baptist, as the bulletin
    does.'
- url: https://www.catholicwalton.com/
  seen: 2026-09-28
  quote: St. John the Baptist and St. Peter’s Church are open each day from 9 am to 4 pm
  note: The older joint site (the diocese's link for Holy Family). A frozen COVID-era letter from Rev.
    Edward Golding; no bulletins. Not the bulletin's home.
- url: https://stjohnthebaptistwalton.com/schedule-of-services/
  seen: 2026-10-07
  quote: const folderId = "1TGq51SjI0RD7HGKSlS8PkKW3ZbPZUV_w";
  note: The page's inline script, read in headed Chrome. It lists the public Drive folder through the
    Drive API and builds the BULLETINS list from it after the page loads.
- url: https://drive.google.com/uc?export=download&id=1izTRFcmvzj9y3qa2whsWkkFISsQyRQcA
  seen: 2026-10-07
  quote: Mass Intentions October 5 – 11
  note: '"October 4, 2026 Bulletin.pdf", the newest file in that folder on 7 October 2026; page 1 is
    headed "Roman Catholic Churches of" St. John the Baptist, Holy Family, St. Peter, as before.'
promoted: 2026-09-28
---

## Publisher

St. John the Baptist (Walton), St. Peter's (Delhi) and Holy Family (Downsville) publish **one**
weekly bulletin. I read the 20 September 2026 issue (the newest posted on 2026-09-28): page 2 is
headed "Roman Catholic Churches of St. John the Baptist, Holy Family, St. Peter", names one pastor
(Father Joseph Arockiasamy, with Father Edward J. Golding in residence) and gives one Mass
schedule for all three churches: Saturday 4:00 pm St. John's and 5:30 pm St. Peter's; Sunday
8:00 am Holy Family, 9:30 am St. Peter's, 11:15 am St. John's; Tuesday, Wednesday and First
Friday 8:00 am St. Peter's and 9:30 am St. John's. The diocese's directory groups the three the
same way (each entry's "Other Worship Sites" names the other two).

## Worship sites

- `churches/st-john-the-baptist-walton.md`: 25 Benton Avenue, Walton.
- `churches/st-peter-delhi.md`: Delhi (parish office 8 Franklin Street).
- `churches/holy-family-downsville.md`: Downsville.

The bulletin and the parish's Schedule of Services name no other place. The diocese's
institutional-records index lists no closed parish in Walton, Delhi or Downsville.

## Website and bulletin provider

The parish site is stjohnthebaptistwalton.com (the directory gives it for St. John's; for Holy
Family it gives the older catholicwalton.com, which is a frozen 2020 page with no bulletins).
Its Schedule of Services page lists each week's bulletin as a link to a separate Google Drive
file (`drive.google.com/file/d/<id>/view`), not a shared folder, so `bulletin_provider: other`
with the page as `website` and `url:` publication. The site sits behind SiteGround's bot
challenge (`/.well-known/sgcaptcha/`): `probe url` and `visit.py` see only the "Robot Challenge
Screen"; a headed Chrome that waits a few seconds gets through, though later loads were served
an interactive captcha. The Drive files themselves download without a browser
(`drive.google.com/uc?export=download&id=<id>`), which is how the quoted issue was read.

**Changed 2026-10-07 to `google_drive`.** As `other` the row never fetched a bulletin: the
weekly runs of 27 September and 4 October both failed with `resolve_failed` ("No PDF links
found on bulletin post page: https://drive.google.com/file/d/1izTRFcm…/view"). The site builds
its BULLETINS list in the browser after the page loads, from a public Drive folder
(`1TGq51SjI0RD7HGKSlS8PkKW3ZbPZUV_w`, named in the page's inline script), so the resolver read
the page before the list was there and then opened a Drive file link as if it were a post. The
row now reads that folder directly (`provider_id: drive-folder <folder URL>`, as
`our-lady-of-victory-st-joseph` does), which never touches the SiteGround challenge. `fetch-check`
resolved it on 2026-10-07 to "October 11, 2026 Bulletin.pdf" (`1W5Z4gEJheeWDgJDCQP5YNjP9PrD-RG5L`),
posted that day after the 4 October issue. `website` stays the parish page, where a person
finds the bulletin.

## Not yet confirmed

Nothing. There was no 27 September issue in the folder.
