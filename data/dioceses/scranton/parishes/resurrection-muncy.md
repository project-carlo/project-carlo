---
name: Church of the Resurrection
website: https://www.resurrectiononline.net/bulletin
bulletin_provider: parishes_online
provider_id: resurrection-church
publication: ['po-org:resurrection-church', 'lpi:0018000000Qc0EZAAZ', 'po-container:03/0730']
group: Resurrection Parish
evidence:
- url: https://container.parishesonline.com/bulletins/03/0730/20261018B.pdf
  seen: 2026-10-16
  quote: CHURCH OF THE RESURRECTION, 75 MUSSER LANE, MUNCY, PA 17756
  note: 'Running footer of the 18 October 2026 issue (pages 2-4). Page 1 is an image (rendered with render.py
    2026-10-16): masthead "Church of the Resurrection / Rev. Sean G. Carpenter, Pastor / 75 Musser Lane,
    Muncy, PA 17756 / www.resurrectiononline.net", and a Mass Schedule box listing OLOL and COR times
    (Saturday 4:00pm OLOL, 5:30pm COR; Sunday 8:30am COR, 10:30am OLOL).'
- url: https://container.parishesonline.com/bulletins/03/0730/20261018B.pdf
  seen: 2026-10-16
  quote: 8:30am COR - Dom Miller by Fr. John Victoria
  note: Page 2 Mass intentions, Sunday 18 October.
- url: https://parishesonline.com/organization/resurrection-church
  seen: 2026-10-16
  note: '`probe po resurrection-church`: 75 Musser Ln, Muncy, LPi id 0018000000Qc0EZAAZ, container 03/0730,
    weekly issues to 2026-10-18. Linked from the parish''s /bulletin page (seen in a browser, visit.py,
    2026-10-16).'
promoted: 2026-10-17
---

## Publisher

The Church of the Resurrection, Muncy publishes its own weekly bulletin through ParishesOnline
(container 03/0730). The 18 October 2026 issue's page 1 (an image) has the masthead "Church of
the Resurrection, Rev. Sean G. Carpenter, Pastor, 75 Musser Lane, Muncy", and every text page
carries the footer "CHURCH OF THE RESURRECTION, 75 MUSSER LANE, MUNCY, PA 17756".

Fr. Carpenter is also pastor of Our Lady of Lourdes, Montoursville; both parishes' bulletins
print a joint Mass schedule and intentions list (OLOL and COR). Montoursville's bulletin is a
different publication with its own masthead, self-hosted on its own site, and both are current,
so these are two rows (`our-lady-of-lourdes-montoursville`).

## Worship sites

One: `resurrection-muncy`. The OLOL Masses in this bulletin's schedule are at Montoursville's
church, which is under that parish's own row.

## Website and bulletin provider

The parish site's /bulletin page embeds the ParishesOnline issue list (rendered in a browser;
plain `probe url` sees only "View our recent bulletins"). `probe po` gives the organization
`resurrection-church`, LPi id 0018000000Qc0EZAAZ and container 03/0730, with weekly issues
through 18 October 2026.

## Not yet confirmed

Page 1 of the bulletin (masthead and Mass schedule) is an image with no text layer, so the
pipeline needs to read it as an image for the schedule; the intentions on page 2 are text.
