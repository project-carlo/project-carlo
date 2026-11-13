---
name: Our Lady of Consolation
website: https://olcny.us/gazetka-parafialna
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://olcny.us/gazetka-parafialna']
group: Deanery B1 (Brooklyn West)
evidence:
- url: https://olcny.us/download/1793309455-f11ccf1b36b151c894119d10ef35cacb
  seen: 2026-11-07
  quote: 'Account Name: Our Lady of Consolation'
  note: 25 October 2026 issue, 4 pages, linked 'Pobierz numer' from the newest card on /gazetka-parafialna.
    Page 1 (masthead is an image, rendered) reads 'Sunday October 25th, 2026 Our Lady of Consolation R.C.
    Church', OUR LADY OF CONSOLATION ROMAN CATHOLIC CHURCH, 184 Metropolitan Avenue, Brooklyn, New York,
    11249, Office 718-388-1942, Website olcny.us; Mass schedule weekdays 7:00 AM English and 7:00 PM Polish,
    Saturday 8:00 AM Polish, Sunday Vigil 7:00 PM Polish, Sunday 8:00 AM Polish, 9:30 AM English, 11:00
    AM Polish, 7:00 PM Polish. Pastor Fr. Wieslaw P. Strzadala, SDS (Salvatorians).
- url: https://olcny.us/gazetka-parafialna
  seen: 2026-11-07
  quote: 'data dodania:  niedziela, 25.10.2026'
  note: 'Bulletin (gazetka parafialna) page, newest first: weekly cards 23.08.2026 through 25.10.2026,
    each with a PNG of page 1 under /storage/Newspaper/ and a ''Pobierz numer'' link to https://olcny.us/download/<epoch>-<hash>,
    which serves the PDF with no .pdf in its address.'
- url: https://parishesonline.com/organization/our-lady-of-consolation-church-11211
  seen: 2026-11-07
  note: 'probe po: ParishesOnline org Our Lady of Consolation Church, 184 Metropolitan Ave (lpi 0018000000QxB7FAAV),
    has no publications; not the bulletin, so not a publication id.'
research:
- method: pnpm fetch:check with page-pdfs https://olcny.us/gazetka-parafialna
  url: https://olcny.us/gazetka-parafialna
  checked: '2026-11-07'
  outcome: unsupported-format
  next_action: When a collector reads extensionless download links (or page-pdfs follows links whose response
    is application/pdf), set bulletin_provider other with that recipe, run fetch:check, and clear the
    fetch_gap.
  retry_when: A collector for extensionless /download/ links lands
- method: Read the newest card's date on /gazetka-parafialna
  url: https://olcny.us/gazetka-parafialna
  checked: '2026-11-07'
  outcome: found
  next_action: Recheck that issues after 25 October 2026 appear; on 7 November the 1 November issue was
    not yet posted.
  revisit_after: 2026-11-21
bulletin_status: available
fetch_gap:
  kind: extensionless-download-link
  seen: 2026-11-07
  note: 'Each issue on https://olcny.us/gazetka-parafialna is linked as https://olcny.us/download/<epoch>-<hash>
    with no .pdf in the address; it serves the PDF, but page-pdfs skips it (fetch:check 2026-11-07: ''No
    PDF links found on bulletin page''). The card''s date is in the text ''data dodania: niedziela, DD.MM.YYYY''.'
  url: https://olcny.us/download/1793309455-f11ccf1b36b151c894119d10ef35cacb
---

## Publisher

Our Lady of Consolation (Polish and English, served by the Salvatorian Fathers, SDS) publishes its own four-page weekly bulletin (gazetka parafialna) as a PDF on https://olcny.us/gazetka-parafialna. The newest issue on 7 November 2026 was dated Sunday 25 October 2026 (card 'data dodania: niedziela, 25.10.2026'; link https://olcny.us/download/1793309455-f11ccf1b36b151c894119d10ef35cacb). Its page 1 header and masthead are images (rendered 2026-11-07): "Sunday October 25th, 2026 Our Lady of Consolation R.C. Church", "OUR LADY OF CONSOLATION ROMAN CATHOLIC CHURCH, 184 Metropolitan Avenue, Brooklyn, New York, 11249", office 718-388-1942, website olcny.us. Page 4's text gives "Account Name: Our Lady of Consolation". No LPi, John Patrick or Church Bulletin Inc. footer. The ParishesOnline org our-lady-of-consolation-church-11211 exists but has no publications.

## Worship sites

One church, Our Lady of Consolation, 184 Metropolitan Avenue: the bulletin's schedule lists only this church (weekdays 7:00 AM English and 7:00 PM Polish; Saturday 8:00 AM Polish; Sunday Vigil 7:00 PM Polish; Sunday 8:00 AM Polish, 9:30 AM English, 11:00 AM Polish, 7:00 PM Polish), and the homepage gives the same times. The directory, deanery list, GCatholic 16629 and Mass finder 1127 list no other building.

## Website and bulletin provider

`unsupported`, fetch_gap `extensionless-download-link`: the issues are real PDFs, but each is linked as `/download/<epoch>-<hash>` with no `.pdf`, and `fetch:check` with `page-pdfs https://olcny.us/gazetka-parafialna` reported 'No PDF links found on bulletin page' (2026-11-07). The website is set to the bulletin page so a future collector can read it. The masthead and cover are images; the schedule on page 1 has a text layer.

## Not yet confirmed

The 1 November 2026 issue was not posted by 7 November; whether the parish posts weekly with a lag of about two weeks is to be rechecked after 21 November 2026 (research).
