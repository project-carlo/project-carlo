---
name: St. Joseph, Oradell/New Milford
website: https://sjcnj.org/
bulletin_provider: parishes_online
provider_id: saint-joseph-roman-catholic-church
publication: ['po-org:saint-joseph-roman-catholic-church', 'lpi:0018000000Qc1SHAAZ', 'po-container:04/0064']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
  seen: 2026-11-03
  quote: All Saints Day ~ November 1, 2026
  note: Page 1 masthead 'Saint Joseph Roman Catholic Church … Oradell/New Milford, NJ', pastor Rev. Christian
    G. Scalo; parish office 105 Harrison St., New Milford; school 305 Elm St., Oradell. 8 pages, text
    layer. The same issue is self-hosted at https://sjcnj.org/wp-content/uploads/2026/10/2026-Nov1-Bulletin.pdf,
    whose ad pages carry 'Saint Joseph Roman Catholic Church | 04-0064'.
- url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
  seen: 2026-11-03
  quote: Saturday 5:00 pm
  note: 'Page 1 Mass schedule: Saturday 5:00 pm; Sunday 7:30am, 9am, 10:30 am, 12 noon; daily Monday -
    Saturday 8:30 am. No other worship site named.'
- url: https://parishesonline.com/organization/saint-joseph-roman-catholic-church
  seen: 2026-11-03
  note: 'probe po: ''St. Joseph Church'', 105 Harrison St, New Milford, NJ 07646-2698, website http://sjcnj.org/,
    LPi id 0018000000Qc1SHAAZ, container 04/0064, latest issue 2026-11-01; probe container 04/0064 also
    found the 8 November 2026 issue (Thirty-Second Sunday, same masthead).'
- url: https://sjcnj.org/masses-and-bulletin/
  seen: 2026-11-03
  note: Parish WordPress page; visit.py reports po-org:saint-joseph-roman-catholic-church on it, and it
    links yearly bulletin pages (/2026-bulletins/, newest 2026-Nov1-Bulletin.pdf).
bulletin_status: available
publication_reviews:
- parish: st-john-the-evangelist-bergenfield
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Saint Joseph Roman Catholic Church, Oradell/New Milford alone,
      with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names St. John the Evangelist, Bergenfield
      alone, with its own Mass times.
- parish: st-mary-dumont
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Saint Joseph Roman Catholic Church, Oradell/New Milford alone,
      with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/saint-mary-s-church-dumont-nj-07628/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names St. Mary's Church, Dumont alone, with
      its own Mass times.
- parish: ascension-new-milford
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Saint Joseph Roman Catholic Church, Oradell/New Milford alone,
      with its own Mass times.
  - url: https://files.ecatholic.com/39014/bulletins/20261101.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names Church of the Ascension, New Milford
      alone, with its own Mass times.
---

## Publisher

Saint Joseph Roman Catholic Church, Oradell/New Milford, publishes its own weekly bulletin through LPi (ParishesOnline org `saint-joseph-roman-catholic-church`, container 04/0064). I read the 1 November 2026 issue (8 pages, text): its page-1 masthead is "Saint Joseph Roman Catholic Church … Oradell/New Milford, NJ", with Rev. Christian G. Scalo as pastor. The 8 November issue was already in the container on 2026-11-03.

## Worship sites

One church, `st-joseph-oradell`: the masthead's Mass schedule (Saturday 5:00 pm; Sunday 7:30, 9:00, 10:30 am and 12 noon; Monday to Saturday 8:30 am) names no other place. The directory lists the parish once (123, at the parish office's address, 105 Harrison Street, New Milford) and GCatholic lists one church (18527, Elm St., Oradell); both are this one church. The bulletin also names the school (305 Elm St., Oradell) and a "MC" used for adoration, which are parish buildings, not separate Mass sites.

## Website and bulletin provider

https://sjcnj.org/ (WordPress) answers `probe get` and self-hosts copies of the LPi issue on yearly pages (`/2026-bulletins/`). `visit.py` finds the ParishesOnline org on its Masses and Bulletin page, and `probe po` shows it live (latest 2026-11-01). Provider `parishes_online` with the org slug, so the row does not depend on the site's yearly pages.

Fetch check (2026-11-03, headed): ok, picked the 2026-11-01 issue from container 04/0064 through the org's publication page.

## Not yet confirmed

Nothing outstanding.
