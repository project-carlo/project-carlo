---
name: St. Stanislaus and Our Mother of Sorrows Parishes
website: https://ststanserie.org/
bulletin_provider: parishes_online
provider_id: st-stanislaus-our-mother-of-sorrows-churches
publication: ['po-org:st-stanislaus-our-mother-of-sorrows-churches', 'lpi:0018000000QxBkSAAV', 'po-container:14/1710']
group: 'Erie partnership: St. Stanislaus, Our Mother of Sorrows; pastor Rev. Jason Glover'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1710/20261025B.pdf
  seen: 2026-10-23
  quote: Saint Stanislaus & Our Mother of Sorrows Catholic Churches
  note: 'Page 1 masthead of the 25 October 2026 issue (4 pages, container 14/1710): one title over both
    parishes, ''Fr. Jason A. Glover, S.T.L., Pastor'', ''Fr. Jerry Priscaro, Resident Priest (St. Ann''s)'',
    two secretaries (Helen Gangemi, Kay Villa), and one MASS TIMES box: Saturday 4:00PM and Sunday 9:00AM
    St. Stanislaus, Sunday 11:00AM St. Casimir, Monday-Friday 12:05PM and First Saturday 9:00AM St. Ann''s.
    The same page also heads the issue ''TRADITIONAL LATIN MASS APOSTOLATE AT ST. HEDWIG''S / LATIN MASS:
    Sunday at 9:30AM, Tuesday at 5:30PM''.'
- url: https://container.parishesonline.com/bulletins/14/1710/20261025B.pdf
  seen: 2026-10-23
  quote: MASSES FOR THE WEEK (Our Mother of Sorrows)
  note: 'Page 2: one table of Mass intentions for Our Mother of Sorrows (11:00am (SC) Sundays, 12:05PM
    (SA) weekdays) beside ''MASS INTENTIONS (Saint Stanislaus)'' and a combined ''SANCTUARY CANDLES''
    list for St. Stanislaus, Our Mother of Sorrows, St. Ann''s and St. Casimir''s. St. Hedwig is not in
    these tables; its Mass intentions are in the Latin Mass Community''s own bulletin (see open/st-hedwig-latin-mass-bulletin).'
- url: https://motherofsorrowerie.org/images/weeklybulletin/906f814436ab6b2c4e8e711e8cafa2b5.pdf
  seen: 2026-10-23
  quote: Saint Stanislaus & Our Mother of Sorrows Catholic Churches
  note: 'Our Mother of Sorrows'' own diocese-hosted site (weeklybulletin.php, link text ''Sunday October
    25 2026 Thirtieth Sunday in Ordinary Time'') serves a PDF byte-identical to the ParishesOnline issue:
    both 2,191,842 bytes, md5 3f37c4e349d69d939fee021cfc114112. Issues of 18 October (a641e42b...), 11
    October (f93d0d70...) and 4 October (2e55a263...) are also byte-identical between motherofsorrowerie.org
    and container 14/1710. So Our Mother of Sorrows has no bulletin of its own.'
- url: https://ststanserie.org/weeklybulletin.php
  seen: 2026-10-23
  quote: parishesonline.com/organization/st-stanislaus-our-mother-of-sorrows-churches
  note: St. Stanislaus' diocese-hosted site embeds the ParishesOnline organization st-stanislaus-our-mother-of-sorrows-churches
    (probe url also reports it as the site's publication) and its weekly-bulletin page carries no PDFs
    of its own.
- url: https://parishesonline.com/organization/st-stanislaus-our-mother-of-sorrows-churches
  seen: 2026-10-23
  note: 'probe po: title ''St. Stanislaus & Our Mother of Sorrows Churches'', LPi 0018000000QxBkSAAV,
    516 East 13th Street, Erie 16503, container 14/1710, latest issue 2026-10-25 (issues 10-25, 10-18,
    10-11, 10-04 listed).'
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE%20-%20Partnering%20Our%20Mother%20of%20Sorrows%20Erie%20and%20St.%20Stanislaus%20Erie.pdf
  seen: 2026-10-23
  quote: such that both parishes are served by one pastor
  note: 'Partnering decree, effective July 9, 2024: Our Mother of Sorrows partnered with St. Stanislaus,
    one pastor, one office, one vigil Mass.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  note: 'Clergy list ''Updated 8/7/2026'' (read via scratch/map-erie/raw/clergy_pdf.txt): Glover, Rev.
    Jason A., pastor of St. Stanislaus and Our Mother of Sorrows, Erie. Agrees with the bulletin masthead.'
research:
- method: pnpm fetch:check --diocese erie --parish st-stanislaus-erie --expected-identity "Mother of Sorrows"
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/st-stanislaus-our-mother-of-sorrows-churches
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1710, 20261025B.pdf), identity matched on page 1,
    issue date observed 2026-10-25; freshness reads future only because the Sunday issue is posted two
    days early on 2026-10-23.
---

## Publisher

St. Stanislaus and Our Mother of Sorrows (Erie) are partnered under one pastor, Rev. Jason A. Glover (decree effective 2024-07-09), and print one weekly bulletin through ParishesOnline (organization st-stanislaus-our-mother-of-sorrows-churches, container 14/1710). I read the 25 October 2026 issue on 2026-10-23: the page 1 masthead is titled 'Saint Stanislaus & Our Mother of Sorrows Catholic Churches' and gives one Mass-times box for St. Stanislaus, St. Casimir and St. Ann's; page 2 lists intentions for both parishes. Both parishes' websites point to this one bulletin: ststanserie.org embeds the ParishesOnline organization, and motherofsorrowerie.org (a diocese-hosted site with its own weeklybulletin.php) posts a PDF that is byte-identical to the container's issue, checked for the four issues of 4, 11, 18 and 25 October. So Our Mother of Sorrows (directory 10221) is folded into this row, per the one-bulletin rule; it has no bulletin of its own and no separate row.

St. Hedwig (the Latin Mass apostolate), a secondary church of St. Stanislaus, is carried as a church of this row because the combined bulletin prints its Mass times in the page 1 heading every week (orchestrator decision 2026-10-23). The Latin Mass Community also posts its own two-page bulletin at latinmasserie.org (Wix attachment the pipeline cannot read yet); a separate row is deferred, see open/st-hedwig-latin-mass-bulletin.

## Worship sites

Four churches have Mass in this bulletin's schedule: St. Stanislaus (516 E. 13th St.; Saturday 4 PM, Sunday 9 AM, weekdays by call-ahead), St. Casimir (630 Hess Ave.; Sunday 11 AM; the parish church of Our Mother of Sorrows by the 2016-17 designation decree) St. Ann (921/931 East Ave.; Monday-Friday 12:05 PM, first Saturday 9 AM) and St. Hedwig (521 E. 3rd St.; Latin Mass Sunday 9:30 AM, Tuesday 5:30 PM, listed in the page 1 heading only). Two buildings the diocese or GCatholic list are excluded as closed: Holy Family, Erie (relegated, effective 2025-12-29) and St. Mary of the Immaculate Conception (closed 2015); see their excluded/ records. The directory also carries Our Mother of Sorrows as a parish record at 630 Hess Ave. with a locator pin about 450 m south of St. Casimir (42.1356, -80.0576); it is the same place as St. Casimir (linked on the st-casimir-erie church record), not a fifth church.

## Website and bulletin provider

Website https://ststanserie.org/ (the directory's homepage for St. Stanislaus, alive, embeds the ParishesOnline organization). Provider parishes_online, provider_id and publication ids from `probe po` on 2026-10-23: po-org:st-stanislaus-our-mother-of-sorrows-churches, lpi:0018000000QxBkSAAV, po-container:14/1710. The PO organization lists website www.ststaner.org, a variant of the diocese's ststanserie.org.

## Not yet confirmed

Nothing open on identity. The directory's pastor fields disagree (locator: Rev. James T. O'Hara for St. Casimir and St. Ann, Very Rev. John Malthaner for Our Mother of Sorrows); I followed the clergy list and the bulletin masthead (Glover). The masthead's resident priest at St. Ann's, Fr. Jerry Priscaro, matches the clergy list ('Priest in Residence ... St. Ann, Erie').
