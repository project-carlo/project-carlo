---
name: Church of St. Patrick
website: https://www.stpatrickpottsville.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14122', 'po-org:st-patrick-church-17901', 'lpi:0018000000QxAinAAF']
group: ''
evidence:
- url: https://files.ecatholic.com/14122/bulletins/20261018.pdf
  seen: 2026-10-18
  quote: CHURCH OF SAINT PATRICK
  note: 'Page 1 masthead of the 18 October 2026 issue (Bon Venture Services layout): "Rev. John S. Pendzick,
    Pastor", parish office 319 Mahantongo Street, Pottsville.'
- url: https://files.ecatholic.com/14122/bulletins/20261018.pdf
  seen: 2026-10-18
  quote: SCHEDULE OF MASSES Saturday … 4:00 pm Sunday … 8:00 am & 10:00 am
  note: 'Page 1: weekday Masses Mon., Tue., Wed., Fri. & Sat. 8:00 am, Thursday 6:00 pm. One church; page 2
    candle intentions name "Our Lady''s Chapel", a side chapel.'
- url: https://www.stpatrickpottsville.org/
  seen: 2026-10-18
  note: 'Behind Cloudflare (probe url HTTP403; read in a browser with parish-site-access visit.py, which loaded
    it on the second run): an eCatholic site, ecatholic:14122, with a /bulletins page.'
- url: https://parishesonline.com/organization/st-patrick-church-17901
  seen: 2026-10-18
  note: 'probe po: an old ParishesOnline org (lpi 0018000000QxAinAAF, 319 Mahantongo St) with no publications.'
---

## Publisher

The Church of St. Patrick, Pottsville, publishes its own weekly bulletin through eCatholic
(site 14122). I read the 18 October 2026 issue. The page-1 masthead is "CHURCH OF SAINT
PATRICK", "Rev. John S. Pendzick, Pastor", with the parish office at 319 Mahantongo Street.
The schedule is Saturday 4:00 pm and Sunday 8:00 am & 10:00 am, weekdays 8:00 am, and
Thursday 6:00 pm. It covers one church.

## Worship sites

- St. Patrick, 319 Mahantongo St. (`st-patrick-pottsville`).

GCatholic and the diocesan parish map list this one church. "Our Lady's Chapel" in the
candle intentions is a side chapel of the church. Nothing ruled out. The diocesan map's page
is out of date on staff: it still names "Pastor: Rev. Richard Clement", while the current
bulletin names Fr. Pendzick.

## Website and bulletin provider

stpatrickpottsville.org is an eCatholic site behind Cloudflare. `probe url` gets 403. In a
real browser (`visit.py`) it loaded and embeds `ecatholic:14122`. Issues are at
files.ecatholic.com/14122/bulletins/YYYYMMDD.pdf, with no Cloudflare in front, and
`issues.py ecatholic` found the 18 October 2026 issue. The old ParishesOnline org (no
publications) is recorded among the publication ids.

Fetch check (2026-10-18, `fetch_check_rows.py`): resolved to
files.ecatholic.com/14122/bulletins/20261018.pdf, dated 2026-10-18, which is this week's
issue.

## Not yet confirmed

Nothing.
