---
name: Catholic Churches of Brushton, Hopkinton, North Bangor and St. Regis Falls
website: http://www.hcsmsasa.org
bulletin_provider: parishes_online
provider_id: st-mary-st-augustine
publication:
- po-org:st-mary-st-augustine
- lpi:0018000000Qx7FLAAZ
- po-container:04/0689
group: The Catholic Community of St. Augustine
evidence:
- url: https://container.parishesonline.com/bulletins/04/0689/20260927B.pdf
  seen: '2026-09-30'
  quote: In Brushton, Hopkinton, North Bangor & St. Regis Falls
  note: 'Masthead, page 1 of the 27 September 2026 issue (4 pages, text layer): "The Roman Catholic Church
    In Brushton, Hopkinton, North Bangor & St. Regis Falls", then "Holy Cross Church, Hopkinton, NY",
    "St. Mary’s Church, Brushton, NY", "St. Ann’s Church, St. Regis Falls, NY" and "The Roman Catholic
    Community of St. Augustine in North Bangor, NY", "Sept. 27, 2026, 26th Sunday in Ordinary Time". Pastor
    Rev. Kris C. Lauzon (page 3).'
- url: https://container.parishesonline.com/bulletins/04/0689/20260927B.pdf
  seen: '2026-09-30'
  quote: '9:45am: St. Ann: People of the parish'
  note: 'Page 2, Mass intentions for 28 Sept to 4 Oct: Sat 4:00pm SM (St. Mary), Sun 8:00am SA (St. Augustine),
    9:45am St. Ann, 11:30am HC (Holy Cross); weekdays 9:00am SM (Mon, Wed, Sat), 9:00am SA (Tue), 8:00am
    St. Ann (Thu, Fri). One schedule for all four churches.'
- url: https://container.parishesonline.com/bulletins/04/0689/20260927B.pdf
  seen: '2026-09-30'
  quote: The St. Mary & St. Augustine Altar Rosary Society
  note: 'Page 1: shared parish activities for the four churches (St. Mary and St. Augustine Altar Rosary
    Society meets at the Deacon John Dwyer Parish Center; Holy Cross has its own religious-formation slot),
    and page 2 lists the collections of Holy Cross, St. Mary, St. Ann and St. Augustine together.'
- url: http://www.hcsmsasa.org
  seen: '2026-09-30'
  quote: 8 AM at St. Augustine's Church, North Bangor
  note: 'Parish website (plain HTML, no Cloudflare), read 2026-09-30: title "The Roman Catholic Church
    in Brushton, Hopkinton, North Bangor & St. Regis Falls"; Mass Times Saturday 4 PM St. Mary''s, Brushton;
    Sunday 8 AM St. Augustine''s, North Bangor, 9:45 AM St. Ann''s, St. Regis Falls, 11:30 AM Holy Cross,
    Hopkinton; embeds the ParishesOnline widget id=0018000000Qx7FLAAZ.'
- url: https://parishesonline.com/organization/st-mary-st-augustine
  seen: '2026-09-30'
  note: '`probe po st-mary-st-augustine` (the page is JavaScript): "St. Mary - St. Augustine", 1347 Washington
    St, Brushton, website https://www.staugustinesandstmarys.org/, ids po-org:st-mary-st-augustine, lpi:0018000000Qx7FLAAZ,
    po-container:04/0689; weekly issues 2026-08-23 to 2026-09-27, all at container 04/0689.'
---

## Publisher

One weekly bulletin, published through ParishesOnline (container 04/0689, organization
`st-mary-st-augustine`, LPi id 0018000000Qx7FLAAZ) and embedded on the parishes' own website
hcsmsasa.org. I read the 27 September 2026 issue (4 pages, all with a text layer). Its
page 1 masthead reads "The Roman Catholic Church In Brushton, Hopkinton, North Bangor & St.
Regis Falls" and lists Holy Cross Church (Hopkinton), St. Mary's Church (Brushton), St. Ann's
Church (St. Regis Falls) and "The Roman Catholic Community of St. Augustine in North Bangor".
Page 2 has one list of Mass intentions for all four churches, and page 3 names one pastor,
Rev. Kris C. Lauzon, with one parish office (St. Augustine's Rectory, 2472 US Route 11, North
Bangor, 518-483-6674). Weekly issues from 23 August to 27 September 2026 all sit in the same
container (`probe po`), so this is not a one-off.

The diocese's directory (rcdony.org) gives all four churches the same website (hcsmsasa.org) and
phone (518-483-6674) and the same pastor, but groups only North Bangor ("The Catholic Community
of St. Augustine"); the other three have no group. The bulletin shows they are one publisher
regardless.

## Worship sites

Four churches, all in the 27 September 2026 schedule (page 2 intentions and the parish site's Mass
Times): St. Mary's, Brushton (Saturday 4:00 pm; weekdays 9:00 am); St. Augustine's, North Bangor
(Sunday 8:00 am; Tuesday 9:00 am); St. Ann's, St. Regis Falls (Sunday 9:45 am; Thursday and
Friday 8:00 am); Holy Cross, Hopkinton (Sunday 11:30 am). Church records:
`st-mary-brushton`, `st-augustine-north-bangor`, `st-ann-st-regis-falls`, `holy-cross-hopkinton`.
Both rosters list exactly these four in the area (GCatholic 18246, 18247, 18334, 18283; directory
brushton, north-bangor, st-regis-falls, hopkinton). Nothing the bulletin, the diocese or GCatholic
lists is left over.

The old ParishesOnline account name ("St. Mary - St. Augustine") names two of the four and the
old domain staugustinesandstmarys.org (GCatholic's stmarysbrushton.org redirects to it) no longer
answers `probe url` (SSL error); that is the trap the README warns of, an account name that lags the
masthead. The four-church masthead wins.

## Website and bulletin provider

`website` is hcsmsasa.org, which is the address the diocese directory gives for all four churches.
It serves plain HTML (`probe url`: 200, title "The Roman Catholic Church in Brushton, Hopkinton, North
Bangor & St. Regis Falls", publication lpi:0018000000Qx7FLAAZ) and embeds
`parishesonline.com/publicationWidget?type=bulletin&id=0018000000Qx7FLAAZ`. The provider is
ParishesOnline; `probe po st-mary-st-augustine` returned the three ids recorded in `publication`
and the latest issue, 2026-09-27.

## Not yet confirmed

The 27 September bulletin says St. Ann's heating-system work is scheduled to begin on 5 October and
"should take one week"; if Masses there move for that week it does not change the row.
Otherwise nothing outstanding.
