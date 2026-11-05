---
name: Our Lady of Fatima & St. Nicholas
website: https://fatimanicholas.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055
publication: ['url:https://www.church-bulletin.org/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055',
  'ecatholic:14272']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055/2026-11-01.pdf
  seen: 2026-11-05
  quote: 153 Washington Place, Passaic, NJ 07055
  note: 'Page 1 of the 1 November 2026 issue (Solemnity of All Saints): masthead OUR LADY OF FATIMA &
    SAINT NICHOLAS RC CHURCH, 153 Washington Place, Passaic; Rev. Rolands Uribe, Pastor; one Mass schedule:
    Saturday 4:00 PM English, 7:00 PM; Sunday (Spanish) 9:00 AM, 10:30 AM, 12:00 PM, 1:30 PM; Monday to
    Friday 7:00 PM Spanish. No other church is named.'
- url: https://files.ecatholic.com/14272/bulletins/20261018.pdf
  seen: 2026-11-05
  quote: 641 Our Lady Fatima / St. Nicholas, Passaic, NJ John Patrick Publishing Company
  note: The 18 October 2026 copy on the parish's eCatholic site, page 6 ad footer; page 1 masthead gives
    153 Washington Pl., Passaic and the same Mass schedule. A grep of all 6 pages finds no Exchange Place
    and no chapel.
- url: https://church-bulletin.org/?id=641
  seen: 2026-11-05
  note: JPP customer 641 redirects to https://www.church-bulletin.org/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055,
    titled Our Lady of Fatima & Saint Nicholas Roman Catholic Church Bulletin, listing weekly issues 2024-11-10
    to 2026-11-01.
- url: https://fatimanicholas.org/bulletins
  seen: 2026-11-05
  note: 'eCatholic site 14272 (read with visit.py): the Bulletin page lists files.ecatholic.com/14272/bulletins/
    issues, newest October 18, 2026; issues.py found no file for 25 October, 1 or 8 November (403). Site
    footer: 153 Washington Pl, Passaic, NJ 07055.'
- url: https://files.ecatholic.com/14272/bulletins/20220612.pdf
  seen: 2026-11-05
  quote: St. Nicholas R.C. Church
  note: '12 June 2022 issue, page 1 sidebar: St. Nicholas R.C. Church, 153 Washington Pl.; Office: Our
    Lady of Fatima R.C. Church, 32 Exchange Place; same weekend schedule as today.'
bulletin_status: available
---

## Publisher

Our Lady of Fatima and St. Nicholas, Passaic (merged 2022) publishes one weekly bulletin through John Patrick Publishing (customer 641), posted on church-bulletin.org and copied to the parish's eCatholic site. Page 1 of the 1 November 2026 issue (`https://www.church-bulletin.org/bulletin/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055/2026-11-01.pdf`, read 2026-11-05) has the masthead "OUR LADY OF FATIMA & SAINT NICHOLAS RC CHURCH, 153 Washington Place, Passaic, NJ 07055", Rev. Rolands Uribe, Pastor, and one Mass schedule. The 18 October 2026 eCatholic copy's footer reads "641 Our Lady Fatima / St. Nicholas, Passaic, NJ John Patrick Publishing Company".

## Worship sites

- `st-nicholas-passaic`: St. Nicholas church, 153 Washington Place, the address in the masthead. The schedule (Saturday 4:00 PM English, 7:00 PM; Sunday Spanish 9:00, 10:30, 12:00, 1:30; Monday-Friday 7:00 PM) names no other place. The 12 June 2022 issue already gave "St. Nicholas R.C. Church 153 Washington Pl." with the same weekend times, and "Office: Our Lady of Fatima R.C. Church 32 Exchange Place".

The former Our Lady of Fatima church, 32 Exchange Place (GCatholic 18995, and the finder pin directory:14272), appears in no current schedule; the legacy St. Nicholas site (`https://1j1pea.sites.ecatholic.com/`, eCatholic 14090, trial expired June 2023, read 2026-11-05) gives it as "Office/Mailing Address: 32 Exchange Pl." No source read says the building closed, so it is in `open/our-lady-of-fatima-passaic` rather than `excluded/`. The finder's two pins: directory:14272 (the merged parish, pinned at 32 Exchange Place) and directory:14090 (St. Nicholas, Passaic, the pre-merger entry with the same Mass schedule at 153 Washington Place). Both carry the one schedule the bulletin gives for St. Nicholas church, so both are linked to `st-nicholas-passaic`.

## Website and bulletin provider

The website is the parish's eCatholic site (site id 14272), whose Bulletin page lists eCatholic copies up to 18 October 2026; `issues.py ecatholic ecatholic:14272` found none for 25 October-8 November (403), while the John Patrick listing has 25 October and 1 November. So the row reads the John Patrick listing: provider `other`, recipe `page-pdfs https://www.church-bulletin.org/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055`. `fetch:check` on 2026-11-05 picked the 1 November 2026 issue ("page-pdfs on https://www.church-bulletin.org/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055: current", 4 days old; identity unverified as no expected identity is supplied). `ecatholic:14272` is kept in `publication` because its files are copies of this bulletin. The legacy site ecatholic:14090 posts no bulletin and is not recorded as a publication.

## Not yet confirmed

Whether any Mass is still celebrated in the former Our Lady of Fatima church at 32 Exchange Place: see `open/our-lady-of-fatima-passaic`.
