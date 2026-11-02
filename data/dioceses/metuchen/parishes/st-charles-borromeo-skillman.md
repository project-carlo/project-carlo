---
name: St. Charles Borromeo
website: http://borromeo.org
bulletin_provider: other
provider_id: page-pdfs http://borromeo.org/sermons/
publication: ['url:https://embeds.sermoncloud.com/saint-charles-borromeo/sermons']
group: ''
evidence:
- url: https://s3.amazonaws.com/account-media/22349/uploaded/f/0e21596336_1793280749_fnwebbulletin-20261101.pdf
  seen: 2026-11-02
  quote: 'GPS Church location: 47 Skillman Road, Skillman, NJ 08558'
  note: 'The 1 November 2026 ''November 1, 2026 Bulletin'' from SermonCloud''s API (4 pages, text): page
    2 gives ''WEEKEND MASSES Confessions: Saturday 4:00 PM; Saturday Vigil: 5:00 PM; Sunday: 8:30, 10:00
    and 11:30 AM; DAILY MASS Monday, Tuesday, Wednesday, Thursday, Friday: 9:00 AM'', ''Contact: 609.466.0300
    www.borromeo.org'', ''Mailing address: 376 Burnt Hill Road, Skillman, NJ 08558''. A short web bulletin
    of announcements; it names no pastor and no other church.'
- url: https://api.sermoncloud.com/saint-charles-borromeo/sermons
  seen: 2026-11-02
  quote: November 1, 2026 Bulletin
  note: 'SermonCloud JSON for the account ''saint-charles-borromeo'' (the call the embed makes): items
    titled ''November 1, 2026 Bulletin'', ''October 25, 2026 Bulletin'', ... each with speaker ''Msgr.
    Gregory Malovetz'' and a media.notes URL to an s3.amazonaws.com/account-media/22349/... PDF. The finder
    lists Msgr. Gregory E. S. Malovetz as pastor.'
- url: http://borromeo.org/sermons/
  seen: 2026-11-02
  quote: 'To view a Bulletin: Click the 3 dots on the right, select the download arrow, click on Notes
    button.'
  note: The parish site's 'Bulletins/ Homilies' page (WordPress) is an iframe of embeds.sermoncloud.com/saint-charles-borromeo/sermons;
    the home page menu item 'Bulletins/ Homilies' goes here.
research:
- method: visit.py on the embed, a network log of the page's requests, probe get on the API and probe
    pdf on the newest media.notes file; also issues.py discovermass (no bulletins listed) and probe get
    on stcharlesskillman.flocknote.com (JS shell, 'Loading')
  url: https://api.sermoncloud.com/saint-charles-borromeo/sermons
  checked: '2026-11-02'
  outcome: found
  next_action: Clear fetch_gap if a collector reads SermonCloud's API; look for a fuller weekly bulletin
    if one is published elsewhere
  retry_when: A SermonCloud collector exists, or the parish names another bulletin host
bulletin_status: available
fetch_gap:
  kind: sermoncloud-api-embed
  seen: 2026-11-02
  note: Bulletins are listed by a JSON API (api.sermoncloud.com/saint-charles-borromeo/sermons; each item's
    media.notes is an s3.amazonaws.com PDF URL) inside an iframe on borromeo.org/sermons/; fetch:check
    finds 'No PDF links found' on that page. The newest PDF (1 November 2026) is a normal text PDF and
    is current.
  url: https://api.sermoncloud.com/saint-charles-borromeo/sermons
---

## Publisher

St. Charles Borromeo, 47 Skillman Road, Skillman, publishes its weekly bulletin through SermonCloud, embedded in the 'Bulletins/ Homilies' page of its WordPress site (borromeo.org/sermons/, an iframe of embeds.sermoncloud.com/saint-charles-borromeo/sermons). The embed lists items titled 'November 1, 2026 Bulletin', 'October 25, 2026 Bulletin' and so on, posted by 'Msgr. Gregory Malovetz', each with a PDF under s3.amazonaws.com/account-media/22349/. The 1 November 2026 PDF (read 2026-11-02) is a 4-page web bulletin of announcements. Its page 2 gives the Mass schedule below and 'GPS Church location: 47 Skillman Road, Skillman, NJ 08558'. It doesn't print a masthead or name a pastor; the identity rests on that address, the phone 609.466.0300 (the finder's number) and www.borromeo.org, and on the issue being posted from the parish's own site. The finder's pastor line is 'Rev. Msgr. Gregory E. S. Malovetz'.

A different parish with a similar name, St. Charles Borromeo, 176 Stagecoach Road, Sicklerville NJ (churchofscb.org), came up in a search; it is in another diocese and is not this parish.

## Worship sites

One church, 47 Skillman Road (directory:24511, gcatholic:18646). The bulletin gives one set of Mass times and no second site. The finder's Mass list for this entry is empty.

## Website and bulletin provider

Website: http://borromeo.org (the finder gives http://www.borromeo.org, which redirects there). `probe url` says DEAD-DNS for www.borromeo.org though `probe get` loads it. The bulletin isn't a PDF on the page; it sits behind a SermonCloud JSON API. Discover Mass has a church page for it (st-charles-borromeo-skillman-nj) that lists no bulletins, so it isn't a publisher here. Provider `other`; `fetch` can't collect it (*Fetch check*).

## Not yet confirmed

Whether a fuller bulletin exists: the 4-page file reads like the weekly insert of a larger bulletin, and the weekly 'fnwebbulletin' file name suggests it is a web-only edition. I found no other bulletin source (the Discover Mass page is empty; the stcharlesskillman.flocknote.com page named in the bulletin is a JavaScript shell that showed only 'Loading' to probe get). Retry trigger in `research`.

## Fetch check

`pnpm fetch:check` on 2026-11-02 with `page-pdfs http://borromeo.org/sermons/` reported `resolve_failed`: 'No PDF links found on bulletin page'. The PDF links are only in the SermonCloud API response, so the row has `fetch_gap` kind `sermoncloud-api-embed`; the recipe is a placeholder that doesn't work yet.
