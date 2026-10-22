---
name: St. Rose, Latrobe
website: https://www.stroselatrobe.org/bulletins/
bulletin_provider: other
provider_id: dated-post
publication: ['url:https://www.stroselatrobe.org/bulletins/']
group: ''
evidence:
- url: https://www.stroselatrobe.org/wp-content/uploads/2026/10/10182026.pdf
  seen: 2026-10-22
  quote: ST. ROSE CATHOLIC CHURCH
  note: 'Page 1 masthead of the 18 Oct 2026 issue (7 pages): "ST. ROSE CATHOLIC CHURCH 4969 Route 982 ·
    Latrobe, PA 15650 (724) 537-3709 · www.stroselatrobe.org A Parish of the Diocese of Greensburg",
    "October 18, 2026", "Reverend Fr. Ronald Maquinana ..........Pastor". Names no other parish or church.'
- url: https://www.stroselatrobe.org/wp-content/uploads/2026/10/10182026.pdf
  seen: 2026-10-22
  quote: 9:30 am…………Living and Deceased Parishioners
  note: 'Page 2 "Mass Intentions" for the week: Saturday October 17th 4:00 pm, Sunday October 18th 9:30
    am, weekdays 8:30 am (Wednesday 6:00 pm), Saturday October 24th 4:00 pm, all at St. Rose (the page
    is headed "SAINT ROSE CATHOLIC CHURCH LATROBE, PENNSYLVANIA").'
- url: https://www.stroselatrobe.org/bulletins/
  seen: 2026-10-22
  note: 'Bulletin index on the parish''s WordPress site (diocese template): one post per issue, newest
    first (OCTOBER 18, 2026; OCTOBER 4, 2026; "SEPTEMBER 27, 2027" [sic]; SEPTEMBER 13, 2026 ...). Each
    post embeds a dFlip viewer whose source is the PDF, e.g. wp-content/uploads/2026/10/10182026.pdf.
    Some weeks are missing (no 11 Oct or 20 Sep post).'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=162
  seen: 2026-10-22
  note: 'Directory: St. Rose Parish, 4969 Route 982, pastor Father Ronald L. Maquiñana; "Saturday: 4:00
    p.m.; Sunday: 9:30 a.m."; no Partner Parishes listed.'
- url: https://parishesonline.com/organization/st-john-the-evangelist-st-rose
  seen: 2026-10-22
  note: 'probe po: the only LPi organization with St. Rose in its name is an empty St. John the
    Evangelist org (306 Saint Johns Dr, no issues, no container), left from a former pairing. The LPi
    geo-search around Latrobe (6 miles) lists no St. Rose organization.'
---

## Publisher

St. Rose Parish, Latrobe publishes its own weekly bulletin and posts it on its own website. The 18
October 2026 issue (read 2026-10-22; the newest post that day) has the masthead "ST. ROSE CATHOLIC
CHURCH, 4969 Route 982 · Latrobe ... A Parish of the Diocese of Greensburg" with Fr. Ronald Maquinana
as pastor, and names no other parish. The diocese directory gives St. Rose no partner parish. St. Rose
was once paired with St. John the Evangelist (an empty LPi org "st-john-the-evangelist-st-rose"
survives), but St. John now shares Holy Family's bulletin (holy-family-and-st-john-latrobe), and that
bulletin does not mention St. Rose.

## Worship sites

One: St. Rose church, 4969 Route 982. The bulletin's Mass intentions (page 2) list Saturday 4:00 pm,
Sunday 9:30 am and weekday Masses, all at St. Rose, and name no other building.

## Website and bulletin provider

`website` is the parish site's bulletin index, which lists one post per issue, newest first, each
embedding the PDF in a dFlip viewer. Provider `other`. `pnpm fetch:check` (2026-10-22) resolved it as
"dated-post on https://www.stroselatrobe.org/bulletins/: current" and fetched the 18 October PDF
(`wp-content/uploads/2026/10/10182026.pdf`), so `provider_id` is the recipe it printed, `dated-post`.
The post titles carry the date (one is mistyped "September 27, 2027"); the PDF names are `MMDDYYYY.pdf`.

## Not yet confirmed

The parish skips some weeks (no 11 October or 20 September post); if the index lags further, a
fetch may return the previous issue.
