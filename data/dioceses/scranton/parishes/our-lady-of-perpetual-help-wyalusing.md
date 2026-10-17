---
name: Our Lady of Perpetual Help Parish
website: https://olophparish.org/bulletins/
bulletin_provider: other
provider_id: ''
publication: ['url:https://olophparish.org/bulletins/']
group: Our Lady of Perpetual Help Parish
evidence:
- url: https://sspeterandpaulchurch.net/
  seen: 2026-10-16
  quote: Wednesday & Friday 12 Noon, or as posted in their bulletin
  note: 'Homepage of Saints Peter and Paul, Towanda (read 2026-10-16): "Masses at Our Lady of Perpetual
    Help in Wyalusing : Saturday Vigil 6 PM and Sunday 11 AM; No Mass Monday, Tuesday, Thursday; Wednesday
    & Friday 12 Noon, or as posted in their bulletin." The word "bulletin" links https://olophparish.org/bulletins/.'
- url: https://www.dioceseofscranton.org/find-a-parish/our-lady-of-perpetual-help-parish-wyalusing
  seen: 2026-10-16
  quote: Reverend Jose Joseph Kuriappilly – Pastor
  note: The finder gives the parish 245 State Street, website www.olophparish.org, and one worship site,
    Saint Mary of the Assumption Church. Towanda's finder page names the same pastor.
- url: https://olophparish.org/bulletins/
  seen: 2026-10-16
  note: 'Behind Cloudflare: `probe url` got HTTP 403; visit.py (headed Chrome) was challenged on every
    load in five runs on 2026-10-16 and 2026-10-17 (8, 10, 14, 12 and 20 loads), for both the homepage and
    /bulletins/. Not read.'
- url: https://discovermass.com/church/st-mary-of-the-assumption-wyalusing-pa/
  seen: 2026-10-16
  note: Discover Mass has a page for "Our Lady of Perpetual Help, 245 State St., Wyalusing" but lists
    no bulletins (issues.py, 2026-10-16). GCatholic's website for the church, olphpa.org, does not resolve
    (probe url DEAD-DNS). ParishesOnline has no organization under the obvious slugs, and no Wayback Machine
    capture of olophparish.org exists.
revisit: Open https://olophparish.org/bulletins/ in a browser (parish-site-access visit.py --bulletin;
  Cloudflare blocked every load on 2026-10-16/17), read the newest issue's masthead and Mass schedule,
  record its publication id and file pattern, and confirm it is a separate bulletin from Towanda's. If
  the page carries no bulletin, ask the parish office (570-746-1006) and consider no_bulletin.
revisit_after: 2026-10-24
---

## Publisher

Our Lady of Perpetual Help Parish, Wyalusing (one church, St. Mary of the Assumption) shares its
pastor, Rev. Jose Joseph Kuriappilly, with Saints Peter and Paul, Towanda (both finder pages).
Towanda's bulletin prints a box with Wyalusing's Mass times, but its masthead names Towanda alone,
and Towanda's homepage points readers to Wyalusing's **own** bulletin for its schedule ("or as
posted in their bulletin", linking https://olophparish.org/bulletins/). So Wyalusing is recorded
as a separate publisher, at that page. **The bulletin itself has not been read**: the site is
behind Cloudflare and no browser load got through (see evidence). This row's existence and
website rest on Towanda's link, not on an issue.

## Worship sites

One: `st-mary-of-the-assumption-wyalusing`, the only site the finder lists. Its current Mass
times come from Towanda's 18 October 2026 bulletin.

## Website and bulletin provider

`website` is the bulletin page Towanda links. Provider `other` (a self-hosted page; nothing at
ParishesOnline, Discover Mass lists no issues, no eCatholic id seen). No `provider_id` and no
publication id beyond the page URL, because the page has not been read.

## Not yet confirmed

Everything about the bulletin itself: whether /bulletins/ is current, how issues are posted, and
that it is distinct from Towanda's (it could in principle be Towanda's file re-posted). See
`revisit`. If it turns out to be Towanda's bulletin, merge this row into `sts-peter-paul-towanda`.
