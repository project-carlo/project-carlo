---
name: St. Mary, Mother of God Parish
website: https://www.mmog.church/
bulletin_provider: parishes_online
provider_id: saint-mary-mother-of-god-church
publication: ['po-org:saint-mary-mother-of-god-church', 'lpi:0018000000Qc2DQAAZ', 'po-container:03/1430']
group: Cohort 15 (Middletown, Keansburg, Atlantic Highlands)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1430/20261025B.pdf
  seen: 2026-10-30
  quote: 19 Cherry Tree Farm Road Middletown, NJ 07748
  note: '25 October 2026 issue (16 pages; pages 2-13 have a text layer in this issue). Page 4: ''Pastor
    Rev. Jeffrey J. Kegley'', Associate Pastor Rev. Vic Magdaraog, Parochial Vicar Rev. Marcin Kania;
    MASS SCHEDULE: ''Saint Mary, Mother of God Church Saturday Vigil: 5:00 p.m. Sunday: 8:00 a.m., 10:00
    a.m., 12:00 p.m. & 5:00 p.m. Daily Mass Monday through Friday , 8:15 am & 12 pm'' and ''Our Lady of
    the Most Blessed Sacrament Shrine Saturday 8:15 a.m.''. Names St. Mary alone.'
- url: https://container.parishesonline.com/bulletins/03/1430/20261101B.pdf
  seen: 2026-10-30
  note: '1 November 2026 issue (16 pages, pages 1-13 image-only; read from renders of pages 1-2): cover
    ''Saint Mary, Mother of God Church Middletown, New Jersey November 1, 2026''; page 2 ''Fr. Jeff Kegley
    | From the Pastor'', signed ''Father Jeff Kegley, Pastor''. Same org, container 03/1430.'
- url: https://www.mmog.church/bulletin
  seen: 2026-10-30
  quote: Click here for the Current Bulletin
  note: Parish site bulletin page; visit.py --links shows the button goes to https://parishesonline.com/organization/saint-mary-mother-of-god-church.
    The footer reads 'The Parish of Saint Mary 19 Cherry Tree Farm Road Middletown, NJ 07748' and 'Saint,
    Mary, Mother of God Parish'.
- url: https://parishesonline.com/organization/saint-mary-mother-of-god-church
  seen: 2026-10-30
  note: 'probe po saint-mary-mother-of-god-church: lpi 0018000000Qc2DQAAZ, container 03/1430, website
    stmarychurchnj.org, address 19 Cherry Tree Farm Rd., Middletown (New Monmouth) 07748-2390, latest
    issue 2026-11-01.'
- url: https://www.church-bulletin.org/saint-mary-mother-of-god-church-middletown-nj-07748
  seen: 2026-10-30
  note: 'John Patrick listing 678 (Saint Mary, Mother of God Church) has no latest edition in tools/jppc-trenton.tsv
    or the jsonl scan: a dead listing, not a second bulletin.'
- url: https://www.mmog.church/masstimes
  seen: 2026-10-30
  quote: 'Saturday Vigil: 5:00PM'
  note: 'Site''s Mass Times page: ''Sunday: 8:00AM, 10:00AM, 12:00PM & 5:00PM Weekdays: 8:15 AM & 12:00PM''.
    stmarychurchnj.org (the finder''s website) redirects to mmog.church.'
promoted: 2026-10-30
research:
- method: fetch:check on the row, 1 November 2026 issue
  url: https://container.parishesonline.com/bulletins/03/1430/20261101B.pdf
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Read the masthead of the next issues with probe pdf; no action while the row resolves to
    the current issue
  retry_when: An issue over 25,000,000 bytes stops the row being text-checked again, or the parish posts
    a smaller copy of the bulletin on its own site
bulletin_status: available
---

## Publisher

St. Mary, Mother of God (the finder's 'St. Mary R.C. Parish', 19 Cherry Tree Farm Rd, Middletown) publishes its own bulletin through LPi/ParishesOnline (org `saint-mary-mother-of-god-church`, container 03/1430). The 25 October 2026 issue's page 4 gives the staff (Rev. Jeffrey J. Kegley, pastor) and the Mass schedule for the church and for the Our Lady of the Most Blessed Sacrament Shrine; it names no other parish.

## Worship sites

Two: the church at 19 Cherry Tree Farm Rd (`st-mary-mother-of-god-middletown`) and the Our Lady of the Most Blessed Sacrament Shrine, 26 Leonardville Rd, New Monmouth, which GCatholic lists as 'St. Mary' chapel and which the bulletin's Mass schedule gives a Saturday 8:15 a.m. Mass (`our-lady-of-the-most-blessed-sacrament-shrine-new-monmouth`).

## Website and bulletin provider

The finder's stmarychurchnj.org redirects to https://www.mmog.church/ (Squarespace); its Bulletin page's button goes to the ParishesOnline org above. The listing 678 at John Patrick has no edition. Recent issues mix text and image-only pages (1 November: pages 1-13 images); `fetch:check` reports an image-only issue as a pdf with unverified identity.

## Not yet confirmed

The 1 November 2026 issue is 49,157,632 bytes, over `fetch:check`'s 25,000,000-byte inspection limit, so the check passed as `pdf_signature` with no text or identity check (the 25 October issue is 17.6 MB and reads). Identity rests on the masthead read above. The parish site links only the ParishesOnline org, so there is no smaller copy to pin; if issues stay over the limit, ask whether a `page-pdfs` row on a smaller copy exists.
