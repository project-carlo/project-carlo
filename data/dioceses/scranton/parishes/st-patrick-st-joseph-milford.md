---
name: Catholic Communities of St. Joseph & St. Patrick
website: https://www.stjosephsmatamoras.com/bulletins-1.html
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stjosephsmatamoras.com/bulletins-1.html']
group: Saint Patrick Parish Milford; Saint Joseph Parish
evidence:
- url: https://nebula.wsimg.com/ca0c0f691c16a8720a72464f253cc00b?AccessKeyId=A3711114AD1870F3198A&disposition=0&alloworigin=1
  seen: 2026-10-16
  quote: The Catholic Communities of St. Joseph & St. Patrick
  note: 'Page 2 header of the 4 October 2026 issue (Twenty-Seventh Sunday in Ordinary Time), the newest
    linked on 2026-10-16. Page 1: "St. Patrick & St. Joseph", "Reverend Joseph J. Manarchuck Pastor",
    a worship schedule for both churches, and both offices (200 East High St. Milford, www.saintpatricksmilford.com;
    309 Avenue F Matamoras, www.stjosephsmatamoras.com).'
- url: https://nebula.wsimg.com/ca0c0f691c16a8720a72464f253cc00b?AccessKeyId=A3711114AD1870F3198A&disposition=0&alloworigin=1
  seen: 2026-10-16
  quote: 4:00pm (SJ)
  note: 'Page 2 intentions for 5-11 October: Masses coded (SP) St. Patrick and (SJ) St. Joseph.'
- url: https://www.stjosephsmatamoras.com/bulletins-1.html
  seen: 2026-10-16
  quote: October 4, 2026
  note: 'St. Joseph''s site, Bulletins page (GoDaddy Website Builder): one link per Sunday to a nebula.wsimg.com
    file, January to 4 October 2026, in no order.'
- url: https://www.saintpatricksmilford.com
  seen: 2026-10-16
  note: 'St. Patrick''s own site (in the finder and the bulletin) reset every connection on 2026-10-16
    (probe url: UNREACHABLE, ConnectionResetError; visit.py: ERR_CONNECTION_RESET).'
- url: https://discovermass.com/church/the-church-of-saint-patrick-milford-pa/
  seen: 2026-10-16
  note: Discover Mass pages for St. Patrick, Milford and St. Joseph, Matamoras (st-joseph-matamoras-pa)
    list no bulletins (issues.py).
promoted: 2026-10-17
---

## Publisher

St. Patrick Parish, Milford and St. Joseph Parish, Matamoras (two canonical parishes in
the finder) share a pastor, Rev. Joseph J. Manarchuck, and one weekly bulletin, "The
Catholic Communities of St. Joseph & St. Patrick". The 4 October 2026 issue (the newest
posted on 2026-10-16) gives one worship schedule for both churches on page 1, with each
parish's staff and office, and codes its intentions (SP) and (SJ). One bulletin, so one row
for both.

## Worship sites

Two: St. Patrick, Milford (`st-patrick-milford`) and St. Joseph, Matamoras
(`st-joseph-matamoras`), matching the finder. GCatholic also lists Holy Family, Millrift as
a mission of St. Joseph; the bulletin does not mention it, so it is an open question
(`open/holy-family-millrift.md`).

## Website and bulletin provider

The bulletin is posted on St. Joseph's site, whose Bulletins page links one PDF per Sunday
on GoDaddy's file host (`nebula.wsimg.com/<hash>?AccessKeyId=...`), with the date only in
the link text and the links in no particular order. St. Patrick's own site
(saintpatricksmilford.com) reset every connection here, so whether it posts the bulletin
too is unknown; the website is St. Joseph's page, which does. The PDF has a text layer. No
publisher id, so `other`. The file names carry no date, so the resolver dates each link by its text; it takes
these `nebula.wsimg.com` links as PDFs since 2026-10-17. `fetch:check` after promotion
(2026-10-17) could not load the page (`ERR_CONNECTION_RESET` from the sandbox), so no recipe
is pinned; `page-pdfs` on the website should read it.

## Not yet confirmed

Whether saintpatricksmilford.com also posts the bulletin (re-try in a browser). The
newest issue was 12 days old when read: check that the page keeps up.
