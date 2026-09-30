---
name: Eastern Lake Ontario Catholics
website: https://www.elocparishes.org
bulletin_provider: parishes_online
provider_id: eastern-lake-ontario-catholics
publication: ['po-org:eastern-lake-ontario-catholics', 'lpi:001RP00000arY5JYAU', 'po-container:03/1493']
group: Eastern Lake Ontario Catholics (Adams, Brownville, Henderson, Sackets Harbor)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1493/20260927B.pdf
  seen: 2026-09-30
  quote: Eastern Lake Ontario Catholics September 27, 2026
  note: 'Page 1 (masthead) of the 27 September 2026 issue, ParishesOnline container 03/1493 (6 pages, text layer). It lists four churches with their addresses: St. Andrew''s, 107 Woolsey Street, Sackets Harbor; Queen of Heaven, 8900 US RT 3, Henderson; Immaculate Conception, 214 West Main Street, Brownville; St. Cecilia''s, 17 Grove Street, Adams.'
- url: https://container.parishesonline.com/bulletins/03/1493/20260927B.pdf
  seen: 2026-09-30
  quote: 4:00 pm (IC) 4:30 pm (SC) 8:30 am (QH) 9:00 am (IC) 10:30 am (SA) 11:00 am (SC)
  note: 'Page 2, "LITURGY SCHEDULE", weekend of 26-27 September (repeated for 3-4 October): one schedule for all four churches, keyed by letters. The weekday Masses of 28 September to 2 October are also spread over IC, SC, QH and SA.'
- url: https://container.parishesonline.com/bulletins/03/1493/20260927B.pdf
  seen: 2026-09-30
  quote: 'SC= St. Cecilia''s in Adams IC = Immac. Conception in Brownville SA = St. Andrews in Sackets Harbor QH = Queen of Heaven in Henderson'
  note: Page 2, the key to the schedule codes. The Sunday intention "All the People of Our Four Parishes" on the same page names the four.
- url: https://www.elocparishes.org/
  seen: 2026-09-30
  note: 'The parish site (eCatholic, custom domain; behind Cloudflare, read with visit.py). Its "Normal Mass Schedule" is the same four churches and times as the bulletin; its Bulletins link goes to https://parishesonline.com/organization/eastern-lake-ontario-catholics. It embeds po-org:eastern-lake-ontario-catholics (and ecatholic:39874, the site''s own id, not a bulletin).'
- url: https://parishesonline.com/organization/eastern-lake-ontario-catholics
  seen: 2026-09-30
  note: '`probe po eastern-lake-ontario-catholics`: title "Eastern Lake Ontario Catholics", address 119 W. Main St, Brownville; ids po-org:eastern-lake-ontario-catholics, lpi:001RP00000arY5JYAU, po-container:03/1493; weekly issues 23 Aug to 27 Sept 2026, newest 2026-09-27.'
---

## Publisher

Eastern Lake Ontario Catholics publishes **one** weekly bulletin for four churches. The 27
September 2026 issue (ParishesOnline container 03/1493, 6 pages, text layer) has the
masthead "Eastern Lake Ontario Catholics", pastor Fr. Shane Lynch and assistant pastor Fr.
Albert Hauser, and prints the four churches' names and addresses on page 1. Page 2 is one
"Liturgy Schedule" for all four with a code key (SC Adams, IC Brownville, SA Sackets
Harbor, QH Henderson): Saturday 4:00 pm IC and 4:30 pm SC; Sunday 8:30 am QH, 9:00 am IC,
10:30 am SA and 11:00 am SC; weekday Masses rotating among the four (Mon 8:30 IC, Tue 8:30
SC, Wed 8:30 QH and 5:30 pm IC, Thu 8:30 SA, Fri 8:30 SC in the week of 28 September). The
parish's own site shows the same "Normal Mass Schedule".

The diocese's directory lists the four as separate entries (adams-1, adams-2, brownville,
sackets-harbor), all with the website elocparishes.org and Fr. Lynch as pastor; only the
Brownville entry carries a group name ("The Roman Catholic Community of Brownville and
Dexter", the 2004 merger of Immaculate Conception, Brownville with St. Elizabeth Seton,
Dexter, per the parish's history page). They are one bulletin, so one row.

## Worship sites

- `st-cecilia-adams`, 17 Grove Street, Adams (directory adams-1, GCatholic 18230).
- `queen-of-heaven-henderson`, 8900 Route 3, Henderson (directory adams-2, GCatholic 18280).
- `immaculate-conception-brownville`, 214 West Main Street, Brownville (directory
  brownville, GCatholic 18244).
- `st-andrew-sackets-harbor`, 107 Woolsey Street, Sackets Harbor (directory
  sackets-harbor, GCatholic 18245).

Not here: St. Elizabeth Seton (Dexter), the other half of the "Brownville and Dexter"
community. Neither the diocese's directory nor GCatholic lists a Dexter church, and the
27 September bulletin schedules no Mass there; the parish's history page says the two
parishes merged in December 2004 but I found no source on whether Dexter's building still
holds Mass. A lead for whoever owns "Dexter" (it is not in either roster, so it moves no
coverage number): the church stood at Bronson and Orchard Streets, Dexter.

## Website and bulletin provider

www.elocparishes.org is the parish's eCatholic site (the diocese's directory and the diocese's
Parish Bulletins page both send readers to it, or to the ParishesOnline organization). Its
Bulletins link goes to ParishesOnline, so the bulletin is read there: provider
`parishes_online`, provider_id the organization slug, and all three ids of that one
organization (`po-org`, `lpi`, `po-container`) recorded so no other row can claim them. The
LPi id is 18 characters (001RP00000arY5JYAU), a newer prefix than the 0018... ids of the
Watertown organizations. The bare `http://www.elocparishes.org` timed out in the browser and
returns 403 to `probe url`; `https://www.elocparishes.org` loads.

## Not yet confirmed

Whether St. Elizabeth Seton, Dexter still holds public Mass (see above); a call to the
Brownville office (315-782-1143) or a look at Dexter would settle it.
