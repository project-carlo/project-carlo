---
name: St. Kateri Tekakwitha Parish
website: https://stkateriparish.org
bulletin_provider: discover_mass
provider_id: st-kateri-tekakwitha-parish-schenectady-ny
publication: ['discovermass:st-kateri-tekakwitha-parish-schenectady-ny', 'discovermass:st-helen-schenectady-ny',
  'ecatholic:15529']
group: ''
evidence:
- url: https://discovermass.com/church/st-kateri-tekakwitha-parish-schenectady-ny/
  seen: 2026-09-28
  quote: 'Parish Office: 2216 Rosa Road,S chenectady'
  note: 'Page 1 of the 27 September 2026 issue (Discover Mass lists it by date). The PDF''s text layer
    splits words (''UnionS treet''); quotes are copied as extracted. Page 1 lists ''Union Street Church:
    1803 Union Street'' and ''Rosa Road Church: 2216 Rosa Road'' with the Mass schedule of each.'
- url: https://discovermass.com/church/st-kateri-tekakwitha-parish-schenectady-ny/
  seen: 2026-09-28
  quote: Very Rev. Robert Longobucco,V .G., Pastor
  note: 27 September 2026 issue, page 1.
- url: https://discovermass.com/church/st-helen-schenectady-ny/
  seen: 2026-09-28
  note: A second Discover Mass listing (titled 'Saint Kateri Tekawitha Parish', slug from the former St.
    Helen's) serves the same 27 September 2026 issue, same page 1 text (issues.py, 2026-09-28).
- url: https://stkateriparish.org/bulletins
  seen: 2026-09-28
  note: eCatholic site, behind Cloudflare; read in a browser (parish-site-access visit.py) on 2026-09-28.
    Embeds ecatholic:15529; its archive listed issues only through 13 September 2026 (files.ecatholic.com/15529/bulletins/20260920.pdf
    and 20260927.pdf answered 403), while Discover Mass had 27 September.
---

## Publisher

St. Kateri Tekakwitha Parish (GCatholic dates it 2012), which joined St. Helen's (Union Street) and Our Lady of
Fatima (Rosa Road), publishes one weekly bulletin for both churches. The 27 September 2026
issue (Discover Mass) page 1 gives the parish office at 2216 Rosa Road, pastor Very Rev.
Robert Longobucco, and two church columns: the Union Street church, 1803 Union Street
(Saturday 5 pm, Sunday 9:30 am, Monday and Tuesday 9 am) and the Rosa Road church, 2216
Rosa Road (Sunday 11:30 am, Thursday 6 pm, Friday 9 am). The same schedule is on the diocese
directory page.

## Worship sites

Two: `st-kateri-tekakwitha-union-street-niskayuna` and `st-kateri-tekakwitha-rosa-road-schenectady`.
The directory has one entry for the parish ("Union Street & Rosa Rd", directory:436, linked
to the Union Street church); GCatholic has one per church. The school at 1801 Union Street is
not a worship site. The Schenectady County Historical Society's church list names the
Union Street church "formerly St. Helen's" and Our Lady of Fatima, 2216 Rosa Road, "now
St. Kateri Tekakwitha Parish"; the records index agrees (Our Lady of Fatima and St. Helen's
records at St. Kateri).

## Website and bulletin provider

stkateriparish.org is an eCatholic site behind Cloudflare (`probe url` HTTP4XX; visit.py
loaded it on the second run). It posts the bulletin as `ecatholic:15529`, but two weeks
behind: its archive stopped at 13 September on 2026-09-28. Discover Mass carries the same
bulletin current to 27 September under two church slugs, so `bulletin_provider:
discover_mass` with the parish-named slug as `provider_id`; all three ids are recorded as
`publication`.

## Not yet confirmed

Whether the eCatholic archive catches up; if Discover Mass stops, switch to `ecatholic`
with the eCatholic site as `website`.
