---
name: Holy Spirit
website: https://holyspiritparishnj.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:30384', 'po-container:04/1007']
group: ''
evidence:
- url: https://files.ecatholic.com/30384/bulletins/20261025.pdf
  seen: 2026-11-04
  quote: Holy Spirit, Pequannock, NJ
  note: '25 October 2026 issue (page 2: ''October 25, 2026 Thirtieth Sunday in Ordinary Time''). Page
    1 masthead: MASS TIMES DAILY(M-F) 8:30 AM; SATURDAY 5:00 PM; SUNDAY 7:30 & 10:00 AM, 7:00 PM; www.holyspiritparishnj.org;
    FR. CESAR JARAMILLO PASTOR. Page 2 LITURGY FOR THE WEEK lists those Masses for 24-30 October. The
    quote is the page 5 LPi ad footer, ''Holy Spirit, Pequannock, NJ 04-1007''.'
- url: https://holyspiritparishnj.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py. eCatholic bulletin archive, newest link 'October 25, 2026'
    -> files.ecatholic.com/30384/bulletins/20261025.pdf, then weekly back through 2026. The site also
    links a bimonthly 'HS Newsletter' in documents/ (latest Vol 11 No 3, May-August 2026), which is not
    the weekly bulletin.
- url: https://container.parishesonline.com/bulletins/04/1007/20261108B.pdf
  seen: 2026-11-04
  note: 'probe container 04/1007: the same LPi bulletin, 8 November 2026 issue, page 1 identical masthead
    (MASS TIMES ... www.holyspiritparishnj.org ... FR. CESAR JARAMILLO). No ParishesOnline org slug found
    (probe po on holy-spirit-church-07440 and variants: no such organization).'
research:
- method: probe po on org slugs holy-spirit-church-07440, holy-spirit-07440, holy-spirit-pequannock, holy-spirit-parish-07440,
    holy-spirit-roman-catholic-church-07440, holy-spirit-catholic-church-07440, holy-spirit-rc-church-07440;
    ParishesOnline API search?q=
  checked: '2026-11-04'
  outcome: not-found
  next_action: Find the ParishesOnline org for container 04/1007 (an LPi widget id on the parish site
    or a parishesonline.com link) and switch the row to parishes_online, which posts issues earlier than
    the eCatholic copies
  retry_when: An org slug or LPi id for container 04/1007 turns up, or the eCatholic copies stop being
    posted
- method: Reconcile fetch:check and visit.py --links on /bulletins (upload stamps), with probe get on
    LPi container 04/1007
  url: https://holyspiritparishnj.org/bulletins
  checked: '2026-11-05'
  outcome: found
  next_action: Find the ParishesOnline org for container 04/1007 and switch the row to parishes_online;
    until then fetch takes the eCatholic copy
  retry_when: An org slug or LPi id for container 04/1007 turns up
bulletin_status: available
---

## Publisher

Holy Spirit, Pequannock publishes its own weekly LPi bulletin. The 25 October 2026 issue on its eCatholic site (`https://files.ecatholic.com/30384/bulletins/20261025.pdf`, read 2026-11-04) has on page 1 the parish's MASS TIMES, website www.holyspiritparishnj.org and pastor "FR. CESAR JARAMILLO"; page 2 is dated "October 25, 2026 Thirtieth Sunday in Ordinary Time"; the LPi ad footer reads "Holy Spirit, Pequannock, NJ 04-1007". The same bulletin is in LPi's container 04/1007, whose 8 November 2026 issue has the same page 1.

## Worship sites

- `holy-spirit-pequannock`: the only church. Page 1's MASS TIMES (daily M-F 8:30 AM; Saturday 5:00 PM; Sunday 7:30 & 10:00 AM, 7:00 PM) and page 2's LITURGY FOR THE WEEK name no other place.

The finder has two pins for this parish, directory:30384 (the eCatholic site id, no address) and directory:5732 (318 Newark-Pompton Tpke); GCatholic lists Holy Spirit (18968). Our Lady of Fatima Chapel, 32 W Franklin Ave, Pequannock (GCatholic 38951), is the FSSP's Latin Mass chapel with its own bulletin; this bulletin does not mention it (grep "Fatima": no hits), so it is a row of its own (`our-lady-of-fatima-chapel-pequannock`).

## Website and bulletin provider

`holyspiritparishnj.org` is the parish's eCatholic site (id 30384, the finder pin id), and `probe url` reads it. Its /bulletins page lists weekly issues as `files.ecatholic.com/30384/bulletins/<YYYYMMDD>.pdf`; on 2026-11-04 the newest was 25 October (1 and 8 November answered 403). Provider `ecatholic` from the website; `fetch:check` on 2026-11-04 picked `20261025.pdf` (10 days old: fresh). The LPi container 04/1007 already had the 8 November issue, but no ParishesOnline org was found for it, so `fetch` can't read it by org slug (see research). The container id is recorded as a publication form of this bulletin. Reconcile's fetch:check on 2026-11-05 again picked the 25 October copy while the container had 1 and 8 November. The `?t=` upload stamps on /bulletins show the site posts in batches, one to three weeks late: 27 September, 4 and 11 October all uploaded on 12 October, then 18 and 25 October on 28 October. So the live row will usually trail the printed bulletin by a week or more, and it will stay that way until the container's org slug is found.

## Not yet confirmed

- The ParishesOnline org for container 04/1007 (see research). The eCatholic copies lag: the 1 November issue was not posted by 4 November.
