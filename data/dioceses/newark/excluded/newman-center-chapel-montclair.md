---
name: Newman Center Chapel, Montclair State University
reason: no-bulletin
line1: 894 Valley Road
city: Montclair
state: NJ
postal_code: '07043'
decided: 2026-11-03
roster: ['directory:117']
evidence:
- url: https://www.redhawkcatholic.com/copy-of-about-us
  seen: 2026-11-03
  note: 'Red Hawk Catholic (the Montclair State Newman Center, the directory''s website) ''Chapel Schedule''
    page, text drawn as an image (read from a quick_snap.py screenshot; recheck can''t find it): ''CHAPEL
    SCHEDULE Fall 2026 … Mass Times Sunday 5:00 PM & 8:00 PM; Monday - Wednesday 5:30 PM; Thursday 7:00
    PM; Friday 8:30 AM … All at the Newman Center Chapel''. No restriction to students is stated.'
- url: https://www.redhawkcatholic.com/contact
  seen: 2026-11-03
  note: 'Wix page (read with quick_snap.py): ''Newman Center 894 Valley Rd Montclair, NJ 07043'', chaplain
    and director Fr. Jim Chern. The site''s menu (Home, About Us, Chapel Schedule, FOCUS, Catholic Counselling,
    Donate, Calendar, Contact) has no bulletin.'
- url: https://church-bulletin.org/624
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/newman-catholic-center-upper-montclair-nj-07043, ''Newman Catholic
    Center Bulletin'': a John Patrick listing with no issues, only the week''s readings; church-bulletin.org/?id=624
    and jppc.net/onlinebulletins/624template.pdf give the same empty page.'
- url: https://rcan.org/parishes/
  seen: 2026-11-03
  note: 'Archdiocese directory entry 117: Newman Center Chapel, 894 Valley Road, Montclair, NJ 07043,
    website redhawkcatholic.com.'
revisit: Check church-bulletin.org/624 for issues; if the Newman Center posts its own bulletin, make it
  a parish row with a church at 894 Valley Road (campus rule in diocese.md Rules settled).
revisit_after: 2027-02-01
---

## Why it is excluded

The Newman Center Chapel at Montclair State (894 Valley Road) holds Mass: Red Hawk Catholic's 'Chapel Schedule, Fall 2026' (read 2026-11-03) gives Sunday 5:00 and 8:00 pm, Monday-Wednesday 5:30 pm, Thursday 7:00 pm and Friday 8:30 am, 'All at the Newman Center Chapel'. The schedule is posted publicly with no restriction to students, and the archdiocese lists the chapel in its parish directory (117), so I judged the Mass public; under the campus rule (diocese.md *Rules settled*) it would be a church row. But no bulletin is published: the site has no bulletin page, and John Patrick's listing for the 'Newman Catholic Center' (id 624) shows no issues. No parish bulletin includes the chapel either (St. Cassian's and St. Teresa of Calcutta's 1 November 2026 issues give schedules for their own churches only). The rule makes a campus ministry a parish row only when it posts its own bulletin, so the chapel is excluded as `no-bulletin`: open with public Mass, nothing the pipeline can read.

## What would change this

Issues on church-bulletin.org/624 (or a bulletin page on redhawkcatholic.com): then a parish row `newman-center-montclair` with provider `other`, `page-pdfs https://church-bulletin.org/624`, and a church row at 894 Valley Road. Revisit 2027-02-01, at the start of the spring semester.
