---
name: Our Lady of Sorrows, White Plains
website: https://www.olscc.com/
bulletin_provider: unsupported
provider_id: page-pdfs https://www.olscc.com/
publication: ['url:https://www.olscc.com/']
group: ''
evidence:
- url: https://www.olscc.com/_files/ugd/107fe4_3e9be5a85452459ca7d8bd409c5b08e1.pdf
  seen: 2026-10-07
  quote: Our Lady of Sorrows Parish
  note: Official home page links this six-page bulletin naming Our Lady of Sorrows and giving its public
    Mass schedule; Wix-hosted media PDF.
- url: https://www.olscc.com/_files/ugd/107fe4_704762d8eab74fa09f75509eebad17ae.pdf
  seen: 2026-11-09
  quote: Our Lady of Sorrows Parish
  note: The bulletin the homepage links on November 9, 2026, with 'Saturday, October 24, 2026' in its
    intentions (the October 25 issue). fetch:check instead picked https://www.olscc.com/_files/ugd/107fe4_827aafc7b2064986b1af6c6dd88aff35.pdf,
    the '2027 Mass Book' intention form.
research:
- method: fetch:check with page-pdfs https://www.olscc.com/, and the archive page /archived-bulletins
    read in Chrome
  url: https://www.olscc.com/archived-bulletins
  checked: '2026-11-09'
  outcome: unsupported-format
  next_action: When a collector can pick the bulletin among undated Wix ugd PDFs (by link position or
    text), set bulletin_provider other with that recipe, check that it picks this week's issue, and clear
    fetch_gap. The homepage copy also lagged two weeks on November 9.
  retry_when: A collector for the first-pdf-not-bulletin gap kind lands
fetch_gap:
  kind: first-pdf-not-bulletin
  seen: 2026-11-09
  note: The Wix homepage links the current bulletin as an unlabelled, undated _files/ugd hash-named PDF
    (107fe4_704762….pdf, the October 25, 2026 issue on 2026-11-09) after a 'Printable Mass Intention Form'
    PDF; page-pdfs on https://www.olscc.com/ picks the form (first-listed). /archived-bulletins lists
    'Week of 10/25/2026' etc. as script links. Hash names leave no filename glob to select the bulletin.
  url: https://www.olscc.com/
---

## Publisher

Official home page links this six-page bulletin naming Our Lady of Sorrows and giving its public Mass schedule; Wix-hosted media PDF.

## Channel and grouping

The parish's Wix site links its current bulletin from the homepage as an unlabelled, undated _files/ugd PDF placed after a 'Printable Mass Intention Form' PDF; /archived-bulletins lists earlier weeks ('Week of 10/25/2026' and back to 9/20/2026). On November 9, 2026 the homepage bulletin was the October 25 issue. The pinned page-pdfs recipe picked the intention form (a '2027 Mass Book' sign-up sheet), not the bulletin, and hash file names leave no filename filter, so the row is `unsupported` with a `first-pdf-not-bulletin` fetch_gap until a collector can read it.

Earlier finding kept: the current masthead, not administrative merger or account name, determines one publisher, and linked external eCatholic sites are not automatically its publication ids.

## Worship sites and scope

Linked worship-site records for Our Lady of Sorrows, White Plains: [Our Lady of Sorrows](../churches/our-lady-of-sorrows-white-plains.md). Each church record retains its building-specific Mass evidence.
