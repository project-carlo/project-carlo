---
name: St. Ambrose Catholic Church
website: https://stambroselatham.com
bulletin_provider: parishes_online
provider_id: st-ambrose-church
publication: ['po-org:st-ambrose-church', 'lpi:0018000000Qc0EvAAJ', 'po-container:03/0807']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0807/20260927B.pdf
  seen: 2026-09-28
  quote: St. Ambrose Church, Latham, NY 03-0807
  note: 'LPi footer on the advertising pages of the 27 September 2026 issue. Pages 1-6 are images with
    no text layer; page 1 (rendered with render.py and read) is the masthead: "Saint AMBROSE Catholic
    Community ... September 27, 2026", "MASS SCHEDULE / WEEKEND MASS Saturday | 04:00pm Sunday | 09:00am,
    11:00am / WEEKDAY MASS Monday-Thursday 12:10pm", "Pastor: Reverend Brian Kelly", "St. Ambrose Catholic
    Church, 347 Old Loudon Road, Latham, NY 12110".'
- url: https://parishesonline.com/organization/st-ambrose-church
  seen: 2026-09-28
  note: '`probe po` 2026-09-28: org st-ambrose-church, 347 Old Loudon Rd, Latham, LPi 0018000000Qc0EvAAJ,
    container 03/0807, weekly issues through 2026-09-27. Found by web search.'
- url: https://discovermass.com/church/st-ambrose-latham-ny/
  seen: 2026-09-28
  note: '`issues.py discovermass` 2026-09-28: no bulletins listed.'
promoted: 2026-09-28
---

## Publisher

St. Ambrose publishes its own weekly bulletin through ParishesOnline (container 03/0807).
The 27 September 2026 issue's cover is an image: "Saint AMBROSE Catholic Community, Rooted
in Christ", pastor Reverend Brian Kelly, with one church's schedule (Saturday 4 pm, Sunday
9 and 11 am, Monday to Thursday 12:10 pm) and the contact "St. Ambrose Catholic Church, 347
Old Loudon Road, Latham". Only the advertising pages have a text layer, footed "St. Ambrose
Church, Latham, NY 03-0807".

## Worship sites

One: `st-ambrose-latham`. Catholic Central School, named on the diocese's page, is a school,
not a worship site, and is in no roster.

## Website and bulletin provider

stambroselatham.com is the parish site (named on the bulletin cover and by the diocese);
it is behind Cloudflare and stayed BLOCKED in visit.py on 2026-09-28. A web search found its
ParishesOnline organization, and `probe po` gives the ids. GCatholic's
churchofstambrose.org no longer resolves (DEAD-DNS).

**Image-only bulletin:** the masthead and schedule pages have no text layer, so the
pipeline will need to read this bulletin as images.

## Not yet confirmed

Whether stambroselatham.com's bulletin page links this organization (the site did not
load). Not needed for fetching, which goes by `provider_id`.
