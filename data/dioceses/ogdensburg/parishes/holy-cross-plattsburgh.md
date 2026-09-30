---
name: Holy Cross Parish
website: https://holycrosspbg.org/
bulletin_provider: parishes_online
provider_id: st-john-the-baptist-church-12901
publication: ['po-org:st-john-the-baptist-church-12901', 'lpi:0018000000Qx6iwAAB', 'po-container:04/0730']
group: Holy Cross Parish
evidence:
- url: https://container.parishesonline.com/bulletins/04/0730/20260927B.pdf
  seen: 2026-09-30
  quote: Holy Cross Parish Office - 7 Margaret Street Plattsburgh, NY 12901
  note: 'Page 1 of the 27 September 2026 issue (container 04/0730), under "Twenty-Sixth Sunday in Ordinary Time September 27, 2026". The page then lists, each with its own daily and weekend Mass times, Our Lady of Victory (4919 S Catherine St.), St. John''s (18 Broad St.), St. Peter''s (114 Cornelia St.) and St. John XXIII Newman Center (90 Broad Street, "5:00 PM Sunday"). The letters of the church headings are spaced out in the text layer, so only the office line is quoted.'
- url: https://container.parishesonline.com/bulletins/04/0730/20260927B.pdf
  seen: 2026-09-30
  quote: 'Email: PlattsburghOffice@rcdony.org | Website: www.HolyCrossPBG.org'
  note: 'Page 1 masthead. Page 2 lists the pastoral staff: Rev. Father Kevin McEwan, Pastor; Rev. Tyler M. Fitzgerald and Rev. Douglas Schirmer, Parochial Vicars. Page 3, "Masses for the Week", gives the Sunday 4 October times 8:30 (SJ), 10:00 (OLV), 11:15 (SP) and 5:00 (NC).'
- url: https://parishesonline.com/organization/st-john-the-baptist-church-12901
  seen: 2026-09-30
  note: '`probe po st-john-the-baptist-church-12901`: title "Holy Cross Parish - St. John the Baptist Church", website https://holycrosspbg.org/, address 7 Margaret Street, Plattsburgh 12901, LPi id 0018000000Qx6iwAAB, container 04/0730, newest issues 2026-09-27, 2026-09-20 and 2026-09-13.'
- url: https://holycrosspbg.org/
  seen: 2026-09-30
  quote: View Our Bulletin
  note: 'eCatholic site behind Cloudflare; read in a browser (parish-site-access visit.py). The "View Our Bulletin" banner links to https://www.parishesonline.com/find/st-john-the-baptist-church-12901, the ParishesOnline organization above. Mass Times block: "Saturday: 4:00 PM at St. Peter''s / 5:15 PM at St. John''s", "Sunday: 8:30 AM at St. John''s / 10:00 AM at Our Lady of Victory / 11:15 AM at St. Peter''s / 5:00 PM at Newman Center (Last Mass May 10)".'
- url: https://www.rcdony.org/parish/plattsburgh
  seen: 2026-09-30
  note: Directory entries directory:plattsburgh-1 to -4 (Our Lady of Victory, St. Peter's, St. John the Baptist, St. John XXIII Newman Center) all carry group "Holy Cross Parish", website holycrosspbg.org and pastor Reverend Kevin M. McEwan.
---

## Publisher

Holy Cross Parish, Plattsburgh publishes one weekly ParishesOnline (LPi) bulletin, container
04/0730, organization `st-john-the-baptist-church-12901` (the organization kept the name of
the church whose account it was; its title is now "Holy Cross Parish - St. John the Baptist
Church"). The 27 September 2026 issue's page 1 is headed "Holy Cross Parish Office - 7
Margaret Street Plattsburgh, NY 12901" and gives the Mass times of four places: Our Lady of
Victory, St. John's, St. Peter's and the St. John XXIII Newman Center. The same issue was
posted on 2026-09-27 and there were issues for 20 and 13 September, so the container is live.

The diocese's directory groups the four places as "Holy Cross Parish" (pastor Rev. Kevin M.
McEwan), so the directory, the parish website and the bulletin agree: **one row, four
churches**. The former parishes' own websites (broadstreetcatholics.org, now DEAD-DNS;
olvc.org and saintpeterschurch.org, which `probe url` reads as NO-PARISH-WORDS shells) were not followed: nothing on holycrosspbg.org or in
the bulletin points to a separate bulletin for any of them, and GCatholic's websites for the
three churches are those old domains.

## Worship sites

Four, all in the 27 September 2026 bulletin:

- `our-lady-of-victory-plattsburgh` (4919 S. Catherine St.): Sunday 10:00 AM, Tuesday and Thursday 8:00 AM.
- `st-john-the-baptist-plattsburgh` (18 Broad St.): Saturday 5:15 PM, Sunday 8:30 AM, Monday, Wednesday and Friday 8:00 AM.
- `st-peter-plattsburgh` (114 Cornelia St.): Saturday 4:00 PM, Sunday 11:15 AM, Monday to Friday 12:05 PM.
- `st-john-xxiii-newman-center-plattsburgh` (90 Broad St.): Sunday 5:00 PM, the campus (SUNY Plattsburgh) Mass. The parish website still says "5:00 PM at Newman Center (Last Mass May 10)", a spring-semester note that predates the autumn start; the bulletin's 4 October list includes "5:00pm (NC)", so it holds Mass again in the academic year.

Not here: St. Joseph, 1349 Military Turnpike (GCatholic 18310) is a former church, now an outreach
center of the Morrisonville community (`excluded/st-joseph-plattsburgh-west`). Discover Mass
also has a page "St. Mary of the Lake Oratory" (Cumberland Head) whose address is St. Mary's,
Champlain: it is a mislabelled listing and not one of these churches.

## Website and bulletin provider

`holycrosspbg.org` is the directory's website and is an eCatholic site (id 25294, behind
Cloudflare: `probe url` HTTP4XX, loaded with visit.py on the second try). It hosts no
bulletin files: `issues.py ecatholic 25294` finds nothing for any Sunday or Friday, and the
"View Our Bulletin" banner goes to ParishesOnline, which is why the row is
`parishes_online` and `ecatholic:25294` is not recorded as a publication. The ids came from
`probe po st-john-the-baptist-church-12901`.

## Not yet confirmed

- Whether the bulletin's Newman Center Mass continues through the semester (the website's "Last Mass May 10" line is stale until the parish updates it).
