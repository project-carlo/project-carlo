---
name: St. Genevieve
website: https://www.stgensparish.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-genevieve-catholic-church-flourtown-pa-19031
publication: ['url:https://www.church-bulletin.org/saint-genevieve-catholic-church-flourtown-pa-19031']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-genevieve-catholic-church-flourtown-pa-19031/2026-10-25.pdf
  seen: 2026-10-28
  quote: St. Genevieve Catholic Church
  note: 'John Patrick listing 119, issue of 25 October 2026 (8 pages, text layer). Page 1 masthead: ''St.
    Genevieve Catholic Church, 1225 Bethlehem Pike | Flourtown, PA 19031, 30th Sunday in Ordinary Time,
    October 25, 2026, 215-836-2828, www.stgensparish.com''; one Mass box (Saturday vigil 5pm; Sunday 7:30,
    10:30, 5pm; weekdays). Pastor Rev. Carl F. Janicki. Page 2 Mass intentions list the same times; no
    other church or chapel appears.'
- url: https://www.church-bulletin.org/saint-genevieve-catholic-church-flourtown-pa-19031
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 119 'Saint Genevieve Catholic Church', Flourtown, PA 19031; latest edition October 25,
    2026.
- url: https://www.stgensparish.com/
  seen: 2026-10-28
  note: 'probe url: HTTP 403 (bot block). visit.py (Chrome): loads, title ''St. Genevieve Parish - Flourtown,
    PA'', an eCatholic site (ecatholic:38659 embedded) whose only bulletin link (''Bullletins'') goes
    to https://church-bulletin.org/?id=119; no files.ecatholic.com PDF. So the eCatholic id is not the
    publication.'
promoted: 2026-10-29
bulletin_status: available
---

## Publisher

St. Genevieve, Flourtown (Rev. Carl F. Janicki, Pastor) publishes its own weekly bulletin through John Patrick Publishing, listing 119 ('Saint Genevieve Catholic Church', Flourtown, PA 19031). The 25 October 2026 issue's masthead names St. Genevieve alone, with one Mass schedule (Saturday vigil 5 pm; Sunday 7:30 am, 10:30 am, 5 pm; weekdays Monday 8 am communion service, Tuesday 6:30 am, Tuesday to Friday 8 am). It is a single-church parish; the directory's older Sunday 9 AM and noon Masses no longer appear.

## Website and bulletin provider

`other`, reading `page-pdfs` on the listing. stgensparish.com is an eCatholic site (id 38659) that answers 403 to `probe url` and loads in Chrome, but its Bulletins link goes only to the John Patrick listing, so the eCatholic id stays out of `publication` (Playbook lesson, as for Our Lady of the Sacred Heart, Hilltown).

## Not the same as Saint Miriam

The other Flourtown listing (286, 'Saint Miriam Parish & School', 654 Bethlehem Pike) is an Old Catholic parish, not a Roman Catholic one: see excluded/saint-miriam-parish-flourtown.md. Its bulletin is a different publication from this one.

## Fetch check

`fetch:check` (2026-10-28, headed Chrome) with the `page-pdfs` recipe on the listing picked `https://www.church-bulletin.org/bulletin/saint-genevieve-catholic-church-flourtown-pa-19031/2026-10-25.pdf`: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` only because the check was given no expected identity (the masthead was read from the text layer, above). The check printed no separate recipe; the one in `provider_id` is the one used.
