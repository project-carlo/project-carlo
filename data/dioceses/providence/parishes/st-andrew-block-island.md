---
name: St. Andrew
website: https://www.standrewblockisland.com/sacraments
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-andrew-church-02807', 'lpi:0018000000Qx7uSAAR']
group: ''
evidence:
- url: https://www.standrewblockisland.com/sacraments
  seen: 2026-11-15
  quote: Spring Street Parish Center
  note: 'Parish site (Squarespace, ''Rev. Joseph Protano, Pastor''), page ''Mass Schedule & Social'' (read
    with visit.py): ''Summer services (Mid-June-September) Chapel Street Church: Daily Mass 8 am, Mondays
    - Thursdays; Saturdays 5 pm; Sundays 8 am and 10 am''; ''Post Labor Day (September-October) Chapel
    St.''; ''Fall services (October-December) Spring Street Parish Center: Daily Mass 8 am, Mondays -
    Thursdays; Saturdays 5 pm; Sundays 10 am''; ''Winter services (January-Easter Vigil) Spring Street
    Parish Center: ... Sundays 10 AM''. No bulletin; the page embeds the ''Saint Andrew''s Ladies Guild,
    Block Island'' Facebook page.'
- url: https://parishesonline.com/organization/st-andrew-church-02807
  seen: 2026-11-15
  note: 'probe po: ''St. Andrew Church'', PO Box 279, Block Island, RI 02807-0279; lpi 0018000000Qx7uSAAR;
    ''no publications: this organization does not publish a bulletin here now''. Its website http://saintandrewblockisland.com/index.html
    is now a slots spam squat (probe url SPAM-SQUAT, redirects to clarkfarmmarket.com).'
- url: http://www.angelfire.com/ex/standrewschurch
  seen: 2026-11-15
  note: 'The finder''s homepage for 12168: probe url UNREACHABLE; the browser reported ERR_BLOCKED_BY_CLIENT.'
- url: https://www.facebook.com/Saintandrewblockisland
  seen: 2026-11-15
  note: '''Saint Andrew''s Ladies Guild, Block Island'' page (linked from the parish site): an intro and
    short posts; no bulletin seen in the logged-out view.'
revisit: 'Look for a current St. Andrew bulletin: the parish site https://www.standrewblockisland.com
  (no bulletin link on 2026-11-15), probe po st-andrew-church-02807 (no publications on 2026-11-15), or
  ask the office (401-466-5519, standrewbi@gmail.com). Set the provider once one is found.'
revisit_after: 2027-03-01
research:
- method: probe po st-andrew-church-02807 (found by '<name>-church-<zip>')
  url: https://parishesonline.com/organization/st-andrew-church-02807
  checked: '2026-11-15'
  outcome: not-found
  next_action: Re-run probe po st-andrew-church-02807
  retry_when: The org lists a publication, or the parish site links a bulletin
- method: probe url and visit.py --text/--links on https://www.standrewblockisland.com (home, /sacraments,
    /about, /contact, /new-index, /new-page-1, /new-page-3); visit.py on the linked Facebook page; probe
    url on the finder's angelfire page and the ParishesOnline org's website saintandrewblockisland.com
  url: https://www.standrewblockisland.com
  checked: '2026-11-15'
  outcome: not-found
  next_action: Recheck the parish site and Facebook page for a posted bulletin, or ask the office
  retry_when: The site adds a bulletin page, or the office says where a bulletin is posted
bulletin_status: not-found
---

## Publisher

No bulletin found. St. Andrew, Block Island (Rev. Joseph Protano, Pastor) has a ParishesOnline org (`st-andrew-church-02807`, LPi 0018000000Qx7uSAAR) with no publications, and its current site https://www.standrewblockisland.com has no bulletin page; it posts the seasonal Mass schedule on its "Mass Schedule & Social" page (/sacraments). The finder's homepage (an angelfire page) does not load, and the ParishesOnline org's website (saintandrewblockisland.com) is a spam squat. The Facebook page the site embeds is the Ladies' Guild's and carried no bulletin when read. The org's ids are kept in `publication` so audit can match them if the bulletin returns.

## Worship sites

Two, used by season (parish site, /sacraments, read 2026-11-15; contact page "Church Locations: 23 Chapel Street; 22 Spring Street"): the Chapel Street Church, 23 Chapel St. (mid-June to October), and the Spring Street Parish Center, 22 Spring St. (October to Easter). The finder (12168) gives the same split: Sunday 10:00 AM "Parish Center, Spring St.; October to May" and 8:00/10:00 AM "Summer - Chapel Street Church".

## Website and bulletin provider

`no_bulletin`, so the row and its churches stay in the records but off the site (Settled policy 4). The website is the parish site's schedule page, the one place the parish publishes its Masses.

## Not yet confirmed

Whether the parish publishes a bulletin anywhere (print only, email, or Facebook); see `revisit` and `research`.
