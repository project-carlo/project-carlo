---
name: Saint Ignatius of Loyola
website: https://www.stignatiusofloyola.org/bulletin
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.stignatiusofloyola.org/bulletin']
group: ''
evidence:
- url: https://www.stignatiusofloyola.org/_files/ugd/b7c955_0f300c33c83d4f9285f82f5c43830804.pdf
  seen: 2026-10-19
  quote: St. Ignatius of Loyola Catholic Church
  note: 'The 18 October 2026 issue (8 pages), linked as "This Weeks Bulletin". Page 1: "St. Ignatius of
    Loyola Catholic Church October 18, 2026 Twenty-Ninth Sunday in Ordinary Time", "Rev. Joseph R. Howard
    Pastor", "Deacon Steve Huete Parish Manager", "1095 Church Road, Orrtanna, Pennsylvania 17353 www.stignatiusofloyola.org".'
- url: https://www.stignatiusofloyola.org/_files/ugd/b7c955_0f300c33c83d4f9285f82f5c43830804.pdf
  seen: 2026-10-19
  quote: Rev. Joseph R. Howard
- url: https://www.stignatiusofloyola.org/bulletin
  seen: 2026-10-19
  note: 'The Wix "Weekly Church Bulletin" page (read in a browser): "This Weeks Bulletin" (the 18 October
    issue), then "Previous Bulletins" October 11, October 4, September 27 ... May 3, each an undated _files/ugd/<hash>.pdf
    link. The site header''s own "Bulletin" link points to a different file, b7c955_dda2d8e07f0049df9199c38f69969c76.pdf,
    which is the January 27 & 28, 2018 issue.'
promoted: 2026-10-20
---

## Publisher

St. Ignatius of Loyola, 1095 Church Road, Orrtanna publishes its own weekly bulletin as a
PDF on its Wix site. I read the 18 October 2026 issue: page 1 names this church alone, with
Rev. Joseph R. Howard as pastor and Deacon Steve Huete as parish manager, and gives Saturday
Vigil 5:00 pm and Sunday 8:00 and 10:30 am. Matches the diocesan directory. No partner
parish.

## Worship sites

- St. Ignatius of Loyola, 1095 Church Rd, Orrtanna (`st-ignatius-loyola-orrtanna`). The
  bulletin's other rooms ("Lower Loyola", the parish center) are parish buildings with no
  Mass of their own.

## Website and bulletin provider

`website` is the "Weekly Church Bulletin" page; each issue is an undated Wix file
(`/_files/ugd/<hash>.pdf`), so `other` with `url:` publication.

The first fetch check (2026-10-20) picked the wrong file: `page-pdfs on
https://www.stignatiusofloyola.org/bulletin: titled`, choosing
`b7c955_dda2d8e07f0049df9199c38f69969c76.pdf`, the site header's "Bulletin" link, which is
the **27-28 January 2018** issue (Bishop Gainer, Fr. DiBiccaro). This week's issue is the link
titled "This Weeks Bulletin". Every link on the page is undated, and both titles counted as
"titled", so the first listed won. The resolver now prefers a link titled "This Week's",
"Current" or "Latest Bulletin" over a bare "Bulletin" (same PR). The re-run on 2026-10-20
picked `b7c955_0f300c33c83d4f9285f82f5c43830804.pdf`, the 18 October issue quoted above, and
the recipe `page-pdfs` is pinned.

## Not yet confirmed

Nothing open. The pick rests on the link's title, so if the site renames "This Weeks Bulletin" the fetch may fall back to the 2018 header link.
