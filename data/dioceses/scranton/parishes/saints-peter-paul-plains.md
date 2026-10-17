---
name: Saints Peter & Paul Parish
website: https://sspeterandpaulplains.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://sspeterandpaulplains.com/Sunday-Bulletin']
group: Saints Peter & Paul Parish
evidence:
- url: https://sspeterandpaulplains.com/LinkClick.aspx?fileticket=TrZOr1DOEi4%3d&tabid=2011&portalid=34&mid=3661
  seen: 2026-10-16
  quote: 'Saturday: 4:00pm - Saints Peter & Paul Sunday: 7:30am - Saints Peter & Paul 10:30am - Saints
    Peter & Paul'
  note: '20 September 2026 issue (the Sunday Bulletin page''s ''September 20, 2026'' link), page 1. Pastor
    Rev. Robert J. Simon. Page 2: weekday Masses Tuesday-Friday 12:15pm.'
- url: https://sspeterandpaulplains.com/LinkClick.aspx?fileticket=WqpfrF04bgg%3d&tabid=2011&portalid=34&mid=3661
  seen: 2026-10-16
  note: '4 October 2026 issue: every page is an image (rendered with render.py). Page 1: ''Saints Peter
    & Paul Parish, 13 Hudson Road, Plains''; Mass schedule Saturday 4:00pm, Sunday 7:30am and 10:30am;
    Rev. Robert J. Simon, Pastor.'
- url: https://sspeterandpaulplains.com/Sunday-Bulletin
  seen: 2026-10-16
  note: DNN page listing one LinkClick.aspx?fileticket=... link per Sunday (read with visit.py). On 2026-10-16
    the link labelled 'October 11, 2026' served a 1 January 2017 bulletin, an upload mistake.
promoted: 2026-10-17
---

## Publisher

Saints Peter & Paul Parish, Plains publishes its own weekly bulletin on its website. The 20
September 2026 issue lists every weekend Mass as at Saints Peter & Paul (Saturday 4:00pm,
Sunday 7:30am and 10:30am) and weekday Masses Tuesday-Friday at 12:15pm; the 4 October issue
(image-only) has the same weekend schedule.

## Worship sites

One: Saints Peter & Paul Church, 13 Hudson Road (`sts-peter-and-paul-plains`). The parish
absorbed two Wilkes-Barre churches that are now closed: St. Dominic (last Mass 11 June 2022,
kept for the parish's food pantry; `excluded/st-dominic-wilkes-barre.md`) and, with the
suppression of St. Andre Bessette Parish, St. Stanislaus Kostka (last Mass 19 June 2022;
`excluded/st-stanislaus-kostka-wilkes-barre.md`). St. Andre Bessette's former Holy Saviour
church is also closed (`excluded/holy-saviour-wilkes-barre.md`).

## Website and bulletin provider

`other`: sspeterandpaulplains.com/Sunday-Bulletin (DotNetNuke) lists one
`LinkClick.aspx?fileticket=` download per Sunday, labelled with the date. The links have
no .pdf in the URL, and recent issues are scanned images (the 4 October one entirely), so
the pipeline will need to read them as images. No recipe pinned.

## Not yet confirmed

The newest link ("October 11, 2026") served a 2017 file on 2026-10-16; check that later
weeks are uploaded correctly.
