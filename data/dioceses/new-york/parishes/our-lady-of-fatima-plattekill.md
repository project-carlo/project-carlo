---
name: Our Lady of Fatima - Plattekill
website: https://olfplattekill.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/493
publication: ['url:https://church-bulletin.org/493']
group: ''
evidence:
- url: https://church-bulletin.org/493/2026-10-04.pdf
  seen: 2026-10-08
  quote: 27th Sunday in Ordinary Time, October 3rd & 4th, 2026
  note: Current JPPC 493 issue, page 1; linked from the parish bulletin page.
- url: https://church-bulletin.org/493/2026-10-04.pdf
  seen: 2026-10-08
  quote: |-
    Saturday Vigil: 5:00pm (Vespers/Adoration 4:30pm)
    Sunday: 8:30am (Lauds/Adoration 8:00am)
    & 11:00am (English)12:30pm (Spanish)
  note: October 4, 2026 issue, page 1, public Mass schedule.
- url: https://olfplattekill.org/bulletins-1?research=20261008
  seen: 2026-10-08
  quote: http://www.jppc.net/onlinebulletin/493template.pdf
  note: Official bulletin page, read October 8; identifies JPPC 493 despite the stale template URL.
- url: https://church-bulletin.org/493
  seen: 2026-10-08
  quote: October 11, 2026 Bulletin
  note: Pinned page-pdfs collector replayed against the complete freshly fetched HTTP HTML, without homepage
    discovery. It selected the already-posted October 11 issue; the selected PDF downloaded HTTP 200 with
    six pages. This is an HTTP snapshot replay plus direct PDF download, not a live browser fetch:check.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-wallkill-ny-12589/2026-10-11.pdf
  seen: 2026-10-08
  note: Complete October 11 issue downloaded and read. Holy Rosary image-only page 1 was rendered and
    visually read; the other issues have extractable text. Future issue already posted on October 8, not
    a claim that October 11 Masses occurred.
promoted: 2026-10-11
---

## Publisher

The parish bulletin page explicitly links JPPC 493. The actual October 3/4, 2026 issue was read at church-bulletin.org/493/2026-10-04.pdf, with current parish Mass intentions and schedule. Its public timetable agrees with the live Our Lady of Fatima website. The earlier failed template is superseded by an actual readable issue, not a no-bulletin finding.

## Worship sites

Our Lady of Fatima in Plattekill holds Saturday vigil 5 PM and Sunday 8:30/11 AM and 12:30 PM Spanish. No second venue is asserted from the publisher account.

## Website and bulletin provider

The supported recipe is `page-pdfs https://church-bulletin.org/493`. It starts at the parish-specific JPPC archive, not at a general parish homepage, and pins the collector. On October 8, 2026, replay of the complete freshly fetched archive HTML through the repository resolver selected `https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-wallkill-ny-12589/2026-10-11.pdf` as current (October 11, already posted). The selected file downloaded HTTP 200, six pages, and its actual parish content was checked. Holy Rosary page 1 was read visually because its pages are scans; no image-only-text extraction claim is made. The other issues contain readable text.

The initial abbreviated Mozilla user agent received HTTP 406 from these JPPC pages; a complete current Chrome user agent with HTML Accept/Accept-Language headers returned the genuine archive and PDF. Holy Rosary also loaded in owned T3 tab tab_4. This access distinction is not a publisher failure. The test used HTTP snapshots and direct PDF downloads, not another browser or a live fetch:check. No CSV promotion is performed here.
