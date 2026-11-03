---
name: Our Lady of Lourdes
website: https://www.ollwhs.org
bulletin_provider: parishes_online
provider_id: parish-community-of-our-lady-of-lourdes
publication: ['po-org:parish-community-of-our-lady-of-lourdes', 'lpi:0018000000QxA3oAAF', 'po-container:03/1054']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1054/20261101B.pdf
  seen: 2026-11-02
  quote: 390 County Road 523
  note: 1 November 2026 issue (8 text pages). The page 1 masthead names 'Our Lady of Lourdes Catholic
    Church Whitehouse Station, New Jersey' alone, 'Pastor Rev. Jason Pavich', 'Pastoral Support Rev. Maurice
    T. Carlton', Deacons Curran, Webb, Woods and Paolino (Emeritus); 'Mass Schedule Monday-Wednesday &
    Friday | 8:30 am Thursday | 12:00 pm Saturday Vigil | 4:30 pm Sunday | 8:30 and 10:30 am'. No other
    church or chapel is named.
- url: https://parishesonline.com/organization/parish-community-of-our-lady-of-lourdes
  seen: 2026-11-02
  note: 'probe po: ''Parish Community of Our Lady of Lourdes'', 390 County Road 523, Whitehouse Station,
    NJ 08889, website www.ollwhs.org, LPi id 0018000000QxA3oAAF, container 03/1054; latest issue 2026-11-01
    (8 November answered 403 on 2026-11-02, not yet posted).'
- url: https://www.ollwhs.org/bulletin
  seen: 2026-11-02
  note: The parish's Bulletin page (read with visit.py; probe url said DEAD-DNS for every host on 2026-11-02)
    embeds the ParishesOnline viewer for container 03/1054 (issues 11 October to 1 November 2026) and
    links 'View Past Bulletins' to the org page. No other publisher is linked.
bulletin_status: available
---

## Publisher

Our Lady of Lourdes, Whitehouse Station publishes its own weekly bulletin through LPi / ParishesOnline (org parish-community-of-our-lady-of-lourdes, container 03/1054). The 1 November 2026 issue (read 2026-11-02) names 'Our Lady of Lourdes Catholic Church Whitehouse Station, New Jersey', '390 County Road 523', and 'Pastor Rev. Jason Pavich', who is also the finder's pastor. It names no other church.

## Worship sites

One church (directory:24554, gcatholic:18619). The masthead's Mass schedule (Monday-Wednesday and Friday 8:30 am, Thursday 12:00 pm, Saturday Vigil 4:30 pm, Sunday 8:30 and 10:30 am) gives no other location, and the finder lists no other worship site.

## Website and bulletin provider

Website https://www.ollwhs.org (finder, GCatholic, masthead and the ParishesOnline org). Its Bulletin page embeds only the ParishesOnline container, so the row is `parishes_online` with the org slug as `provider_id`.

## Fetch check

`PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check` on 2026-11-02 picked https://container.parishesonline.com/bulletins/03/1054/20261101B.pdf (the 1 November 2026 issue): transport ok, PDF, issue date observed 2026-11-01, freshness fresh (2 days), identity unverified by the tool; I read that issue myself (evidence above).

## Not yet confirmed

Nothing open for this row.
