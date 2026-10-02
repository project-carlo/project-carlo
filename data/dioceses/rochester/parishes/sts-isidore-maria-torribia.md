---
name: Ss. Isidore & Maria Torribia Parish
website: https://simtparish.org
bulletin_provider: parishes_online
provider_id: sts-isidore-maria-torribia-parish
publication:
- po-org:sts-isidore-maria-torribia-parish
- lpi:0018000000Qx7QSAAZ
- po-container:04/0677
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0677/20261004B.pdf
  seen: '2026-10-02'
  quote: Sts. Isadore & Maria Torribia Parish, Addison, NY 04-0677
  note: '4 October 2026 issue, page 4 (the only page with a text layer): LPi container 04-0677 (spelled "Isadore"
    there). Pages 1-3 are images.'
- url: https://container.parishesonline.com/bulletins/04/0677/20260927B.pdf
  seen: '2026-10-02'
  note: '27 September 2026 issue, page 1 (image, read with render.py): "Saints Isidore & Maria Torribia Parish SEPTEMBER
    27, 2026 - TWENTY-SIXTH SUNDAY IN ORDINARY TIME". Mass Schedule: "St. Catherine of Siena Church (Parish Office)
    Sunday 9:00 AM Tuesday 9:00 AM; St. Stanislaus, Bishop & Martyr Church Sunday 11:30 AM Friday 4:30 PM; St. Joseph
    the Carpenter Church Monday 5:30 PM Saturday 4:00 PM". Footer: "ST. STANISLAUS ... 7646 Whitehead Hill Rd. Bradford,
    NY", "ST. CATHERINE OF SIENA 51 Maple St. Addison, NY 14801", "ST. JOSEPH THE CARPENTER 8508 Main Street Campbell,
    NY".'
- url: https://www.simtparish.org/schedules/bulletin/
  seen: '2026-10-02'
  quote: Weekly Bulletin Available for Download
  note: The parish's bulletin page embeds the ParishesOnline publication links; visit.py reports lpi:0018000000Qx7QSAAZ
    and po-container:04/0677 on it. `probe po sts-isidore-maria-torribia-parish` gives the org slug and the same
    ids, weekly issues through 2026-10-04.
- url: https://www.simtparish.org/
  seen: '2026-10-02'
  quote: 'MASS SCHEDULE FOR ST. STANISLAUS, BISHOP & MARTYR Sunday: 11:30 a.m. Friday: 4:30 p.m.'
  note: Parish home page, Regular Parish Mass Schedule (also St. Catherine Sunday and Tuesday 9:00 a.m., St. Joseph
    Monday 5:30 p.m. and Saturday 4:00 p.m.).
- url: https://ps.dor.org/directory/ss-isidore-maria-torribia/
  seen: '2026-10-02'
  quote: Ss. Isidore & Maria Torribia, a multi-site parish, Addison, New York, Steuben County
- url: https://www.dor.org/learning-and-living-your-faith/sacraments/sacramental-records/
  seen: '2026-10-02'
  note: 'Sacramental-records index: St. Catherine of Siena (Addison), St. Joseph (Campbell), St. Stanislaus (Bradford)
    and St. William (Cameron Mills) keep records at Ss. Isidore & Maria Torribia, Addison.'
promoted: 2026-10-02
---

## Publisher

Saints Isidore & Maria Torribia Parish, Addison, publishes one weekly bulletin on ParishesOnline (container 04/0677) covering three churches. The 27 September 2026 masthead (an image page) is "Saints Isidore & Maria Torribia Parish" and its Mass Schedule lists St. Catherine of Siena, St. Stanislaus Bishop & Martyr and St. Joseph the Carpenter. One row; the diocese groups nothing else with it. The Locator's address spelling "Ss. Isidore & Maria Torriba" is a typo for the same parish.

## Worship sites

Three, all in the bulletin: `st-catherine-of-siena-addison` (Sunday 9:00, Tuesday 9:00), `st-stanislaus-bishop-martyr` (Bradford: Sunday 11:30, Friday 4:30) and `st-joseph-carpenter` (Campbell: Saturday 4:00, Monday 5:30). Not here: St. William, Cameron Mills, which the sacramental index lists as merged and which is on no schedule (no closure source sought). The diocese directory and Locator show older times (St. Catherine Saturday 6:00 pm; St. Stanislaus Friday 5:30 pm).

## Website and bulletin provider

simtparish.org redirects to www.simtparish.org (an abcparishes.org-era WordPress site); its Weekly Bulletin page embeds the ParishesOnline widget, so `provider_id: sts-isidore-maria-torribia-parish` (the live value) is right and `publication` holds the three forms. **The bulletin's pages 1-3 are images** (page 4, the ad page, has text), so the pipeline needs to read them as images. The GCatholic and Locator website abcparishes.org is the parish's old domain.

## Not yet confirmed

Nothing.
