---
name: St. Ann and Holy Angels
website: https://17009.sites.ecatholic.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:17009']
group: ''
evidence:
- url: https://files.ecatholic.com/17009/bulletins/20260927.pdf
  seen: 2026-09-30
  note: 'Image-only PDF (one sheet, no text layer), read with parish-site-access render.py, so `recheck` cannot find text in it. The 27 September 2026 issue, inside page: "26th Sunday In Ordinary Time / September 26-27, 2026 / Sat. 4:00 PM (SA) People of the Parish / Sat. 8:00AM(SA) ... Sun.10:00AM(HA)", weekday intentions 8:00AM (SA) Monday and Thursday, 8:00AM (HA) Tuesday and Wednesday, a "FEAST OF HOLY ANGELS TRIDUUM MASSES" box (29 and 30 September 8am Holy Angels Church, 1 October 8am St. Ann Church), and "Giving Reports / St Ann: ... Holy Angels: ..." and a cover reading "Holy Angels & St. Ann''s Parish Families invite you to Holy Angels Harvest Dinner ... Holy Angels Hall, Altona".'
- url: https://17009.sites.ecatholic.com/mass-schedule
  seen: 2026-09-30
  quote: 'Saturday: 4:00 PM St. Ann''s, Mooers Forks'
  note: 'Parish website Mass Schedule page (eCatholic, behind Cloudflare; read in a browser with parish-site-access visit.py on 2026-09-30, so `recheck` reports it unreachable). It continues "Sunday: 8:00 AM St. Ann''s, Mooers Forks / 10:00 AM Holy Angels, Altona / Monday: 8:00 AM St. Ann''s, Mooers Forks / Tuesday: 8:00 AM Holy Angels, Altona / Thursday: 8:00 AM St. Ann''s, Mooers Forks / Friday: 8:00 AM Holy Angels, Altona".'
- url: https://17009.sites.ecatholic.com/our-parishes
  seen: 2026-09-30
  quote: Holy Angels Church 522 Devils Den Road Altona, NY 12910
  note: 'Parish website "Our Parishes" page (same caveat): "St. Ann''s Church 3066 State Route 11 Mooers Forks, NY 12959" and "St. Ann and Holy Angels Offices 24 Town Hall Road Mooers Fork, NY 12959 Phone: 518-236-5632", email mooersforkssec@rcdony.org. The site''s title is "ST. ANN and HOLY ANGELS, Altona and Mooers Forks".'
- url: https://discovermass.com/church/angels-and-saints-champlain-ny/
  seen: 2026-09-30
  note: 'Discover Mass page "Angels and Saints" (URL says Champlain, address is 3062 U.S. Route 11, Mooers Forks, website 17009.sites.ecatholic.com): Mass Times "Saturday 4:00pm, Sunday 8:00am, Monday 8:00am, Thursday 8:00am" and no bulletins. A listing for St. Ann only; it confirms the website id belongs to this parish.'
- url: https://www.rcdony.org/parish/altona
  seen: 2026-09-30
  note: 'Directory: directory:altona (Church of the Holy Angels, 522 Devils Den Road, Altona) and directory:mooers-forks (St. Ann''s Church, 3062 Route 11, Mooers Forks) both give website https://17009.sites.ecatholic.com/, phone 518-236-5632 and pastor Reverend Pedro Edgardo (Jay) N.; no group is recorded.'
---

## Publisher

One weekly bulletin on eCatholic site 17009 (`files.ecatholic.com/17009/bulletins/YYYYMMDD.pdf`, newest 27 September 2026 read on 2026-09-30; 4 October not yet posted) covers two churches, St. Ann's (Mooers Forks) and Holy Angels (Altona). The 27 September issue is a single image sheet whose Mass intentions are coded "(SA)" and "(HA)" and whose giving report has one column per church; its cover flyers are headed "Holy Angels & St. Ann's Parish Families" and "St. Ann's & Holy Angels Parishes". The parish website is titled "ST. ANN and HOLY ANGELS, Altona and Mooers Forks" and gives one office (24 Town Hall Road, Mooers Forks), one phone (518-236-5632) and one pastor (Rev. Pedro Edgardo (Jay) N.). The diocese's directory lists the two churches separately but with the same website, phone and pastor. **One row, two churches.** The bulletin is image-only, so the pipeline will need to read it as an image.

## Worship sites

- `holy-angels-altona` (522 Devils Den Road): Sunday 10:00 AM, Tuesday and Friday 8:00 AM.
- `st-ann-mooers-forks` (3062 Route 11): Saturday 4:00 PM, Sunday 8:00 AM, Monday and Thursday 8:00 AM.

Not here, and why no record is a church: GCatholic still lists **St. Joseph, 83 Maple St., Mooers** (18307; its website `stannstjoseph.rcdony.org` is this parish's old domain) and **St. Louis of France, 8965 Route 22, Chazy 12992** (18333; GCatholic gives Holy Angels' old phone 518-236-5848; Wikipedia's parish list calls it a mission of Altona at Sciota). Neither appears in the bulletin's schedule or on the parish website, and nothing read says when or whether they closed: `open/st-joseph-mooers` and `open/st-louis-of-france-sciota`. The ParishesOnline organization "St. Ann & St. Joseph Church" (PO Box 89, Mooers Forks; website annandangels.org, DEAD-DNS) publishes nothing. The two parishes were "St. Ann's-St. Joseph's (Mooers), established in 1992 from a merger of both churches" according to Wikipedia's list of Ogdensburg parishes (not a primary source).

## Website and bulletin provider

`17009.sites.ecatholic.com` is the directory's website for both churches; it is behind Cloudflare (`probe url` HTTP4XX) and loaded with `visit.py` on the eighth load. The eCatholic site id 17009 was confirmed by `visit.py`, and the issue by `issues.py ecatholic ecatholic:17009` (27 September 2026 answers 200). The eCatholic site id is the `publication`; the provider id stays empty.

## Not yet confirmed

- St. Joseph (Mooers) and St. Louis of France (Sciota): see the two open records.
