---
name: Our Lady of the Immaculate Conception and Good Shepherd Parishes
website: https://sites.google.com/view/olichome-freeland-pa/home
bulletin_provider: other
provider_id: page-pdfs https://sites.google.com/view/olichome-freeland-pa/2026-bulletins
publication: ['url:https://sites.google.com/view/olichome-freeland-pa/2026-bulletins', 'url:https://sites.google.com/view/good-shepherd-church-drums-pa/2026-bulletins']
group: Our Lady of the Immaculate Conception Parish; Good Shepherd Parish
evidence:
- url: https://drive.google.com/uc?export=download&id=19PIsk77S1SnnHw-5zfLXHWhm5s_fb-xp
  seen: 2026-10-16
  quote: OUR THREE PARISHES HAVE SOME EXCITING EVENTS COMING UP!
  note: The 18 October 2026 bulletin ("10/18" on both parishes' 2026 Bulletins pages, the same Drive file),
    page 3. Page 4 is headed "Our Lady of the Immaculate Conception", page 5 "St. Patrick's Worship Site",
    page 6 "Good Shepherd Church", each with that church's Mass intentions.
- url: https://drive.google.com/uc?export=download&id=19PIsk77S1SnnHw-5zfLXHWhm5s_fb-xp
  seen: 2026-10-16
  quote: Sat. 10/17 4:00 PM Rev. Francis Skitski by His Parishioners Sun. 10/18 11:00 AM
  note: Page 4, Immaculate Conception's Mass intentions.
- url: https://drive.google.com/uc?export=download&id=19PIsk77S1SnnHw-5zfLXHWhm5s_fb-xp
  seen: 2026-10-16
  quote: Sat 10/17 5:00 PM Chris Alford by His Parents, Tyra and Mike Sun 10/18 9:45 AM
  note: Page 5, St. Patrick's Worship Site.
- url: https://drive.google.com/uc?export=download&id=19PIsk77S1SnnHw-5zfLXHWhm5s_fb-xp
  seen: 2026-10-16
  quote: Saturday, October 17 6:00PM Pearl & John Sipple
  note: Page 6, Good Shepherd Church.
- url: https://drive.google.com/uc?export=download&id=1X3TR9axoQQ_9v0jWoruXKYb9Y6nREPd9
  seen: 2026-10-16
  quote: 'A nine-person Transition Team was formed, consisting of three members each from the parishes
    affected by the merger: St. Patrick’s Parish, Our Lady of the Immaculate Conception, and Good Shepherd
    Parish.'
  note: Letter to St. Patrick's parishioners dated June 6, 2026, page 2 of the 6/7 bulletin (then headed
    "Immaculate Conception Parish"). It also lists "Strengthen communication in the combined bulletin".
- url: https://drive.google.com/uc?export=download&id=13NOlOS34rRg62XHyHyWXyIIPEfLC5Blj
  seen: 2026-10-16
  quote: 6:00 PM Welcoming Mass for the Parishioners of St. Patrick’s
  note: 28 June 2026 bulletin, page 5 (Mass of Wednesday 7/1). From the 5 July issue on, the bulletin
    carries a St. Patrick's section.
- url: https://sites.google.com/view/olichome-freeland-pa/2026-bulletins
  seen: 2026-10-16
  note: Lists the 2026 issues as Drive file links labelled by date ("10/4", "10/11", "10/18", ...). The
    Good Shepherd site (sites.google.com/view/good-shepherd-church-drums-pa/2026-bulletins) links the
    very same Drive file ids for every week.
- url: https://stpatrickswhitehaven.org/bulletin/
  seen: 2026-10-16
  note: 'St. Patrick''s own WordPress site (read with visit.py; plain fetches get 403). Its bulletin page
    lists "Bully-Sunday-..." PDFs, newest "Bully-Sunday-June-28-2026.pdf": nothing posted since the merger.'
revisit: Check that the 2026-bulletins page (or its 2027 successor) still lists new issues and repin the
  recipe if the page moved.
revisit_after: 2027-01-15
promoted: 2026-10-17
---

## Publisher

One weekly bulletin for three canonical communities with one pastor ("Father Mike"):
Our Lady of the Immaculate Conception, Freeland; Good Shepherd, Drums; and, since 1 July
2026, St. Patrick's, White Haven, merged into Our Lady of the Immaculate Conception (the
diocese finder lists St. Patrick Church as a worship site of that parish). The 18 October
2026 issue says "OUR THREE PARISHES HAVE SOME EXCITING EVENTS COMING UP!" (page 3) and
gives each church its own page of Mass intentions: Immaculate Conception (page 4), "St.
Patrick's Worship Site" (page 5) and Good Shepherd Church (page 6). Both parishes' Google
Sites link the same Drive file for every 2026 week (10/18 is
`19PIsk77S1SnnHw-5zfLXHWhm5s_fb-xp` on both), so this is one bulletin, not two.

The merger: a 6 June 2026 letter to St. Patrick's parishioners (in the 7 June bulletin)
names a transition team from "the parishes affected by the merger: St. Patrick's Parish,
Our Lady of the Immaculate Conception, and Good Shepherd Parish" and mentions "the combined
bulletin"; the 28 June issue announces a "Welcoming Mass for the Parishioners of St.
Patrick's" on 1 July; St. Patrick's section appears from the 5 July issue. St. Patrick's
own site's bulletin page stops at 28 June 2026, so its old channel is silent.

## Worship sites

Three, all in the current bulletin with weekend Masses:
- Immaculate Conception (Our Lady of the Immaculate Conception), 898 Centre Street,
  Freeland (`our-lady-of-the-immaculate-conception-freeland`).
- St. Patrick, 411 Allegheny Street, White Haven (`st-patrick-white-haven`).
- Good Shepherd, 87 South Hunter Highway, Drums (`good-shepherd-drums`).

The diocese's consolidated-parishes list gives the old Freeland parishes St. Ann, St.
Antony, St. Casimir and St. John Nepomucene as "(closed 2008)" with records here; only the
church at 898 Centre Street is in either roster (the finder calls it "Saint Ann Church",
see its record), so none of the others has a record. GCatholic gives Good Shepherd the
website gs-sjb.org (the name suggests a former Good Shepherd and St. John Bosco site; not
checked). St. John Bosco now publishes its own bulletin (`saint-john-bosco-conyngham`).

## Website and bulletin provider

The Our Lady of the Immaculate Conception Google Site (the finder's link for that parish),
whose "2026 Bulletins" page links one Google Drive PDF per week. Provider `other`: its
resolver reads Drive file links. Recipe `page-pdfs
https://sites.google.com/view/olichome-freeland-pa/2026-bulletins` is pinned by inspection;
`fetch:check` (run on 2026-10-17 against a temporary parishes.csv holding this row) picked the 18 October 2026 Drive file ("current"). The links are labelled by
date ("10/18") but not listed in date order, and the page is yearly: the 2025 page now
lives at /2026-bulletins/2025-bulletins, so expect the recipe's page to change in January
2027. Both parishes' bulletin pages are recorded as `publication`s. Page 7 is an image
(a flyer); the Mass pages have text.

## Not yet confirmed

Whether a 2027 page replaces "2026-bulletins" (revisit in January). Good Shepherd remains
a separate canonical parish in the finder; the shared bulletin, not the canonical status,
makes this one row.
