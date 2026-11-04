---
name: St. Peter Claver Parish, Montclair
website: http://saintpeterclaverchurch.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area G
evidence:
- url: http://saintpeterclaverchurch.org/
  seen: 2026-11-03
  quote: Mass every Sunday. English 9AM, Español 11AM , French/Creole 1PM
  note: Static site (pages Home, Our Staff, Sacraments, Events, Ministries, Contact); no bulletin link.
    Still shows a 15 March 2020 COVID suspension notice and events up to October 2024. saintpeterclaverchurch.com
    (the Facebook page's website) redirects here.
- url: https://church-bulletin.org/648
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/saint-peter-claver-roman-catholic-church-montclair-nj-07042,
    ''Saint Peter Claver Roman Catholic Church Bulletin'', 56 Elmwood Avenue, Montclair: a John Patrick
    listing with no issues, only the week''s readings. church-bulletin.org/?id=648 and jppc.net/onlinebulletins/648template.pdf
    return the same empty listing page.'
- url: https://www.facebook.com/stpeterclaverchurch
  seen: 2026-11-03
  note: 'Facebook page ''Saint Peter Claver RC Church'', 56 Elmwood Ave, Montclair (read logged out with
    quick_snap.py): latest visible post 14 January 2026 (a Colombian lunch on 18 January 2026); no bulletins
    posted.'
revisit: Check whether John Patrick listing 648 posts issues (it is set up for the parish but empty).
revisit_after: 2027-02-01
research:
- method: probe url and probe get on the parish site and its pages; Facebook page read logged out; John
    Patrick listing 648 (found in earlier batches' jp_scan.sh output); probe po guesses st-peter-claver-church-07042,
    saint-peter-claver-church-07042, st-peter-claver-07042
  url: https://church-bulletin.org/648
  checked: '2026-11-03'
  outcome: not-found
  next_action: Reload church-bulletin.org/648 for dated issues; if present, set provider other with page-pdfs
    https://church-bulletin.org/648 and run fetch:check
  retry_when: The John Patrick listing 648 shows issues, or the parish site adds a bulletin link
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No current bulletin found. John Patrick Publishing has a listing for the parish (id 648, 'Saint Peter Claver Roman Catholic Church Bulletin', 56 Elmwood Avenue), but on 2026-11-03 it showed no issues, only the week's readings. The parish site links no bulletin, and the Facebook page (latest visible post 14 January 2026) posts none. The empty listing suggests the parish is a John Patrick customer whose issues are not put online, or a lapsed account; I couldn't tell which.

## Worship sites

- St. Peter Claver, 56 Elmwood Avenue (`st-peter-claver-montclair`): the parish site says 'Mass every Sunday. English 9AM, Español 11AM , French/Creole 1PM' (undated page, read 2026-11-03).

The directory (119) and GCatholic (18483) list this one church.

## Website and bulletin provider

http://saintpeterclaverchurch.org/ is a static site with no bulletin page; saintpeterclaverchurch.com redirects to it. `no_bulletin` (Settled policy 4 keeps the row and its church in the records, off the site). probe po found no ParishesOnline org for the guessed slugs.

## Not yet confirmed

Whether John Patrick listing 648 will carry issues; see `research` (revisit 2027-02-01). The Mass times come from an undated, partly stale site page.
