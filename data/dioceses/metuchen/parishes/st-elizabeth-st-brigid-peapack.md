---
name: St. Elizabeth - St. Brigid
website: https://www.sainteb.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:19770']
group: ''
evidence:
- url: https://files.ecatholic.com/19770/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: G60616 (CK) - St. Elizabeth/St. Brigid, Far Hills
  note: '1 November 2026 issue (8 pages). Page 1 (rendered; its text layer is in an unmapped font) is
    the masthead ''The Parish Family of St. Elizabeth [34 Peapack Road, Far Hills, NJ 07931] … St. Brigid
    [129 Main Street, Peapack, NJ 07977]'', www.sainteb.org, ''Reverend John G. Hillier, PhD, Administrator
    of St. Elizabeth-St. Brigid Parish'', Rev. James Tucker parochial vicar; Mass schedule ''St. Brigid:
    Daily Mass (Monday - Friday) 9:00 AM, Saturday 4:30 PM, Sunday 7:30 AM, 9:30 AM & 11:30 AM; St. Elizabeth:
    Sunday 8:30 AM & 10:30 AM''. The quoted Bon Venture code line is on the ad pages 7 and 8.'
- url: https://files.ecatholic.com/19770/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: '9:30 AM (St. Brigid) Mass:  For the Parishioners'
  note: 'Page 2, ''ST. ELIZABETH - ST. BRIGID PARISH'' liturgical schedule for 2-8 November 2026: weekday
    Masses 9:00 AM at St. Brigid; Saturday 12:00 PM (St. Elizabeth) and 4:30 PM (St. Brigid); Sunday 7:30,
    9:30, 11:30 (St. Brigid) and 8:30, 10:30 (St. Elizabeth).'
- url: https://www.sainteb.org/bulletins
  seen: 2026-11-02
  note: Bulletin page (eCatholic site 19770; read with parish-site-access visit.py, since probe get answers
    403) lists weekly issues at files.ecatholic.com/19770/bulletins/<YYYYMMDD>.pdf, newest 20261101, then
    20261025, 20261018 …
- url: https://diometuchen.org/parishfinder
  seen: 2026-11-02
  note: 'Finder has two pins for this one parish: directory:24487 ''St. Elizabeth - St. Brigid (St. Brigid
    Worship Site)'', 129 Main Street, Peapack, and directory:25192 ''(St. Elizabeth Worship Site)'', 34
    Peapack Road, Far Hills; both list ''Worship Sites: St. Elizabeth Church … St. Brigid Church'' and
    website sainteb.org. Clergy line ''Pastor: Rev. Msgr. Edward C. Puleo'' differs from the masthead.'
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

St. Elizabeth - St. Brigid Parish (Peapack and Far Hills) publishes one weekly bulletin, printed by Bon Venture (code line 'G60616 (CK) - St. Elizabeth/St. Brigid, Far Hills' on the ad pages) and posted on the parish's own eCatholic site (id 19770). I read the 1 November 2026 issue (2026-11-02). Its page 1 is an image-like layer (pdftotext gives garbage), so I rendered it: the masthead is 'The Parish Family of St. Elizabeth … St. Brigid', with both churches' addresses, www.sainteb.org, and 'Reverend John G. Hillier, PhD, Administrator of St. Elizabeth-St. Brigid Parish'. The finder's pastor line (Msgr. Edward C. Puleo, with Fr. Hillier 'In Residence') is out of date. Page 2's liturgical schedule is a readable text layer. I didn't look for a sponsors.bonventure.net listing: the parish hosts the issue itself, and under *Rules settled* the parish-hosted copy is the one recorded.

## Worship sites

Two churches, both named in the masthead and with Masses in the 2-8 November schedule: St. Elizabeth Church, 34 Peapack Road, Far Hills (Saturday noon, Sunday 8:30 and 10:30) and St. Brigid Church, 129 Main Street, Peapack (weekdays 9:00, Saturday 4:30, Sunday 7:30, 9:30, 11:30). These match the finder's two worship-site pins (directory:24487, directory:25192), GCatholic's two churches (18649, 18650) and the worship-sites roster. Nothing else is listed.

## Website and bulletin provider

Website https://www.sainteb.org, the eCatholic site that hosts the bulletin (`ecatholic:19770`); its Bulletin page also links saintelizabeth-saintbrigid.org, the domain GCatholic gives. Provider `ecatholic`, read from `files.ecatholic.com/19770/bulletins/<YYYYMMDD>.pdf`.

## Not yet confirmed

Nothing open. The masthead text on page 1 can't be rechecked by quote (unmapped font); the evidence quotes the ad-page code line and the page-2 schedule instead.

## Fetch check

`pnpm fetch:check` on 2026-11-02 picked `files.ecatholic.com/19770/bulletins/20261101.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `fresh` (2 days), identity unverified by the tool (page 1 is unreadable text); I read the masthead myself (above).
