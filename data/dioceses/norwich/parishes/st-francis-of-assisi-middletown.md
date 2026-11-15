---
name: St. Francis of Assisi
website: https://parishesonline.com/organization/st-francis-of-assisi-church-06457
bulletin_provider: parishes_online
provider_id: st-francis-of-assisi-church-06457
publication: ['po-org:st-francis-of-assisi-church-06457', 'lpi:0018000000QxAElAAN', 'po-container:03/1299']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1299/20261115B.pdf
  seen: 2026-11-14
  quote: Middletown, CT. 06457
  note: 'Page 1 masthead of the November 15, 2026 issue names St. Francis of Assisi Catholic Church, 10
    Elm Street, Middletown, alone, with its own schedule: Saturday 4pm Vigil, Sunday English 9am and Spanish
    11am; weekday Masses Monday-Wednesday 5pm.'
- url: https://www.stfrancisct.com/
  seen: 2026-11-14
  note: The parish site the diocese's list gives answered HTTP 500 to probe url and to visit.py (parish-site-access).
- url: https://saintjohnmiddletownct.weebly.com/area-parish-bulletins.html
  seen: 2026-11-14
  note: St. John Middletown's Area Parish Bulletins page links 'Saint Francis of Assisi - Middletown'
    to parishesonline.com/find/st-francis-of-assisi-church-06457.
promoted: 2026-11-14
research:
- method: probe url and visit.py on the parish site
  url: https://www.stfrancisct.com/
  checked: '2026-11-14'
  outcome: access-blocked
  next_action: Open the site again with visit.py and, if it links this bulletin, set it as website
  retry_when: Next audit of this diocese
  revisit_after: 2027-05-01
bulletin_status: available
---

## Publisher

St. Francis of Assisi, Middletown publishes its own LPi bulletin, ParishesOnline org `st-francis-of-assisi-church-06457` (container 03/1299, lpi:0018000000QxAElAAN; `probe po` gives the org address 10 Elm St, Middletown). The November 15, 2026 issue (read 2026-11-14) has on page 1 "St. Francis of Assisi CATHOLIC CHURCH ... 10 Elm Street Middletown, CT. 06457" and pastor Fr. Kennedy.

## Worship sites

The page 1 schedule lists Masses at the one church only: "Saturday/Sábado , 4pm Vigil", Sunday English 9am and Spanish 11am, and weekday Masses Monday to Wednesday at 5pm. No mission or chapel is named. The diocese's List of Parishes (March 6, 2026) lists the one church, matching.

## Website and bulletin provider

The diocese's list gives www.stfrancisct.com, which answered HTTP 500 on 2026-11-14 to both `probe url` and `visit.py`, so `website` is the ParishesOnline organization page; the masthead prints "www.stfrancis.com" (apparently a typo for the same domain). St. John Middletown's Area Parish Bulletins page links this org. fetch reads it by `provider_id`.

## Not yet confirmed

Whether stfrancisct.com comes back; if it does and links the bulletin, it can replace the ParishesOnline page as `website`.
