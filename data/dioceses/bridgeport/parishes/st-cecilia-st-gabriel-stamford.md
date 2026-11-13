---
name: Parish of St. Cecilia – St. Gabriel
website: https://stcecilia-stgabriel.org/weekly-bulletins/
bulletin_provider: parishes_online
provider_id: st-cecilia-st-gabriel-parish
publication: ['po-org:st-cecilia-st-gabriel-parish', 'lpi:0018000000QxB0OAAV', 'po-container:03/1150']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1150/20261115B.pdf
  seen: 2026-11-12
  quote: Masses at St. Gabriel Church
  note: 'Page 1 masthead of the 15 November 2026 issue (rendered and read): ''The Parish of St. Cecilia
    - St. Gabriel Roman Catholic Church'', ''St. Cecilia 1184 Newfield Ave'', ''St. Gabriel 948 Newfield
    Ave'', ''Stamford CT 06905'', ''Fr. John Connaughton, Pastor''. Masses: daily Monday-Friday 7:30 a.m.
    at St. Cecilia; St. Cecilia Saturday Vigil 5:30 p.m., Sunday 7:30, 9:00 and 11:15 a.m.; St. Gabriel
    Saturday 8:00 a.m. and Vigil 4:00 p.m. A box headed ''Notre Dame du Perpetuel Secours / St. Gabriel
    Church 203.406.0343'' lists ''French Creole Masses Saturday (Vigil Mass) 6:00 p.m. & Sunday 8:00 a.m.'',
    ''English Masses - Sunday 11:00 a.m.'' and Thursday Mass and Exposition 6:30-8:30 p.m. The text layer
    also carries a hidden 4 October masthead under the visible one.'
- url: https://stcecilia-stgabriel.org/weekly-bulletins/
  seen: 2026-11-12
  note: The parish site's Weekly Bulletins page links https://www.parishesonline.com/find/st-cecilia-st-gabriel-parish
    (found by saving the HTML with probe get --out).
- url: https://parishesonline.com/organization/st-cecilia-st-gabriel-parish
  seen: 2026-11-12
  note: 'probe po: ''St. Cecilia - St. Gabriel Parish'', 1184 Newfield Ave, Stamford, Connecticut, 06905-2597;
    LPi 0018000000QxB0OAAV, container 03/1150; latest issue 2026-11-15, weekly back to 2026-10-11.'
- url: https://bptdiocesedev.wpenginepowered.com/wp-content/uploads/2016/12/notre-dame-du-perpetuel.pdf
  seen: 2026-11-12
  note: 'The directory''s website for Notre Dame du Perpétuel Secours (directory:1435) is a one-page scanned
    flyer (image only, rendered): ''Haitian Quasi-Parish'', ''948 Newfield Ave. Stamford, Ct 06905'',
    ''Rev. Father Guy Dormevil, Moderator'', ''Office: 894 Newfield Ave.'', Mass Saturday 6:00 PM and
    Sunday 8:00 AM; its announcements are dated June-October 2022. Not a bulletin series.'
research:
- method: 'Looked for a bulletin of Notre Dame du Perpétuel Secours''s own: the directory''s website link
    (a 2022 flyer), the diocese''s directory page and mass-times API for parish_id 1435, and the host
    parish''s 15 November 2026 bulletin'
  url: https://www.bridgeportdiocese.org/parishes/notre-dame-du-perpetuel-secours-haitian-quasi-parish-stamford/
  checked: '2026-11-12'
  outcome: not-found
  next_action: If a Notre Dame du Perpétuel Secours bulletin or site with issues turns up, give it its
    own parish row with St. Gabriel's Haitian Masses
  retry_when: The diocese's directory gives the quasi-parish a website other than the 2022 flyer
bulletin_status: available
---

## Publisher

The parish publishes a weekly LPi bulletin on ParishesOnline (org `st-cecilia-st-gabriel-parish`, container 03/1150). The 15 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1150/20261115B.pdf`, read 2026-11-12; page 1 rendered because its text layer also holds a hidden 4 October masthead) has on page 1 "The Parish of St. Cecilia - St. Gabriel Roman Catholic Church", "St. Cecilia 1184 Newfield Ave", "St. Gabriel 948 Newfield Ave", "November 15, 2026" and "Fr. John Connaughton, Pastor".

## Worship sites

- `st-cecilia-stamford`: daily Masses Monday-Friday 7:30 a.m.; Saturday Vigil 5:30 p.m.; Sunday 7:30, 9:00 and 11:15 a.m.
- `st-gabriel-stamford`: Saturday 8:00 a.m. and Vigil 4:00 p.m.; and, in the page 1 box "Notre Dame du Perpetuel Secours / St. Gabriel Church", French Creole Masses Saturday 6:00 p.m. and Sunday 8:00 a.m., English Sunday 11:00 a.m., and Thursday Mass with Exposition 6:30-8:30 p.m.

**Notre Dame du Perpétuel Secours** (directory:1435, Haitian quasi-parish, moderator Rev. Guy Dormevil) is on this row under the rule settled for this diocese (a community housed at a parish's church with its own moderator is a row of its own only if it publishes its own bulletin). I found no bulletin of its own: the directory's website for it is a scanned one-page flyer whose announcements run June-October 2022, and the diocese's page gives no other link. Its Masses are printed in this parish's bulletin. The directory gives it St. Cecilia's address (1184 Newfield Avenue), but both the current bulletin and the 2022 flyer ("948 Newfield Ave.") put its Masses at St. Gabriel Church, so its roster entry is linked on `st-gabriel-stamford`. The diocese's mass-times API for parish_id 1435 gives Sunday 08:00 (Creole) and Saturday 18:00, which agrees.

The flyer gives the quasi-parish's office as 894 Newfield Ave., the address GCatholic gives for St. John Fisher Seminary (gcatholic:40356); the seminary is recorded in `open/st-john-fisher-seminary-stamford`.

The diocese's directory (directory:1443) and its mass-times roster list these two churches; GCatholic lists St. Cecilia (21962) and St. Gabriel (21964).

## Website and bulletin provider

The parish site (WordPress) has a Weekly Bulletins page that links `https://www.parishesonline.com/find/st-cecilia-st-gabriel-parish`. Provider `parishes_online`, provider_id the org slug. `probe po` (2026-11-12) lists weekly issues to 15 November 2026. Page 1 has text but carries an older masthead hidden under the current one, so read it rendered.

`fetch:check` on 2026-11-12 (headed Chrome) picked `https://container.parishesonline.com/bulletins/03/1150/20261115B.pdf`, the 15 November 2026 issue read above and the newest posted. It reported issue date `conflict` (2026-10-04 against 2026-11-15) and freshness unknown: the 4 October date comes from the hidden older masthead in page 1's text layer; the rendered page shows November 15, 2026.

## Not yet confirmed

Whether Notre Dame du Perpétuel Secours publishes anything of its own beyond the host bulletin's box (see research).
