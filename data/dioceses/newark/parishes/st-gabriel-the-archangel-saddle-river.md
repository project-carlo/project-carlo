---
name: St. Gabriel the Archangel, Saddle River
website: https://www.stgabrielsr.org/index.php?page=mass
bulletin_provider: other
provider_id: page-pdfs https://www.stgabrielsr.org/index.php?page=mass
publication: ['po-container:03/0374']
group: ''
evidence:
- url: https://www.stgabrielsr.org/_content/sidebar/mass/2026-11-01%20Bulletin.pdf
  seen: 2026-11-03
  note: 'Page 1 of the 1 November 2026 issue (6 pages; pages 1-4 image only, read rendered with parish-site-access
    render.py). Masthead: ST. GABRIEL THE ARCHANGEL CATHOLIC CHURCH, SUNDAY, NOVEMBER 1, 2026; Weekend
    Masses Saturday 5:00pm (Vigil), Sunday 8:00am, 10:00am, 11:30am, 6:00pm (not in summer); Weekday Masses
    Monday-Saturday 9:00am, Tuesday-Thursday also 6:30am (not in summer); Contact Us 88 East Saddle River
    Road, Saddle River, NJ 07458; Rev. Frank J. Fano, Pastor.'
- url: https://container.parishesonline.com/bulletins/03/0374/20261101B.pdf
  seen: 2026-11-03
  quote: St. Gabriel the Archangel, Saddle River, NJ 03-0374
  note: LPi container 03/0374 carries the same 6-page issue; the quote is the ad-page footer (page 5).
    The 8 November issue answered 403 on 3 November (not yet posted).
- url: https://www.stgabrielsr.org/index.php?page=mass
  seen: 2026-11-03
  quote: _content/sidebar/mass/2026-11-01 Bulletin.pdf
  note: Parish Mass Schedule page (the menu's 'Sunday Bulletin' link points here); lists issues newest
    first, named 'YYYY-M-D Bulletin.pdf'.
research:
- method: probe po on guessed org slugs (st-gabriel-the-archangel, -church, -saddle-river, -church-saddle-river)
  url: https://parishesonline.com/organization/st-gabriel-the-archangel-church
  checked: '2026-11-03'
  outcome: not-found
  next_action: Find the org slug from a ParishesOnline or LPi link (the parish site has none) and switch
    the row to parishes_online if its issues match container 03/0374
  retry_when: A ParishesOnline search or a link to the org turns up
bulletin_status: available
---

## Publisher

St. Gabriel the Archangel, 88 East Saddle River Road, Saddle River, publishes its own weekly bulletin, printed by LPi (container 03/0374). I read page 1 of the 1 November 2026 issue (image, rendered): the masthead names "St. Gabriel the Archangel Catholic Church" alone, with its own Mass schedule, address and staff (Rev. Frank J. Fano, Pastor). The ad pages carry the footer "St. Gabriel the Archangel, Saddle River, NJ 03-0374".

## Worship sites

- St. Gabriel the Archangel Church, 88 East Saddle River Road (`st-gabriel-the-archangel-saddle-river`): every Mass in the schedule. No other building is named.

The directory (185) and GCatholic (18553) list only this church. Msgr. Ron Rozniak, Priest in Residence here, is also listed as Pastor Emeritus in Our Lady of Mount Carmel, Ridgewood's bulletin; that is a residence, not a shared parish, and the two bulletins are separate (different mastheads, pastors and schedules).

## Website and bulletin provider

The parish's own site (stgabrielsr.org) posts each LPi issue on its Mass Schedule page, newest first, as `_content/sidebar/mass/YYYY-M-D Bulletin.pdf`; the 1 November issue was up on 3 November. The same issue is at ParishesOnline container 03/0374, but I found no ParishesOnline organization slug for it (`probe po` on the obvious slugs returned other parishes or none), so the row is `other`, reading the parish page with a pinned `page-pdfs` recipe. Pages 1–4 are image-only; the pipeline has to read them as images.

Fetch check (2026-11-03): `page-pdfs on https://www.stgabrielsr.org/index.php?page=mass: current`, picked `2026-11-01 Bulletin.pdf` (`fresh`). Recipe pinned in `provider_id`.

## Not yet confirmed

The ParishesOnline org slug, which would let the row read the container directly (`parishes_online`).
