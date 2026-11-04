---
name: St. Patrick Pro-Cathedral, Newark
website: https://www.spnewark.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://www.church-bulletin.org/saint-patrick-s-pro-cathedral-newark-nj-07102']
group: Planning Area I
evidence:
- url: https://www.spnewark.com/worship-schedule
  seen: 2026-11-04
  quote: Saturday 4:00 pm - Vigil Mass (English) in the Main Church
  note: Squarespace site. The schedule page gives Saturday 4:00 pm, Sunday 9:00 am (English) and 11:30
    am (Spanish), daily Mass Monday to Friday 12:15 pm, and says to check Facebook or Instagram for changes.
    No page of the site (home, worship-schedule, resources-1, welcome, about, contact) links a bulletin
    or any PDF.
- url: https://www.spnewark.com/contact
  seen: 2026-11-04
  quote: 91 Washington Street, Newark, NJ 07102
  note: 'Contact page: church at 91 Washington Street, ''Saint Patrick’s Rectory / Convent 39 Bleeker
    Street'', phone (973) 623-0822 (the number GCatholic gives for St. John, 22 Mulberry St).'
- url: https://church-bulletin.org/672
  seen: 2026-11-04
  quote: Readings for the Week of November 1, 2026
  note: 'John Patrick listing 672 redirects to saint-patrick-s-pro-cathedral-newark-nj-07102 (''Saint
    Patrick''s Pro-Cathedral, Newark, NJ 07102'', 91 Washington Street) and shows only the week''s readings:
    no bulletin posted. 672A, 672B, 672J and 672O are JP''s generic archive page.'
- url: https://rcan.org/clergy-appointments-december-2021/
  seen: 2026-11-04
  quote: appointed pastor of Saint Patrick Pro Cathedral, Newark and Saint John Parish, Newark effective
    September 8, 2021 and ending June 30, 2027
  note: Shared pastor with St. John, Newark (st-john-newark).
- url: https://rcan.org/clergy-appointments-july-2026/
  seen: 2026-11-04
  quote: Reverend Juan Alexander Ortega-Ortiz has been appointed temporary administrator of Saint Patrick
    ProCathedral, Newark, effective September 7, 2026, and ending November 30, 2026
  note: This post names only St. Patrick.
revisit: Recheck https://church-bulletin.org/672 for a posted bulletin (and the site for a bulletin link);
  if one appears, set provider other with page-pdfs on the listing.
revisit_after: 2027-01-04
research:
- method: John Patrick listing 672 (found in 029-map jp-400-799.tsv by town) and letter-suffixed listings
    672A/B/J/O
  url: https://church-bulletin.org/672
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the listing for an uploaded issue; if one appears, pin page-pdfs https://church-bulletin.org/672,
    run fetch:check and set provider other
  retry_when: The listing shows a bulletin issue rather than only the readings
  revisit_after: 2027-01-04
- method: probe po on guessed ParishesOnline slugs st-patrick-pro-cathedral-07102, st-patricks-pro-cathedral-07102,
    st-patrick-church-07102
  checked: '2026-11-04'
  outcome: not-found
  next_action: Try visit.py on the site's Facebook page for a posted bulletin
  retry_when: A source names a publisher or the site adds a bulletin link
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish's Squarespace site (https://www.spnewark.com/) gives its Mass schedule but links no bulletin or PDF on any page read on 4 November 2026 (home, worship-schedule, resources-1, welcome, about, contact). Its John Patrick Publishing listing, church-bulletin.org/672 ('Saint Patrick's Pro-Cathedral, Newark, NJ 07102'), shows only the week's readings, which is how JP shows a parish that posts nothing. Guessed ParishesOnline slugs found no org. The listing URL is kept in `publication` so a later bulletin there is recognised.

St. Patrick and St. John (22 Mulberry St) shared a pastor (rcan.org, December 2021, to 30 June 2027) and share the phone (973) 623-0822, so the batch checked for one bulletin covering both: none was found for either. St. Patrick's own schedule names only the Main Church; it does not list St. John's Masses. St. John is its own `no_bulletin` row (`st-john-newark`). If a bulletin turns up that covers both, merge.

## Worship sites

`st-patrick-pro-cathedral-newark`, 91 Washington Street (worship-schedule page, 4 November 2026: Saturday 4:00 pm, Sunday 9:00 am and 11:30 am, weekdays 12:15 pm). The directory's address (39 Bleeker Street) is the rectory/convent, per the contact page.

## Website and bulletin provider

`no_bulletin` (Settled policy 4: kept in the records, off the site). The website is the parish's own site.

## Not yet confirmed

Whether the parish posts a bulletin on Facebook or Instagram (the schedule page points there for changes): not checked. See `research` and `revisit`.
