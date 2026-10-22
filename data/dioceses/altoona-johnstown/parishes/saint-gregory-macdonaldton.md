---
name: Saint Gregory Parish, MacDonaldton
website: https://discovermass.com/church/st-gregory-berlin-pa/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Rev. Michael Wolfe (Meyersdale area)
evidence:
- url: https://discovermass.com/church/st-gregory-berlin-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for St. Gregory.
  note: 'Discover Mass page exists ((814) 634-8150, a Mass schedule) but its Bulletins tab is empty ("Shucks! There are no bulletins available."): not a live channel. It is also the directory homepage for St. Gregory and the only page found for the others, so it is the row''s website.'
- url: https://meyersdalecatholic.flocknote.com/home
  seen: 2026-10-21
  note: 'A Flocknote sign-up page (247 High Street, Meyersdale), titled in the browser "Sts. Philip and James, St. Gregory, St. Michael, and St. Mary" (rendered title; not in the raw HTML), so the four act as one group for messaging. It shows a sign-up form only; /notes, /bulletin and similar paths redirect to a login. No bulletin is public.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory entry for Saint Gregory Parish, MacDonaldton: clergy "Rev. Michael Wolfe, Pastor", (814) 634-8150. The same Rev. Michael Wolfe is pastor of the other three Meyersdale-area parishes (Saints Philip and James, Saint Gregory, Saint Mary, Saint Michael). The directory lists no homepage for this parish.'
- url: https://www.webparish.com/aj/PhilipandJames/
  seen: 2026-10-21
  quote: This site maintained by Creighton Web Services
  note: 'Stale diocesan webparish.com stub (it still names Rev. James M. Dugan as pastor of Sts. Philip and James, and no Mass times or bulletin). Not a bulletin source.'
- url: https://www.facebook.com/SsPhilipAndJamesCatholicChurch
  seen: 2026-10-21
  note: 'Facebook page of Sts. Philip and James, Meyersdale (219 followers per a search snippet of 26 Aug 2026: "We welcome Fr. Michael Wolfe to our parish."). Behind the login wall in the sandbox, so I could not see whether it posts a bulletin. If it does, it is the likeliest shared channel for all four.'
revisit: 'Find a bulletin: Sts. Philip and James Facebook page (login wall), a call to the Meyersdale rectory, or a parish site; one bulletin may cover all four Wolfe parishes'
revisit_after: 2027-01-15
---

## Publisher

No bulletin found, so `bulletin_provider: no_bulletin` (the row is kept in the records and left off the site, README settled policy 4). Saint Gregory Parish, MacDonaldton is one of four Somerset County parishes (Saints Philip and James, Meyersdale; Saint Gregory, MacDonaldton; Saint Mary, Pocahontas; Saint Michael, Salisbury) that the diocesan directory gives to Rev. Michael Wolfe as pastor. A single bulletin for the four is plausible: they have one Flocknote group named for all four churches, and the old diocesan webparish stubs pair them (Sts. Philip and James with St. Gregory; St. Michael with St. Mary). But no bulletin was found for any of them, so there is nothing to show that one bulletin carries several, and the rows stay separate (a missing bulletin is not evidence of a shared one). If a joint bulletin turns up, merge the four rows with `pnpm diocese merge`.

Channels checked on 2026-10-21, none live:

- Discover Mass pages for all four (st-gregory-berlin-pa, st-mary-pocahontas-pa, st-michael-west-salisbury-pa, saints-philip-and-james-meyersdale-pa): each says "There are currently no bulletins available". No other Discover Mass church page exists for Meyersdale, Salisbury, Pocahontas or Macdonaldton (sitemap grep).
- ParishesOnline: empty organizations ss-philip-and-james-church-15552 and st-michael-church-15565; none found for St. Mary or St. Gregory (search API near each church).
- Flocknote meyersdalecatholic.flocknote.com: sign-up page only.
- webparish.com/aj/PhilipandJames and /Michael-Mary: stale stubs, no bulletin.
- Guessed homepages (meyersdalecatholic.org/.com, sspjmeyersdale.org, ssphilipandjames.org, stgregorymacdonaldton.org, stmarypocahontas.org, stmichaelwestsalisbury.org): DNS fails.
- Look-alike hits that are other parishes: church-bulletin.org "Saints Philip and James Parish" is Exton, PA; saintmichaelchurch.weebly.com is St. Michael in Cambria County (Fr. Auguscik); parishbulletins.com/bulletins/065 is a Guelph, Ontario bulletin.
- Facebook (SsPhilipAndJamesCatholicChurch): login wall.

## Worship sites

One church, St. Gregory (see churches/saint-gregory-macdonaldton). The other three Wolfe churches are separate rows: Saints Philip and James (Meyersdale), St. Mary (Pocahontas) and St. Michael (Salisbury). The diocese lists nothing else for this parish.

## Website and bulletin provider

`website` is the Discover Mass page https://discovermass.com/church/st-gregory-berlin-pa/ only because the row needs a unique URL and no parish homepage exists (the directory has none; for St. Gregory the directory itself gives this page). It is not a bulletin source. `publication` is empty because no bulletin id was found.

## Not yet confirmed

Where, if anywhere, the bulletin is published (a Facebook post, Flocknote only, or a printed-only bulletin), and whether the four share one. Next step: open the Sts. Philip and James Facebook page logged in, or phone the rectory ((814) 634-8150); if a bulletin turns up, set the provider and publication and merge the four rows if it carries them all.

**Pastor sources disagree (2026-10-21).** The diocese's clergy list
(https://www.dioceseaj.org/clergy/) names Rev. Michael Wolfe pastor of Saints Philip and James,
Meyersdale, Saint Gregory, MacDonaldton, Saint Mary, Pocahontas and Saint Michael, West
Salisbury. The New Baltimore parish's schedule page (https://newbaltimorecatholic.com/schedule/)
says "In residence Fr. Stephen Shin, OFMcap Pastor of Ss. Philip & James, Meyersdale & St.
Gregory, MacDonaldton". The `group` keeps the diocese's version; neither changes the row, since
no bulletin was found either way. Whichever pastor is current, his parish office is the place to
ask about a bulletin.


- Re-checked 2026-10-21 (task 25): DuckDuckGo searches for the four Meyersdale-area parishes (by name, by Fr. Michael Wolfe, by town) found only Discover Mass, the stale webparish.com stubs, mass-time aggregators, the Sts. Philip and James Facebook page (login wall; mobile and mbasic Facebook URLs also redirect to login) and church-bulletin.org `?id=144`, which is Saints Philip and James, Exton (a look-alike). `discovermass-church-urls.txt` has no Discover Mass slug for these towns beyond the ones already recorded. St. Peter, Somerset's current bulletin (stpetersparish.com site_docs/10648.pdf; its parochial vicar is the sacramental minister at West Salisbury and Pocahontas) has no hit for Meyersdale, Salisbury, Pocahontas, Gregory or Wolfe. Still no bulletin; stays `no_bulletin`.
