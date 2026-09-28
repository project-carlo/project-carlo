---
name: St. Patrick Church
reason: no-bulletin
line1: 9168 Main St.
city: Taberg
state: NY
postal_code: '13471'
decided: 2026-09-26
roster: ['gcatholic:18051', 'directory:33193']
evidence:
- url: https://gcatholic.org/churches/usa-02/18051
  seen: 2026-09-25
  quote: 9168 Main St., Taberg, New York 13471-1848
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Patrick'', 9168
    Main St., Taberg, NY, 13471; kind: Church'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: Listed in Diocese of Syracuse parish finder (Mass-times map) as 'St. Patrick', 9168 Main Street,
    Taberg, NY, 13471-1848
- url: https://discovermass.com/church/st-patrick-taberg-ny/
  seen: 2026-09-26
  quote: Saturday 5:15pm Sunday 7:30am , 10:00am
  note: 'Discover Mass (MassTimes.org) listing for St. Patrick, 9168 Main St., Taberg: Masses Saturday 5:15
    pm, Sunday 7:30 and 10:00 am, Monday-Thursday 9:00 am; confessions Saturday 4:30 pm. "There are currently
    no bulletins available for St. Patrick." It lists no other church.'
- url: https://www.syracusediocese.org/st-patrick-taberg
  seen: 2026-09-26
  quote: Sacramental Records for St. Ann Mission, Glenmore (Annsville) are retained here.
  note: The diocese's page for St. Patrick (Cloudflare; read in a browser). Pastor Rev. Francis A. Wapen,
    stpatstaberg@syrdio.org; it gives no website.
- url: https://parishesonline.com/organization/st-patrick-st-anne
  seen: 2026-09-26
  note: '`probe po st-patrick-st-anne`: organization "St. Patrick / St. Anne", 9168 Main St, Taberg (LPi
    id 0018000000Qc2cIAAR), "no publications". Its public page (parishesonline.com/find/st-patrick-st-anne,
    read in a browser) links weekly "publications" at customer-data-prod-bucket.s3.amazonaws.com/generic-publications/pol/20260920GB.pdf:
    LPi''s one-page generic bulletin, with no parish content (probe pdf: no mention of Taberg or St. Patrick).'
---

## Why it is excluded

Open, with public Mass, but no bulletin the pipeline could read. St. Patrick, Taberg is a one-church
parish (pastor Fr. Francis A. Wapen) with weekend Masses (Saturday 5:15 pm, Sunday 7:30 and 10:00 am,
per Discover Mass/MassTimes.org, and daily Mass Monday to Thursday). What I checked for a bulletin:

- The diocese's page and directory give no website at all.
- ParishesOnline has an organization, "St. Patrick / St. Anne" (st-patrick-st-anne), but `probe po`
  finds no publications, and the "View Bulletin" links on its public page are LPi's generic weekly
  one-page insert (`generic-publications/pol/...GB.pdf`), not a parish bulletin.
- Discover Mass: "There are currently no bulletins available for St. Patrick."
- Web searches for "St. Patrick Taberg bulletin" and the pastor's name found nothing else.

So this is `no-bulletin`, not closed. The Mass times are from MassTimes.org via Discover Mass, not from
the parish, so they are not re-dated here beyond 2026-09-26.

## What would change this

A parish bulletin appearing on ParishesOnline (the organization exists; watch for a container), a
parish website or Facebook page that posts one, or the parish office confirming where it is published.
