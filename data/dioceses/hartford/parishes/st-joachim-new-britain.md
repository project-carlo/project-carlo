---
name: St. Joachim Parish
website: https://stjoachimct.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: []
group: ''
evidence:
- url: https://stjoachimct.org/bulletin/140-bulletin-11-8-26-32nd-sunday-in-ordinary-time-parish-968/file
  seen: 2026-11-13
  note: 'Behind a 403 for non-browser clients; read in a browser (parish-site-access visit.py, screenshot
    of Chrome''s PDF viewer). Page 1 of 3: ''SAINT JOACHIM PARISH'', 860 229-4894, parish@stjoachimct.org,
    www.stjoachimct.org, ''Sunday, November 8, 2026, Thirty-Second Sunday in Ordinary Time''. The Mass
    schedule lower on page 1 was not read.'
- url: https://stjoachimct.org/
  seen: 2026-11-13
  quote: SATURDAY - ST. ANN
  note: 'Behind a 403 for non-browser clients; read in a browser (parish-site-access visit.py). Weekend
    Mass: Saturday St. Ann 4:00pm; Sunday St. Mary 9:00am English, 10:30am and 12:15pm Español; daily
    Mass at St. Mary Monday-Saturday 9:00am, Miércoles 7:00pm Español. Footer: ST. MARY CHURCH 544 Main
    St, New Britain, CT 06051; ST. ANN CHURCH 47 Clark St, New Britain, CT 06051. Upcoming events list
    ''Vigil Mass (St. Ann)'' on 14 November 2026.'
- url: https://stjoachimct.org/bulletin
  seen: 2026-11-13
  note: 'Behind a 403 for non-browser clients; read in a browser (visit.py --bulletin). Newest-first list
    of weekly issues: 140 (11-8-26), 139 (11-1-26 All Saints), 138 (10-25-26), 137 (October 18, 2026)
    and so on back to 128 (August 16, 2026).'
- url: https://www.courant.com/2017/05/07/list-of-parish-closures-and-mergers-by-town/
  seen: 2026-11-13
  quote: St. Mary and St. Ann merging to form St. Joachim
  note: Hartford Courant list of the 2017 pastoral plan, 7 May 2017.
research:
- method: fetch:check with provider other on https://stjoachimct.org/bulletin (browser)
  url: https://stjoachimct.org/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a collector reads Solutio/Joomla /file endpoints (gap joomla-file-endpoint),
    then set provider other with the printed recipe
  retry_when: A joomla-file-endpoint collector lands
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'The Solutio (Joomla) Bulletin page at stjoachimct.org/bulletin lists one issue per Sunday, newest
    first (''Bulletin 11.8.26. 32nd Sunday in Ordinary Time - Parish'', /bulletin/140-.../file), read
    in the browser with visit.py. The /file links carry no .pdf name and the site answers 403 to probe
    get, probe pdf and render.py; fetch:check (2026-11-13) followed the /file links as pages and failed:
    ''No PDF links found on bulletin page''. In Chrome the link opens a 3-page PDF.'
  url: https://stjoachimct.org/bulletin/140-bulletin-11-8-26-32nd-sunday-in-ordinary-time-parish-968/file
---

## Publisher

St. Joachim Parish, New Britain publishes a weekly bulletin on its own Solutio (Joomla) site. The issue read is Sunday, November 8, 2026 (3 pages, opened in Chrome's PDF viewer through parish-site-access visit.py because the site answers 403 to the probes): page 1 masthead "SAINT JOACHIM PARISH", 860 229-4894, parish@stjoachimct.org, www.stjoachimct.org. The directory's St. Mary link, smnb.org, redirects to stjoachimct.org.

## Worship sites

Two, from the parish home page (read in the browser, 13 November 2026): St. Ann Church, 47 Clark St (Saturday 4:00pm; `st-ann-new-britain`) and St. Mary Church, 544 Main St (Sunday 9:00am English, 10:30am and 12:15pm Español, daily Mass Monday-Saturday 9:00am and Wednesday 7:00pm Español; `st-mary-new-britain`). These are the directory's 35 and 38 and GCatholic's 22132 and 22137. The 2017 plan merged St. Mary and St. Ann into St. Joachim (Hartford Courant, 7 May 2017). The Mass schedule printed in the bulletin itself was not read (only the top of page 1 was visible in the screenshot).

## Website and bulletin provider

`unsupported`, gap `joomla-file-endpoint`: each issue is linked as `/bulletin/<n>-<title>/file`, with no .pdf in the address, and the site answers 403 to non-browser clients. fetch:check (2026-11-13, provider `other` on the Bulletin page) followed those links as pages and failed with "No PDF links found on bulletin page". When a collector reads these endpoints, set the provider back to `other` and record the recipe fetch:check prints.

## Not yet confirmed

The bulletin's own Mass schedule (page 1, lower half) was not read; the site's home page schedule was used. Rendering the full page needs a browser download of the /file link.
