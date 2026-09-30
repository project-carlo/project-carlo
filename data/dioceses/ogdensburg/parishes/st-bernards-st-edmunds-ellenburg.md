---
name: St. Bernard's and St. Edmund's Parish
website: http://www.cathcommsbse.org/
bulletin_provider: other
provider_id: ''
publication: ['url:http://www.cathcommsbse.org/']
group: St. Bernard's and St. Edmund's Parish
evidence:
- url: http://www.cathcommsbse.org/var/m_8/8d/8dc/64111/1024614-09-27-2026-aab32.pdf?download
  seen: 2026-09-30
  quote: ST. BERNARD’S & ST. EDMUND’S PARISH 26th Sunday in Ordinary Time. September 27, 2026.
  note: Page 1 of the 27 September 2026 bulletin (2 pages, text layer), linked from the parish home page as "Bulletin for the Weekend of the 26th Sunday in Ordinary Time - Sunday, September 27, 2026". The masthead block continues "Schedule of Holy Mass Saturday 4:00pm St. Bernard’s Church (SB) 6:00pm St. Edmund’s Church(SE) Sunday 8:00am SE 10:30am SB", with "St. Bernard’s Church Est. 1875 10 Church Pond Road Lyon Mountain. NY 12952" and "St. Edmund’s Church Est. 1883 5526 State Route 11 Ellenburg Center. NY 12934", Fr. Tojo Chacko HGN, pastor.
- url: http://www.cathcommsbse.org/var/m_8/8d/8dc/64111/1024614-09-27-2026-aab32.pdf?download
  seen: 2026-09-30
  quote: Monday, September 28th, 2026 5:30pm (SE):Pat Rodriguez
  note: 'Page 2, "Mass & Envelope Schedule": weekday Masses 5:30pm (SE) Monday, 9:00am (SB) Tuesday, no Mass Wednesday 30 September, 9:00am (SE) Thursday, 9:00am (SB) Friday; weekend 3 and 4 October as the weekend of 26 and 27 September.'
- url: http://www.cathcommsbse.org/
  seen: 2026-09-30
  quote: Saturday 4:00 p.m. (SB) - 6:00 p.m. (SE)
  note: 'Parish home page (an "e-lite" site, no Cloudflare), read 2026-09-30: "Welcome to the home page of St Edmund''s in Ellenburg and St Bernard''s in Lyon Mt." with the weekday schedule (Monday 5:30 p.m. SE, Tuesday 9 am SB, Thursday 9 am SE, Friday 9 am SB) and "Always check our current bulletin for changes". The bulletin is a weekly PDF uploaded under "Parish Bulletin" with "Download File"; file names change every week (`/var/m_8/8d/8dc/64111/<n>-09-27-2026-aab32.pdf?download`).'
- url: https://www.rcdony.org/parish/ellenburg
  seen: 2026-09-30
  note: 'Directory: directory:ellenburg-1 (St. Edmund''s Church, 5526 State Route 11, Ellenburg) and directory:ellenburg-2 (St. Bernard''s Church, 10 Church Pond Rd, Lyon Mountain), group "St. Bernard''s and St. Edmund''s Parish", website cathcommsbse.org, Pastor Reverend Tojo Chacko, HGN, phone 518-594-3907.'
---

## Publisher

St. Bernard's and St. Edmund's Parish (Lyon Mountain and Ellenburg) publishes its own weekly bulletin as a PDF on its website, cathcommsbse.org. The 27 September 2026 issue's first page is headed "ST. BERNARD'S & ST. EDMUND'S PARISH" and lists the Mass schedule of both churches ("Saturday 4:00pm St. Bernard's Church (SB), 6:00pm St. Edmund's Church (SE); Sunday 8:00am SE, 10:30am SB"); page 2 gives the week's Mass intentions for both. Pastor: Fr. Tojo Chacko, HGN. The directory groups the two as "St. Bernard's and St. Edmund's Parish": **one row, two churches.** The diocese's Parish Bulletins page links the same site for Ellenburg Center and Lyon Mountain.

## Worship sites

- `st-bernards-lyon-mountain` (10 Church Pond Rd): Saturday 4:00 PM, Sunday 10:30 AM, Tuesday and Friday 9:00 AM.
- `st-edmunds-ellenburg` (5526 State Route 11): Saturday 6:00 PM, Sunday 8:00 AM, Monday 5:30 PM, Thursday 9:00 AM.

Both Mass-schedule lists (bulletin and home page) cover exactly these two. The bulletin also advertises Chateaugay's St. Patrick's pot-roast dinner; Chateaugay is another region's parish (Chateaugay, Constable and Fort Covington) and not part of this bulletin.

## Website and bulletin provider

`cathcommsbse.org` is a self-hosted site (file paths `/var/m_8/.../<n>-<date>-<hash>.pdf?download`, no Cloudflare; `probe url` ok, title "Home - St.Bernard's and St Edmund's Parishes") that posts the current bulletin on its home page as a dated PDF link; there is no archive. Provider `other`, publication `url:http://www.cathcommsbse.org/` (the page that lists the bulletin), no provider id. The pipeline resolves the PDF by the link text "Bulletin for the Weekend of ...".

## Not yet confirmed

- Whether the parish keeps earlier bulletins anywhere (the home page shows only the current one).
