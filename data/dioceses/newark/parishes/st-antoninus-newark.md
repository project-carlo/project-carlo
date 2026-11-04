---
name: St. Antoninus, Newark
website: https://www.saintantoninuschurch.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area I
evidence:
- url: https://files.constantcontact.com/9566502f601/2f812d57-6e54-490c-b5e8-acab61a578fb.pdf
  seen: 2026-11-04
  quote: 'Daily Mass: Tues. thru Sat. noon (Guadalupe Chapel)'
  note: 'The last bulletin found online: a 4-page parish-made PDF for Christ the King, 23 November 2025,
    linked as ''Read this Sunday''s Bulletin'' from the 21 November 2025 Constant Contact newsletter.
    Page 1 masthead ''St. Antoninus Church 337 South Orange Avenue, Newark, NJ 07103 … Pastor: Rev. Joseph
    A. Meagher''; no printer''s footer. Sunday Mass 8AM in rectory, 10 AM in church, Spanish 1:30PM.'
- url: https://myemail.constantcontact.com/Solemnity-of-Christ-the-King-this-Sunday---procession-after-Mass---Tomorrow--Sat---Divine-Mercy-Love-Feast-tomorrow.html?soid=1129341871705&aid=qULM9GztIFc
  seen: 2026-11-04
  quote: Read this Sunday's Bulletin.
  note: Constant Contact newsletter of 21 November 2025 (reached from the homepage link conta.cc/4ih8EXG);
    the bulletin link points to the PDF above.
- url: https://www.saintantoninuschurch.org/
  seen: 2026-11-04
  quote: November 21, 2025 - This Sunday is the Solemnity of Christ the King
  note: 'Weebly site. Its homepage lists ''[ST ANTONINUS NEWS] Constant Contact'' newsletters weekly through
    2025; the newest is 21 November 2025 and no page carries a 2026 date. No bulletin page in the menu
    (probe url: no publications, no bulletin links).'
- url: https://www.facebook.com/SaintAntoninusChurch
  seen: 2026-11-04
  quote: Sunday Mass begins at 10 a.m.
  note: 'Facebook page read with visit.py (logged out): intro only; the visible post is from May 2022;
    no bulletin.'
- url: https://rcan.org/wahw-june-2026-letter-cardinal-tobin/
  seen: 2026-11-04
  quote: St. Antoninus Parish, Newark
  note: Listed with the Parish of the Transfiguration, Newark among the June 2026 Parish Mission Partners
    pilot parishes.
revisit: 'Look for a current St. Antoninus bulletin: the site''s homepage newsletter list (stopped at
  21 November 2025), a joint Mission Partners bulletin with Transfiguration (church-bulletin.org/585),
  or a new channel. If one appears, set the provider and run fetch:check.'
revisit_after: 2027-02-01
research:
- method: probe url and probe get on the parish site (home, Mass page, clergy, calendar, pastor's page,
    events pages); Wayback CDX for saintantoninuschurch.org from 2026
  url: https://www.saintantoninuschurch.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look for a 2026 newsletter or bulletin link on the site, or another channel (a new site,
    a Constant Contact archive)
  retry_when: Revisit date or the site's homepage shows a 2026 newsletter
  revisit_after: 2027-02-01
- method: Run JP scan output (scratch/newark-map-1/029-map/jp-*.tsv) grepped for antoninus, 07103, newark;
    probe po st-antoninus-church-07103, saint-antoninus-church-07103, st-antoninus-church-7103
  checked: '2026-11-04'
  outcome: not-found
  next_action: None unless a masthead names a printer
  retry_when: A bulletin with a printer's footer appears
- method: 'Constant Contact newsletters linked from the homepage: the 21 November 2025 email links the
    23 November 2025 bulletin PDF on files.constantcontact.com'
  url: https://files.constantcontact.com/9566502f601/2f812d57-6e54-490c-b5e8-acab61a578fb.pdf
  checked: '2026-11-04'
  outcome: not-found
  next_action: Find a current newsletter (subscribe or ask the parish office, 973-623-0258); if bulletins
    still go out only by email, record unsupported with a fetch_gap for emailed newsletters
  retry_when: A 2026 newsletter or bulletin turns up
bulletin_status: not-found
---

## Publisher

No current bulletin found. St. Antoninus made its own 4-page bulletin (no printer's footer) and sent it with its weekly Constant Contact newsletter: the last one found is for 23 November 2025 (Christ the King), linked as 'Read this Sunday's Bulletin' from the 21 November 2025 email; its page 1 masthead reads 'St. Antoninus Church 337 South Orange Avenue, Newark, NJ 07103 … Pastor: Rev. Joseph A. Meagher'. The parish homepage lists those newsletters weekly through 2025 and nothing after 21 November 2025; no page carries a 2026 date. No John Patrick listing or ParishesOnline org was found.

The parish is a June 2026 'Parish Mission Partners' pilot with the Parish of the Transfiguration (rcan.org June 2026 letter). Different pastors (Fr. Josephat Kalema at Transfiguration), and Transfiguration posts no bulletin either; no joint bulletin found. Separate rows.

## Worship sites

- St. Antoninus, 337 South Orange Avenue (`st-antoninus-newark`): the 23 November 2025 bulletin gives 'Sunday Mass: 8AM in Rectory; 10 AM in Church … Spanish Mass 1:30PM … Daily Mass: Tues. thru Sat. noon (Guadalupe Chapel)'. The rectory chapel and Our Lady of Guadalupe chapel are on the same property, so one church row.

GCatholic's Most Blessed Sacrament (153721), the Franciscan Friars of the Renewal friary at 375 13th Avenue, is a few blocks away; the friars sponsor the parish's Thanksgiving dinner (23 November 2025 bulletin) but no source shows a public Mass at the friary: `excluded/most-blessed-sacrament-friary-newark`.

## Website and bulletin provider

https://www.saintantoninuschurch.org/ (directory 141's website, Weebly). `no_bulletin`, with research and a revisit (Settled policy 4). If bulletins still go out only by email, the row would become `unsupported` with a fetch_gap.

## Not yet confirmed

Whether the parish still sends a weekly bulletin in 2026, and where. See research.
