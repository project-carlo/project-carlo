---
name: St. Vincent de Paul (Latin parish)
revisit: Ask the parish office (516-352-2127) or the diocese whether the Latin parish still has a public
  Mass (Sunday 8:45 AM) in the cathedral; read the June 2027 appointments list for St. Vincent de Paul,
  Elmont.
revisit_after: 2027-01-15
roster: ['gcatholic:16839', 'mass-times:church-of-st-vincent-de-paul-elmont']
evidence:
- url: https://gcatholic.org/churches/usa-02/16839
  seen: 2026-11-13
  quote: 'Using the building: St. Vincent de Paul Malankara Cathedral'
  note: 'GCatholic church 16839: St. Vincent de Paul, Elmont, Rite Roman (Latin), parish 1951, 1500 De
    Paul St., telephone +1 (516) 352-2127; no website.'
- url: https://www.drvc.org/mass-times/
  seen: 2026-11-13
  note: 'DRVC Mass Schedules by Parish, Elmont: ''Church of St. Vincent de Paul Sunday: 8:45 AM'', linking
    http://www.stvincentdepaulparish.org/public/default.aspx. The same Sunday time as the parish''s 2019
    site; the page carries many stale schedules.'
- url: https://www.drvc.org/vicariates-deaneries/
  seen: 2026-11-13
  note: The deanery list (modified 2025-10-20) still names 'St. Vincent de Paul, Elmont' between St. Boniface,
    Elmont and Our Holy Redeemer, Freeport.
- url: https://www.drvc.org/adoration-of-our-lord-in-the-blessed-sacrament/
  seen: 2026-11-13
  note: 'Undated diocesan adoration list: ''Elmont Church of St. Vincent de Paul Eucharistic Adoration
    on the first Friday of every month from 9:00 a.m. - 10:30 a.m.'''
- url: https://web.archive.org/web/20191220220822/http://www.stvincentdepaulparish.org/public/Default.aspx
  seen: 2026-11-13
  note: 'Last full snapshot of the Latin parish''s site (read with visit.py): ''Saint Vincent de Paul
    Roman Catholic Parish'', Administrator Rev. Msgr. Richard M. Figliozzi; Mass Monday, Wednesday, Friday
    8:30am; Saturday 4:00pm; Sunday 8:45am; parish office at 1510 De Paul Street. The May 2020 snapshot
    says ''NO Masses until further notice''; from June 2022 the domain redirects to a parking page, and
    on 2026-11-13 it does not resolve (DEAD-DNS).'
line1: 1500 De Paul Street
city: Elmont
state: NY
postal_code: '11003'
research:
- method: probe url on the Latin parish's domain; Wayback Machine snapshots of it
  url: http://www.stvincentdepaulparish.org/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Phone the parish office (516-352-2127) or ask the diocese whether a Latin Mass is still
    celebrated
  retry_when: A diocesan or parish source gives a current Latin Mass schedule or announces the parish's
    suppression
- method: drvc.org WordPress search for 'Vincent de Paul Elmont', 'Elmont' and 'Malankara'; GCatholic
    16839 and 5047; the cathedral's site malankaracatholiccathedral.us; St. Boniface, Elmont's 8 November
    2026 bulletin
  url: https://www.drvc.org/wp-json/wp/v2/search?search=Vincent%20de%20Paul%20Elmont
  checked: '2026-11-13'
  outcome: not-found
  next_action: Read the June 2025 and June 2026 appointment lists (image-only) for St. Vincent de Paul,
    Elmont
  retry_when: Appointment lists read, or the cathedral's site posts a schedule
- method: Read the June 24, 2026 appointments list (5 image pages, rendered by the survey) for St. Vincent
    de Paul, Elmont
  url: https://www.drvc.org/the-following-official-appointments-and-announcements-have-been-made-by-the-most-reverend-john-o-barres-bishop-o-f-rockville-centre-unless-otherwise-noted-all-are-effective-june-24-2026/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Read the June 2025 list; phone the parish office
  retry_when: A later appointments list or diocesan notice names the parish
- method: 'Reconcile: read the June 24, 2025 appointments list (8 image pages rendered by the survey,
    scratch/rockville-centre-map-1/001-survey/img/a25-*.jpg) for St. Vincent de Paul, Elmont'
  url: https://www.drvc.org/
  checked: '2026-11-13'
  outcome: not-found
  next_action: The list never names St. Vincent de Paul, Elmont. It retires Msgr. Richard M. Figliozzi
    (the Latin parish's administrator on its 2019 site) 'from Pastor of the Church of Saint Joseph, Babylon',
    so he no longer served Elmont by 2025. Phone the parish office or ask the diocese whether the Latin
    Mass continues.
  retry_when: A later appointments list or diocesan notice names the parish, or the parish office answers
---

## What is known

St. Vincent de Paul, Elmont is a Latin parish (GCatholic 16839: "Rite: Roman (Latin)", parish 1951) that GCatholic says is "Using the building: St. Vincent de Paul Malankara Cathedral" at 1500 De Paul Street; the building is the Syro-Malankara eparchy's cathedral since 2013 (excluded as `st-vincent-de-paul-malankara-cathedral-elmont`). The diocese's deanery list (modified 2025-10-20) still names "St. Vincent de Paul, Elmont", its undated adoration list gives first-Friday adoration there, and its Mass-times page gives only "Sunday: 8:45 AM".

That 8:45 AM is the Sunday Mass on the parish's own site in December 2019 (Wayback snapshot: "Saint Vincent de Paul Roman Catholic Parish", Administrator Rev. Msgr. Richard M. Figliozzi, Mass Monday, Wednesday, Friday 8:30am, Saturday 4:00pm, Sunday 8:45am). In May 2020 the site said "NO Masses until further notice"; by June 2022 the domain had lapsed to a parking page, and it no longer resolves. No current Latin Mass schedule or bulletin was found: not on drvc.org (searched for "Vincent de Paul Elmont", "Elmont", "Malankara"), not on the cathedral's site (no schedule at all), not on GCatholic, and St. Boniface, Elmont's 8 November 2026 bulletin does not mention it.

## Why it is not decided

Nothing current shows a Latin Mass here, but nothing says the parish closed or was suppressed: the diocesan Mass-times line matches the 2019 schedule and may simply be stale. Under the diocese's rule for shared buildings, the building gets a church row for the Latin parish only if it still has public Mass there. If a source shows a current Latin Mass, make a parish row (its bulletin, if any) and a church for the building with directory:68's address; if a source says the parish no longer has Mass, move this to `excluded/` (closed, with `last_mass` if given) and the cathedral record already covers the building. The steps are in `revisit`.

The June 24, 2026 appointments list (read 2026-11-13) names no priest for St. Vincent de Paul, Elmont; its only Elmont entry moves a priest's residence to St. Boniface. The June 2025 list was not read for this.

Reconcile (2026-11-13) read the June 24, 2025 list too: it does not name St. Vincent de Paul, Elmont, and it retires Msgr. Richard M. Figliozzi, the Latin parish's administrator on its 2019 site, "from Pastor of the Church of Saint Joseph, Babylon". Neither list names a priest for the Latin parish; that is absence, not a suppression notice.
