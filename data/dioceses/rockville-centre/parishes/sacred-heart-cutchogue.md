---
name: Sacred Heart
website: https://www.sacredheartolgc.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['po-container:03/4112']
group: North Fork (Fr. Bartholomew)
evidence:
- url: https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file
  seen: 2026-11-13
  note: 'November 15, 2026 issue on the parish''s Solutio site (downloaded through Chrome; a 12-page scan,
    Creator ''Canon iR-ADV C5840 PDF'', no text layer: read by rendering). Page 2 masthead ''SACRED HEART
    PARISH / OUR LADY OF GOOD COUNSEL CHURCH, MATTITUCK'', ''NOVEMBER 15, 2026'', Mass schedule Saturday
    5:00 pm, Sunday 8:00 am and 10:00 am, weekdays 09:00am Monday-Wednesday and Friday, ''Thursday No
    Mass''; footer ''14300 Main Rd, Mattituck, NY 11952 | www.sacredheartolgc.org''. Page 3: ''REV. MIKE
    BARTHOLOMEW, PASTOR''. Page 12 footer: ''www.4lpi.com Sacred Heart Parish, Our Lady of Good Counsel
    Church 03-4112''.'
- url: https://www.sacredheartolgc.org/
  seen: 2026-11-13
  quote: '** all Masses are at Our Lady of Good Counsel, Mattituck'
  note: 'Home page read with visit.py (probe url gets 403): weekend Mass Saturdays 5:00pm, Sundays 8:00am,
    10:00am; daily Mon/Tues/Wed/Fri 9:00am; footer ''Rectory Office: 3000 Depot Lane, Cutchogue, NY 11935
    | Mailing: P.O. Box 926, Cutchogue, NY 11935 / Our Lady of Good Counsel Church:14300 Main Rd, Mattituck,
    NY 11952''.'
- url: https://container.parishesonline.com/bulletins/03/4112/20261115B.pdf
  seen: 2026-11-13
  note: 'LPi container 03/4112 (from the page 12 footer) is live: probe container finds the 2026-11-15
    issue (HTTP 200).'
research:
- method: 'Looked for the ParishesOnline organization of container 03/4112 so fetch can read it: probe
    po on sacred-heart-parish-our-lady-of-good-counsel-church (with -11935 and -11952), sacred-heart-11935,
    sacred-heart-11952, sacred-heart-parish-11935, sacred-heart-parish-11952, sacred-heart-church-11935,
    sacred-heart-church-11952, sacred-heart-rc-church-11935, sacred-heart-r-c-church-11935, sacred-heart-roman-catholic-church-11935,
    sacred-heart-cutchogue, sacred-heart-church-cutchogue, sacred-heart-parish-cutchogue, our-lady-of-good-counsel-11952,
    our-lady-of-good-counsel-church-11952 (none exist; sacred-heart-parish and sacred-heart-roman-catholic-church
    are other states'' parishes); a DuckDuckGo search; the site embeds no LPi id'
  url: https://container.parishesonline.com/bulletins/03/4112/20261115B.pdf
  checked: '2026-11-13'
  outcome: not-found
  next_action: Find the org slug or LPi id (a 4lpi.com or parishesonline.com link on the parish site or
    social pages, or the ParishesOnline church search in a browser), then set bulletin_provider parishes_online
    with that provider_id and run fetch:check
  retry_when: A ParishesOnline org page or LPi id for Sacred Heart, Cutchogue/Mattituck turns up, or fetch
    gains a container collector
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (run as provider other via tools/fc_unsupported.sh)
    found the 15 November post but failed: ''No PDF links found on bulletin page: .../823-lpi-bulletin-11-15-2026-web/file''
    (the /file URL is the PDF, a scan, and answers 403 outside a browser). The same bulletin is in LPi
    container 03/4112 (20261115B.pdf live), but no ParishesOnline org slug was found, and fetch reads
    ParishesOnline only by org slug.'
  url: https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file
publication_reviews:
- parish: our-lady-of-ostrabrama-cutchogue
  decision: separate
  evidence:
  - url: https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file
    seen: 2026-11-13
    note: The 15 November 2026 masthead (page 2) names Sacred Heart Parish, Our Lady of Good Counsel Church,
      Mattituck alone, LPi 03-4112, with its own Mass times (Saturday 5:00, Sunday 8:00 and 10:00).
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-ostrabrama-roman-catholic-church-cutchogue-ny-11935/2026-11-15.pdf
    seen: 2026-11-13
    note: The 15 November 2026 masthead names Our Lady of Ostrabrama Roman Catholic Church, 3000 Depot
      Lane, Cutchogue alone; the issue is John Patrick job 4037 with its own Mass times (Sunday 8:00,
      9:30 Polish, 11:00).
- parish: st-agnes-greenport
  decision: separate
  evidence:
  - url: https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file
    seen: 2026-11-13
    note: The 15 November 2026 masthead (page 2) names Sacred Heart Parish, Our Lady of Good Counsel Church,
      Mattituck alone, LPi 03-4112, with its own Mass times (Saturday 5:00, Sunday 8:00 and 10:00).
  - url: https://container.parishesonline.com/bulletins/03/4114/20261115B.pdf
    seen: 2026-11-13
    note: The 15 November 2026 masthead names the Church of Saint Agnes, 523 Front Street, Greenport alone,
      LPi 03-4114, with its own Mass times (Saturday 4:00 and 7:30 Spanish, Sunday 8:00 and 10:00).
- parish: st-patrick-southold
  decision: separate
  evidence:
  - url: https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file
    seen: 2026-11-13
    note: The 15 November 2026 masthead (page 2) names Sacred Heart Parish, Our Lady of Good Counsel Church,
      Mattituck alone, LPi 03-4112, with its own Mass times (Saturday 5:00, Sunday 8:00 and 10:00).
  - url: https://container.parishesonline.com/bulletins/03/4110/20261115B.pdf
    seen: 2026-11-13
    note: The 15 November 2026 masthead names St. Patrick Church, 52125 Main Road, Southold alone, LPi
      03-4110, with its own Mass times (Saturday 5 pm, Sunday 8 and 10 am).
---

## Publisher

Sacred Heart Parish (canonically of Cutchogue; its Masses are at Our Lady of Good Counsel, 14300 Main Road, Mattituck) publishes its own weekly bulletin, printed by LPi (page 12 footer "www.4lpi.com Sacred Heart Parish, Our Lady of Good Counsel Church 03-4112"). The November 15, 2026 issue on the parish site (`https://www.sacredheartolgc.org/news/bulletin/823-lpi-bulletin-11-15-2026-web/file`, read 2026-11-13 by rendering: it is a scan with no text) has, after LPi's cover, the page 2 masthead "SACRED HEART PARISH / OUR LADY OF GOOD COUNSEL CHURCH, MATTITUCK" and one Mass schedule: Saturday 5:00 pm; Sunday 8:00 am and 10:00 am; weekdays 9:00am Monday, Tuesday, Wednesday and Friday ("Thursday No Mass"). Page 3 names "REV. MIKE BARTHOLOMEW, PASTOR" and a retired priest in residence; no associate is listed.

Fr. Bartholomew is also pastor of Our Lady of Ostrabrama (Cutchogue), St. Agnes (Greenport) and St. Patrick (Southold). Their bulletins are separate: Ostrabrama's is John Patrick job 4037, St. Patrick's is LPi 03-4110, St. Agnes's is parish-made, and each masthead names one parish (see `publication_reviews`).

## Worship sites

One: Our Lady of Good Counsel, 14300 Main Road, Mattituck (`our-lady-of-good-counsel-mattituck-church`). The parish home page says "** all Masses are at Our Lady of Good Counsel, Mattituck" (2026-11-13), and the livestream list shows every Mass there.

Ruled out: the Sacred Heart church building, Main Road, Cutchogue, which the diocesan locator (directory:104), GCatholic (16830) and the Mass-times page still list. It closed at the end of December 2012 (Suffolk Times, 6 December 2012; Newsday's report of the final Mass, 23 December 2012): `excluded/sacred-heart-cutchogue-church.md`. The rectory office address on the site, 3000 Depot Lane, Cutchogue, is Our Lady of Ostrabrama's.

## Website and bulletin provider

sacredheartolgc.org is a Solutio (Joomla) site (the diocesan locator wrongly links sacredheartnm.org, North Merrick's site; the Mass-times page links sacredheartolgc.org). Its `/news/bulletin` list links `/news/bulletin/<n>-lpi-bulletin-<m>-<d>-<yyyy>-web/file`, which answers 403 outside a browser. Following the diocese's settled rule, the printer's listing was looked for first: LPi container 03/4112 is live, but no ParishesOnline organization for it was found (see `research`), and fetch reads ParishesOnline only by org slug. The row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, keeping `po-container:03/4112`. The parish's copies are scans with no text layer.

## Not yet confirmed

The ParishesOnline org slug and LPi id for container 03/4112. With either, set `bulletin_provider: parishes_online`, run fetch:check and clear `fetch_gap`.
