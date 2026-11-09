---
name: St. Joseph - New Paltz
website: https://stjosephnewpaltz.org
bulletin_provider: parishes_online
provider_id: the-community-of-st-joseph
publication: ['ecatholic:12896', 'po-org:the-community-of-st-joseph', 'lpi:0018000000Qc1UyAAJ', 'po-container:04/0144']
group: ''
evidence:
- url: https://files.ecatholic.com/12896/bulletins/20260927.pdf?t=1790794774000
  seen: 2026-10-07
  quote: "MISSION  STATEMENT \n“The parish family of St. Joseph, nourished by the Word of God and the\
    \ sacraments of the Roman Catholic Church \nand animated by the life of St. Francis of Assisi, proclaims,\
    \ radiates and lives the love of God in our community.” \nEucharist \n \nam \nam \nBaptism \n \nReconciliation\
    \ \n \n \nMarriage \nat \nno \ninstruction law. \n \nAnointing o"
  note: The September 27 issue identifies the parish family of St. Joseph and contains current parish
    Mass intentions and the October 3-4 parish celebrations. Other churches mentioned as destinations
    are not folded into this publisher.
- url: https://container.parishesonline.com/bulletins/04/0144/20261108B.pdf
  seen: 2026-11-09
  quote: Fr. Richard Crawley, O.F.M., Cap. -Pastor
  note: November 8, 2026 issue on ParishesOnline (container 04/0144, org the-community-of-st-joseph);
    the masthead names St. Joseph Church, 34 So. Chestnut St., New Paltz, and its Mass schedule. The parish's
    own eCatholic archive (ecatholic:12896) stopped at October 25.
promoted: 2026-10-08
research:
- method: 'Parish Bulletins page in headed Chrome (visit.py) and eCatholic dated paths: the page lists
    October 25, 2026 as newest; files.ecatholic.com/12896/bulletins/20261101.pdf and 20261108.pdf answer
    403'
  url: https://stjosephnewpaltz.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: None while ParishesOnline is the channel; the eCatholic archive is kept as a fallback id
  retry_when: The ParishesOnline container stops receiving weekly issues
- method: 'ParishesOnline coordinates search API, then probe po the-community-of-st-joseph: container
    04/0144 has weekly issues through November 8, 2026'
  url: https://parishesonline.com/organization/the-community-of-st-joseph
  checked: '2026-11-09'
  outcome: found
  next_action: Switched the row to parishes_online by org slug; fetch:check picks the November 8 issue
---

## Publisher and worship sites

The September 27 issue identifies the parish family of St. Joseph and contains current parish Mass intentions and the October 3-4 parish celebrations. Other churches mentioned as destinations are not folded into this publisher.

Linked worship-site records for St. Joseph - New Paltz: [St. Joseph](../churches/st-joseph-new-paltz.md). Each church record retains its building-specific Mass evidence.

## Website and publication

Since November 2026 the row reads ParishesOnline (org `the-community-of-st-joseph`, container 04/0144), which had the November 1 and November 8 issues on 2026-11-09 while the parish's eCatholic archive (`ecatholic:12896`, linked from stjosephnewpaltz.org/bulletins) still ended at October 25 and its dated paths for November 1 and 8 answered 403. The November 8 container issue carries the St. Joseph Church, New Paltz masthead. The eCatholic id stays in `publication` as the parish's other channel.

## Recheck

If the ParishesOnline container stops receiving weekly issues, re-read the eCatholic archive at https://stjosephnewpaltz.org/bulletins. Address and name verification flags remain false where exact agreement from two independent sources has not been documented.
