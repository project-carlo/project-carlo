---
name: St. Matthew and Corpus Christi
website: https://www.stmatthewsde.com/
bulletin_provider: parishes_online
provider_id: st-matthew-parish-and-corpus-christi
publication: ['po-org:st-matthew-parish-and-corpus-christi', 'lpi:0018000000Qx8z7AAB', 'po-container:03/1356']
group: New Castle Deanery; one bulletin, one pastor (Rev. Michael P. Darcy) and one parish office for
  both churches
evidence:
- url: https://container.parishesonline.com/bulletins/03/1356/20261025B.pdf
  seen: 2026-10-27
  quote: ST. MATTHEW & CORPUS CHRISTI PARISH OFFICES ARE LOCATED AT 901 E. NEWPORT PIKE
  note: 'Page 1 of the 25 October 2026 issue (container 03/1356): one cover with two Mass-time boxes,
    ''STM MASS TIMES'' (Tue/Thu 8:30am, Sat 5:15pm, Sun 7:00am and 9:00am) and ''CC MASS TIMES'' (Mon/Wed
    8:30am, Sat 4:00pm, Sun 8:00am and 10:30am), one staff list headed ''REV. FR. MICHAEL P. DARCY, K.
    H. S., PASTOR'' and ''REV. FR. CHRISTOPHER P. HANLEY, PAROCHIAL VICAR'', and both church addresses.'
- url: https://container.parishesonline.com/bulletins/03/1356/20261025B.pdf
  seen: 2026-10-27
  quote: ST MATTHEW CATHOLIC CHURCH  |  CORPUS CHRISTI PARISH
  note: Running head of pages 2-8; page 2 lists 'DAILY MASS INTENTIONS' under 'St. Matthew' and 'Corpus
    Christi' in one issue.
- url: https://parishesonline.com/organization/st-matthew-parish-and-corpus-christi
  seen: 2026-10-27
  note: 'probe po: org ''St. Matthew Parish and Corpus Christi'', LPi id 0018000000Qx8z7AAB, container
    03/1356, website stmatthewsde.com, address 3 Curtis Ave; weekly issues, latest 2026-10-25 (also 10-18,
    10-11, 10-04).'
- url: https://www.stmatthewsde.com/bulletin-photo-gallery
  seen: 2026-10-27
  note: 'Browser (visit.py --bulletin): the site''s ''Bulletin'' link goes to this page, which embeds
    po-org:st-matthew-parish-and-corpus-christi. Site title ''Home | St.M/CC Parishes''. The diocese map
    (directory:129 and :106) gives both parishes this website.'
---

## Publisher

One ParishesOnline (LPi) bulletin, container 03/1356, covers both churches. The 25 October 2026 issue prints a single cover with St. Matthew's and Corpus Christi's Mass times side by side, one pastor and one parochial vicar, one staff list and 'ST. MATTHEW & CORPUS CHRISTI PARISH OFFICES ARE LOCATED AT 901 E. NEWPORT PIKE'. Pages 2 onward carry the running head 'ST MATTHEW CATHOLIC CHURCH | CORPUS CHRISTI PARISH', and the Mass intentions list both churches. So the two canonical parishes are one row. This is not inferred from the shared associate in The Dialog's appointments: the masthead says it.

## Worship sites

Two churches: St. Matthew, 901 E. Newport Pike (Wilmington 19804) and Corpus Christi, 903 New Road (Wilmington 19805, the Elsmere area; the deaneries page and GCatholic say Elsmere). The bulletin prints both Mass schedules (see the churches' records).

## Website and bulletin provider

stmatthewsde.com is the parish site for both (the bulletin cover also prints corpuschristide.com e-mail addresses; www.corpuschristide.com timed out on a probe, 2026-10-27, and plays no part in the bulletin). Its Bulletin page embeds the ParishesOnline org, so the resolver reads it as `parishes_online`. GCatholic's saintmatthewsparish.org and ccparishwilmington.org are old domains (the latter a parked page, per the diocese notes).

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-matthew-corpus-christi-wilmington` (2026-10-27): resolved by the ParishesOnline org to container 03/1356, 20261025B.pdf (5.9 MB), transport ok, document type PDF, fresh (2 days; issue date read from the text 'SUNDAY, OCTOBER 25, 2026'). Identity is 'unverified' by the tool (none supplied); the masthead read above settles it.

## Not yet confirmed

Nothing outstanding.
