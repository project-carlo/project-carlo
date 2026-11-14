---
name: Christ the King
website: https://www.ctkrcc.org/bulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.ctkrcc.org/bulletins']
group: ''
evidence:
- url: https://www.canva.com/design/DAHZlltyniw/h8EVowKfNcCsuE2_aZlU8w/view
  seen: 2026-11-13
  note: 'Canva design titled ''Bulletin | November 8 2026'', reached from the archive''s newest ''Read''
    link (canva.link/t9arvw49vgg46tq) and read with visit.py --text: ''NOVEMBER 8TH 2026 / THIRTY-SECOND
    SUNDAY IN ORDINARY TIME / ISSUE NO. 292 / 2 INDIAN HEAD ROAD | COMMACK | NY | 11725 / www.ctkrcc.org'';
    SUNDAY MASS ''Saturday Vigil | 5PM, Sundays | 8AM, 10AM, 12PM''; DAILY MASS ''Monday to Saturday |
    9AM''; Pastoral staff ''Fr. Robert Ketcham''. No other place of Mass; no printer named.'
- url: https://www.ctkrcc.org/bulletins
  seen: 2026-11-13
  note: 'Squarespace ''BULLETIN ARCHIVE'' read with visit.py: issues newest first (''Thirty-second Sunday
    in Ordinary Time, November 8, 2026'', ''All Saints, November 1, 2026'', ...), each with a ''Read''
    link to canva.link or canva.com/design/.../view.'
research:
- method: fetch:check (provider other, unpinned, via tools/fc_unsupported.sh)
  url: https://www.ctkrcc.org/bulletins
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Set provider other with a Canva recipe once a collector reads Canva design views, then
    run fetch:check
  retry_when: A Canva collector lands or the parish posts bulletin PDFs
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-13
  url: https://www.ctkrcc.org/bulletins
  note: The Squarespace Bulletin Archive lists each issue as a 'Read' link to a canva.link short link
    (newest 'Thirty-second Sunday in Ordinary Time, November 8, 2026' -> https://canva.link/t9arvw49vgg46tq),
    which opens a Canva design viewer (canva.com/design/DAHZlltyniw/.../view, title 'Bulletin | November
    8 2026'); no PDF is linked. See research for the fetch:check result.
---

## Publisher

Christ the King, Commack, publishes its own weekly bulletin as a Canva design. The newest issue on 2026-11-13, "Bulletin | November 8 2026" (`https://www.canva.com/design/DAHZlltyniw/h8EVowKfNcCsuE2_aZlU8w/view`, read as text with visit.py), gives "NOVEMBER 8TH 2026", "ISSUE NO. 292", "2 INDIAN HEAD ROAD | COMMACK | NY | 11725", www.ctkrcc.org, and Fr. Robert Ketcham at the head of the pastoral staff. No printer is named.

## Worship sites

One: the church at 2 Indian Head Road (`christ-the-king-commack-church`). The issue's SUNDAY MASS (Saturday Vigil 5PM; Sundays 8AM, 10AM, 12PM) and DAILY MASS (Monday to Saturday 9AM) name no other place, and the diocesan locator, GCatholic and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

ctkrcc.org is a Squarespace site; its `/bulletins` page is a Bulletin Archive, newest first, whose 'Read' links are canva.link short links or canva.com design-view links. The bulletin exists only in Canva's JavaScript viewer, so the row is `unsupported` with fetch_gap `canva-design-viewer`, as Beach Catholic.

fetch:check (2026-11-13, provider `other` for the check) reported resolve_failed "No PDF links found on bulletin page".

## Not yet confirmed

Nothing about the parish. The row goes live when a collector reads Canva design views or the parish posts PDFs; see research.
