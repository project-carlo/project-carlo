---
name: St. Peter's Parish (Massena and Louisville)
website: https://massenacatholics.com/
bulletin_provider: parishes_online
provider_id: st-peters-parish-in-massena
publication: ['po-org:st-peters-parish-in-massena', 'lpi:0018000000Qc0EiAAJ', 'po-container:06/0114']
group: St. Peter's Parish
evidence:
- url: https://container.parishesonline.com/bulletins/06/0114/20260927B.pdf
  seen: 2026-09-30
  quote: Sacred Heart & St. Lawrence, Massena, NY 06-0114
  note: 'Page 5 (advertiser footer) of the 27 September 2026 issue in container 06/0114: "St. Mary & St.
    Joseph/Sacred Heart & St. Lawrence, Massena, NY 06-0114". The footer is LPi''s account name and still
    names St. Joseph, which no longer has Mass (see excluded/st-joseph-massena.md), so it is not a membership
    list. Page 1 is letter-spaced in the text layer, so the masthead is not quoted.'
- url: https://container.parishesonline.com/bulletins/06/0114/20260927B.pdf
  seen: 2026-09-30
  quote: 6:00pm (SL) † Rose Alma Bourden by Friends & Family
  note: 'Page 4, "CALENDAR" of the 27 September 2026 issue: Saturday 26 September 4:00pm (SH) Sacred Heart
    and 6:00pm (SL) St. Lawrence; Sunday 27 September 8:00am (SM) and 11:00am (SM) St. Mary''s, 9:30am
    (SH). The weekday Masses are at Sacred Heart and St. Mary''s.'
- url: https://container.parishesonline.com/bulletins/06/0114/20260927B.pdf
  seen: 2026-09-30
  quote: ST. PETER’S PARISH, MASSENA, NY September 27, 2026
  note: Running head of pages 2 and 3. One bulletin, headed "St. Peter's Parish", for all the Massena-area
    churches.
- url: https://container.parishesonline.com/bulletins/06/0114/20261004B.pdf
  seen: 2026-09-30
  note: The 4 October 2026 issue is already posted (probe container 06/0114). Same page-1 schedule as
    27 September (Saturday 4 pm Sacred Heart and 6 pm St. Lawrence; Sunday 8 and 11 am St. Mary's and
    9:30 am Sacred Heart), so the schedule below is the one in force until 31 October.
- url: https://massenacatholics.com/mass-times
  seen: 2026-09-30
  quote: 6:00 PM St. Lawrence Church
  note: 'Parish site (eCatholic, behind Cloudflare; read in a browser with parish-site-access visit.py).
    Mass Times page: Saturday 4:00 PM Sacred Heart Church and 6:00 PM St. Lawrence Church; Sunday 8:00
    AM St. Mary''s, 9:30 AM Sacred Heart, 11:00 AM St. Mary''s. Footer lists four addresses: Sacred Heart,
    St. Joseph''s (22 Bayley Rd.), St. Lawrence (30 Willard Rd, Louisville) and St. Mary''s.'
- url: https://massenacatholics.com/bulletins-1
  seen: 2026-09-30
  quote: View Past Bulletins
  note: 'Parish "Bulletins" page (browser): embeds ParishesOnline organization st-peters-parish-in-massena
    (lpi:0018000000Qc0EiAAJ, po-container:06/0114) and links its weekly issues (20260927B, 20260920B,
    20260913B, 20260906B). Also carries eCatholic site id 12074, but the bulletin is not an eCatholic
    file (issues.py ecatholic finds no Sunday-dated issue), so that id is not recorded as a publication.'
- url: https://www.rcdony.org/parish/massena
  seen: 2026-09-30
  quote: 'Worship sites: St. Mary''s Church - Massena Worship sites: St. Lawrence Church - Louisville'
  note: 'Diocesan directory: "St. Peter''s Parish", Sacred Heart Church (212 Main Street) with worship
    sites St. Mary''s and St. Lawrence; it lists no St. Joseph.'
- url: https://www.nny360.com/news/stlawrencecounty/changes-coming-to-area-catholic-communities-on-nov-1/article_03d6fbd0-b5c6-5400-a5ad-766fb7489267.html
  seen: 2026-09-30
  quote: The Massena and Louisville churches include Sacred Heart and St. Mary’s in Massena and St. Lawrence
    in Louisville.
  note: Watertown Daily Times, 2 Sep 2026. Paywalled; the body is scrambled in the raw HTML and readable
    only in a browser (visit.py --text), so recheck will probably not find it.
revisit: After 1 November 2026 read the massenacatholics.com bulletin again. Does St. Lawrence still appear
  in the schedule (it is to become an oratory after the last Saturday, 31 October)? Has the schedule changed
  to Saturday 4 pm and Sunday 9 and 11 am? Does this bulletin now also cover Madrid and Waddington (st-marys-waddington
  row)?
revisit_after: 2026-11-08
promoted: 2026-09-30
---

## Publisher

St. Peter's Parish, Massena (pastor Rev. Mark R. Reilly), formed in 2018 from the Massena and Louisville churches, publishes **one** weekly bulletin through ParishesOnline (LPi container 06/0114, organization `st-peters-parish-in-massena`). The 27 September 2026 issue (5 pages, text layer) is headed "ST. PETER’S PARISH, MASSENA, NY" and its calendar (page 4) lists Masses at Sacred Heart (SH), St. Mary's (SM) and St. Lawrence (SL). The 4 October issue was already posted on 30 September and has the same schedule. The diocese's directory groups the same three churches as "St. Peter's Parish" (Sacred Heart is the head church, at 212 Main Street, which is also the ParishesOnline organization's address).

## Worship sites

- `sacred-heart-massena` (212 Main St.): weekend Masses Saturday 4 pm and Sunday 9:30 am, weekday Masses Monday and Wednesday to Friday 12:05 pm.
- `st-marys-massena` (9 Sycamore St.): Sunday 8 am and 11 am, Tuesday 5:30 pm.
- `st-lawrence-louisville` (30 Willard Rd., Louisville, mailing town Massena): Saturday 6 pm. **Ends 31 October 2026**: the Watertown Daily Times of 2 September 2026 quotes Fr. Reilly that St. Lawrence becomes an oratory after the last Saturday, 31 October. It holds Mass today, so it stays a church with a dated revisit.
- Not here: **St. Joseph, 22 Bayley Rd.** (GCatholic 18306; named in the parish site's footer and in the bulletin's advertiser line). It became an oratory after a final Mass in 2017 and no Mass is scheduled: `excluded/st-joseph-massena.md`.

From 1 November 2026 Fr. Reilly also becomes pastor of Madrid and Waddington and the same article announces a new schedule (Massena: Saturday 4 pm, Sunday 9 and 11 am; the 8 am at St. Mary's dropped). The Waddington parish's own site says St. Mary's Parish "will be linked with St. Peter's Parish". That parish keeps its own bulletin for now (`st-marys-waddington`), so the rows stay separate; see *Not yet confirmed*.

## Website and bulletin provider

massenacatholics.com is an eCatholic site (id 12074) behind Cloudflare (`probe url` answers 403; `visit.py` loads it). Its Bulletins page embeds the ParishesOnline organization, and the directory's bulletin page (rcdony.org "Parish Bulletins") links massenacatholics.com/bulletins-1 for Massena. The bulletin is therefore read through ParishesOnline: provider `parishes_online`, provider_id `st-peters-parish-in-massena`, with the org slug, the LPi id and the container recorded as publications. `probe po st-peters-parish-in-massena` shows the latest issue as 2026-09-27 (and 2026-10-04 by container probe).

## Not yet confirmed

- What happens on 1 November: whether the Massena bulletin starts to carry Madrid and Waddington (then `merge st-marys-waddington --into st-peters-parish-massena` if its own PDF at mwcatholics.org goes silent), and that St. Lawrence's Masses stop after 31 October (then move `churches/st-lawrence-louisville.md` to excluded with the date). See `revisit`.
- The exact date of St. Joseph's last Mass (the article says only "2017").
