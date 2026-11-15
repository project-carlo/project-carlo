---
name: St. Kateri Tekakwitha
revisit: 'Find whether any Mass is still held at 84 Exeter Rd.: read St. Bernard''s newest bulletin (church-bulletin.org/saint-bernard-church-north-kingstown-ri-02852)
  for a Kateri or Exeter Mass or a closing/sale notice, and retry kateritekakwitha.org and Rhode Island
  Catholic news on the 11 May 2026 suppression. A Mass in a current schedule makes it a church of st-bernard-north-kingstown
  (or of whoever lists it); a source saying Masses ended or the building closed or was sold moves it to
  excluded/ (closed, last_mass if given).'
revisit_after: 2027-01-15
roster: ['directory:12150', 'gcatholic:22365']
evidence:
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-15
  note: 'Finder entry 12150 ''St. Kateri Tekakwitha Catholic Community (canonically suppressed 05-11-26)'',
    84 Exeter Rd., Exeter, RI 02822, website https://www.stbernardnk.org/; no Mass times (other entries
    carry a ''Times'' schedule). ''05-11-26: Saint Kateri Tekakwitha Community, a quasi-parish in Exeter,
    is canonically suppressed . Limited Mass attendance and sacramental activity following the retirement
    of the community''s longtime priest-administrator, Monsignor Sabourin, necessitated the change. Sacramental
    records will be faithfully maintained at Saint Bernard Parish in North Kingstown''. Contact: St. Bernard
    Parish. Read in a browser (Cloudflare).'
- url: https://www.church-bulletin.org/bulletin/saint-bernard-church-north-kingstown-ri-02852/2026-05-17.pdf
  seen: 2026-11-15
  quote: (St. Bernard and St. Kateri)
  note: '17 May 2026 St. Bernard bulletin: the Mass schedule lists St. Bernard only; St. Kateri appears
    only in ''2026 St. Bernard Award / The SPRED Program Volunteers (St. Bernard and St. Kateri)''. The
    15 November 2026 issue''s schedule (page 1, image) also lists only St. Bernard.'
- url: https://gcatholic.org/churches/usa-01/22365
  seen: 2026-11-15
  note: 'GCatholic 22365: Saint Kateri Tekakwitha (Community), 84 Exeter Rd., Exeter, Rhode Island 02822,
    Plus Code 87HCGFWF+33, website http://www.kateritekakwitha.org/katerichurch.'
parish: st-bernard-north-kingstown
line1: 84 Exeter Rd.
city: Exeter
state: RI
postal_code: 02822
research:
- method: probe url on GCatholic's website for 22365 (http://www.kateritekakwitha.org/katerichurch, https://www.kateritekakwitha.org,
    https://kateritekakwitha.org/)
  url: http://www.kateritekakwitha.org/katerichurch
  checked: '2026-11-15'
  outcome: access-blocked
  next_action: Retry probe url / visit.py on kateritekakwitha.org
  retry_when: The site answers (timed out at the egress proxy on 2026-11-15)
- method: Text grep of St. Bernard bulletins 10, 17, 24 May, 7 June and 8 November 2026 for Kateri, Exeter,
    Sabourin; render of 15 November 2026 page 1 Mass schedule
  url: https://www.church-bulletin.org/saint-bernard-church-north-kingstown-ri-02852
  checked: '2026-11-15'
  outcome: not-found
  next_action: Read the newest St. Bernard bulletin for any Exeter Mass or a statement on the building
  retry_when: A new St. Bernard issue, or a diocesan or news source on the Exeter building, appears
---

## What is known

St. Kateri Tekakwitha, 84 Exeter Rd., Exeter was a quasi-parish (mission 1981, quasi-parish 2008). The diocese's finder (entry 12150, read 2026-11-15) says it was "canonically suppressed" on 11 May 2026 because of "Limited Mass attendance and sacramental activity following the retirement of the community's longtime priest-administrator, Monsignor Sabourin", that its records are kept at St. Bernard, North Kingstown, and it gives St. Bernard as the contact and website. The entry carries no Mass times. St. Bernard's bulletin lists only St. Bernard's own Masses, in the 17 May 2026 issue (text) and the 15 November 2026 issue (page 1, image); St. Kateri appears in May only as a partner in St. Bernard's SPRED program. The community's own site (kateritekakwitha.org, from GCatholic 22365) did not answer on 2026-11-15.

## Why it is not decided

Nothing read shows a Mass at the Exeter building now, but nothing says Masses there ended or the building closed: the decree suppresses the quasi-parish (a canonical act), and absence from St. Bernard's schedule is only absence. Under the README an exclusion needs a source that states the fact, so this stays open. See `revisit` for what would settle it.
