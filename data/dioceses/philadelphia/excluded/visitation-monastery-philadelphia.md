---
name: Visitation Monastery
reason: no-bulletin
line1: 5820 City Ave.
city: Philadelphia
state: PA
postal_code: '19131'
decided: 2026-10-28
roster: ['gcatholic:70928']
evidence:
- url: https://gcatholic.org/churches/usa-03/70928
  seen: 2026-10-28
  note: 'GCatholic ''Visitation'', type Monastery, ''Served by: Visitandines'', 5820 City Ave., Philadelphia
    19131, phone +1 (215) 473-5888, Plus Code 87F6XQR4+WP, last updated 2025-12-21; the Website field
    is blank in the page, and the roster''s visitationnuns.org does not resolve.'
- url: https://catholicphilly.com/2022/06/news/events/novena-of-masses-offered-to-sacred-heart-of-jesus/
  seen: 2026-10-28
  quote: The Visitation Monastery Chapel is located at at 5820 City Avenue in Philadelphia.
  note: 'CatholicPhilly, posted 2022-06-15, an events notice: a novena of Masses honoring the Sacred Heart,
    16 to 24 June 2022, ''Masses are at 7 p.m. each night'', announced publicly with intentions sent in
    by those unable to attend. It is the only evidence read of public Mass here, and is four years old.'
- url: https://catholicphilly.com/2015/07/news/profile/sisters-married-to-christ-live-as-a-family-in-cloisters/
  seen: 2026-10-28
  quote: the Monastery of the Visitation on City Avenue in Philadelphia
  note: 'CatholicPhilly 2015-07-17 profile: one of four cloistered monasteries of women in the archdiocese
    ''that practice strict enclosure''.'
- url: https://archphila.org/parish/
  seen: 2026-10-28
  note: The monastery is not in the directory's parish list; no parish bulletin read in this batch (Presentation
    BVM, St. Margaret, St. Matthias, St. John Vianney, 25 October 2026) lists a Mass at the monastery.
revisit: Confirm whether the monastery chapel holds a regular public Mass now and where it publishes its
  times
revisit_after: 2027-04-28
research:
- method: 'Looked for a monastery website (visitationnuns.org, visitationmonasteryphilly.org, philadelphiavisitation.org,
    visitationphiladelphia.org: DNS dead; visitationmonastery.org unreachable) and searched CatholicPhilly''s
    REST API for the monastery''s Mass times'
  url: https://catholicphilly.com/2022/06/news/events/novena-of-masses-offered-to-sacred-heart-of-jesus/
  checked: '2026-10-28'
  outcome: not-found
  next_action: Find a current monastery site, Facebook page or Mass-times listing giving a regular public
    Mass schedule, or a parish bulletin that lists the monastery's Mass
  retry_when: A working monastery website or a bulletin listing its Mass turns up; the browser could also
    read a social-media page this pass did not try
---

## Why it is excluded

The Monastery of the Visitation (5820 City Avenue, Philadelphia; cloistered Visitation sisters) has a chapel that announced public evening Masses for a Sacred Heart novena in June 2022. That is the only evidence of public Mass found. No regular Mass schedule, website or bulletin is published or reachable: the GCatholic site link is dead (DNS), the other candidate domains don't resolve, and no parish bulletin in this batch lists a Mass at the monastery. By the diocese's rule for monastery chapels (a church row only if a parish bulletin lists the public Mass, a parish row if the house publishes a bulletin) there is nothing to map, so it is excluded `no-bulletin`, not `no-public-mass`: public Mass is likely but not currently confirmed, so this is the less final call.

## What would change this

A current regular Mass schedule for the chapel, or a bulletin of its own, makes it a parish row; a source saying the chapel is for the community only makes it `no-public-mass`.
