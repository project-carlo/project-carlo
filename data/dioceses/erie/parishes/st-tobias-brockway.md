---
name: St. Tobias Parish
website: https://www.sttobias.com
bulletin_provider: discover_mass
provider_id: st-tobias-brockway-pa
publication: ['discovermass:st-tobias-brockway-pa']
group: ''
evidence:
- url: https://discovermass.com/church/st-tobias-brockway-pa/
  seen: 2026-10-23
  quote: WWW.STTOBIAS.COM
  note: 'Current-bulletin download from the Discover Mass church page (cover image class ''bulletin-cover
    X-|2026-10-25|1792773780|3520'': bulletin number 3520, dated 25 October 2026; 6 pages). Page 1 masthead:
    ''ST. TOBIAS CATHOLIC CHURCH'', ''1135 HEWITT STREET * BROCKWAY, PA 15824'', ''PASTOR & DEAN, DUBOIS
    DEANERY VERY REV. JOHN J. DETISCH, V.F.'', ''WEEKEND LITURGY SATURDAY VIGIL 5:00 PM SUNDAY 9:30 AM
    FIRST SUNDAY OF THE MONTH 6:00 PM''. I grepped the whole text layer for Timothy, Bonaventure, Curwensville
    and Grampian: no hit, so the issue is St. Tobias''s alone and does not carry St. Timothy''s Mass times
    (see st-timothy-curwensville).'
- url: https://www.sttobias.com/bulletin
  seen: 2026-10-23
  quote: Weekly Bulletin
  note: Duda site; the Bulletin page's button goes to https://discovermass.com/church/st-tobias-brockway-pa/#bulletins.
    probe url finds publication discovermass:st-tobias-brockway-pa and no other channel.
- url: https://parishesonline.com/organization/st-tobias-church
  seen: 2026-10-23
  note: 'probe po st-tobias-church (LPi 0018000000QxBl2AAF, website www.sttobias.com, 1100 Hewitt St):
    ''no publications: this organization does not publish a bulletin here now''. Empty org, not a channel.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ..................................................................................................
    St. Tobias, Brockway
  note: 'Clergy list updated 8/7/2026, Detisch, VF, Very Rev. John J.: ''Pastor ... St. Tobias, Brockway''
    and ''Administrator ... St. Timothy Parish, Curwensville''.'
- url: https://www.eriercd.org/Parish20810-St-Tobias.html
  seen: 2026-10-23
  note: 'Diocese directory record 20810: one parish record, no mission or secondary church. Sat 5 p.m.;
    Sun 9:30 a.m. and first Sunday 6 p.m.; Tuesday 6 p.m.; Wednesday-Friday 6:45 a.m.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-tobias-brockway --expected-identity Detisch (headed
    Chrome)
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, document type pdf, identity matched on the pastor's surname. Issue
    date and freshness read 'unknown' because the masthead date layout is not parsed; I confirmed by reading
    the downloaded PDF (25 October 2026, bulletin number 3520) and the cover class on the church page.
    Not a failure.
---

## Publisher

St. Tobias Parish, Brockway (1135 Hewitt St., 15824) publishes its own weekly bulletin through Discover Mass (church page `st-tobias-brockway-pa`), linked from the Bulletin page of sttobias.com (a Duda site). I downloaded the current issue on 2026-10-23: bulletin number 3520, dated 25 October 2026, 6 pages. Its masthead names St. Tobias Catholic Church and Very Rev. John J. Detisch, V.F., pastor and dean of the DuBois deanery, and its Mass intentions cover only St. Tobias's Masses.

## Worship sites

One church, St. Tobias at 1135 Hewitt St. Weekend Masses: Saturday 5:00 PM, Sunday 9:30 AM, first Sunday of the month 6:00 PM (masthead); weekdays per the intentions list in the issue.

**Shared pastor, not a shared bulletin.** The clergy list (8/7/2026) makes Detisch pastor of St. Tobias and administrator of St. Timothy, Curwensville (with its secondary mission church St. Bonaventure, Grampian). The 25 October St. Tobias issue contains no word of Timothy, Bonaventure, Curwensville or Grampian, and St. Timothy has a separate website (sttimbon.org) with no bulletin. So no bulletin I could read covers both: they are separate rows (rule: shared pastors don't make shared bulletins). Record the partnership in the Timothy row's text, not `group`, as the diocese has no family number.

## Website and bulletin provider

`fetch` reads Discover Mass by `provider_id`. The Discover Mass download cap is per IP per day, so the church page was read once. The ParishesOnline organization `st-tobias-church` is empty.

## Not yet confirmed

Nothing affecting the row. Only the one issue (25 Oct 2026) was checked for St. Timothy content; earlier issues were not read.
