---
name: Our Lady of Lourdes Parish
website: https://www.ourladyoflourdesmontoursville.org/general-8
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.ourladyoflourdesmontoursville.org/general-8']
group: Our Lady of Lourdes Parish
evidence:
- url: https://www.ourladyoflourdesmontoursville.org/_files/ugd/05a2ee_b9ce758f90df4f09aefd03d8c9a6b0ed.pdf
  seen: 2026-10-16
  quote: Rev. Sean G. Carpenter, Pastor … 800 Mulberry Street, Montoursville, PA 17754 … Saturday 4:00
    pm- OLOL … Sunday 10:30 am - OLOL
  note: Page 1 of the 11 October 2026 issue, headed "OUR LADY OF LOURDES PARISH / TWENTY-EIGHTH SUNDAY
    IN ORDINARY TIME / OCTOBER 11, 2026" (the heading is not in the PDF text layer; read with pdftotext
    -layout). Its Mass Schedule also lists the Resurrection, Muncy Masses (Saturday 5:30 pm, Sunday 8:30
    am, Tuesday and Thursday 9 am).
- url: https://www.ourladyoflourdesmontoursville.org/_files/ugd/05a2ee_b9ce758f90df4f09aefd03d8c9a6b0ed.pdf
  seen: 2026-10-16
  quote: Our Lady of Lourdes & Church of the Resurrection
  note: Heading of the shared Mass-intentions column, page 1.
- url: https://www.ourladyoflourdesmontoursville.org/general-8
  seen: 2026-10-16
  note: The parish's "THIS WEEK'S BULLETIN" page (Wix) links one PDF, labelled "10-11", at _files/ugd/05a2ee_b9ce758f90df4f09aefd03d8c9a6b0ed.pdf
    (read 2026-10-16, in a browser and with curl; the link is in the raw HTML). No archive.
promoted: 2026-10-17
---

## Publisher

Our Lady of Lourdes, Montoursville publishes its own weekly bulletin, headed "OUR LADY OF
LOURDES PARISH" (11 October 2026 issue, page 1), with Rev. Sean G. Carpenter as pastor and the
parish's 800 Mulberry Street address. Fr. Carpenter is also pastor of the Church of the
Resurrection, Muncy, so this bulletin prints both parishes' Mass schedule and a joint
"Our Lady of Lourdes & Church of the Resurrection" intentions list. But Resurrection publishes
its own bulletin with its own masthead through ParishesOnline (container 03/0730, current to 18
October 2026: `resurrection-muncy`), so they are **two rows**: two live channels, no merge.

## Worship sites

One: `our-lady-of-lourdes-montoursville`. The Resurrection church, though listed in this
bulletin's schedule, belongs to the Resurrection row, whose own bulletin covers it.

## Website and bulletin provider

The bulletin page `/general-8` of the parish's Wix site posts only the current issue, as one
PDF under `/_files/ugd/<hash>.pdf` whose name changes every week; the link is in the page's
raw HTML. `probe url` on the homepage found no bulletin link (the menu item is "Bulletin" ->
/general-8, rendered by Wix), and no ParishesOnline, eCatholic or Discover Mass id. So
`website` is the bulletin page itself and the provider is `other`; `provider_id` is left empty
until a `fetch:check` run after promotion suggests a recipe (probably `page-pdfs`).

## Not yet confirmed

The Montoursville file is undated (a hash), so the resolver can only take "the PDF on the
page"; whether the page is updated every week was not checked over several weeks (on 16
October it still had the 11 October issue, which is normal mid-week).
