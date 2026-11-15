---
name: St. Rocco, Johnston
website: https://www.churchofsaintrocco.org/
bulletin_provider: other
provider_id: page-pdfs https://www.churchofsaintrocco.org/archived-bulletins
publication: ['url:https://www.churchofsaintrocco.org/']
group: ''
evidence:
- url: https://www.churchofsaintrocco.org/_files/ugd/29fe1c_19ea809b9b59426493f035326869460d.pdf
  seen: 2026-11-15
  note: 'Issue linked as ''Bulletin'' from the homepage on 2026-11-15: 8 pages, image-only (no text layer),
    read rendered. Page 1 masthead ''St. Rocco Church / "Parrocchia San Rocco" / 927 Atwood Avenue | Johnston,
    Rhode Island 02919'', Rev. Giacomo Capoverdi, Pastor; MASS SCHEDULE: Vigil Saturday Evening Mass 5:00
    pm, Sunday 8am Mass (Bi-Lingual Italian/English), 10:00 am, 12:00 pm; Monday through Friday 7:00 am;
    Saturday Morning & Legal Holidays 8:00 am. Page 2 headed ''THE THIRTY-SECOND SUNDAY IN ORDINARY TIME
    NOVEMBER 8, 2026''.'
- url: https://www.churchofsaintrocco.org/archived-bulletins
  seen: 2026-11-15
  note: Wix 'Archived Bulletins' page (read with visit.py --links) lists dated PDFs oldest first, 'June
    7, 2026' ... 'October 18, ...', each a hashed _files/ugd/29fe1c_<hash>.pdf link.
revisit: Rerun fetch:check and confirm it picks the 22 November 2026 (or later) issue, page 2 header date.
revisit_after: 2026-11-24
bulletin_status: available
---

## Publisher

St. Rocco posts its own weekly bulletin as PDFs on its Wix site. The issue linked as "Bulletin" from the homepage on 15 November 2026 (https://www.churchofsaintrocco.org/_files/ugd/29fe1c_19ea809b9b59426493f035326869460d.pdf) is image-only; read rendered, page 1 is the masthead "St. Rocco Church / 'Parrocchia San Rocco' / 927 Atwood Avenue | Johnston, Rhode Island 02919" with Rev. Giacomo Capoverdi, Pastor, and page 2 is headed "THE THIRTY-SECOND SUNDAY IN ORDINARY TIME NOVEMBER 8, 2026". The 15 November issue had not been posted when checked.

## Worship sites

One church, 927 Atwood Avenue: Saturday 5:00 pm, Sunday 8:00 (bilingual Italian/English), 10:00 am and 12:00 pm, Monday-Friday 7:00 am, Saturday 8:00 am (page 1). St. Brigid, 1231 Plainfield St., Johnston, merged into St. Rocco and closed on 1 July 2019 per the diocesan finder; the November 8 masthead and schedule name no other church. St. Brigid has its own `excluded/` record. St. Rocco Regional School (931 Atwood Ave.) is a school.

## Website and bulletin provider

`other`, recipe `page-pdfs https://www.churchofsaintrocco.org/archived-bulletins` as printed by `fetch:check` on 2026-11-15. The site's header link "Bulletin" (on every page) points to the current issue; the Archived Bulletins page lists older issues oldest first. `fetch:check` picked the header's current issue (`29fe1c_19ea809b...pdf`, the 8 November 2026 issue, the newest posted when checked). File names are Wix hashes (`_files/ugd/29fe1c_<hash>.pdf`) with no date and the issues are image-only, so `fetch:check` reports freshness `unknown`; extraction will need OCR.

## Not yet confirmed

Whether the recipe moves to the next issue when the parish replaces the header "Bulletin" link: rerun `fetch:check` after the 22 November 2026 issue is posted and check page 2's date.
