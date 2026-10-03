---
name: Sacred Heart Parish (Margaretville and Andes)
website: https://sacredheartmargaretville.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://sacredheartmargaretville.org/bulletins/']
group: Sacred Heart Church; St. Ann's
evidence:
- url: https://sacredheartmargaretville.org/wp-content/uploads/2026/09/09-27-2026.pdf
  seen: 2026-09-28
  quote: Sacred Heart Church / Margaretville & St. Anne’s Church / Andes
  note: 'The 27 September 2026 issue, page 2 header. Page 1: "SACRED HEART ROMAN CATHOLIC CHURCH September
    27, 2026", rectory 38 Academy Street, pastor''s servant Rev. Paul J Mijas; "MASS SCHEDULE Weekend:
    Saturday 4:00 pm – St. Anne''s Mission Church, Sunday 9:00 am – Sacred Heart Church"; weekday Thursday
    9:00 am (chapel at the rectory), Friday 11 am adoration followed by Mass. Page 2 still carries a leftover
    header from the Stamford template ("Sacred Heart Church/Stamford & St. Philip Neri/Grand Gorge").'
- url: https://sacredheartmargaretville.org/bulletins/
  seen: 2026-09-28
  quote: Weekly Bulletin
  note: The parish's Bulletins page, a list of dated PDFs in wp-content/uploads (09-27-2026 back to 07-26-26).
promoted: 2026-09-28
---

## Publisher

Sacred Heart, Margaretville and its mission St. Anne's, Andes publish one weekly bulletin. I
read the 27 September 2026 issue: page 1 "SACRED HEART ROMAN CATHOLIC CHURCH", Rev. Paul J
Mijas; its Mass schedule is "Saturday 4:00 pm – St. Anne's Mission Church; Sunday 9:00 am –
Sacred Heart Church", with Thursday and Friday weekday Masses at Sacred Heart, and page 2
reports attendance and collections for "Margaretville" and "Andes" separately.

Fr. Mijas also serves Sacred Heart, Stamford and St. Philip Neri, Grand Gorge, and the two
bulletins share a template (page 2 of this issue still carries a leftover "Sacred Heart
Church/Stamford & St. Philip Neri/Grand Gorge" line). They are nonetheless two bulletins: each
has its own site, masthead, office, collections, attendance and Mass schedule, published as
separate PDFs (`MV…` and `ST…` file names in July and August). So two rows.

## Worship sites

- `churches/sacred-heart-margaretville.md`: Academy Street, Margaretville.
- `churches/st-anne-andes.md`: 375 Main Street, Andes (the diocese's "St. Ann's").

The directory's Margaretville entry lists "St. Ann's" as its other worship site, matching the
bulletin. The directory's notes (Sunday 10:00 am and 12:00 pm) are out of date against the
bulletin.

## Website and bulletin provider

sacredheartmargaretville.org is the parish's WordPress site (the directory links it; GCatholic
still has an older catskill.net/sacredheart address, not checked). Its Bulletins page links each issue as a PDF in
`wp-content/uploads/`. Self-hosted: `bulletin_provider: other`.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/sacred-heart-margaretville.json.gz`) the resolver found
https://sacredheartmargaretville.org/wp-content/uploads/2026/10/10-04-2026-1.pdf this way,
dated that week.

## Not yet confirmed

Nothing.
