---
name: Saint Benedict the Moor Parish (Hill District)
website: https://www.sbtmparishpgh.com
bulletin_provider: ecatholic
provider_id: '26574'
publication: ['ecatholic:26574', 'discovermass:st-benedict-the-moor-pittsburgh-pa']
group: Saint Benedict the Moor Parish
evidence:
- url: https://files.ecatholic.com/26574/bulletins/20261018.pdf
  seen: 2026-10-23
  quote: Bishop Mark Eckman will be visi
  note: 'Issue of 18 October 2026 (4 pages, text layer; ligatures are dropped so quotes stop before them).
    Page 1 is a graphic-style cover whose text layer doubles the masthead letters (''SSaaiinntt BBeenneeddiicctt
    tthhee MMoooorr PPaarriisshh / MMiissssiioonn PPaarriisshh ffoorr BBllaacckk CCaatthhoolliiccss iinn
    PPiittttssbbuurrgghh''); it also reads ''Mass Schedule Sunday 11 am'', ''Livestream facebook.com/SBTMPGH/live'',
    ''Sacrament of Reconciliation at 10:30 am & by appointment'', staff list headed by ''Rev. C. Matthew
    Hawkins Pastor'', and the address ''91 Crawford Street, Pittsburgh PA 15219 ... 412.281.3141''. Page
    4: ''Bishop Mark Eckman will be visiting St. Benedict the Moor Parish on Tuesday, November 3, from
    7 to 9 pm''. Page 2 Mass Intentions: ''October 18, 11 am Twenty-ninth Sunday in Ordinary Time ...
    October 25, 11 am''. The file is the one the parish''s /bulletins archive lists first (https://files.ecatholic.com/26574/bulletins/20261018.pdf?t=1792108066000).'
- url: https://www.sbtmparishpgh.com/bulletins
  seen: 2026-10-23
  quote: Mission Parish for Black Catholics in Pittsburgh
  note: Rendered in headed Chrome (visit.py; Cloudflare-protected eCatholic site 26574). Archive for 2026
    lists issues from January 4 to October 18, 2026 (no October 25 yet), with PDF links files.ecatholic.com/26574/bulletins/<yyyymmdd>.pdf?t=...;
    page footer '91 Crawford Street, Pittsburgh, PA 15219, office@sbtmparishpgh.com, 412.281.3141'. A
    separate 'Bulletin Inserts' page exists.
- url: https://discovermass.com/church/st-benedict-the-moor-pittsburgh-pa/
  seen: 2026-10-23
  note: Discover Mass listing 'St. Benedict the Moor - Personal Parish'; its 18 October 2026 issue is
    byte-identical to the eCatholic 20261018.pdf (md5 7a932ec102c78ee81120d5772de2e9ec) and it already
    carries the 25 October issue (4 pages, same masthead and 'Sunday 11am' Mass Schedule) that the eCatholic
    archive had not yet listed. A mirror of the same bulletin, not a second publisher.
- url: https://parishesonline.com/organization/st-benedict-the-moor-church-15219
  seen: 2026-10-23
  note: 'probe po: LPi org 0018000000Qx7qlAAB ''St. Benedict the Moor Church'', 91 Crawford St, Pittsburgh
    15219, website sbtmparishpgh.com, ''no publications: this organization does not publish a bulletin
    here now''. This is the empty org the survey noted; the parish publishes on eCatholic (and Discover
    Mass), not ParishesOnline. Not recorded as a publication id.'
- url: https://diopitt.org/saint-benedict-the-moor-parish
  seen: 2026-10-23
  note: 'Diocese parish page (directory roster): Reverend C. Matthew Hawkins (Pastor); Sunday: 11:00 a.m.;
    address given as 1500 Centre Avenue; phone 412-281-3141. The predecessor list names it ''St. Benedict
    the Moor - New Personal Parish'', Hill District.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese pittsburgh --parish saint-benedict-the-moor-pittsburgh (headed Chrome)
  url: https://www.sbtmparishpgh.com/bulletins
  checked: '2026-10-23'
  outcome: found
  next_action: None; pick was files.ecatholic.com/26574/bulletins/20261018.pdf (PDF, 960934 bytes, fresh,
    newest in the archive); the 25 October issue was on Discover Mass only.
  retry_when: The eCatholic archive stops updating while Discover Mass continues (then switch the row
    to discovermass:st-benedict-the-moor-pittsburgh-pa)
bulletin_status: available
---

## Publisher

Saint Benedict the Moor Parish, the 'Mission Parish for Black Catholics in Pittsburgh' (a personal parish, settled Rule 4: an ordinary row because it publishes), publishes its own weekly bulletin on its eCatholic site (id 26574). The 18 October 2026 issue (read 2026-10-23) is headed Saint Benedict the Moor Parish with Rev. C. Matthew Hawkins as pastor and 91 Crawford Street; its Mass Schedule box reads 'Sunday 11 am' with a Facebook livestream. The LPi account st-benedict-the-moor-church-15219 is empty (no publications), so ParishesOnline is not a channel.

Discover Mass carries the same PDF (byte-identical for 18 October) a few days earlier than the eCatholic archive, so it is a mirror: recorded as a second publication id, not a separate row.

## Worship sites

One church, St. Benedict the Moor at 91 Crawford Street (see churches/saint-benedict-the-moor-pittsburgh.md). The diocese lists no other building for the parish.

## Website and bulletin provider

sbtmparishpgh.com is diocese-provided eCatholic behind Cloudflare. `fetch` reads eCatholic from the website (/bulletins archive); bulletin files are on files.ecatholic.com/26574/bulletins/<yyyymmdd>.pdf, which downloads without a browser. A fetch check result is in research below.

## Not yet confirmed

The eCatholic archive had no 25 October issue on 23 October (the Discover Mass copy did); the next-week issue should appear by the weekend. Weekday Masses are not printed; only Sunday 11 am is.
