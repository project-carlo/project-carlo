---
name: Liverpool Catholic Community (Christ the King, Epiphany, Pope John XXIII)
website: https://liverpoolnycatholic.org
bulletin_provider: discover_mass
provider_id: christ-the-king-liverpool-ny
publication: ['discovermass:christ-the-king-liverpool-ny', 'discovermass:immaculate-heart-of-mary-liverpool-ny']
group: Liverpool Catholic Community
evidence:
- url: https://bulletins.discovermass.com/download.php?bulletin=a0o2U6lLj%2ByRegtGcRfkrrW2R2Xfa11Efp2P3zMoJ1QP74ElNYoNB5Fg6T%2BUcrCiQpU1%2FL%2B%2Fo1Jp1R5iohWgbrVyEVCofS6N8IGtyoAN6FA%3D
  seen: 2026-09-26
  quote: CHRIST THE KING … EPIPHANY PARISH … 1001 Tulip Street … POPE JOHN XXIII
  note: 'The 27 September 2026 issue ("Twenty-Sixth Sunday in Ordinary Time"), listed on
    discovermass.com/church/christ-the-king-liverpool-ny/. The download link is a Discover Mass token.
    Page 1 masthead names the three parishes with their offices; page 2 calendar gives Masses at CTK,
    EP and PJXXIII only.'
- url: https://bulletins.discovermass.com/download.php?bulletin=a0o2U6lLj%2ByRegtGcRfkrrW2R2Xfa11Efp2P3zMoJ1QP74ElNYoNB5Fg6T%2BUcrCiQpU1%2FL%2B%2Fo1Jp1R5iohWgbrVyEVCofS6N8IGtyoAN6FA%3D
  seen: 2026-09-26
  quote: 8:00 AM Mass - Fr. McKeon (EP) … 8:30 AM Mass - Fr. Zach (CTK) … 10:30 AM Mass - Fr. Zach (PJXXIII)
  note: Page 2 of the same issue ("Event Calendar"), Sunday 27 September. Saturday 3 October lists "4:00PM Vigil Mass" at CTK and EP and "5:30PM Vigil Mass"
    at PJXXIII.
- url: https://discovermass.com/church/christ-the-king-liverpool-ny/
  seen: 2026-09-26
  quote: Christ the King
  note: 'The Discover Mass church page the pipeline reads (provider_id). issues.py found weekly issues,
    newest 2026-09-27; it is the same series the parish site embeds as Discover Mass archive widget
    3532, which runs weekly back to at least October 2025.'
- url: https://bulletins.discovermass.com/download.php?bulletin=H2MJpdWp%2FZPADzRSdtmtqsFQHEdN97W0Pw6ApQKzZG5VQJTMvlZVMOoeFPLLgPYmYQs8sfHF3yeYt3V1Oum6pgaJPK3lA6%2FsyRqhV2bypbs%3D
  seen: 2026-09-26
  quote: Catholic Family of Epiphany … Beginning Pentecost Sunday, May 24th, this shared bulletin will include
    news, events, ministries, and important updates from all three parishes
  note: 'Epiphany''s own last bulletin, 17 May 2026 (Discover Mass archive widget 3533, "Epiphany
    Parish Bulletin Archives (Prior to May 24, 2026)", church page discovermass.com/church/immaculate-heart-of-mary-liverpool-ny/).
    Page 2, under "Coming Soon: A Combined Bulletin for the Liverpool Catholic Community".'
- url: https://liverpoolnycatholic.org/bulletin
  seen: 2026-09-26
  quote: Epiphany Parish Bulletin Archives (Prior to May 24, 2026)
  note: The community site's Bulletins page (eCatholic site, behind Cloudflare; read with
    parish-site-access visit.py). It embeds two Discover Mass archive widgets, 3532 (current, issues to
    27 September 2026) and 3533 (Epiphany, last issue 17 May 2026), and its footer lists the three
    parishes' offices.
---

## Publisher

One weekly bulletin, published through Discover Mass (Diocesan), serves the three Liverpool
parishes of Christ the King, Epiphany and Pope John XXIII. I read the 27 September 2026 issue: its
page-1 masthead lists all three parishes with their addresses and offices (Christ the King, 21
Cherry Tree Circle; Epiphany Parish, 1001 Tulip Street; Pope John XXIII, 8290 Soule Road) under the
banner "CHRIST THE KING | EPIPHANY PARISH | POPE JOHN XXIII", and its page-2 calendar gives the
weekend Masses of all three churches: Saturday 4:00 pm at Christ the King and at Epiphany, 5:30 pm
at Pope John XXIII; Sunday 8:00, 9:30 and 11:00 am at Epiphany, 8:30 am at Christ the King and
10:30 am at Pope John XXIII. The 20 September issue has the same masthead.

The combined bulletin began on Pentecost Sunday, 24 May 2026. Epiphany published its own
("Catholic Family of Epiphany") until 17 May 2026, and that last issue announces the change in its
own words (see evidence). Its Discover Mass series (widget 3533, church page
`immaculate-heart-of-mary-liverpool-ny`) has no issue after 17 May, and the community site files it
as "Epiphany Parish Bulletin Archives (Prior to May 24, 2026)". So Epiphany's own channel is silent
and the shared one is current: one row, per the README's merge rule. Its old Discover Mass id is
recorded in `publication` so that nobody creates a second row from it. Before May 2026, the Christ
the King series (widget 3532) already carried Christ the King and Pope John XXIII; I did not read
an issue from before May, so whether the two ever published separately is not checked.

## Worship sites

Three churches, the ones the 27 September 2026 schedule lists:

- `churches/christ-the-king-liverpool.md` (21 Cherry Tree Circle)
- `churches/epiphany-st-joseph-the-worker-liverpool.md` (Epiphany Parish at the former St. Joseph
  the Worker church, 1001 Tulip Street)
- `churches/pope-john-xxiii-liverpool.md` (8290 Soule Road)

Not here: **Immaculate Heart of Mary**, 425 Beechwood Avenue. It was Epiphany's second worship site
until the bishop relegated it to profane use in 2023; its last Mass was the 4 pm vigil on
23 September 2023 (`excluded/immaculate-heart-of-mary-liverpool.md`). The diocese's list still
carries "St. Joseph the Worker, Liverpool (See Catholic Community of Epiphany Parish)"; that is the
Tulip Street church itself, not another building.

## Website and bulletin provider

liverpoolnycatholic.org is the three parishes' shared eCatholic site (eCatholic site id 32299,
not recorded as a publication because it hosts no bulletin: the Bulletins page only embeds the
Discover Mass widgets). It answers plain HTTP clients with 403 (Cloudflare) and was read in a browser
with `visit.py`. The pipeline reads Discover Mass by church slug: `christ-the-king-liverpool-ny`
serves the combined bulletin (issues.py: weekly, newest 2026-09-27), so it is `provider_id`. The
diocese's parish finder gives this site for all three parishes.

## Not yet confirmed

Nothing needed for the row. Pope John XXIII and Christ the King have no Discover Mass series of
their own that I found (`pope-john-xxiii-liverpool-ny` is a 404 on Discover Mass).
