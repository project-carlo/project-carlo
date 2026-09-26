---
name: St. Paul Mission
reason: closed
line1: ''
city: Fabius
state: NY
postal_code: '13063'
parish: church-of-the-nativity-tully
decided: 2026-09-26
roster: ['directory:33202']
evidence:
- url: https://www.syracusediocese.org/parishes
  seen: 2026-09-26
  quote: St. Paul Mission, Fabius (CLOSED - See Church of the Nativity @ Immaculate Conception, Pompey)
  note: The diocese's alphabetical parish list (behind Cloudflare; read in a browser, copy in the orchestrator's
    scratchpad diocese-parish-list.txt). The parish finder lists it as "St. Paul Mission (Closed)" with
    no address.
- url: https://www.syracusediocese.org/church-of-the-nativity-pompey
  seen: 2026-09-26
  quote: Sacramental records for St. Paul Mission, Fabius are retained here.
  note: The successor's page on the diocese site (behind Cloudflare; read with parish-site-access visit.py).
- url: https://container.parishesonline.com/bulletins/06/0037/20260927B.pdf
  seen: 2026-09-26
  quote: 'Sunday Masses: 8 a.m. Immaculate Conception, Pompey9:30 a.m. St. Joseph’s, LaFayette11:30 a.m.
    St. Patrick’s, Otisco'
  note: The successor's current bulletin (27 September 2026). Its masthead schedule (Saturday 4:30 p.m.
    St. Leo's, Tully, plus these three) and its page-2 Mass intentions name no church in Fabius.
- url: https://icpompey.org/wp-content/uploads/detailhistory1.pdf
  seen: 2026-09-26
  quote: The present brick church was erected in 1975.
  note: Immaculate Conception, Pompey's parish history. St. Paul's in Fabius was its mission (a former
    Universalist church bought 1891); a new brick church was built on Route 80 east of the village and
    dedicated 7 December 1975. Undated; says nothing of the closure.
---

## Why it is excluded

The diocese's parish list says the mission closed: "St. Paul Mission, Fabius (CLOSED - See Church
of the Nativity @ Immaculate Conception, Pompey)", and the diocese's page for Pompey says its
sacramental records are kept there. The successor's current bulletin (Church of the Nativity,
27 September 2026) has a schedule of four churches, St. Leo's (Tully), Immaculate Conception
(Pompey), St. Joseph's (LaFayette) and St. Patrick's (Otisco), and no Mass anywhere in Fabius,
in the masthead or in the week's intentions. So the parish closed and the successor holds no
Mass there.

No date for the last Mass was found, so `last_mass` is empty. The Pompey history dates the 1975
brick church "on Route 80 east of the village"; a web search turned up a real-estate listing for
a "former" church at 7955 Route 80, Fabius, but the listing page (loopnet.com) refused every
fetch, so neither the address nor a sale is recorded as evidence. The address is left at the
town.

## What would change this

Nothing expected. A dated closure (Catholic Sun, or the Nativity parish's history) would fill in
`last_mass`, and the listing, if readable, would give the street address.
