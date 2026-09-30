---
name: Our Lady of Grace Parish (Morristown, Hammond and Rossie)
website: https://www.stjohnpeterpatrick.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:5458']
group: Our Lady of Grace
evidence:
- url: https://files.ecatholic.com/5458/bulletins/20260927.pdf
  seen: 2026-09-30
  quote: The Saturday Mass in Morristown is livestreamed on YouTube
  note: Page 1 of the 27 September 2026 issue, under the Mass list (codes M, R, H). The masthead naming
    Our Lady of Grace Parish and its three churches is an image on the same page (seen with render.py,
    2026-09-30), so it cannot be quoted from the text layer.
- url: https://files.ecatholic.com/5458/bulletins/20260927.pdf
  seen: 2026-09-30
  quote: At Rossie and Hammond & upon request with Parish Priest (Rectory)
  note: 'Page 1, Sacrament of Penance line: confession at St. John before Saturday Mass and on First Fridays,
    "At Rossie and Hammond" on request.'
- url: https://files.ecatholic.com/5458/bulletins/20260913.pdf
  seen: 2026-09-30
  quote: Marie and Charles Elphick by Friends at St. Patrick’s
  note: '13 September 2026 issue, page 1, Sunday 8:00 am, code R: the R Mass is at St. Patrick’s, Rossie.'
- url: https://www.stjohnpeterpatrick.org/events/mass/20260927
  seen: 2026-09-30
  quote: 'Location: St. Patrick''s, Rossie'
  note: 'Parish event page (eCatholic, behind Cloudflare; browser): Sunday 27 September 2026, 8:00 AM,
    repeats every Sunday. The 9:30 AM event (events/mass-1) is at "St. Peters Church, Hammond" and the
    11:00 AM event (events/mass-2) at "St. Johns Church, Morristown".'
- url: https://www.stjohnpeterpatrick.org/about-st-john-the-evangelist
  seen: 2026-09-30
  quote: the new parish of “The Roman Catholic Community of Morristown, Hammond & Rossie” was formed
  note: 'Parish history page (browser): merger realised 20 January 2009 under Rev. Kevin McEwan.'
- url: https://www.stjohnpeterpatrick.org/bulletins
  seen: 2026-09-30
  note: 'Bulletins page (browser): lists every issue from 4 December 2022 to 27 September 2026, each a
    files.ecatholic.com/5458/bulletins/YYYYMMDD.pdf link; no separate bulletin for any single church.'
---

## Publisher

Our Lady of Grace Parish publishes one weekly bulletin for Morristown, Hammond and Rossie through
eCatholic (site 5458; `files.ecatholic.com/5458/bulletins/YYYYMMDD.pdf`, newest 27 September 2026, and
the parish's Bulletins page lists every Sunday back to December 2022). The masthead of the 27 September
2026 issue is an image at the top of page 1 (viewed with `render.py`, so it is not in the text layer and
`recheck` cannot find it): "OUR LADY OF GRACE PARISH / St. Peter’s Church – Hammond, St. Patrick’s Church –
Rossie, St. John the Evangelist Church – Morristown / P.O. Box 216 • Morristown, NY 13664 / Rev. Leagon
Carlin, Pastor ... website: stjohnpeterpatrick.org". Below it the Mass list uses the codes M, R and H:
Saturday 5:30 pm M; Sunday 8:00 am R, 9:30 am H, 11:00 am M; Tuesday and Wednesday 5:30 pm M; Thursday
and Friday 8:00 am M. The text layer confirms R is Rossie ("Marie and Charles Elphick by Friends at St.
Patrick’s" is the 8:00 am R intention on 13 September) and the parish site's recurring events say so:
8:00 AM "Location: St. Patrick's, Rossie", 9:30 AM "Location: St. Peter's Church, Hammond", 11:00 AM
"Location: St. John's Church, Morristown".

The diocese directory lists all three under the group "Our Lady of Grace" (Morristown, Hammond,
Rossie) with the website stjohnpeterpatrick.org, and the parish site's history says the three were
merged on 20 January 2009 as "The Roman Catholic Community of Morristown, Hammond & Rossie". They are
one bulletin.

## Worship sites

Three, all in the Mass list: `st-john-the-evangelist-morristown` (Saturday vigil, Sunday 11:00 am and
the weekday Masses), `st-peter-hammond` (Sunday 9:30 am) and `st-patrick-rossie` (Sunday 8:00 am).
The parish's "Future Mass Schedule" page (dated 12/12/16) describes an abandoned plan to move Rossie's
8:00 am slot to Redwood in summer; that plan has not happened (Redwood belongs to the Alexandria Bay
cluster's bulletin, another region's row). The original St. Peter's Church on Route 37 was demolished in
1965 (parish history), and Jacques Cartier State Park summer Mass ended in 1998; neither is a site now.

## Website and bulletin provider

eCatholic, site 5458; website stjohnpeterpatrick.org (behind Cloudflare: `probe url` HTTP4XX; visit.py
loaded it in one to several tries and reported `ecatholic:5458`). The bulletin has a text layer; only
the masthead box is an image.

## Not yet confirmed

Nothing outstanding on structure.
