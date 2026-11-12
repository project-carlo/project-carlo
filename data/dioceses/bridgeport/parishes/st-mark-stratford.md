---
name: St. Mark
website: https://stmarkstfd.org/
bulletin_provider: parishes_online
provider_id: st-mark-church-06614
publication: ['po-org:st-mark-church-06614', 'lpi:0018000000Qc28DAAR', 'po-container:04/0152']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0152/20261115B.pdf
  seen: 2026-11-12
  note: 'Page 1 of the 15 November 2026 issue is an image (rendered with parish-site-access render.py;
    recheck cannot find text there). Masthead ''ST. MARK ROMAN CATHOLIC CHURCH''; ''Mass Schedule: Weekend
    Mass Saturday 5:00pm Vigil, Sunday 7:30am, 9:30am, 11:30am; Weekday Mass Monday through Saturday 8:00
    am''; contact ''St. Mark Roman Catholic Church, 500 Wigwam Ln, Stratford, CT 06614''; Pastor Reverend
    Reginald Norman. Names no other church.'
- url: https://container.parishesonline.com/bulletins/04/0152/20261115B.pdf
  seen: 2026-11-12
  quote: St. Mark Church, Stratford, CT 04-0152
  note: LPi ad-page footer on page 7 (text layer).
- url: https://stmarkstfd.org/bulletin/
  seen: 2026-11-12
  note: The parish site's bulletin page embeds the ParishesOnline publication widget for id 0018000000Qc28DAAR.
- url: https://parishesonline.com/organization/st-mark-church-06614
  seen: 2026-11-12
  note: 'probe po: org st-mark-church-06614, ''St. Mark Church'', 500 Wigwam Ln, Stratford 06614, container
    04/0152, latest issue 2026-11-15, weekly issues back through October.'
bulletin_status: available
---

## Publisher

St. Mark, Stratford publishes its own weekly LPi bulletin on ParishesOnline (org `st-mark-church-06614`, container 04/0152). The 15 November 2026 issue (`https://container.parishesonline.com/bulletins/04/0152/20261115B.pdf`, read 2026-11-12) has the masthead "ST. MARK Roman Catholic Church" on page 1 with its Mass schedule, Pastor Reverend Reginald Norman and "500 Wigwam Ln, Stratford, CT 06614"; it names no other parish. Pages 1-6 are images (only the ad pages 7-8 carry text), so page 1 was rendered and read by eye.

## Worship sites

- `st-mark-stratford`: the one church in the page 1 Mass schedule (Saturday 5:00pm Vigil; Sunday 7:30, 9:30, 11:30am; Monday-Saturday 8:00am). The page also lists a 24-hour Adoration Chapel, which is adoration, not a separate Mass site.

The diocese's directory (directory:1463) and GCatholic (22012) list this one church.

## Website and bulletin provider

`stmarkstfd.org` embeds the ParishesOnline widget (LPi id 0018000000Qc28DAAR); `probe po` finds weekly issues, newest 2026-11-15. Provider `parishes_online`, read by org slug. The bulletin's content pages are image-only, so the pipeline will need to read them as images.

`fetch:check` on 2026-11-12 picked `https://container.parishesonline.com/bulletins/04/0152/20261115B.pdf` (the 15 November 2026 issue; freshness `future`, the right pick mid-week; identity unverified as reported, masthead checked by hand above).

## Not yet confirmed

Nothing open.
