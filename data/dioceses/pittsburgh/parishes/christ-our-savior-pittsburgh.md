---
name: Christ Our Savior Parish (North Side and Brighton Heights)
website: https://www.christoursaviorpgh.org
bulletin_provider: parishes_online
provider_id: christ-our-savior-parish-15212
publication: ['po-org:christ-our-savior-parish-15212', 'lpi:0013b00001oFqQJAA0', 'po-container:14/1701']
group: Christ Our Savior Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1701/20261018B.pdf
  seen: 2026-10-23
  quote: Christ Our Savior, Pittsburgh, PA 14-1701
  note: 18 October 2026 issue, container 14/1701, 8 pages; pages 1-7 are images with no text layer, the
    quote is the LPi ad-page footer (page 8). Rendered with pdftoppm, page 1 reads 'Christ Our Savior
    Parish / Saint Cyril Church 3854 Brighton Road / Saint Boniface Church 2206 East Street / Saint Peter
    Church 720 Arch Street / The Twenty-Ninth Sunday in Ordinary Time, October 18, 2026 / Father Michael
    Caridi, Pastor'. recheck cannot find the image text.
- url: https://container.parishesonline.com/bulletins/14/1701/20261018B.pdf
  seen: 2026-10-23
  note: Page 1 Mass Schedule box (rendered image). Saturday 4:00 PM (vigil) in St. Cyril Church; 5:30
    PM (vigil) in St. Boniface Church. Sunday 8:00 AM in St. Boniface Church; 10:00 AM in St. Peter Church;
    12:00 PM in St. Cyril Church. Weekday 9:00 AM Mon.-Sat. in St. Cyril Church; 12:00 PM Wed. & Fri.
    in St. Peter Church. Page 2 Mass Intentions for 18-25 October name only St. B, St. P and St. C. Matches
    the directory weekend times for the three churches.
- url: https://www.christoursaviorpgh.org
  seen: 2026-10-23
  note: Rendered in headed Chrome (visit.py --bulletin). verdict ok; publications lpi:0013b00001oFqQJAA0,
    po-org:christ-our-savior-parish-15212, po-container:14/1701, ecatholic:21454. The 'Bulletins' link
    goes to parishesonline.com/organization/christ-our-savior-parish-15212 and the page embeds the 20261025B,
    20261018B, 20261011B and 20261004B container PDFs. ecatholic:21454 hosts the site only, no bulletin
    files, so it is not recorded as a publication id.
- url: https://parishesonline.com/organization/christ-our-savior-parish-15212
  seen: 2026-10-23
  note: 'probe po: ''Christ Our Savior Parish'', 720 Arch Street, Pittsburgh 15212; lpi 0013b00001oFqQJAA0;
    container 14/1701; latest issue 2026-10-25, then 10-18, 10-11, 10-04, 09-27, 09-20.'
- url: https://parishesonline.com/organization/most-precious-blood-of-jesus-parish
  seen: 2026-10-23
  note: 'probe po: this second LPi org (0018000000Qx7sEAAR, title ''Most Precious Blood of Jesus - Latin
    Mass Community'', website institute-christ-king.org) resolves to the same container 14/1701 and lists
    the same 2026-10-25 issue. The 18 Oct 14/1701 footer names Christ Our Savior, so the org is a stale
    account pointing at this bulletin; it is not recorded as a publication of either row (see most-precious-blood-of-jesus-pittsburgh).'
- url: https://diopitt.org/christ-our-savior-pittsburgh
  seen: 2026-10-23
  quote: On July 1, 2019, these four parishes were formally merged to create the Christ Our Savior Parish.
  note: Diocese history page (headed Chrome; diopitt.org answers 403 to recheck).
bulletin_status: available
publication_reviews:
- parish: most-precious-blood-of-jesus-pittsburgh
  decision: separate
  evidence:
  - url: https://institute-christ-king.org/images/pittsburgh/bulletins/2026-10-18.pdf
    seen: 2026-10-23
    note: 'Masthead comparison of the two 18 October 2026 bulletins: the Institute''s PDF (rendered) has
      the masthead ''Most Precious Blood of Jesus Parish ... Personal Parish for the Extraordinary Form'',
      Canon William Avis, and serves one church, 3250 California Avenue; the Christ Our Savior masthead
      (ParishesOnline 14/1701) names Fr. Michael Caridi and serves three other churches (St. Peter, St.
      Boniface, St. Cyril of Alexandria). Different publishers, mastheads, clergy and member churches;
      a stale LPi org named for Most Precious Blood merely points at 14/1701.'
---

## Publisher

Christ Our Savior Parish (North Side and Brighton Heights), formed 2019-07-01 from Holy Wisdom (North Side/Spring Hill), St. Peter (North Side) and St. Cyril of Alexandria (Brighton Heights) (the Risen Lord parish merged in too, but its church went to Most Precious Blood), publishes one weekly bulletin on ParishesOnline container 14/1701. The 18 October 2026 issue (read 2026-10-23) has image pages; rendered, page 1 is headed "Christ Our Savior Parish" and names Saint Cyril, Saint Boniface and Saint Peter Churches with one Mass Schedule box, and the ad-page footer reads "Christ Our Savior, Pittsburgh, PA 14-1701". Pastor Fr. Michael Caridi, parish office 720 Arch Street, 412-761-1552 (the directory gives the same phone and pastor for all three churches).

## Worship sites

Three churches hold Mass: St. Boniface (East Street), St. Cyril of Alexandria (Brighton Road) and St. Peter (Arch Street), each in the 18 October Mass schedule and the directory. Ruled out: St. Ambrose (Spring Hill) and Our Lady, Queen of Peace (North Side), both from GCatholic, both relegated to profane use on 2022-03-28 per the diocese's history page (see excluded/). Most Precious Blood of Jesus (the former Risen Lord church, 3250 California Ave) is NOT part of this parish: the history page says Risen Lord Church became the church of the separate personal parish; it has its own bulletin (see parishes/most-precious-blood-of-jesus-pittsburgh.md).

## Website and bulletin provider

christoursaviorpgh.org is diocese-provided eCatholic (site 21454) behind Cloudflare; read in headed Chrome. Its Bulletins link and widget lead to the ParishesOnline container. **The bulletin pages are images** (pages 1-7 of 8 have no text layer in the 18 Oct issue), so the pipeline must read the Mass schedule from the rendered page. The masthead prints St. Boniface at "2206 East Street", the diocese directory and GCatholic "2208 East Street" (recorded on the church).

## Not yet confirmed

Nothing outstanding for the row. The newest container issue (25 October) postdates today; the 18 October issue was read in full for the schedule.
