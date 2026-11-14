---
name: St. Paul Chong Ha-Sang (Flushing)
website: https://www.stpaulqueens.org/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery Q4 (Queens East)
evidence:
- url: https://rkddfxgkkmylcddibsaq.supabase.co/storage/v1/object/sign/bulletins/11.01.26.pdf
  seen: 2026-11-05
  quote: 성 바오로 정하상 천주교회 (퀸즈성당)
  note: 1 November 2026 issue (No. 2817), 12 pages, mostly Korean; opened through a signed URL the site
    creates per click (the bucket is not public, so this address needs the site's token). Page 1 masthead
    (an image) names St. Paul Chong Ha-Sang Roman Catholic Church, 32-15 Parsons Boulevard Flushing, NY
    11354, Web StPaulQueens.org, Pastor Rev. Andrew M. Kim; page 12 repeats the name in text with 'November
    1, 2026 (Year A) No. 2817'. Page 8 (an image) has the one Mass schedule (미사 시간), naming no other church.
- url: https://www.stpaulqueens.org/
  seen: 2026-11-05
  note: React single-page app on Vercel backed by Supabase (rkddfxgkkmylcddibsaq.supabase.co). Its Bulletins
    panel reads table 'bulletins' (English UI) or 'bulletins_ko' (Korean UI); on 2026-11-05 both returned
    the same rows (same ids and storage_path; newest 2026-11-01 '11.01.26.pdf', then 10.25.26.pdf, 10.18.26.pdf),
    with only the title translated ('All Saints' / '모든 성인 대축일'). Clicking an issue opens a one-hour signed
    URL from storage bucket 'bulletins'. Read with parish-site-access visit.py and the site's public REST
    API.
research:
- method: 'fetch:check unpinned on https://www.stpaulqueens.org/ (NoBulletin: no bulletin page link found)'
  url: https://www.stpaulqueens.org/
  checked: '2026-11-05'
  outcome: unsupported-format
  next_action: Set provider other with the new collector's recipe, run fetch:check, and clear fetch_gap
    once it picks this week's issue
  retry_when: A collector that lists a Supabase table and signs its storage URLs lands, or the site exposes
    plain PDF links
bulletin_status: available
fetch_gap:
  kind: supabase-signed-storage
  seen: 2026-11-05
  note: stpaulqueens.org is a React app with no bulletin links in its HTML; issues are rows in its Supabase
    table 'bulletins' (storage_path e.g. 11.01.26.pdf) and open only through a one-hour signed URL from
    the private storage bucket 'bulletins' (POST /storage/v1/object/sign/bulletins/<path> with the site's
    public anon key). The public object URL answers HTTP 400.
  url: https://www.stpaulqueens.org/
---

## Publisher

St. Paul Chong Ha-Sang, the Korean parish in Flushing, publishes its own weekly bulletin on its own site (stpaulqueens.org, Bulletins). The 1 November 2026 issue, No. 2817 (read 2026-11-05, the newest posted), has a masthead (page 1, an image) "성 바오로 정하상 천주교회 (퀸즈성당) / St. Paul Chong Ha-Sang Roman Catholic Church / 32-15 Parsons Boulevard Flushing, NY 11354", Pastor Rev. Andrew M. Kim; page 12 repeats the Korean name in text.

## Worship sites

One church. The Mass schedule on page 8 (an image) lists Saturday anticipated Mass 8 PM; Sunday 8 AM (Korean), 9:30 AM (student Mass, English), 11 AM (Korean), 5 PM (youth Mass, Korean); weekdays Monday-Saturday 7 AM, Thursday 8 PM and first Friday 8 PM. It names no other church. The diocese directory, deanery list, GCatholic 16804 and Mass finder 1159 list only this church.

## Language editions

One issue a week, mostly Korean with English pages (announcements on page 10, homily on page 11). The site's English and Korean views list the same files (same storage_path) under translated titles, so there are no separate language editions.

## Website and bulletin provider

stpaulqueens.org is a React single-page app: its Bulletins button opens a panel filled from the site's Supabase database, and each issue opens through a signed storage URL that expires after an hour. The page has no bulletin links in its HTML. `unsupported`, with a `fetch_gap` (`supabase-signed-storage`): on 2026-11-05 fetch:check found no bulletin link on the homepage, and the storage bucket's public URL answers HTTP 400, so no recipe can reach the files yet.

## Not yet confirmed

Nothing about the parish itself; only collection, which waits on a collector (see research).
