---
name: Holy Name of Jesus & St. Elizabeth
website: https://www.hnjpocomoke.org
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Ocean Deanery
evidence:
- url: https://www.hnjpocomoke.org/fr-dan-s-corner
  seen: 2026-10-27
  quote: 29th Sunday in Ordinary Time October 18, 2026
  note: 'The page behind the site''s ''Bulletin'' menu item (menu label ''Bulletin'', href /fr-dan-s-corner;
    the home page has no other bulletin link): a Wix page of weekly announcements as HTML text and no
    PDF, image or file link. It was still the 18 October issue on 27 October, with a notice that Fr. Dan
    Staniskis is away after surgery on 10 and 13 October and ''All Sunday and Saturday evening Masses
    will be celebrated at the usual times by visiting priests''.'
- url: https://www.hnjpocomoke.org/mass-confession-times
  seen: 2026-10-27
  quote: 'Pastor: Fr. Dan Staniskis'
  note: 'Every page''s header reads ''Holy Name of Jesus  St. Elizabeth  Pocomoke, MD  Westover, MD  Catholic
    Parish  Pastor: Fr. Dan Staniskis'': one parish site and one pastor for both churches. The page lists
    Holy Name Tuesday 9am, Saturday 4pm, Sunday 9:30am and St. Elizabeth Wednesday 8:30 am, Saturday 5:30
    pm, Sunday 8 am, Sunday 5 pm Spanish Mass.'
- url: https://cdow.org/deaneries/
  seen: 2026-10-27
  quote: Holy Name of Jesus, Pocomoke City
  note: The deaneries page names Holy Name of Jesus alone, in the Ocean Deanery; St. Elizabeth, Westover
    is in the directory and GCatholic but on neither the deaneries page nor the summer guide.
revisit: Check whether hnjpocomoke.org's Bulletin page links a PDF or image, or a publisher lists the
  parish.
revisit_after: 2027-01-27
research:
- method: curl and probe url on hnjpocomoke.org (home, /mass-confession-times, /fr-dan-s-corner, /resources,
    /contact-us), grep of the page source for pdf, filesusr, bulletin, parishesonline and ecatholic links;
    `probe po` on guessed slugs (holy-name-of-jesus-pocomoke, -pocomoke-city, -st-elizabeth, st-elizabeth-westover);
    the John Patrick template redirects jppc.net/onlinebulletins/<n>template.pdf for the unassigned Delaware
    numbers 300-320
  url: https://www.hnjpocomoke.org/fr-dan-s-corner
  checked: '2026-10-27'
  outcome: unsupported-format
  next_action: Re-read the bulletin page for a linked PDF or image; if the parish starts posting one,
    set the provider (page-pdfs or page-images recipe) and run fetch:check. Otherwise look for the parish
    on ParishesOnline, John Patrick (a Maryland number) or Facebook.
  retry_when: The /fr-dan-s-corner page links a PDF or image, or a publisher lists Holy Name of Jesus,
    Pocomoke
  revisit_after: 2027-01-27
bulletin_status: unsupported-format
---

## Publisher

The parish has a website bulletin page, not a file bulletin. hnjpocomoke.org (Wix) calls its /fr-dan-s-corner page 'Bulletin': weekly announcements as HTML text (the 18 October 2026 issue was still up on 27 October), with no PDF or image. The pipeline reads PDFs and images, so this is `no_bulletin` (kept in the records, off the site) with `bulletin_status: unsupported-format`. The earlier survey note that no bulletin was found (probe url, browser) is right about files; the text page was missed because its menu href is not named for a bulletin.

## One row, two churches

The site header names 'Holy Name of Jesus, Pocomoke, MD' and 'St. Elizabeth, Westover, MD', one pastor (Fr. Dan Staniskis), one phone ((410) 957-1215 in the directory for both) and one Mass-times page listing both. The directory gives both entries the same website. So the two churches are one parish row. St. Elizabeth is not on the deaneries page or the summer guide, so it is the parish's second church, not a separate parish on the diocese's list.

## Worship sites

[[holy-name-of-jesus-pocomoke-city]] and [[st-elizabeth-westover]].

## Not yet confirmed

No downloadable bulletin was found; no ParishesOnline organization (four guessed slugs) and none of the John Patrick Delaware numbers is this parish. Mass times are on the parish site's Mass page; the directory's times for both churches match it exactly. See `research`.
