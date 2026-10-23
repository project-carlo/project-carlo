---
name: Churches of St. Anne and Holy Family, Rostraver and West Newton
website: https://www.stannerostraver.org
bulletin_provider: parishes_online
provider_id: church-of-st-anne-15012
publication: ['po-org:church-of-st-anne-15012', 'lpi:0018000000QxBzLAAV', 'po-container:14/1743', 'po-org:holy-family-church-15089',
  'lpi:0018000000QxBzUAAV', 'url:https://www.stannerostraver.org/bulletins/', 'url:https://www.holyfamilywn.org/bulletins/']
group: 'Same pastor: St. Anne + Holy Family (Sayson)'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1743/20261025B.pdf
  seen: 2026-10-22
  quote: SAINT ANNE AND HOLY FAMILY
  note: 'Page 1 masthead of the 25 Oct 2026 issue (8 pages): "CHURCHES OF SAINT ANNE AND HOLY FAMILY",
    "OCTOBER 25, 2026 30TH SUNDAY IN ORDINARY TIME", then two contact blocks: "CHURCH OF SAINT ANNE 1870
    Rostraver Road, Rostraver Township, PA 15012 724-872-3555 www.stannerostraver.org" (Weekends Saturday
    4:30pm, Sunday 8:00 am & 11:00am; Weekdays Monday, Thursday & Friday 8:00 am) and "HOLY FAMILY CHURCH
    225 North Second Street, West Newton, PA 15089 724-872-6123 www.holyfamilywn.org" (Weekends Saturday
    4:00 pm, Sunday 11:00 am; Weekdays Tuesday & Wednesday 8:00 am).'
- url: https://container.parishesonline.com/bulletins/14/1743/20261025B.pdf
  seen: 2026-10-22
  quote: MASS SCHEDULE AND INTENTIONS
  note: 'Page 2: one intentions list for both churches, coded HF and SA ("4:00 pm | HF", "4:30 pm |SA|",
    "8:00 am | SA", "11:00 am | HF", "11:00 am | SA"), 24 October to 1 November. No other place is named.'
- url: https://parishesonline.com/organization/church-of-st-anne-15012
  seen: 2026-10-22
  note: 'probe po: org "Church of St. Anne, Rostraver", 1870 Rostraver Rd (LPi 0018000000QxBzLAAV), container
    14/1743, latest issues 2026-10-25, 10-18, 10-11.'
- url: https://parishesonline.com/organization/holy-family-church-15089
  seen: 2026-10-22
  note: 'probe po: org "Holy Family Church", 225 N Second St, West Newton (LPi 0018000000QxBzUAAV), the
    same container 14/1743 with the same issues: both organizations carry one bulletin.'
- url: https://www.holyfamilywn.org/october-16-2026/
  seen: 2026-10-22
  note: 'Holy Family''s diocese-template site (403 to probe url; curl with a browser User-Agent reads
    it): its /bulletins/ page lists one post per issue; this post embeds wp-content/uploads/2026/10/October-18-2026.pdf,
    whose page 1 is the same "CHURCHES OF SAINT ANNE AND HOLY FAMILY" masthead dated October 18, 2026.'
- url: https://www.stannerostraver.org/bulletin-october-18-2026/
  seen: 2026-10-22
  note: 'St. Anne''s site: its /bulletins/ page lists one post per issue; this post embeds wp-content/uploads/2026/10/Bulletin-Oct-18-2026.pdf,
    the same joint 18 October issue. Its separate "Bulletin-announcement-Oct-17-18-2026.pdf" (11 image-only
    pages) is the diocese''s weekly announcement packet ("For use the weekend of Oct. 17-18, 2026 / DIOCESAN
    NEWS/EVENTS"), not a bulletin.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=299
  seen: 2026-10-22
  note: 'Directory: Holy Family Parish, 225 North Second Street, West Newton, pastor Father Joel A. Sayson,
    "Saturday: 4:00 p.m.; Sunday: 11:00 a.m."; LocationID=250, St. Anne Parish, 1870 Rostraver Road, Rostraver
    Township, same pastor, "Saturday: 4:30 p.m.; Sunday: 8:00 a.m., 11:00 a.m.". Neither lists Partner
    Parishes.'
promoted: 2026-10-23
---

## Publisher

Holy Family Parish, West Newton and St. Anne Parish, Rostraver Township (two canonical parishes with one pastor,
Fr. Joel A. Sayson) publish one weekly bulletin through LPi / ParishesOnline, container 14/1743. The 25 October
2026 issue (read 2026-10-22) is headed "CHURCHES OF SAINT ANNE AND HOLY FAMILY", gives each church's address,
phone, website and Mass times side by side, and has one intentions list coded SA / HF. Both parishes' LPi
organizations (`church-of-st-anne-15012`, `holy-family-church-15089`) point at that one container, and both
parish websites repost the same issue (18 October: St. Anne's `Bulletin-Oct-18-2026.pdf`, Holy Family's
`October-18-2026.pdf`, same masthead). One bulletin, so one row, although the diocese directory lists the two
as separate parishes with no "Partner Parishes" entry. St. Anne (directory 250) was in batch 8's roster; it is
taken into this row because the bulletin is shared.

## Worship sites

Two: St. Anne church, 1870 Rostraver Road, Rostraver Township, and Holy Family church, 225 North Second Street,
West Newton, the only places in the bulletin's schedule and intentions. The "St. Anne Church Blessed Sacrament
Chapel" (page 5) is inside St. Anne church, not a separate site.

## Website and bulletin provider

`website` is St. Anne's site, the one the masthead lists first; it posts each issue. Provider `parishes_online`,
org slug `church-of-st-anne-15012`: `fetch:check` on 2026-10-22 fetched
`container.parishesonline.com/bulletins/14/1743/20261025B.pdf`, the 25 October issue. Publications record both
organizations, both LPi ids, the container and both parish sites' bulletin pages, all of which carry this one
bulletin.

## Not yet confirmed

Nothing. The pairing is not in the directory's "Partner Parishes" field; if the two ever split their bulletin,
the second LPi organization (`holy-family-church-15089`) would show its own container.
