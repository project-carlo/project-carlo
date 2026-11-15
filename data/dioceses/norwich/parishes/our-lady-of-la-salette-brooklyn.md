---
name: Our Lady of La Salette and Our Lady of Lourdes
website: https://www.ourladylasaletteandlourdes.org/bulletins
bulletin_provider: parishes_online
provider_id: our-lady-of-lasalette-brooklyn-ct-and-our-lady-of-lourdes-hampton-ct
publication: ['po-org:our-lady-of-lasalette-brooklyn-ct-and-our-lady-of-lourdes-hampton-ct', 'lpi:0018000000QbzyBAAR',
  'po-container:04/0499']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0499/20261115B.pdf
  seen: 2026-11-14
  note: Page 1 (an image, rendered with render.py) of the November 15, 2026 issue is headed 'Our Lady
    of La Salette Church / Our Lady of Lourdes Mission Church' with both addresses (25 Providence Rd,
    Brooklyn; 41 Cedar Swamp Rd, Hampton) and Saturday Vigil 4:00 PM (La Salette), Sunday Mass 8:00 AM
    (La Salette), 9:30 AM (Lourdes), 11:00 AM (La Salette); Rev. Ben Vinjoe, Administrator.
- url: https://container.parishesonline.com/bulletins/04/0499/20261115B.pdf
  seen: 2026-11-14
  quote: Our Lady of La Salette and Our Lady of Lourds
  note: 'Page 2 text: heading of the weekly Mass schedule with intentions (Saturday 4:00 pm, Sunday 8:00
    and 11:00 am, Tuesday-Friday 8:00 am); page 4 footer ''Our Lady of LaSalette (Brooklyn, CT) and Our
    Lady of Lourdes (Hampton, CT) | 04-0499''.'
- url: https://parishesonline.com/organization/our-lady-of-lasalette-brooklyn-ct-and-our-lady-of-lourdes-hampton-ct
  seen: 2026-11-14
  note: 'probe po: ''Our Lady of LaSalette (Brooklyn, CT) and Our Lady of Lourdes (Hampton, CT)'', 21
    Providence Rd, Brooklyn, website www.ourladylasaletteandlourdes.org, lpi 0018000000QbzyBAAR, container
    04/0499, latest issue 2026-11-15. The diocese''s locator map links this org for both churches.'
- url: https://www.ourladylasaletteandlourdes.org/
  seen: 2026-11-14
  note: 'probe url: a Wix site titled ''Our Lady Of Lasalette and Our Lady of Lourdes Parish'', linking
    /bulletins; no publisher id in the static HTML. GCatholic''s www.lasalette-lourdes.org does not resolve
    (DEAD-DNS).'
research:
- method: probe pdf on the November 15, 2026 issue (container 04/0499); page 1 has no text layer
  url: https://container.parishesonline.com/bulletins/04/0499/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check whether the pipeline OCRs page 1; without it, the 9:30 AM Lourdes Mass is in no text
    page (the page-2 intentions list only La Salette Masses)
  retry_when: After the first pipeline run on this row
bulletin_status: available
---

## Publisher

Our Lady of La Salette, Brooklyn, with its mission Our Lady of Lourdes, Hampton, publishes one LPi bulletin, container 04/0499 (org `our-lady-of-lasalette-brooklyn-ct-and-our-lady-of-lourdes-hampton-ct`). Page 1 of the November 15, 2026 issue (read 2026-11-14) is an image; rendered, it is headed "Our Lady of La Salette Church / Our Lady of Lourdes Mission Church", administrator Rev. Ben Vinjoe. Page 2's text heads the weekly schedule "Our Lady of La Salette and Our Lady of Lourds" and the footer on page 4 names both churches with 04-0499.

## Worship sites

The page 1 schedule covers both churches: Saturday Vigil 4:00 PM, Sunday 8:00 and 11:00 AM at La Salette, Sunday 9:30 AM at Lourdes. The diocese's List of Parishes (March 6, 2026) gives the same: La Salette with "Mission: Our Lady of Lourdes, Hampton Sunday Mass: 9:30 a.m." Nothing else is listed for the parish.

## Website and bulletin provider

The parish's Wix site ourladylasaletteandlourdes.org links `/bulletins`; the ParishesOnline org gives the same site. GCatholic's lasalette-lourdes.org no longer resolves. Page 1 of the issue is an image (pages 2-4 have text), so the Mass times there need OCR.

## Not yet confirmed

Whether the pipeline reads page 1's image schedule (see research). The page-2 intention schedule lists the La Salette Masses only.
