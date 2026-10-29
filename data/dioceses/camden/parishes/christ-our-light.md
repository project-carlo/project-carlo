---
name: The Catholic Community of Christ Our Light
website: https://christourlight.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/christ-our-light-cherry-hill-nj-08034
publication: ['url:https://www.church-bulletin.org/christ-our-light-cherry-hill-nj-08034#john-patrick']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/christ-our-light-cherry-hill-nj-08034/2026-10-25.pdf
  seen: 2026-10-29
  note: Image-only PDF (16 pages, no text layer; page 1 rendered with render.py and read). Masthead 'Christ
    Our Light, 402 Kings Highway North, Cherry Hill, NJ 08034', 'October 25, 2026, 30th Sunday in Ordinary
    Time'; Leadership 'Fr. John Picinic - Pastor'; Liturgies 'Saturday - 4:00 PM | Sunday - 8:30 AM, 10:30
    AM, 6:30 PM', 'Monday thru Friday - 8:00 AM | Saturday - 9:00 AM'. Names this parish alone; recheck
    can't find the words as text.
- url: https://christourlight.net/home/bulletins
  seen: 2026-10-29
  note: 'Read in the browser (visit.py; probe url and probe pdf get HTTP 403, and the issue links have
    no .pdf so fetch:check finds no PDF links there). Joomla ''Bulletins'' page: dated links ''October
    25, 2026'', ''October 18, 2026'', ''October 11, 2026'', ''September 27, 2026'' ... at /home/bulletins/<id>-<month>-<day>-<year>-1/file,
    newest first. The same issue dates appear on the church-bulletin.org listing (which also has 4 October,
    missing here).'
- url: https://www.church-bulletin.org/christ-our-light-cherry-hill-nj-08034
  seen: 2026-10-29
  note: Listing 'Christ Our Light Bulletin' (John Patrick Publishing); dated weekly PDFs 2026-10-04, 10-11,
    10-18, 10-25 (latest). Found through a web search, not linked from the parish's page.
---

## Publisher

The parish publishes weekly on its own Joomla site (`christourlight.net/home/bulletins`, read in the browser 2026-10-29; the site answers 403 to `probe url` and `probe pdf`). The same issues are on the John Patrick Publishing listing `church-bulletin.org/christ-our-light-cherry-hill-nj-08034`, which is the pick because the parish's own links end in `/file` rather than `.pdf` and `fetch:check` finds no PDF links there. The 25 October 2026 issue is an image-only PDF; page 1 (rendered and read) is headed 'Christ Our Light, 402 Kings Highway North, Cherry Hill, NJ 08034' with Fr. John Picinic as pastor and lists Saturday 4:00 PM, Sunday 8:30 AM, 10:30 AM and 6:30 PM, weekdays 8:00 AM and Saturday 9:00 AM. It names no other church.

## Worship sites

One: 402 Kings Highway North (church record `christ-our-light`). The bulletin gives only this address. Resurrection Catholic School is named in the leadership list; it is a school and is not a worship site.

## Website and bulletin provider

`other` with a `page-pdfs` recipe on the church-bulletin.org listing. The directory's and GCatholic's site `christourlight.net` is alive (a browser loads it; the domain redirects `www.` to the bare name). The John Patrick id was not found on the page (the listing is not linked from the site), so the publication identity is the listing URL. The issues are image-only, so the pipeline has to read them as images.

## Not yet confirmed

Nothing blocking. Whether the parish's own copy ever differs from John Patrick's was not compared beyond issue dates (both list 11 and 18 and 25 October).
