---
name: St. Lawrence
website: https://saint-lawrence-church.org
bulletin_provider: other
provider_id: page-pdfs https://saint-lawrence-church.org/bulletins
publication: ['url:https://saint-lawrence-church.org/bulletins']
group: ''
evidence:
- url: https://saint-lawrence-church.org/bulletins
  seen: 2026-10-29
  note: The parish's own Bulletins page (GoDaddy Website Builder, probe get HTTP 200) links nine dated
    PDFs on img1.wsimg.com, 'Bulletin Sept 6 2026 Final.pdf' to 'Bulletin November 1 2026 Final.pdf',
    in no useful order (hash-named download paths). The 25 October file was read.
- url: https://img1.wsimg.com/blobby/go/5f7d4b64-aed9-4c06-9603-9f147e46a35a/downloads/d851761c-2306-4fd0-b9bf-6c3aef85a758/Bulletin%20October%2025%202026%20Final.pdf
  seen: 2026-10-29
  quote: 'Mass Schedule: Saturday Evenings @ 5PM; Sunday Morning @ 9:30AM'
  note: 'The 25 October 2026 issue (2 pages, text layer, md5 8688864a8fc5e11d2e053062b1f5d68b): masthead
    ''Church of Saint Lawrence, 345 Elmwood Lane, Riegelsville, PA 18077'', Rev. Walter J Benn, Pastor,
    Rectory 610-749-2684. Schedule: Saturday 5PM, Sunday 9:30AM, Holy Days 9AM, 12 Noon and 7PM, Monday,
    Tuesday, Wednesday, Friday and Saturday 9AM, Thursday ''Readings & Communion Distribution Only''.
    One church only.'
bulletin_status: available
---

## Publisher

St. Lawrence, Riegelsville (Rev. Walter J. Benn, pastor) publishes its own two-page bulletin on its GoDaddy-built site, `saint-lawrence-church.org/bulletins`; John Patrick has no listing for it (the survey and the batch note found none). The 25 October 2026 issue is headed 'Church of Saint Lawrence, 345 Elmwood Lane, Riegelsville, PA 18077' with one Mass schedule: Saturday 5PM, Sunday 9:30AM, Holy Days 9AM, 12 Noon and 7PM, weekdays Monday, Tuesday, Wednesday, Friday and Saturday 9AM; on Thursday the 9AM service is 'Reading & Communion Distribution Only', not Mass.

## Worship sites

One church, `st-lawrence-riegelsville` (founded 1974, a mission from 1872 per the directory). The Pastor's Corner offers a bus to the March for Life to 'parishioners of St. John the Baptist Parish and St. Lawrence Parish'. St. John the Baptist, Ottsville is a separate directory parish (pastor Rev. Selvaraj Lucas, M.S.C.) with its own site; nothing in this bulletin lists a Mass there, so it is a lead for that batch, not a worship site here.

## Website and bulletin provider

`other`, reading `page-pdfs` on the parish's `/bulletins` page, whose nine links are hash-named `img1.wsimg.com` downloads whose file names carry the date.

## Fetch check

`fetch:check` (2026-10-29, headed Chrome) with the `page-pdfs` recipe in `provider_id` picked `https://img1.wsimg.com/blobby/go/5f7d4b64-aed9-4c06-9603-9f147e46a35a/downloads/d01cf710-6af8-4767-8ff0-87fe7b6ac7d6/Bulletin%20November%201%202026%20Final.pdf?ver=1793201676287`: transport ok, PDF, freshness `future` (the parish posts next Sunday early: the file is the 1 November 2026 issue, masthead 'November 1, 2026 – All Saints Day', same masthead and Mass schedule); the 25 October file is also on the page. Issue date inferred from the file name. Expect `future` whenever the next issue is already posted. The check printed no separate recipe; the one in `provider_id` is the one used. Identity is `unverified` only because the check is given no expected identity; the masthead was read from the file (above).
