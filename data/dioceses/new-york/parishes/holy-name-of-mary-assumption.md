---
name: Holy Name of Mary-Assumption
website: https://holynameofmary-assumption.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:10978']
group: ''
evidence:
- url: https://files.ecatholic.com/10978/bulletins/20261101.pdf
  seen: 2026-11-08
  note: 'November 1, 2026 issue, four pages, image-only (no PDF text; page 1 read from a rendering). Masthead
    ''Holy Name of Mary-Assumption'', Reverend Ivan Lovrić - Pastor, www.holynameofmary-assumption.org,
    Rectory (845) 457-5276, Parish Office (845) 457-1738. One unlabelled schedule: Saturday 4:00 pm; Sunday
    8:30 am & 11:30 am; Monday - Thursday 9:30 am; Friday No Mass.'
- url: https://holynameofmary-assumption.org/
  seen: 2026-11-08
  quote: 89 Union Street Montgomery, NY 12549
  note: 'Homepage (headed Chrome): ''Serving Montgomery and Maybrook'', Mass schedule Saturday 4:00 PM,
    Sunday 8:30 and 11:30 AM, daily 9:30 AM, and one address, 89 Union Street, Montgomery. Its Bulletins
    page is the eCatholic 10978 archive.'
- url: https://www.archny.org/places/holy-name-of-mary-assumption-church
  seen: 2026-11-08
  quote: The Parish Rectory is located at 89 Union Street in Montgomery.
  note: The archdiocese's place page, titled Holy Name of Mary Assumption Church, 89 Union Street, carries
    the same Mass schedule (Saturday 4:00 PM; Sunday 8:30 and 11:30 AM; weekday 9:30 AM) and lists no
    Maybrook location.
revisit: Read the Christmas 2026 issue for any Mass labelled at Assumption, Maybrook.
revisit_after: 2026-12-24
promoted: 2026-11-09
research:
- method: issues.py ecatholic:10978 --weeks 3
  url: https://files.ecatholic.com/10978/bulletins/20261101.pdf
  checked: '2026-11-08'
  outcome: found
  next_action: None; the November 8 file answered 403 on November 8 (eCatholic issues here have posted
    mid-week before).
- method: Homepage, Parish history and archdiocese place page read for a Maybrook (Assumption, 211 Homestead
    Ave.) Mass
  url: https://holynameofmary-assumption.org/parish-history
  checked: '2026-11-08'
  outcome: not-found
  next_action: Look for a Maybrook-labelled Mass in the bulletin (Christmas, Assumption feast on August
    15, funerals) or on the Mass Times page
  retry_when: The December 2026 issues post (Christmas schedules usually name each church)
bulletin_status: available
---

## Publisher

Holy Name of Mary-Assumption publishes a weekly bulletin on eCatholic (site 10978, files.ecatholic.com/10978/bulletins/YYYYMMDD.pdf). The November 1, 2026 issue (read 2026-11-08) is image-only; page 1, read from a rendering, has the masthead 'Holy Name of Mary-Assumption', Reverend Ivan Lovrić - Pastor, rectory and parish office numbers, and one Mass schedule with no church named: Saturday 4:00 pm, Sunday 8:30 am & 11:30 am, Monday - Thursday 9:30 am, Friday no Mass.

The October 2026 session found this publisher and its October 4 issue but left both buildings as open questions because the schedule names no building, so no row was created. Today's reading attributes the schedule to the Montgomery church: the parish homepage prints it beside a single address, 89 Union Street, Montgomery, and the archdiocese's place page, titled Holy Name of Mary Assumption Church at 89 Union Street, carries the same times and no Maybrook location.

## Worship sites

[Holy Name of Mary, Montgomery](../churches/holy-name-of-mary-montgomery.md): the weekly schedule above.

[Assumption, Maybrook](../open/assumption-maybrook.md) (GCatholic: a mission of Holy Name of Mary; the parish history: 'Assumption as a mission church' and the 110th anniversary of Assumption Church in 2017-18) stays open: no source read gives a Mass there now, and none says it closed.

## Website and bulletin provider

The parish site, holynameofmary-assumption.org, is eCatholic-hosted (publication ecatholic:10978), so the `ecatholic` reader takes it from `website`. The issues are scanned images, so the bulletin has to be read as images. Its 'This Week' menu link points to a JPPC template PDF (jppc.net/onlinebulletins/4022template.pdf), not this parish's issue.

## Not yet confirmed

Whether Assumption in Maybrook still has any Mass (see its open record).
