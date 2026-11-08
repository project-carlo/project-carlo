---
name: St. Joseph
website: https://sjmillstone.com
bulletin_provider: other
provider_id: page-pdfs https://sjmillstone.com/bulletins-and-reflections filename=068d_*.pdf
publication: ['url:https://sjmillstone.com/bulletins-and-reflections']
group: ''
evidence:
- url: https://sjmillstone.com/s/068d_2026_11_08.pdf
  seen: 2026-11-02
  quote: 34 Yorktown Road
  note: 'Page 1 of the 8 November 2026 issue (8 pages): ''PARISH COMMUNITY OF Saint Joseph HILLSBOROUGH,
    NEW JERSEY ... NOVEMBER 8, 2026'', ''Web: https://sjmillstone.com'', ''Fr. Hank: fatherhank@sjmillstone.com'',
    ''Address: 34 Yorktown Road Hillsborough, NJ 08844'', MASS SCHEDULE ''Saturday Vigil 4:45 PM; Sunday
    8:00 AM, 9:30 AM, 11:30 AM; Monday-Friday 8:35 AM; Holyday Vigil 7:00 PM; Holyday 8:35 AM & 5:00 PM''.
    Names no other church; no publisher code or ad pages (parish-produced).'
- url: https://sjmillstone.com/bulletins-and-reflections
  seen: 2026-11-02
  quote: Bulletins
  note: 'Squarespace ''Bulletins'' page links the issues newest first: /s/068d_2026_11_08.pdf, 068d_2026_11_01.pdf,
    068d_2026_10_25-1.pdf, 068d_2026_10_18.pdf ... Its first PDF link is an unrelated flyer (/s/Helpful-Sites-for-economic-stress-kcnf.pdf),
    hence the filename filter.'
- url: https://sjmillstone.com/
  seen: 2026-11-02
  quote: 34 Yorktown Road • Millstone Borough Hillsborough, NJ 08844
  note: Footer of the parish site, '© 2026, St. Joseph Parish'. The finder's website http://www.stjosephsparish.com
    redirects here.
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

St. Joseph, 34 Yorktown Road (Borough of Millstone, Hillsborough mailing address), publishes its own weekly bulletin, produced by the parish and posted on its Squarespace site. Page 1 of the 8 November 2026 issue (read 2026-11-02) is headed 'PARISH COMMUNITY OF Saint Joseph HILLSBOROUGH, NEW JERSEY ... NOVEMBER 8, 2026', gives 'Fr. Hank' (fatherhank@sjmillstone.com) as the priest contact and the address '34 Yorktown Road Hillsborough, NJ 08844', and names no other church. The finder lists 'Pastor: Rev. Francis Hilton'; the bulletin calls him only 'Fr. Hank', and I did not find his surname on the site.

The earlier lead (whether Mary, Mother of God shares this bulletin) is answered no: Mary, Mother of God's 1 November 2026 Bon Venture bulletin names only its own church and clergy (Msgr. Joseph Curry), and this bulletin names only St. Joseph. The two rows have different websites and publication ids.

## Worship sites

One church, 34 Yorktown Road (directory:24497, gcatholic:18665). The masthead schedule (Saturday 4:45 pm; Sunday 8:00, 9:30, 11:30 am; Monday to Friday 8:35 am) and the site's Mass Schedule page (read 2026-11-02) name only this church; the summer 11:30 am Mass is held under the parish pavilion on the same grounds, with an in-car congregation in the parking lot.

## Website and bulletin provider

The finder and GCatholic give http://www.stjosephsparish.com, which redirects to https://sjmillstone.com (the site's footer: '© 2026, St. Joseph Parish, 34 Yorktown Road • Millstone Borough Hillsborough'). The bulletin is self-hosted: provider `other` with `page-pdfs https://sjmillstone.com/bulletins-and-reflections filename=068d_*.pdf`; the filter skips a flyer PDF linked above the bulletins. The page is newest first.

## Not yet confirmed

The pastor's full name: the bulletin says 'Fr. Hank'; the finder says Rev. Francis Hilton. Nothing about identity or the Mass schedule depends on it.

## Fetch check

`pnpm fetch:check` on 2026-11-02 (Eastern) resolved `page-pdfs https://sjmillstone.com/bulletins-and-reflections` with the filename filter and picked the 8 November 2026 issue (`/s/068d_2026_11_08.pdf`, 1.3 MB PDF): transport ok, freshness `future` (the parish posts the coming Sunday early). Identity isn't checked by the tool; I read the masthead myself (above). No `recipe` line was printed, so the pinned recipe stays.
