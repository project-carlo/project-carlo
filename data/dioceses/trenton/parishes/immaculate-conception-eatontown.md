---
name: Church of Immaculate Conception
website: http://eatoncatholic.org/
bulletin_provider: other
provider_id: page-pdfs http://eatoncatholic.org/WeeklyBulletin/list.asp
publication: ['url:http://eatoncatholic.org/WeeklyBulletin/list.asp']
group: Cohort 28 (Eatontown, Monmouth Beach, Wayside)
evidence:
- url: http://eatoncatholic.org/WeeklyBulletin/opendoc.asp?b_id=7387
  seen: 2026-10-30
  quote: '미사: 주일 10:30am'
  note: 'Page 1 of the 25 October 2026 issue (no. 2018, 2 pages, Korean, text layer): ''www.eatoncatholic.org'',
    address ''64 Broad St. Eatontown, NJ 07724 | TEL: (732) 389-3830'', ''본당신부'' (pastor) 장 민호 미카엘 (Michael
    Jang), Sunday Mass 10:30am; page 2 notes weekday Mass Monday 2 to Friday 6 November at 7:30 pm in
    the church. Names no other parish; a different file from St. Dorothea''s and Precious Blood''s.'
- url: http://eatoncatholic.org/WeeklyBulletin/list.asp
  seen: 2026-10-30
  quote: Eatontown Korean Catholic Church
  note: Site header 'Eatontown Korean Catholic Church / Church of Immaculate Conception, Eatontown, N.J.'.
    The page (ASP, EUC-KR) lists issues newest first, 25 Oct 2026 (no. 2018) back by week through the
    year, each linked as opendoc.asp?b_id=<n> that serves a PDF (b_id 7387 for 25 October).
- url: https://files.ecatholic.com/14277/documents/2024/7/2024%20July%20-%20Updated%20%20Parish%20Cohorts%20and%20Deaneries.pdf
  seen: 2026-10-30
  note: 'July 2024 cohort list: Cohort 28 is Precious Blood (Monmouth Beach), St. Dorothea (Eatontown),
    Immaculate Conception (Eatontown, in parentheses) and St. Anselm (Wayside).'
research:
- method: fetch:check with the recipe 'page-pdfs http://eatoncatholic.org/WeeklyBulletin/list.asp', then
    'linked-issue-page', 'redirected-pdf' and 'dated-post' on the same page
  url: http://eatoncatholic.org/WeeklyBulletin/list.asp
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: 'Add a collector (or extend page-pdfs) for ASP document links with no .pdf extension: list.asp''s
    issues are ''opendoc.asp?b_id=<n>'' links (relative, 7387 = 25 Oct 2026) that answer 200 application/pdf
    with Content-Disposition inline. Every recipe fails with ''No PDF links found on bulletin page''.
    Fetching one issue by hand (probe pdf, probe get --out) works and the 25 Oct file is a readable 2-page
    Korean PDF.'
  retry_when: A collector that follows extensionless document links (opendoc.asp?b_id=) exists in src/pdf_extract/parish_sites/collectors.py
bulletin_status: available
publication_reviews:
- parish: precious-blood-monmouth-beach
  decision: separate
  evidence:
  - url: http://eatoncatholic.org/WeeklyBulletin/opendoc.asp?b_id=7387
    seen: 2026-10-30
    quote: '미사: 주일 10:30am'
    note: 'Bulletin for Church of Immaculate Conception (row immaculate-conception-eatontown), read by
      its map batch: Page 1 of the 25 October 2026 issue (no. 2018, 2 pages, Korean, text layer): ''www.eatoncatholic.org'',
      address ''64 Broad St. Eatontown, NJ 07724 | TEL: (732) 389-3830'', ''본당신부'' (pastor) 장 민호 미카엘 (Michael
      Jang), Sunday Mass 10:30am; page 2 notes weekday Mass Monday 2 to Friday 6 November at 7:30 pm in
      the church. Names no other parish; a different file from St. Dorothea''s and Precious Blood''s.'
  - url: https://cloud-1de12d.becdn.net/customfile/ebb273e3fe75a6e49bd62ed19bb698286b0f46145f3a7bd41a18ec91be7c6cef/Bulletin-PBC-Oct-25-2026-O30.pdf
    seen: 2026-10-30
    quote: 72 Riverdale Avenue
    note: 'Bulletin for Church of the Precious Blood (row precious-blood-monmouth-beach), read by its
      map batch: Masthead, page 1 of the 25 October 2026 issue (Bulletin-PBC-Oct-25-2026-O30.pdf, 4 pages,
      text layer): Church of the Precious Blood, 72 Riverdale Avenue, Monmouth Beach, NJ 07750, 732-222-4756;
      Rev. Michael Sullivan, Pastor and Rev. Andrés Serna, Parochial Vicar. Mass schedule (Mass intentions):
      Saturday 5:30p; Sunday 8:00a, 9:30a, 11:00a; weekdays 8:30a. Page 3 prints a table, SUNDAY MASSES
      / WEEKDAY MASSES OF OUR LINKED PARISHES, with both Precious Blood and St. Dorothea. The file (md5
      3644811e...) is not the St. Dorothea file (md5 8caa7516...) for the same Sunday: the intentions
      and Mass times are Precious Blood only.'
- parish: st-anselm-wayside
  decision: separate
  evidence:
  - url: http://eatoncatholic.org/WeeklyBulletin/opendoc.asp?b_id=7387
    seen: 2026-10-30
    quote: '미사: 주일 10:30am'
    note: 'Bulletin for Church of Immaculate Conception (row immaculate-conception-eatontown), read by
      its map batch: Page 1 of the 25 October 2026 issue (no. 2018, 2 pages, Korean, text layer): ''www.eatoncatholic.org'',
      address ''64 Broad St. Eatontown, NJ 07724 | TEL: (732) 389-3830'', ''본당신부'' (pastor) 장 민호 미카엘 (Michael
      Jang), Sunday Mass 10:30am; page 2 notes weekday Mass Monday 2 to Friday 6 November at 7:30 pm in
      the church. Names no other parish; a different file from St. Dorothea''s and Precious Blood''s.'
  - url: https://container.parishesonline.com/bulletins/03/1017/20261101B.pdf
    seen: 2026-10-30
    quote: 1028 Wayside Road
    note: 'Bulletin for Church of St. Anselm (row st-anselm-wayside), read by its map batch: Masthead,
      page 1 of the 1 November 2026 issue (8 pages, text layer): ''CHURCH OF SAINT ANSELM'', 1028 Wayside
      Road, Wayside, NJ 07712, 732.493.4411. Mass schedule: Saturday 4:30pm; Sunday 9:00am & 11:00am;
      weekdays Monday, Wednesday and Friday 9:00am; Reconciliation Saturday 3:00-4:00pm. Names this parish
      alone. The 25 October issue (same container) page 2 lists ''Parish Administrator Rev. Carlo Calisin''.'
- parish: st-dorothea-eatontown
  decision: separate
  evidence:
  - url: http://eatoncatholic.org/WeeklyBulletin/opendoc.asp?b_id=7387
    seen: 2026-10-30
    quote: '미사: 주일 10:30am'
    note: 'Bulletin for Church of Immaculate Conception (row immaculate-conception-eatontown), read by
      its map batch: Page 1 of the 25 October 2026 issue (no. 2018, 2 pages, Korean, text layer): ''www.eatoncatholic.org'',
      address ''64 Broad St. Eatontown, NJ 07724 | TEL: (732) 389-3830'', ''본당신부'' (pastor) 장 민호 미카엘 (Michael
      Jang), Sunday Mass 10:30am; page 2 notes weekday Mass Monday 2 to Friday 6 November at 7:30 pm in
      the church. Names no other parish; a different file from St. Dorothea''s and Precious Blood''s.'
  - url: https://uploads.weconnect.com/mce/0d467c11c1f788a43266782aac388b66b0f22551/Bulletin%20DOR%20Oct%2025%202026%20O30.pdf
    seen: 2026-10-30
    quote: 240 Broad Street
    note: 'Bulletin for St. Dorothea Parish (row st-dorothea-eatontown), read by its map batch: Masthead,
      page 1 of the 25 October 2026 issue (Bulletin DOR Oct 25 2026 O30.pdf, 4 pages, text layer): St.
      Dorothea Church, 240 Broad Street, Eatontown, NJ 07724, 732-542-0148; Rev. Michael Sullivan, Pastor
      and Rev. Andrés Serna, Parochial Vicar. Mass intentions: Saturday 4:00p; Sunday 8:30a, 10:00a; Monday,
      Wednesday, Thursday, Friday 12:15p; Tuesday 7:00p; Sunday 3p Filipino/English Mass at St. Dorothea.
      Page 3 prints SUNDAY MASSES / WEEKDAY MASSES OF OUR LINKED PARISHES for Precious Blood and St. Dorothea.
      The file (md5 8caa7516...) differs from Precious Blood''s for the same Sunday.'
---

## Publisher

Immaculate Conception, Eatontown is the diocese's Korean-language community (site title 'Eatontown Korean Catholic Church'). It publishes its own two-page Korean bulletin weekly on eatoncatholic.org (WeeklyBulletin/list.asp, issues served as PDFs by opendoc.asp?b_id=n). The 25 October 2026 issue (no. 2018) gives 64 Broad St., Eatontown, its own pastor (장 민호 미카엘) and a Sunday 10:30am Mass. It names no other parish, so it is a row of its own; the cohort list puts it in parentheses under Cohort 28 (a cohort is not a shared bulletin).

## Worship sites

One church, Immaculate Conception at 64 Broad St. The bulletin lists the Sunday Mass and a weekday Mass in the first week of November; whether the building also hosts English-language Masses is not stated in the bulletin.

## Website and bulletin provider

A self-hosted ASP site. The row is `other` with a `page-pdfs` recipe on the list page, but the fetch resolver cannot collect it: each issue is an extensionless `opendoc.asp?b_id=<n>` link that serves a PDF, so every recipe fails with 'No PDF links found'. See the research item; the bulletin itself is readable by hand.

## Not yet confirmed

The fetch resolver does not collect this site's issues (research). The bulletin is in Korean: identity and Mass times were read from its Latin-script address line and numerals. No English-language Mass at this church was seen.
