---
name: Divine Grace Parish
website: https://divinegracepgh.org
bulletin_provider: parishes_online
provider_id: divine-grace-parish-16066
publication: ['po-org:divine-grace-parish-16066', 'lpi:0018000000Qx7sYAAR', 'po-container:14/1741', 'ecatholic:21503']
group: Divine Grace Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1741/20261025B.pdf
  seen: 2026-10-23
  quote: Holy Redeemer Church
  note: 'Page 1 of the 25 October 2026 issue (container 14/1741, 20 pages, text layer readable): masthead
    ''Divine Grace Parish'' listing three churches with addresses: Saint Ferdinand, 2535 Rochester Road,
    Cranberry Twp.; Saint Gregory, 2 West Beaver Street, Zelienople; Holy Redeemer, 415 4th Street, Ellwood
    City; office 724-776-2888. Page 2 ''Mass Intentions'' lists Masses at all three churches for 24 Oct
    to 1 Nov.'
- url: https://divinegracepgh.org/mass-times
  seen: 2026-10-23
  quote: 5:00 pm Holy Redeemer Church
  note: Parish Mass Times page (diocese-provided eCatholic site 21503, read in headed Chrome; plain fetches
    get 403). One schedule for Saint Ferdinand, Saint Gregory and Holy Redeemer; no other church is listed.
- url: https://files.ecatholic.com/21503/bulletins/20261025.pdf
  seen: 2026-10-23
  note: The parish site's own bulletin archive (divinegracepgh.org/bulletins, lists weekly files back
    to 2022) hosts this file; it is byte-identical (cmp, 25,770,104 bytes) to the ParishesOnline 14/1741
    issue of 25 October 2026, and the 18 October pair is byte-identical too. One bulletin, two hosts.
- url: https://parishesonline.com/organization/divine-grace-parish-16066
  seen: 2026-10-23
  note: 'probe po: org ''Divine Grace Parish'', 2535 Rochester Rd, Cranberry Township; container 14/1741;
    latest issue 2026-10-25.'
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

Divine Grace Parish (Cranberry Township, Zelienople and Ellwood City; pastor Rev. James A. Wehner per the diocese page) publishes one weekly bulletin for its three churches. The 25 October 2026 ParishesOnline issue (container 14/1741) is headed "Divine Grace Parish" and gives the three churches' addresses on page 1; page 2 prints one Mass-intentions list for all three. No sibling parish prints in this container.

## Worship sites

Three churches, each with Masses in the 25 October bulletin and on the parish Mass Times page: Saint Ferdinand (Cranberry Township), Saint Gregory (Zelienople) and Holy Redeemer (Ellwood City). The diocese directory lists the same three. The parish was formed on 1 July 2022 from St. Ferdinand, St. Gregory and Holy Redeemer (parish site, About; the predecessor list at diopitt.org gives St. Ferdinand, St. Gregory (Evans City/Zelienople) and Holy Redeemer (Ellwood City/Koppel/Wampum) as predecessors). Also considered: St. Matthias, Evans City, which the diocese says was absorbed by St. Gregory in 2016 and remained open; the bulletin and Mass Times page list no Mass there, so it is in open/ (st-matthias-evans-city). GCatholic's Holy Redeemer entry gives 300 Crescent Ave, which is the parish office address (web directories list 'Divine Grace Parish - Holy Redeemer Office, 300 Crescent Ave #1'); the church is 415 4th Street per the bulletin, parish site and diocese.

## Website and bulletin provider

divinegracepgh.org is diocese-provided eCatholic (site 21503) behind Cloudflare: `probe url` gets 403, headed Chrome reads it (`visit.py`). The row reads ParishesOnline container 14/1741 by org slug because it carries each issue first; the parish site's /bulletins archive hosts the same PDFs as files.ecatholic.com/21503/bulletins/<yyyymmdd>.pdf, byte-identical on the 25 and 18 October issues (compared 2026-10-23), so it is a fallback, not a second bulletin. The site's rendered home page also links a files.ecatholic.com/21503/documents/2026/9/PIT1026.pdf ad/flyer, not read.

## Not yet confirmed

Nothing outstanding for the row. Weekday Masses are on the Mass Times page and bulletin but are not modelled here.
