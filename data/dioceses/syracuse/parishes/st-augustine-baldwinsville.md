---
name: St. Augustine's Church
website: https://www.staugustinesparish.org
bulletin_provider: parishes_online
provider_id: st-augustines-parish
publication: ['po-org:st-augustines-parish', 'lpi:0018000000Qx7QfAAJ', 'po-container:04/0667']
group: Baldwinsville Catholic Parishes
evidence:
- url: https://container.parishesonline.com/bulletins/04/0667/20260927B.pdf
  seen: 2026-09-26
  quote: St. Augustine, Baldwinsville, NY 04-0667
  note: 'The 27 September 2026 issue. Pages 1-6 are images, so this quote is from the LPi footer on the
    text pages 7-8. Read as rendered images: page 1 is headed "St. Augustine’s Church / September 27,
    2026", pastor Most Reverend Douglas J. Lucia, "7333 O’Brien Road, Baldwinsville, New York 13027";
    page 2''s "Mass Times" box gives St. Augustine''s Sunday 10:30am and Wednesday 10:00am, and St.
    Mary''s and St. Elizabeth Ann Seton''s times.'
- url: https://www.staugustinesparish.org/resources
  seen: 2026-09-26
  quote: View This Week's Bulletin
  note: The parish's Resources page (read in a browser with visit.py); the button links parishesonline.com/organization/st-augustines-parish.
- url: https://parishesonline.com/organization/st-augustines-parish
  seen: 2026-09-26
  note: '`probe po st-augustines-parish`: "St. Augustine''s Parish", 7333 Obrien Rd, LPi id 0018000000Qx7QfAAJ,
    container 04/0667, weekly issues through 2026-09-27.'
---

## Publisher

St. Augustine's publishes its own weekly bulletin through ParishesOnline (LPi), container
04/0667. I read the 27 September 2026 issue (and checked the 20 September one exists). Its first
six pages are scanned images with no text layer, so I read them as rendered images: page 1 is
headed "St. Augustine’s Church", September 27, 2026, with the parish staff (Pastor: Most
Reverend Douglas J. Lucia; Parochial Vicar: Fr. Benjamin Schrantz), its own office hours and its
address, 7333 O’Brien Road. Page 2's "Mass Times" box lists St. Augustine's (weekend Sunday
10:30am, weekday Wednesday 10:00am) and, below it, St. Mary's and St. Elizabeth Ann Seton's
Masses, since the three Baldwinsville parishes share clergy and a Mass rota.

It is one of three Baldwinsville parishes that each publish their own bulletin (St. Mary of the
Assumption: ParishesOnline 06/0074; St. Elizabeth Ann Seton: self-hosted). All three are live,
so each is its own row in the group "Baldwinsville Catholic Parishes"; see
`parishes/st-mary-of-the-assumption-baldwinsville.md`.

## Worship sites

One: St. Augustine's, 7333 O'Brien Road (`churches/st-augustine-baldwinsville.md`).

## Website and bulletin provider

staugustinesparish.org is the parish's own Wix site. Its Resources page's "View This Week's
Bulletin" links the ParishesOnline organization `st-augustines-parish` (LPi 0018000000Qx7QfAAJ,
container 04/0667). `probe url` got HTTP 429 from the site, and `visit.py` loaded it but called
it SPAM-SQUAT: the same false positive as St. Mary's (the word "forex" inside Wix configuration
keys like "ForExpressButtons"). The page is the parish's own, with a welcome from Bishop Lucia.

## Not yet confirmed

The bulletin's schedule pages are images. The pipeline's text extraction will get nothing from
pages 1-6, so reading this bulletin's Mass times needs OCR or the image path. Nothing about the
structure is unconfirmed.
