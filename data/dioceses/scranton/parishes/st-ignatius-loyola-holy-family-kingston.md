---
name: The Parishes of St. Ignatius of Loyola and Holy Family
website: https://www.stignatiuspa.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://sponsors.bonventure.net/?page=1732']
group: Saint Ignatius Loyola Parish; Holy Family Parish Luzerne
evidence:
- url: http://sponsors.bonventure.net/pdfs/1732/2026-10-18.pdf
  seen: 2026-10-16
  quote: '339 NORTH MAPLE AVENUE'
  note: 'Cover (page 1) of the 18 October 2026 issue, "THE PARISHES OF" St. Ignatius and Holy Family: both addresses (339 North Maple Avenue, Kingston; 574 Rear Bennett Street, Luzerne), both Mass schedules, both offices and both websites.'
- url: http://sponsors.bonventure.net/pdfs/1732/2026-10-18.pdf
  seen: 2026-10-16
  quote: 'LUZERNE, PENNSYLVANIA 18709-1332'
  note: 'Page 1. St. Ignatius: Saturday 4:00 PM, Sunday 7:00 & 10:30 AM, Monday-Friday 7:30 AM. Holy Family: Saturday 5:15 PM, Sunday 9:00 AM, Monday-Friday 12:10 PM.'
- url: http://sponsors.bonventure.net/pdfs/1732/2026-10-18.pdf
  seen: 2026-10-16
  quote: 'Holy Family Parish Staff'
  note: 'Page 2: one pastoral staff (Monsignor David L. Tressler, Pastor; Rev. Michael Boris, Assistant Pastor) for both parishes, with each parish''s own staff and mission statement.'
- url: http://sponsors.bonventure.net/?page=1732
  seen: 2026-10-16
  quote: 'Click to View Current Bulletin'
  note: 'Bonventure bulletin page 1732, headed "The Parishes of St. Ignatius of Loyola and Holy Family (Luzerne, PA)": weekly issues at pdfs/1732/<YYYY-MM-DD>.pdf back to 2024. Linked as PARISH BULLETIN from stignatiuspa.com and as BULLETIN & SPONSORS from holyfamilyluzerne.org (both read in a browser).'
---

## Publisher

Saint Ignatius Loyola Parish (Kingston) and Holy Family Parish (Luzerne) are two canonical parishes
in the diocese's finder with one pastor, Monsignor David L. Tressler, and one weekly bulletin,
"The Parishes of St. Ignatius of Loyola and Holy Family". The 18 October 2026 issue's cover (page 1)
gives both churches' addresses and both schedules: St. Ignatius Saturday 4 pm, Sunday 7 and 10:30 am,
weekdays 7:30 am; Holy Family Saturday 5:15 pm, Sunday 9 am, weekdays 12:10 pm. Page 2 has one
pastoral staff over both parish staffs. Both parish websites link the same Bonventure bulletin page
(1732), and Holy Family's site also posts a draft "5-Year Pastoral Plan ... for HF-SIL parishes".

## Worship sites

Two: `st-ignatius-loyola-kingston` and `holy-family-luzerne`, the two places the cover schedules,
and the only worship sites the finder gives the two parishes. GCatholic also lists St. Ann's Chapel
(Hoyt St. & Loveland Ave., Kingston) as a mission of St. Ignatius; the bulletin schedules no Mass
there (the 11 October issue mentions the youth group "working at St. Ann's Chapel"), so it is
`open/st-ann-kingston.md`. The diocese's consolidated-parishes list gives St. Hedwig (closed 2007)
and St. Mary's Annunciation (closed 11/22/2009) in Kingston, and Sacred Heart, St. Ann and St. John
Nepomucene in Luzerne (all closed 1999), none of which is in a roster here.

## Website and bulletin provider

The bulletin is printed and hosted by Bonventure: `sponsors.bonventure.net/?page=1732` lists every
issue since 2024 and links `pdfs/1732/<date>.pdf`. stignatiuspa.com (the finder's website for St.
Ignatius, named on the cover) links it as PARISH BULLETIN; holyfamilyluzerne.org links it as
BULLETIN & SPONSORS. `website` is the St. Ignatius site, `bulletin_provider: other`, no recipe
pinned (`fetch:check` reads only promoted rows). **Quirk:** from this sandbox, HTTPS to
sponsors.bonventure.net fails certificate verification for curl and Python ("unable to get local
issuer certificate"), while plain HTTP works and Chrome loads the HTTPS page; evidence cites the
http:// URLs. The resolver may need the http:// listing (`page-pdfs
http://sponsors.bonventure.net/?page=1732`) as its recipe; check with `fetch:check` after promotion.

## Not yet confirmed

Whether the pipeline can fetch from sponsors.bonventure.net over HTTPS outside this sandbox. The
cover is text, and the masthead quotes are found by `recheck` over HTTP.
