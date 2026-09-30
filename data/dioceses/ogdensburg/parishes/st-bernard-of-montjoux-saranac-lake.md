---
name: St. Bernard of Montjoux Parish
website: https://stbernards.church
bulletin_provider: parishes_online
provider_id: st-bernard-of-montjoux
publication: ['po-org:st-bernard-of-montjoux', 'lpi:0018000000Qc0FAAAZ', 'po-container:06/0140']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0140/20260927B.pdf
  seen: 2026-09-30
  quote: For ad info. call 1-800-950-9952 www.4lpi.com St. Bernard of Montjoux, Saranac Lake, NY 06-0140
  note: 'Page 5 (ad page, the only page with a text layer) of the 27 September 2026 issue, naming the container 06-0140. Pages 1-4 are scanned images, read with parish-site-access render.py: page 1 masthead "St. Bernard of Montjoux Parish, September 27, 2026", "St. Bernard''s Church, 27 St. Bernard''s St. Saranac Lake, NY 12983" and "Church of the Assumption, 826 State Rt. 86, Gabriels, NY", Pastor Father Martin E. Cline.'
- url: https://container.parishesonline.com/bulletins/06/0140/20260927B.pdf
  seen: 2026-09-30
  note: 'Image-only page 4 (Mass intentions and "Sunday Liturgies"): "4:30 p.m. (Anticipated) - St. Bernard''s; 8:00 a.m. - Church of the Assumption; 10:00 a.m. - St. Bernard''s. Weekday Masses: Mon. - no scheduled Mass, Wed. & Fri. - 8:30 a.m., Tues. & Thurs. - 12:00 p.m. - St. Bernard''s". recheck cannot find text from this page.'
- url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/organizations/slug/st-bernard-of-montjoux
  seen: 2026-09-30
  quote: '"slug":"st-bernard-of-montjoux"'
  note: 'ParishesOnline organization (probe po st-bernard-of-montjoux): LPi id 0018000000Qc0FAAAZ, website https://stbernards.church, address 27 Saint Bernard St, Saranac Lake 12983-1834; latest issue 2026-09-27 in container 06/0140. The 4 October 2026 issue (20261004B.pdf) was already posted on 2026-09-30.'
- url: https://www.rcdony.org/parish/saranac-lake
  seen: 2026-09-30
  quote: 'Worship sites: Church of the Assumption - Gabriels'
  note: 'Directory: "St. Bernard''s Church, 27 St. Bernard Street, Saranac Lake" and "Church of the Assumption, 826 State Route 86, Gabriels", both with website www.stbernards.church, telephone 518-891-4616, pastor Reverend Martin E. Cline.'
---

## Publisher

St. Bernard of Montjoux Parish, Saranac Lake publishes its own weekly ParishesOnline (LPi)
bulletin, container 06/0140, organization slug `st-bernard-of-montjoux`. The 27 September
2026 issue's masthead (page 1, an image) reads "St. Bernard of Montjoux Parish" and shows both
"St. Bernard's Church, 27 St. Bernard's St. Saranac Lake, NY 12983" and "Church of the
Assumption, 826 State Rt. 86, Gabriels, NY". Page 4's Mass intentions and "Sunday Liturgies"
list Masses at both. The diocese's directory groups the same two sites under one parish
("Worship sites: Church of the Assumption - Gabriels"), so the directory, the bulletin and
the ParishesOnline organization agree: **one row, two churches**. Container 06/0140 answered 200 for every
sampled Sunday from March to October 2026 (probe container --all --step 4), so it is not a
stale account.

## Worship sites

Two: St. Bernard's, Saranac Lake (`st-bernards-saranac-lake`; Saturday 4:30 PM, Sunday 10:00
AM, weekdays per the bulletin) and the Church of the Assumption, Gabriels
(`assumption-gabriels`; Sunday 8:00 AM only). Not worship sites, ruled out:

- **St. Paul's, Bloomingdale** (GCatholic 18238): last regular Mass early 2016, oratory, sold
  after a final liturgy in April 2023 (`excluded/st-pauls-bloomingdale`).
- **St. John in the Wilderness, Lake Clear** (GCatholic 18289): weekly Masses ended in 2015,
  oratory, sold in 2021 (`excluded/st-john-in-the-wilderness-lake-clear`).

Both were missions of St. Bernard's and appear in no directory entry for this parish nor in the
bulletin's schedule. The parish also runs St. Bernard's School (63 River St.), not a worship
site.

## Website and bulletin provider

`stbernards.church` is the directory's website and the diocesan Parish Bulletins page's link
(`/bulletin`). On 2026-09-30 it did not load: a browser got HTTP 502 ("upstream request
failed") on `/`, `/bulletin` and `www.`, WebFetch got 503, and curl reports an expired TLS
certificate, with the host resolving to two AWS addresses. The page could therefore not be
read; the bulletin was found through ParishesOnline instead (a web search returned
container 06/0140; the organization slug was found by trying `st-bernard-of-montjoux` on the
ParishesOnline API, whose `website` field is `https://stbernards.church`, and which holds the
same address as the directory). The parish website is kept as `website` because it is the
directory's and ParishesOnline's own link; if the domain stays down the row may need
`https://parishesonline.com/organization/st-bernard-of-montjoux`. Pages 1-4 of each of the three
September 2026 issues read (13, 20, 27) are scanned images, so the pipeline will need to read them as images.

## Not yet confirmed

- Whether `stbernards.church` comes back (revisit; the parish's Facebook page was not read).
- Weekday Mass times beyond the 27 September issue's (Wednesday and Friday 8:30 AM, Tuesday and
  Thursday 12:00 PM, none Monday); other issues were not read for a schedule change.
