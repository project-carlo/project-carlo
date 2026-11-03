---
name: Church of the Annunciation, Paramus
website: https://www.annunciationchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/639
publication: ['url:https://www.church-bulletin.org/church-of-the-annunciation-paramus-nj-07652']
group: Planning Area B
evidence:
- url: https://www.church-bulletin.org/bulletin/church-of-the-annunciation-paramus-nj-07652/2026-11-01.pdf
  seen: 2026-11-03
  quote: Welcome to the Parish Family of the Church of the Annunciation
  note: '1 November 2026 issue (6 pages, text layer). Page 1 masthead: ''50 West Midland Avenue | Paramus
    | New Jersey 07652'', ''November 1, 2026''. Page 2 Mass intentions: Sat 5:00 p.m.; Sun 8:00 a.m.,
    11:00 a.m., 5:30 p.m.; weekdays 7:30 a.m. Page 6 footer: ''639 Church of the Annunciation, Paramus,
    NJ (B) John Patrick Publishing, Inc.'''
- url: https://church-bulletin.org/639
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/church-of-the-annunciation-paramus-nj-07652, ''Church of the
    Annunciation Bulletin'': dated issues 2026-11-01, 10-25, 10-18, 10-11, 10-04.'
- url: https://www.annunciationchurch.org/bulletins-1
  seen: 2026-11-03
  note: 'eCatholic page (read with visit.py; probe get gets 403): ''Click here for the Current Bulletin''
    links http://www.jppc.net/onlinebulletins/639template.pdf. The site''s /bulletins page (''Bulletin
    Archives'') lists no files.ecatholic.com issues, and issues.py ecatholic:20359 found none for 18 Oct-1
    Nov 2026.'
bulletin_status: available
publication_reviews:
- parish: our-lady-of-the-visitation-paramus
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/church-of-the-annunciation-paramus-nj-07652/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names the Church of the Annunciation alone, with its own Mass intentions;
      John Patrick id 639. The joint OLV-Annunciation bereavement ministry is announced in both bulletins.
  - url: http://sponsors.bonventure.net/pdfs/4283/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of the Visitation alone, with its own Mass schedule;
      Bon Venture page 4283.
---

## Publisher

The Church of the Annunciation, Paramus, publishes a weekly bulletin printed by John Patrick Publishing (id 639). I read the 1 November 2026 issue: page 1 masthead 'Welcome to the Parish Family of the Church of the Annunciation, 50 West Midland Avenue | Paramus | New Jersey 07652', with Rev. Jungsoo Kim as temporary administrator; page 6 footer '639 Church of the Annunciation, Paramus, NJ (B) John Patrick Publishing, Inc.'. One set of Mass intentions, for one church. Page 2 mentions a bereavement ministry co-sponsored with Our Lady of the Visitation and held at the OLV rectory: a joint ministry, not a shared bulletin (OLV prints its own with Bon Venture).

## Worship sites

- Church of the Annunciation, 50 West Midland Avenue (`annunciation-paramus`): Saturday 5:00 PM; Sunday 8:00 AM, 11:00 AM, 5:30 PM; weekdays 7:30 AM (page 2 intentions, 31 October to 8 November).

The directory (167) and GCatholic (18533) list only this church. GCatholic's Carmelite chapel of St. Therese at Bergen Mall (18535) is not this parish's and closed in 2017 (`excluded/st-therese-chapel-bergen-mall-paramus`); the bulletin does not mention it.

## Website and bulletin provider

https://www.annunciationchurch.org/ is an eCatholic site (ecatholic:20359, behind Cloudflare: probe get 403, visit.py loads it). Its bulletin is not on files.ecatholic.com: the 'Bulletin' page (/bulletins-1) links the John Patrick template jppc.net/onlinebulletins/639template.pdf, which leads to the church-bulletin.org listing. So the provider is `other`, read with `page-pdfs https://church-bulletin.org/639`, and the eCatholic site id is left out of `publication` (it identifies the website, not the bulletin).

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/639: current` and picked church-bulletin.org/bulletin/church-of-the-annunciation-paramus-nj-07652/2026-11-01.pdf, the 1 November 2026 issue read above (date from the text, "November 1, 2026"); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row. The text layer has no Mass schedule box; the times above are from the intentions list.
