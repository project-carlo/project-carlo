---
name: National Shrine of Our Lady of Czestochowa
reason: no-bulletin
line1: 654 Ferry Road
city: Doylestown
state: PA
postal_code: '18901'
decided: 2026-10-29
roster: []
evidence:
- url: https://czestochowa.us/en/contact
  seen: 2026-10-29
  quote: 'Address: 654 Ferry Road, Doylestown, PA 18901'
  note: The shrine's own contact page (read in Chrome; plain probe url gets no answer from the host).
- url: https://czestochowa.us/en
  seen: 2026-10-29
  note: Mass & Confession page for Thursday 29 October 2026 lists three public weekday Masses, 'Weekday
    Mass 7:30 AM', 8:00 AM and 11:30 AM, 'OLC Chapel · English', with named celebrants; its home page
    lists weekly community Masses (SHEMA 'beginning with Mass at 7:30 PM'). The site links a 'Weekly Announcements'
    panel that requires a login, and no bulletin or PDF links.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-catholic-church-doylestown-pa-18901/2026-10-25.pdf
  seen: 2026-10-29
  note: 'Page 2 (image-only, rendered) of Our Lady of Mount Carmel''s 25 October 2026 bulletin: a box
    ''Sacrament of Reconciliation at the Shrine of Our Lady of Czestochowa'' gives confession hours (Monday-Saturday
    11:00-11:45 AM, during the Saturday Vigil Mass 5:00 PM, Sunday 8:00-9:30 AM, 11:00 AM-12:30 PM, 2:30-5:00
    PM). It is a confession box, not a Mass schedule; Mount Carmel''s own Mass schedule (page 3) names
    only its church.'
parish: our-lady-of-mount-carmel-doylestown
revisit: Check czestochowa.us for a public bulletin or weekly announcements; if one is readable, make
  a parish row for the shrine with a church row here
revisit_after: 2027-04-29
research:
- method: 'Chrome (parish-site-access visit.py) on czestochowa.us: home page links, Announcements, Mass
    & Confession, Contact'
  url: https://czestochowa.us/en
  checked: '2026-10-29'
  outcome: not-found
  next_action: Look for a public weekly bulletin or announcements PDF on czestochowa.us (the Announcements
    panel was login-only) or a John Patrick / ParishesOnline listing for the shrine
  retry_when: The shrine's Weekly Announcements become public, or a publisher listing for the shrine appears
  revisit_after: 2027-04-29
---

## Why it is excluded

The National Shrine of Our Lady of Czestochowa (Pauline Fathers, 654 Ferry Road, Doylestown) is open with public Mass: its own site's Mass & Confession page for 29 October 2026 lists weekday Masses at 7:30, 8:00 and 11:30 AM in the OLC Chapel, and Our Lady of Mount Carmel's 25 October 2026 bulletin (page 2, image) mentions a Saturday Vigil Mass at 5:00 PM there in its confession box. It is in neither the archdiocese's directory nor the GCatholic roster (Settled policy 3 lets it in anyway). Under the diocese's settled shrine rule, a shrine outside a parish church gets a church row under a parish whose bulletin lists its Masses, a parish row if it publishes its own bulletin, or `no-bulletin` otherwise. No bulletin lists its Masses: Mount Carmel's box gives confession hours, not a Mass schedule, and its page-3 Mass schedule is Mount Carmel's own. The shrine's site has a per-day HTML schedule and a login-only 'Weekly Announcements' panel, with no bulletin or PDF found (2026-10-29). Excluded `no-bulletin`, not `closed`.

The `parish` field names Mount Carmel only as the Doylestown parish whose bulletin mentions the shrine; the shrine is not its worship site.

## What would change this

A readable weekly bulletin or announcements document from the shrine (then a parish row for the shrine, with this place as its church), or a parish bulletin that prints the shrine's Mass schedule. Its Sunday Mass times were not read here: take them from the shrine's Mass & Confession page when a row is made.
