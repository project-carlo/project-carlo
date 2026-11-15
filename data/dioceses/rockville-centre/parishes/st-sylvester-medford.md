---
name: St. Sylvester
website: https://www.stsylvesterli.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['po-org:st-sylvester-roman-catholic-church', 'lpi:0018000000Qx82rAAB']
group: ''
evidence:
- url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx82rAAB/publications/1794001654588-03-1145%20-%20November%208%20bulletin%20with%20Ads.pdf
  seen: 2026-11-13
  quote: Rev. Gius Garcia, Pastor
  note: '8 November 2026 issue (''32nd Sunday in Ordinary Time ... November 8, 2026''; 16 pages; PDF Creator
    Microsoft Publisher 2021, parish-made), uploaded to the ParishesOnline org. Page 1: Pastoral Staff
    Rev. Gius Garcia, Pastor; Rev. Paul Bersamin, Parochial Vicar. Weekend Masses: Saturday 5:00pm; Sunday
    7:30 am, 9:00 am & 11:00 am; Vietnamese Mass Sunday 3:00 pm; Daily Mass Monday, Tuesday, Thursday
    & Friday 8:30 am in the church. Contacts at stsylvesterli.org, phone 631-475-4506.'
- url: https://parishesonline.com/organization/st-sylvester-roman-catholic-church
  seen: 2026-11-13
  note: 'probe po on the LPi id the site embeds: ''St. Sylvester Roman Catholic Church'', 68 Ohio Ave,
    Medford, NY 11763; website https://www.stsylvesterli.org; user-uploaded publications dated 2026-11-06
    (November 8 bulletin), 2026-10-31, 2026-10-24, 2026-10-17. Container 03/1145 (named in the 8 November
    file name) answered 403 for every week probed back to 2026-10-11.'
- url: https://www.stsylvesterli.org/bulletin
  seen: 2026-11-13
  note: The parish site's Bulletin page embeds parishesonline.com/publicationWidget?type=publication&id=0018000000Qx82rAAB.
bulletin_status: available
fetch_gap:
  kind: po-user-upload
  seen: 2026-11-13
  note: 'The parish uploads its own bulletin to its ParishesOnline org as a user publication (customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx82rAAB/publications/<n>-<name>.pdf,
    file names like ''03-1145 - November 8 bulletin with Ads.pdf''), not as an LPi container issue. fetch:check
    on 2026-11-13: parishes_online with provider_id st-sylvester-roman-catholic-church failed ''No matching
    anchor link found for parishes-online provider_id''; other on stsylvesterli.org/bulletin picked 2022+Ministry+Guide.pdf
    (the site''s widget is a JS iframe); page-pdfs on the org page fetched an HTML ''Online Directory''
    page (not_pdf). probe po lists the uploads with dates.'
  url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx82rAAB/publications/1794001654588-03-1145%20-%20November%208%20bulletin%20with%20Ads.pdf
---

## Publisher

St. Sylvester, 68 Ohio Avenue, Medford lays out its own weekly bulletin (PDF Creator "Microsoft Publisher 2021") and uploads it to its ParishesOnline org (`st-sylvester-roman-catholic-church`, LPi id 0018000000Qx82rAAB). The 8 November 2026 issue (uploaded 2026-11-06, `https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx82rAAB/publications/1794001654588-03-1145%20-%20November%208%20bulletin%20with%20Ads.pdf`, read 2026-11-13) is headed "32nd Sunday in Ordinary Time ... November 8, 2026" and names Rev. Gius Garcia, Pastor, and Rev. Paul Bersamin, Parochial Vicar. Weekend Masses: Saturday 5:00pm; Sunday 7:30 am, 9:00 am and 11:00 am; Vietnamese Mass Sunday 3:00 pm; daily Mass Monday, Tuesday, Thursday and Friday 8:30 am in the church.

The batch brief says St. Sylvester and Resurrection, Farmingville share a pastor (June 2025). Their bulletins are separate: this issue names only St. Sylvester's staff and Masses (it mentions Resurrection only to announce a Holy Hour "at Resurrection on 50 Granny Road, Farmingville"), while Resurrection's 15 November issue has its own masthead and schedule (`resurrection-farmingville`; see `publication_reviews` there).

## Worship sites

One: the church at 68 Ohio Avenue (`st-sylvester-medford-church`). The schedule names no other building. The diocesan locator (directory:133), GCatholic (16883) and the Mass-times page list only this church.

## Website and bulletin provider

www.stsylvesterli.org (Duda) embeds the ParishesOnline publication widget for this LPi id on its Bulletin page. The issues are user uploads on the org, not LPi container issues: container 03/1145, named in the file name, answered 403 for every week back to 11 October. No collector reads them (2026-11-13): `fetch:check` as `parishes_online` found no matching anchor on the org page, unpinned `other` on the Bulletin page picked a 2022 ministry guide PDF, and `page-pdfs` on the org page got an HTML page. The row is `unsupported` with `fetch_gap` `po-user-upload`, keeping its ParishesOnline ids.

## Not yet confirmed

Nothing about the parish or church. When the ParishesOnline collector reads user-uploaded publications, set `bulletin_provider: parishes_online` with `provider_id` st-sylvester-roman-catholic-church, run `fetch:check` and clear `fetch_gap`.
