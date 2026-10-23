---
name: St. Joseph Parish
website: https://www.stjosephwarrenpa.org
bulletin_provider: other
provider_id: page-pdfs https://www.stjosephwarrenpa.org/weeklybulletin.php
publication: ['url:https://www.stjosephwarrenpa.org/weeklybulletin.php#st-joseph-warren']
group: ''
evidence:
- url: https://www.stjosephwarrenpa.org/images/weeklybulletin/b8b4c590a251435c331579a759782d7a.pdf
  seen: 2026-10-23
  quote: Saint Luke Church- 420 North Main Street - Youngsville, PA 16371
  note: 'Page 1 of the issue dated October 25th-October 31st, 2026 (30th Sunday in Ordinary Time; posted
    two days early). Masthead ''Saint Joseph Parish / Saint Joseph Church- 600 Pennsylvania Avenue West
    - Warren, PA 16365'' and ''Saint Luke Church- 420 North Main Street - Youngsville''; Liturgy Schedule
    ''Saturday Vigil: 5:30 PM (St. Joseph) / Sunday: 8:00 AM (St. Luke), 10:00 AM (St. Joseph)* May 1
    through Labor Day Weekend, 10:45 AM (St. Joseph)** September through April''; Reverend Richard C.
    Tomasone, Pastor. Page 2 lists Sunday Mass intentions for both ''(St. Luke)'' and ''(St. Joseph)''.
    Names these two churches and not Holy Redeemer.'
- url: https://www.stjosephwarrenpa.org/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted weeklybulletin.php (scratch/map-erie/tools/weeklybulletin_issues.sh), newest first:
    October 25, 2026 (b8b4c590...pdf), October 18 (60c6d4f4...pdf), October 17 (9496ee9c...pdf, whose
    masthead reads ''28th Sunday in Ordinary Time October 11th-October 17th, 2026'', so the title date
    is the Saturday that week ended, not the issue date). One distinct PDF per issue; the page is current.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ........................................................................................................
    St. Joseph, Warren
  note: 'Clergy list updated 8/7/2026: ''Tomasone, Rev. Richard C. - Pastor - St. Joseph, Warren''. Only
    one assignment, so no shared pastor with Holy Redeemer (O''Hern) or St. John Tidioute (Kalinowski).'
research:
- method: probe url www.stjosephwarrenpa.org; weeklybulletin_issues.sh; probe pdf of the newest issue
  url: https://www.stjosephwarrenpa.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: no ParishesOnline or LPi widget on the site; the diocese-hosted page is the only
    channel.'
- method: pnpm fetch:check --diocese erie --parish st-joseph-warren --expected-identity Tomasone (headed
    Chrome)
  url: https://www.stjosephwarrenpa.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver picked b8b4c590...pdf (October 25-31, 2026, the newest listed): transport
    ok, PDF, identity matched. Issue date ''unknown'' because the masthead gives a date range (''October
    25th-October 31st, 2026''), so overall stays ''unverified'' for that reason only. Recipe is the provider_id.'
publication_reviews:
- parish: holy-redeemer-warren
  decision: separate
  evidence:
  - url: https://www.stjosephwarrenpa.org/images/weeklybulletin/b8b4c590a251435c331579a759782d7a.pdf
    seen: 2026-10-23
    quote: Saint Luke Church- 420 North Main Street - Youngsville, PA 16371
    note: St. Joseph's 25 Oct 2026 masthead covers St. Joseph and St. Luke with Fr. Tomasone; Holy Redeemer's
      25 Oct issue (ParishesOnline 14/0961) is headed Holy Redeemer and St. Anthony of Padua, Sheffield,
      with Fr. O'Hern, and prints its own Mass schedule. The two publish different documents on different
      channels, though they cross-reference joint events (Faith Formation @ HR, All Saints Day coffee
      'at HR and 10:45 am at SJ'). The St. Joseph masthead names St. Joseph and St. Luke; the Holy Redeemer
      masthead names Holy Redeemer and St. Anthony of Padua, Sheffield.
---

## Publisher

St. Joseph Parish, Warren publishes its own weekly bulletin on its diocese-hosted site (`weeklybulletin.php`, one PDF per issue under `images/weeklybulletin/`). The issue dated October 25th-31st, 2026, read on 2026-10-23, is headed 'Saint Joseph Parish', names Saint Joseph Church (600 Pennsylvania Avenue West, Warren) and Saint Luke Church (420 North Main Street, Youngsville), and carries one liturgy schedule for both (Saturday 5:30 PM vigil at St. Joseph; Sunday 8:00 AM St. Luke, 10:45 AM St. Joseph, 10:00 AM from May through Labor Day weekend). Pastor: Rev. Richard C. Tomasone (clergy list updated 8/7/2026).

## Worship sites

Two churches: St. Joseph (parish church) and St. Luke, Youngsville (secondary mission church; the directory and its printable edition of 2026-10-06 list Sunday 8 a.m. there). Holy Redeemer, Warren is a separate parish with its own bulletin (see `publication_reviews`); the two share some events (faith formation 'Warren County Catholic Community', soup kitchen, All Saints Day) but not a bulletin.

## Website and bulletin provider

`other`, read from stjosephwarrenpa.org/weeklybulletin.php (diocese-hosted template, newest first, current to 25 October). Recipe `page-pdfs https://www.stjosephwarrenpa.org/weeklybulletin.php`; see the research entry for the `fetch:check` result.

## Not yet confirmed

Nothing outstanding for the publisher. The 10:00 AM summer Sunday Mass is stated only in the bulletin masthead and directory; it does not affect the church list.
