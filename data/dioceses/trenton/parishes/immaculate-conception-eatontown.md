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
---

## Publisher

Immaculate Conception, Eatontown is the diocese's Korean-language community (site title 'Eatontown Korean Catholic Church'). It publishes its own two-page Korean bulletin weekly on eatoncatholic.org (WeeklyBulletin/list.asp, issues served as PDFs by opendoc.asp?b_id=n). The 25 October 2026 issue (no. 2018) gives 64 Broad St., Eatontown, its own pastor (장 민호 미카엘) and a Sunday 10:30am Mass. It names no other parish, so it is a row of its own; the cohort list puts it in parentheses under Cohort 28 (a cohort is not a shared bulletin).

## Worship sites

One church, Immaculate Conception at 64 Broad St. The bulletin lists the Sunday Mass and a weekday Mass in the first week of November; whether the building also hosts English-language Masses is not stated in the bulletin.

## Website and bulletin provider

A self-hosted ASP site. The row is `other` with a `page-pdfs` recipe on the list page, but the fetch resolver cannot collect it: each issue is an extensionless `opendoc.asp?b_id=<n>` link that serves a PDF, so every recipe fails with 'No PDF links found'. See the research item; the bulletin itself is readable by hand.

## Not yet confirmed

The fetch resolver does not collect this site's issues (research). The bulletin is in Korean: identity and Mass times were read from its Latin-script address line and numerals. No English-language Mass at this church was seen.
