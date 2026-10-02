---
name: St. John Vianney
website: https://sjvbath.org
bulletin_provider: other
provider_id: ''
publication:
- url:https://www.sjvbath.org/bulletin-2/
- url:https://www.sjvbath.org/bulletin-3/
group: ''
evidence:
- url: https://www.sjvbath.org/wp-content/uploads/Sept-27th-26th-Sun-in-OT.pdf
  seen: '2026-10-02'
  note: '27 September 2026 issue, an image-only PDF (4 pages, no text layer; read with render.py; recheck cannot
    search it). Page 1: "St. John Vianney Parish 26th Sunday in Ordinary Time ... September 27th, 2026 ... Celebrations
    of the Lord''s Day Saturday 4:00 pm at St. Mary''s Church; Sunday 8:30 am at St. Gabriel''s Church, 10:30 am
    at St. Mary''s Church", "St. Mary''s Church 32 East Morris St. Bath, NY 14810", "St. Gabriel''s Church 78 Shethar
    St. Hammondsport, NY 14840", "Phone 607-776-3327".'
- url: https://www.sjvbath.org/
  seen: '2026-10-02'
  quote: Welcome to the Parish of St. John Vianney home of St. Mary's Church in Bath, NY & St. Gabriel's Church
    in Hammondsport, NY.
  note: Parish home page, 2 October 2026.
- url: https://www.sjvbath.org/bulletin-2/
  seen: '2026-10-02'
  note: 'Bulletin archive page (linked from the home page): one PDF per Sunday, e.g. /wp-content/uploads/Oct.-4th-27th-Sun-in-OT.pdf,
    Sept-27th-26th-Sun-in-OT.pdf, back to June 2026. The home page also links /bulletin-3/ (latest issue only).
    No publisher id: self-hosted.'
- url: https://ps.dor.org/directory/st-john-vianney/
  seen: '2026-10-02'
  quote: St. John Vianney, a multi-site parish, Bath NY, Steuben County
- url: https://www.dor.org/learning-and-living-your-faith/sacraments/sacramental-records/
  seen: '2026-10-02'
  note: 'Sacramental-records index: St. Gabriel (Hammondsport) and St. Mary (Bath) keep records at St. John Vianney,
    Bath.'
promoted: 2026-10-02
---

## Publisher

St. John Vianney Parish (Bath and Hammondsport) publishes its own weekly bulletin as a PDF on sjvbath.org. The 27 September 2026 issue is headed "St. John Vianney Parish" and lists Masses at St. Mary's (Bath) and St. Gabriel's (Hammondsport). One row; the diocese groups nothing else with it. (GCatholic and the Locator also use the older sjv2012.org site name; not used.)

## Worship sites

Two: `st-marys-bath` (Saturday 4:00 pm, Sunday 10:30 am, Monday and Thursday 11:00 am) and `st-gabriels` (Hammondsport: Sunday 8:30 am, Tuesday and Friday 11:00 am). Nothing else is listed by the bulletin, the site or the diocese directory.

## Website and bulletin provider

www.sjvbath.org is a live WordPress site; its Bulletin menu links two pages (`/bulletin-2/`, the archive, and `/bulletin-3/`, the latest issue) that list the PDFs, so `bulletin_provider: other` with both pages as `url:` publications and no provider_id. **The PDFs are image-only** (no text layer): the pipeline will have to read them as images.

## Not yet confirmed

Whether the 10:30 am Sunday time at Bath is permanent: the diocese directory and Locator say 10:00 am (older), the parish page and bulletin say 10:30.
