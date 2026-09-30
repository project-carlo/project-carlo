---
name: St. Mary's Church, Clayton and the Catholic Community of Alexandria
website: https://www.stmarysclayton.org
bulletin_provider: parishes_online
provider_id: saint-marys-church
publication: ['po-org:saint-marys-church', 'lpi:0018000000Qc2boAAB', 'po-container:06/0098']
group: The Catholic Community of Alexandria
evidence:
- url: https://container.parishesonline.com/bulletins/06/0098/20260927B.pdf
  seen: 2026-09-30
  quote: Catholic Community of Alexandria, Alexandria Bay—Redwood
  note: 'Page 2 of the 27 September 2026 issue (6 pages, text layer), "Weekly Giving" heading. Page 1
    is the masthead: "Welcome to St. Mary’s Church, Clayton & the Catholic Community of Alexandria,
    Alexandria Bay", with Deacon Neil Fuller as Parish Life Coordinator and Rev. Donald A. Robinson as
    Sacramental Minister.'
- url: https://container.parishesonline.com/bulletins/06/0098/20260927B.pdf
  seen: 2026-09-30
  quote: St. Francis Xavier, Redwood
  note: 'Page 1 "Weekend Masses" box: St. Mary’s, Clayton Saturdays 4:00 pm, Sundays 9:30 am; St. Cyril’s,
    Alexandria Bay Saturdays 4:00 pm, Sundays 9:30 am; St. Francis Xavier, Redwood "Sunday 8am Starts
    Memorial Day"; Tabernacle, Thousand Island Park "Sunday 8am July 4th through Labor Day". Page 2 lists
    the week''s Masses with the codes (SM), (SC), (SFX).'
- url: https://container.parishesonline.com/bulletins/06/0098/20261004B.pdf
  seen: 2026-09-30
  quote: Tabernacle, Thousand Island Park
  note: 'The 4 October 2026 issue (already posted on 30 September) has the identical masthead and
    Weekend Masses box, so the September issues are not a one-off. Read with `probe container 06/0098
    --all --step 4`; the 6 September and 9 August issues also carry the masthead and, on page 2, summer
    Sunday 8:00 Masses coded (TIP) and (SFX).'
- url: https://parishesonline.com/organization/saint-marys-church
  seen: 2026-09-30
  note: '`probe po saint-marys-church`: "Saint Mary''s Church", 521 James Street, Clayton, website
    www.stmarysclayton.org, ids po-org:saint-marys-church, lpi:0018000000Qc2boAAB, po-container:06/0098,
    latest issue 2026-09-27, weekly issues back to at least 23 August.'
- url: https://www.stmarysclayton.org/
  seen: 2026-09-30
  quote: PARISH BULLETIN
  note: 'The parish site (loaded in a browser on the first try). Its "PARISH BULLETIN" link goes
    to parishesonline.com/publication-page/saint-marys-church (a 2020 issue path, but the same org). The
    site header still reads "The Catholic Churches of St. Mary''s, Clayton and St. John the Evangelist,
    Lafargeville" (see *Worship sites*).'
- url: http://www.stcyrils.org/
  seen: 2026-09-30
  note: 'The Alexandria Bay site named in the masthead. It answers 403 to curl, `probe url` and visit.py
    (one load), and a TLS error to curl with a browser user agent; not read. Nothing on the ParishesOnline
    side suggests a separate bulletin (see *Not yet confirmed*).'
---

## Publisher

St. Mary's Church, 521 James Street, Clayton publishes one weekly bulletin on ParishesOnline
(org `saint-marys-church`, container 06/0098) for **four** worship sites. The 27 September 2026
issue's page 1 is headed "Welcome to St. Mary’s Church, Clayton & the Catholic Community of
Alexandria, Alexandria Bay", lists one office (Clayton, 315-686-3398), one Parish Life
Coordinator (Deacon Neil Fuller) and one Sacramental Minister (Rev. Donald A. Robinson), and
prints one "Weekend Masses" box for St. Mary's (Clayton), St. Cyril's (Alexandria Bay), St.
Francis Xavier (Redwood) and the Tabernacle (Thousand Island Park). Page 2 gives one weekly
Mass schedule for all of them, with codes (SM), (SC), (SFX) and (TIP), and a "Weekly Giving"
box headed "Catholic Community of Alexandria, Alexandria Bay—Redwood" next to St. Mary's own.
The 4 October issue (posted 30 September) is the same. The directory groups only
Alexandria Bay and Redwood ("The Catholic Community of Alexandria") and lists Clayton alone,
so the diocese's structure and the bulletin's differ: **the bulletin, not the directory,
decides the row**, and it names all of them together.

## Worship sites

Four, all public Mass now:

- **St. Mary's, Clayton** (`st-marys-clayton-church`): Saturday 4:00 pm, Sunday 9:30 am, weekday
  9:00 am.
- **St. Cyril's, Alexandria Bay** (`st-cyril-alexandria-bay`): Saturday 4:00 pm, Sunday 9:30 am,
  weekday 8:00 am.
- **St. Francis Xavier, Redwood** (`st-francis-xavier-redwood`): summer Sunday 8:00 am. The
  bulletin says "Starts Memorial Day"; the 9 August and 6 September issues list (SFX) Sunday
  8:00 Masses, and the 27 September and 4 October issues still list (SFX) at 8:00 on 27 September
  and 4 and 11 October, so it had not yet closed for the season (see *Not yet confirmed*).
- **Tabernacle, Thousand Island Park** (`tabernacle-thousand-island-park`): Sunday 8:00 am "July
  4th through Labor Day" only. In no roster.

Ruled out: **St. John the Evangelist, La Fargeville** is on both rosters and the Clayton
site's header still names it, but the parish site says "No Mass at St. John's, LaFargeville"
and the 2021 press report says it would become an oratory. It is `excluded/st-john-the-evangelist-la-fargeville`.

## Website and bulletin provider

`www.stmarysclayton.org` is the directory's link for Clayton (the directory's Alexandria Bay
and Redwood entries point at `stcyrils.org`, which the bulletin also lists). It links the
ParishesOnline publication page. `probe po saint-marys-church` gives the three forms of the
one ParishesOnline bulletin: `po-org:saint-marys-church`, `lpi:0018000000Qc2boAAB` and
`po-container:06/0098`. The diocese's bulletin page links the same publication for Alexandria
Bay, Clayton and Redwood.

## Not yet confirmed

- Whether St. Cyril's has a bulletin channel of its own: `stcyrils.org` could not be read
  (403 to every fetch tried on 2026-09-30). The Clayton masthead prints it as a site of the
  same community and there is no second ParishesOnline organization under the obvious slugs,
  so one row is what the evidence supports. One more try with `visit.py` on `stcyrils.org/bulletins`
  would settle it.
- When St. Francis Xavier, Redwood stops for the winter: the bulletin gives only "Starts
  Memorial Day". Re-read the mid-October issues.
