---
name: Our Lady of Mercy Parish
website: https://www.ourladyofmercychurch.org
bulletin_provider: discover_mass
provider_id: our-lady-of-mercy-harborcreek-pa
publication: ['discovermass:our-lady-of-mercy-harborcreek-pa']
group: ''
evidence:
- url: https://discovermass.com/church/our-lady-of-mercy-harborcreek-pa/
  seen: 2026-10-23
  quote: Weekend Mass Schedule
  note: 'Current-bulletin download from the Discover Mass church page (cover image class ''bulletin-cover
    X-|2026-10-25|1792766660|3528'': bulletin number 3528, dated 2026-10-25; 6 pages). Page 1 reads ''October
    25, 2026 - The Thirtieth Sunday in Ordinary Time'', ''Our Lady of Mercy Church'', ''MASS TIMES Weekend
    Mass Schedule: Saturday 4:30 p.m.; Sunday 9:30 a.m.; Weekday: Tuesday-Friday 8:30 a.m.; Confessions:
    Saturday 3:45 p.m.'', ''837 Bartlett Rd. Harborcreek, PA 16421'', ''Rev. Matthew Kujawinski, Pastor''.
    The page lists Oct 25, 18, 11, 4 and Sep 27 and earlier issues in its archive.'
- url: https://www.ourladyofmercychurch.org/
  seen: 2026-10-23
  note: 'probe url: HTTP 200, title ''Our Lady of Mercy Parish | Harborcreek, Pa'', embeds discovermass:our-lady-of-mercy-harborcreek-pa;
    no other bulletin channel found on the page.'
- url: https://www.eriercd.org/Parish10204-Our-Lady-of-Mercy.html
  seen: 2026-10-23
  note: 'Diocese directory record 10204 (GCatholic 24454): one parish record, no mission, partner or secondary
    church. Sat 4:30 p.m.; Sun 9:30 a.m.; Tuesday through Friday 8:30 a.m.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Kujawinski, Rev. Matthew J.
  note: 'Clergy list ''Updated 8/7/2026'': ''Pastor ... Our Lady of Mercy, Harborcreek, 837 Bartlett Road''.
    No other assignment.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish our-lady-of-mercy-harborcreek --expected-identity Kujawinski
    (headed Chrome); first try with 'Our Lady of Mercy' did not match the first-page text
  url: https://discovermass.com/church/our-lady-of-mercy-harborcreek-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok and a PDF; identity matched on the pastor's surname (the phrase 'Our
    Lady of Mercy' is in the PDF's page-1 text but did not match, probably a layout split); issue date
    reads 'unknown' because the masthead date 'October 25, 2026 — The Thirtieth Sunday' uses an em dash.
    I confirmed date and number 3528 by reading the downloaded PDF and the cover class on the church page.
    Not a failure.
- method: 'pnpm fetch:check --diocese erie (headed Chrome), final fetch check; Discover Mass download.php
    returned a 134-byte body (curl of the same URL: ''Maximum number of files downloaded today. Please
    contact Discover Mass for support.'')'
  checked: '2026-10-23'
  outcome: access-blocked
  next_action: Re-run fetch:check for this row after the Discover Mass per-IP daily cap resets; do not
    retry in a loop. Resolution of the church page and the download URL succeeded, so only the PDF download
    (document type, identity and issue date) is unverified in this run; see earlier evidence for the identity
    read by the scout.
  retry_when: Discover Mass daily cap resets
---

## Publisher

Our Lady of Mercy Parish, Harborcreek (837 Bartlett Rd., 16421) publishes its own weekly bulletin, which its website serves through Discover Mass (church page `our-lady-of-mercy-harborcreek-pa`, no ParishesOnline organization found). I downloaded the current issue on 2026-10-23 from the church page: bulletin number 3528, dated 25 October 2026, 6 pages, masthead 'Our Lady of Mercy Church' with the Bartlett Road address, Mass times and parish staff headed by Rev. Matthew Kujawinski, Pastor (clergy list agrees). Content is this parish's alone. The directory lists a single parish record with no mission, partner or secondary church.

## Worship sites

One church, Our Lady of Mercy at 837 Bartlett Rd. Mass times in the 25 Oct issue: Saturday 4:30 p.m., Sunday 9:30 a.m., Tuesday-Friday 8:30 a.m. (Monday 26 Oct 'NO MASS'); confessions Saturday 3:45 p.m.

## Website and bulletin provider

`ourladyofmercychurch.org` embeds the Discover Mass church page; `fetch` reads it by `provider_id`. One Discover Mass download per IP per day is the cap, so the page was read once.

## Not yet confirmed

Nothing affecting the row.
