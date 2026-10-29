---
name: The Parish of All Saints
website: https://www.allsaintsnj.org
bulletin_provider: parishes_online
provider_id: the-parish-of-all-saints
publication: ['po-org:the-parish-of-all-saints', 'lpi:0018000000QxBFMAA3', 'po-container:03/1255']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1255/20261025B.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue, page 1 (rendered with render.py and read; pages 1-5 are images with no
    text layer, page 6 is advertising and its footer reads ''The Parish of All Saints, Millville, NJ 03-1255'').
    The cover is headed ''ALL SAINTS'' with the church drawn, Rev. Peter Idler, V.F., Pastor, and the
    address ''621 Dock St., Millville, NJ - 856-825-0021''. Holy Mass Schedule: 1st Saturday 9:00am Purgatorial
    Society Mass; Saturday 4:00pm Vigil; Sunday 8:00am and 10:30am; ''Monday through Friday - 8:00am -
    in the chapel''; Thursday Eucharistic Adoration 9am-6pm with Benediction at 6pm. Names this parish
    alone and lists no other church by name.'
- url: https://www.allsaintsnj.org/
  seen: 2026-10-29
  quote: 8AM Daily Mass is now being held in the Saint John Bosco Chapel (inside the All Saints Parish
    Building, maroon awning)
  note: 'Home page. Its Mass Schedule block: weekend Saturday Vigil 4:00PM, Sunday 8:00AM and 10:30AM;
    weekday Monday-Friday 8:00AM; 1st Saturdays 9:00AM; address 621 Dock Street, Millville, NJ 08332.
    The page''s ''Join Us'' heading names Saint John Bosco and Saint Mary Magdalen.'
- url: https://parishesonline.com/organization/the-parish-of-all-saints
  seen: 2026-10-29
  note: 'probe po 0018000000QxBFMAA3: organization ''The Parish of All Saints'', 621 Dock St, Millville,
    NJ 08332, website allsaintsnj.org, latest issue 2026-10-25 (container 03/1255); the site''s /bulletins
    page embeds publicationWidget?id=0018000000QxBFMAA3.'
- url: https://www.camdendiocese.org/decrees-establishing-st-gabriel-the-archangel-parish-and-the-parish-of-all-saints-on-oct-29/
  seen: 2026-10-29
  quote: The Parish of All Saints will be established through the merger of St. John Bosco Parish and
    St. Mary Magdalen Parish, both in Millville.
  note: 'Diocese news, 2010-10-29: ''The seat of the new parish will be St. Mary Magdalen Church''; established
    1 December 2010.'
research:
- method: pnpm fetch:check --diocese camden --parish the-parish-of-all-saints
  url: https://container.parishesonline.com/bulletins/03/1255/20261025B.pdf
  checked: '2026-10-29'
  outcome: found
  next_action: None; the pick is the 2026-10-25 issue (transport ok, PDF, fresh at 4 days). Its pages
    1-5 have no text layer, so the issue date is inferred from the URL and the identity unverified; the
    pipeline will need image reading for this bulletin.
---

## Publisher

The parish publishes its own weekly bulletin through LPi / ParishesOnline (organization `the-parish-of-all-saints`, LPi id 0018000000QxBFMAA3, container 03/1255); the parish site is a WeConnect site (footer 'WeConnect | By LPi') whose /bulletins page embeds the ParishesOnline widget. The 25 October 2026 issue (read 2026-10-29) is mostly image pages: page 1 is headed ALL SAINTS, names Rev. Peter Idler, V.F. as pastor and gives 621 Dock St., Millville, with Saturday 4:00pm vigil, Sunday 8:00am and 10:30am and Monday to Friday 8:00am 'in the chapel'. It names no other parish. The directory lists the same pastor ('Father Peter Idler') and address, and the 2026 priest assignments name no second parish for him.

## Worship sites

The parish was formed on 1 December 2010 from St. John Bosco and St. Mary Magdalen, Millville, with St. Mary Magdalen Church (621 Dock Street) as its seat (diocese decree news, 2010-10-29). Two places hold Mass now, both at 621 Dock Street: **St. Mary Magdalen Church** (weekend Masses) and the **Saint John Bosco Chapel** in the parish building, a converted classroom of the former St. Mary Magdalen Regional School, consecrated 31 January 2026 'to host the celebration of daily Mass' (Catholic Star Herald, 2026-02-05); the parish home page says the 8AM daily Mass 'is now being held' there. The bulletin's schedule says only 'in the chapel' for weekdays, and the home page links the chapel by name, so the weekday Mass is attributed to the chapel and the weekend Masses to the church; the bulletin does not say which building holds the weekend Masses, which is inferred from the church being the parish seat.

GCatholic's St. John Bosco (2 Hillcrest Ave., gcatholic:18932) is the **former parish church**, closed and sold in 2020 (Catholic Star Herald, 2026-02-05); it has an `excluded/` record. It is not the chapel, which is a new building at a different address.

## Website and bulletin provider

The directory's website, allsaintsnj.org, is current (probe url 200, 2026-10-29). GCatholic's, theparishofallsaints.org, has no DNS. ParishesOnline is the provider, read by `provider_id` (the organization slug). `fetch:check` (2026-10-29) picked the 2026-10-25 issue: transport ok, PDF, fresh (4 days).

## Not yet confirmed

Which building holds the weekend Masses (St. Mary Magdalen Church, inferred) is not stated in the bulletin. The bulletin's pages are images, so `fetch:check` reports the issue date as inferred from the file name and the publication identity as unverified; the masthead was read from a rendered page instead.
