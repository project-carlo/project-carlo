---
name: Holy Spirit & St. Joseph's
website: https://holyspirit-saintjoseph.org
bulletin_provider: parishes_online
provider_id: st-josephs-catholic-church-and-church-of-the-holy-spirit
publication: ['po-org:st-josephs-catholic-church-and-church-of-the-holy-spirit', 'lpi:0018000000Qc1XLAAZ',
  'po-container:06/0030']
group: 'Cluster: Holy Spirit (Webster) and St. Joseph''s (Penfield)'
evidence:
- url: https://container.parishesonline.com/bulletins/06/0030/20261004B.pdf
  seen: 2026-10-02
  quote: St. Joseph’s Catholic Church and Church of the Holy Spirit 06-0030
  note: 'LPi footer on the ad pages (10-12) of the 4 October 2026 issue, container 06/0030. Pages 1-9
    are images; rendered with render.py, page 1 is headed "HOLY SPIRIT - ST. JOSEPH’S, OCTOBER 4, 2026
    | 27TH SUNDAY IN ORDINARY TIME" and page 2 gives "REGULAR MASS SCHEDULE" for both churches (Holy Spirit:
    Saturday Vigil 4:00 pm, Sunday 8:30 am & 10:30 am, weekdays Monday - Friday 9:00 am; St. Joseph’s:
    Saturday Vigil 4:30 pm, Sunday 8:00 am, 9:30 am, 11:00 am, 5:00 pm, weekdays Monday - Saturday 9:00
    am). recheck cannot find the image text.'
- url: https://ps.dor.org/directory/church-of-the-holy-spirit/
  seen: 2026-10-02
  quote: Cluster (St. Joseph's)
  note: 'Directory of Parishes listing for Holy Spirit: a cluster with St. Joseph''s, one pastor (Very
    Rev. James A. Schwartz), one combined Mass schedule, and "Weekly Bulletin Website: https://holyspirit-saintjoseph.org/".'
- url: https://ps.dor.org/directory/st-josephs/
  seen: 2026-10-02
  quote: Cluster (Church of the Holy Spirit Church)
  note: 'Directory of Parishes listing for St. Joseph''s: the same cluster and the same combined schedule.
    Its website field is https://www.sjcpenfield.com/.'
- url: https://sjcpenfield.com/lander
  seen: 2026-10-02
  note: 'sjcpenfield.com, the site the Parish Locator and the Directory give for St. Joseph''s, is now
    a parked domain (a registrar parking-lander page with no parish content; probe url: NO-PARISH-WORDS,
    visit.py lands on /lander).'
- url: https://parishesonline.com/organization/st-josephs-catholic-church-and-church-of-the-holy-spirit
  seen: 2026-10-02
  note: 'probe po: organization ''St. Joseph''s Catholic Church and Church of the Holy Spirit'', website
    https://www.holyspirit-saintjoseph.org/, address 43 Gebhardt Road, Penfield; issues 2026-10-04, 09-27,
    09-20 in container 06/0030.'
promoted: 2026-10-02
---

## Publisher

One bulletin for both churches. The 4 October 2026 issue (ParishesOnline container 06/0030) is
headed "HOLY SPIRIT - ST. JOSEPH'S" and its "Regular Mass Schedule" lists both churches
(Holy Spirit, Webster, and St. Joseph's, Penfield). Its LPi footer reads "St. Joseph's
Catholic Church and Church of the Holy Spirit 06-0030". Pages 1-9 of the PDF are images
(pages 10-12, ads, have text), so the pipeline will need the image path for this bulletin.

**One bulletin or two (the lead).** One. The Parish Locator lists St. Joseph (43 Gebhardt Rd)
as its own group with site `sjcpenfield.com`, and Holy Spirit separately. But the diocese's
Directory of Parishes lists both as one cluster ("Cluster (St. Joseph's)", same pastor, same
combined Mass schedule), the parish's own site `holyspirit-saintjoseph.org` is the "Weekly
Bulletin Website" on both listings, the only ParishesOnline organization is the joint one, and
`sjcpenfield.com` is now a parked domain. There is no separate St. Joseph's bulletin to
publish. The locator's separate listing is stale.

## Worship sites

Two: `holy-spirit` (1355 Hatch Road, Webster) and `st-josephs` (43 Gebhardt Road, Penfield).
Both appear in the 4 October Mass schedule. Nothing else is listed for the cluster.

## Website and bulletin provider

`holyspirit-saintjoseph.org` is behind Cloudflare (probe url 403, visit.py BLOCKED on every
load in this session), but ParishesOnline names it as the organization's website and the
directory names it as the bulletin website. fetch reads ParishesOnline by `provider_id`, so
the site does not need to load. The PO organization slug, LPi id and container were read with
`probe po`.

## Not yet confirmed

The parish site itself was never read (Cloudflare). The weekday and Sunday times above come
from page 2 of the bulletin as an image and from the Directory listing. The Directory
listing is dated 1/27/25; the bulletin is current.
