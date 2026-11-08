---
name: Our Lady of Mercy, Jersey City
website: https://olmnj.org/
bulletin_provider: unsupported
provider_id: ''
publication: ['po-container:04/0032']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0032/20261108B.pdf
  seen: 2026-11-03
  quote: Our Lady of Mercy Catholic Church  |  04-0032
  note: '8 November 2026 LPi issue, 6 pages; pages 1-4 are images (read with render.py). Page 1 masthead:
    ''OUR LADY OF MERCY PARISH BULLETIN, 40 Sullivan Drive, Jersey City, NJ 07305, 201-434-7500 olmjcparish@olmnj.org
    olmnj.org, November 8, 2026 The Thirty-Second Sunday in Ordinary Time''. Page 2 is the pastor''s column
    to ''Our Lady of Mercy Parish Family and Friends''. The quote is the page 5-6 ad footer.'
- url: https://olmnj.org/
  seen: 2026-11-03
  note: 'probe url: Squarespace site ''Our Lady of Mercy Parish in Jersey City''; its only bulletin link
    is https://container.parishesonline.com/bulletins/04/0032/20260906B.pdf (6 September 2026), behind
    the ''Sunday Bulletin'' menu item. Homepage ''Mass Schedule Monday to Friday: 7am & 8:30am Saturday:
    8:30am, 5pm Sunday: 8am, 10am, 12noon''.'
revisit: Find the ParishesOnline org slug for container 04/0032 (see research), then set bulletin_provider
  parishes_online, provider_id the slug, clear fetch_gap and run fetch:check.
revisit_after: 2026-12-01
research:
- method: 'probe po on guessed org slugs: our-lady-of-mercy-{church,catholic-church,parish}-07305, our-lady-of-mercy-07305,
    -07304/-07306 variants, numbered suffixes -1..-6, Jersey City suffixes; our-lady-of-mercy-church and
    our-lady-of-mercy-catholic-church are Baton Rouge and Redding orgs. ParishesOnline search page (browser)
    and the PO API''s search endpoint returned nothing usable.'
  url: https://parishesonline.com/organization/our-lady-of-mercy-church-07305
  checked: '2026-11-03'
  outcome: not-found
  next_action: 'Find the org slug: open a ParishesOnline link in a future issue or on olmnj.org, look
    for a ''parishesonline.com/find/<slug>'' link, or search parishesonline.com by name and town in the
    browser; then set bulletin_provider parishes_online with that slug, clear fetch_gap and run fetch:check'
  retry_when: olmnj.org or an issue links a ParishesOnline org, or a ParishesOnline search method works
  revisit_after: 2026-12-01
bulletin_status: available
fetch_gap:
  kind: po-org-unknown
  seen: 2026-11-03
  note: The current LPi bulletin is in container 04/0032 (20261108B.pdf, 8 November 2026), but no ParishesOnline
    org slug for it was found, and the parishes_online collector reads by slug. The parish site's 'Sunday
    Bulletin' menu links only the 6 September 2026 issue, so page-pdfs on it would pick a stale file.
  url: https://container.parishesonline.com/bulletins/04/0032/20261108B.pdf
---

## Publisher

Our Lady of Mercy, Jersey City publishes a weekly bulletin printed by LPi, ParishesOnline container 04/0032. I read the 8 November 2026 issue (container.parishesonline.com/bulletins/04/0032/20261108B.pdf), rendering its image pages: the page 1 masthead reads 'OUR LADY OF MERCY PARISH BULLETIN, 40 Sullivan Drive, Jersey City, NJ 07305 … olmnj.org, November 8, 2026', page 2 is the pastor's column to 'Our Lady of Mercy Parish Family and Friends', and the ad-page footer reads 'Our Lady of Mercy Catholic Church | 04-0032'. Nothing in it names another parish.

## Worship sites

- Our Lady of Mercy, 40 Sullivan Drive (`our-lady-of-mercy-jersey-city`): the homepage gives Monday to Friday 7am and 8:30am, Saturday 8:30am and 5pm, Sunday 8am, 10am and 12noon (2026-11-03).

The directory (83) and GCatholic (18440) list only this church.

## Website and bulletin provider

`unsupported`, with `fetch_gap` `po-org-unknown`. The bulletin is current in container 04/0032, but the `parishes_online` collector reads by org slug, and none was found (see research). The parish's Squarespace site https://olmnj.org/ links only the 6 September 2026 issue from its 'Sunday Bulletin' menu, so a `page-pdfs` recipe on it would pick a stale file. Once the slug turns up, set the provider to `parishes_online` with that slug, add `po-org:` and `lpi:` ids to `publication`, clear the gap and run fetch:check.

Fetch check (2026-11-03): refused, 'unsupported, so fetch has no collector for it'.

## Not yet confirmed

The ParishesOnline org slug and LPi id. The Mass schedule is from the homepage, not the bulletin (the issue's schedule is in an image not yet read).
