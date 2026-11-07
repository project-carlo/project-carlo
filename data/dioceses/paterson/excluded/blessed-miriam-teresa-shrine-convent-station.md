---
name: Holy Family Chapel (Shrine of Blessed Miriam Teresa)
reason: no-bulletin
line1: 2 Convent Rd.
city: Convent Station
state: NJ
postal_code: 07960
decided: 2026-11-04
roster: ['gcatholic:40308']
evidence:
- url: https://www.scnj.org/chapel
  seen: 2026-11-04
  quote: Visits to the Shrine and Crypt of Blessed Miriam Teresa Demjanovich, S.C., are available by appointment
    only.
  note: Holy Family Chapel page of the Sisters of Charity of Saint Elizabeth (read with parish-site-access
    visit.py --text). Under 'Daily Mass Times Effective Saturday, February 7, 2026' it gives Monday -
    Friday 11:00 a.m., Saturday 9:15 a.m., Sunday 9:15 a.m.; contact Sister Margaret McCann, SC, Sacristan,
    P.O. Box 476 Convent Station, NJ 07961-0476. It says nothing about who may attend.
- url: https://gcatholic.org/churches/usa-03/40308
  seen: 2026-11-04
  quote: 2 Convent Rd., Convent Station, New Jersey 07960
  note: GCatholic 40308 'Blessed Miriam Teresa', Shrine, in Holy Family Chapel; shrine since 2016.10.16;
    website scnj.org.
- url: https://files.ecatholic.com/11361/bulletins/20261101.pdf
  seen: 2026-11-04
  note: The neighbouring St. Thomas More bulletin of 1 November 2026 schedules only its own church; a
    grep for Miriam and Chapel finds nothing.
revisit: Check scnj.org/chapel for a bulletin, and whether its Masses are stated to be public
revisit_after: 2027-05-01
research:
- method: probe url and visit.py --text on scnj.org (home, /chapel, /copy-of-blessed-miriam-teresa); probe
    pdf on the 5 PDFs the home page links
  url: https://www.scnj.org/chapel
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look for a chapel or shrine bulletin from the Sisters of Charity, and for a statement that
    the chapel's Masses are open to the public
  retry_when: scnj.org posts a chapel bulletin or newsletter with a Mass schedule, or a parish bulletin
    starts listing Holy Family Chapel
  revisit_after: 2027-05-01
---

## Why it is excluded

GCatholic's Blessed Miriam Teresa shrine (40308) is Holy Family Chapel at the Sisters of Charity of Saint Elizabeth motherhouse, 2 Convent Rd., Convent Station, next to St. Thomas More. The congregation's chapel page (`https://www.scnj.org/chapel`, read 2026-11-04) posts "Daily Mass Times Effective Saturday, February 7, 2026: Monday - Friday 11:00 a.m., Saturday 9:15 a.m., Sunday 9:15 a.m.", and says "Visits to the Shrine and Crypt of Blessed Miriam Teresa Demjanovich, S.C., are available by appointment only" (Monday-Thursday, 9:00 a.m.-3:00 p.m.).

No bulletin carries this schedule: the chapel page and the Blessed Miriam Teresa page link no bulletin, and the five PDFs on the scnj.org home page are congregational items (the Fall 2025 magazine, a May 2026 newsletter, jubilee lists, 2023 assembly acts). The St. Thomas More bulletin of 1 November 2026 doesn't mention the chapel. So it is not a church row.

Reason `no-bulletin` is a judgement. The Mass times are posted on the public site without restriction, so this record treats the Masses as public. But the chapel is a motherhouse chapel, and the shrine itself is by appointment only. If the Masses turn out to be for the community only, the reason would be `no-public-mass`. Either way the place stays off the site.

GCatholic gives postal code 07960; the congregation's mailing address is P.O. Box 476, Convent Station 07961-0476.

## What would change this

A bulletin listing Holy Family Chapel's Masses (from the Sisters or from a parish) would make it a church row under that bulletin's parish. A statement that the Masses are for the community only would change the reason to `no-public-mass`.
