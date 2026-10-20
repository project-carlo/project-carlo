---
name: Sacred Heart of Jesus Parish
website: https://www.sacredheartcornwall.org/
bulletin_provider: discover_mass
provider_id: sacred-heart-of-jesus-cornwall-pa
publication: ['discovermass:sacred-heart-of-jesus-cornwall-pa']
group: ''
evidence:
- url: https://discovermass.com/church/sacred-heart-of-jesus-cornwall-pa/
  seen: 2026-10-19
  quote: Saturday5pm,Sunday8am& 10:30am
  note: 'Issue of 25 October 2026 (already posted on 19 October), page 2 (the text layer drops
    spaces): "Sacred Heart of Jesus, October 25, 2026, 717-273-1574, 30th Sunday in Ordinary Time,
    WEBSITE: sacredheartcornwall.org, Pastor, Fr. Rodrigo A. Arrázola ... Mass times: Saturday 5pm,
    Sunday 8am & 10:30am, Mon 12pm, Tues—Fri 8am ... Mailing Address: PO BOX 136, Cornwall, PA 17016".'
- url: https://discovermass.com/church/sacred-heart-of-jesus-cornwall-pa/
  seen: 2026-10-19
  quote: 'WEBSITE: sacredheartcornwall.org'
- url: https://www.sacredheartcornwall.org/
  seen: 2026-10-19
  note: Behind Cloudflare; probe url gets 403, and parish-site-access visit.py was challenged on every
    load (BLOCKED). The bulletin was read on Discover Mass instead.
---

## Publisher

Sacred Heart of Jesus, 2596 Cornwall Road, Cornwall, publishes its own weekly bulletin
through Diocesan (Discover Mass). The 25 October 2026 issue (posted by 19 October) names
Sacred Heart of Jesus alone, Fr. Rodrigo A. Arrázola, pastor, with Saturday 5pm, Sunday 8am
and 10:30am, Monday noon and Tuesday to Friday 8am Masses; the intentions list those Masses
and nothing elsewhere.

## Worship sites

- Sacred Heart of Jesus, Cornwall (`sacred-heart-of-jesus-cornwall`). No other building in
  the bulletin, the diocese's page or GCatholic.

## Website and bulletin provider

sacredheartcornwall.org (the website the diocese and the bulletin give) is behind
Cloudflare and never loaded in the sandbox, so its bulletin link wasn't seen. Discover
Mass's church page `sacred-heart-of-jesus-cornwall-pa` (found with Discover Mass's search
for "cornwall") lists weekly issues through 25 October 2026 whose masthead is this parish's.
Provider `discover_mass` with that slug.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows): the resolver found the newest issue on the Discover Mass church page, but the download returned Discover Mass's 134-byte "Maximum number of files downloaded today" page (a per-IP daily cap the sandbox's shared egress reached; curl got the same page). Not a resolver fault; re-run on another day.

## Not yet confirmed

That the parish site itself links Discover Mass (blocked); the bulletin's own masthead
settles which parish it is.
