---
name: The Church of Saint Stephen, Kearny
website: https://ststephenkearny.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/628
publication: ['url:https://www.church-bulletin.org/saint-stephen-s-church-kearny-nj-07032']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-stephen-s-church-kearny-nj-07032/2026-11-01.pdf
  seen: 2026-11-04
  quote: 628 St. Stephen, Kearny, NJ (B) John Patrick Publishing Company
  note: '1 November 2026 issue, 12 pages, text layer. Page 1 masthead: ''The Church of Saint Stephen ~
    La Iglesia de San Esteban'', ''Archdiocesan Sanctuary of the Four Chaplains'', ''141 Washington Avenue,
    Kearny, NJ 07032'', ''www.ststephenkearny.com'', ''All Saints Day – November 1, 2026''; Liturgy Schedule:
    Saturday Vigil 5:00 pm (English); Sunday 8:00 am, 10:00 am, 12:00 pm (English), 1:30 pm (Español),
    7:00 pm (English); Monday-Friday 9:00 am; Wednesday 7:00 pm (Español); Saturday 8:30 am. Footer on
    page 12 (quoted).'
- url: https://church-bulletin.org/628
  seen: 2026-11-04
  note: Redirects to church-bulletin.org/saint-stephen-s-church-kearny-nj-07032; dated weekly issues,
    newest 2026-11-01.
- url: https://ststephenkearny.com/
  seen: 2026-11-04
  note: eCatholic site (ecatholic:13535; probe get answers 403, visit.py loads it, title 'St. Stephens
    Church - Kearny, NJ'). It links https://www.jppc.net/onlinebulletins/628template.pdf and https://www.church-bulletin.org/saint-stephen-s-church-kearny-nj-07032;
    its files.ecatholic.com PDFs are newsletters and forms, not bulletins.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

The Church of Saint Stephen, Kearny, publishes a weekly bulletin printed by John Patrick Publishing (id 628). I read the 1 November 2026 issue (12 pages, text): page 1 masthead 'The Church of Saint Stephen ~ La Iglesia de San Esteban, Archdiocesan Sanctuary of the Four Chaplains, 141 Washington Avenue, Kearny, NJ 07032', with one Liturgy Schedule; page 12 footer '628 St. Stephen, Kearny, NJ (B) John Patrick Publishing Company'. It does not mention Our Lady of Sorrows, St. Cecilia or the Redemptoris Mater seminary (grep for 'Sorrows', 'Seminar', 'Neocatechumen', 'Passaic', 'chapel': no hits).

## Worship sites

- The Church of Saint Stephen, 141 Washington Avenue (`st-stephen-kearny`): Saturday Vigil 5:00 pm; Sunday 8:00 am, 10:00 am, 12:00 pm, 1:30 pm (Spanish), 7:00 pm; Monday-Friday 9:00 am; Wednesday 7:00 pm (Spanish); Saturday 8:30 am.

The directory (94) and GCatholic (18460) list this church. GCatholic also lists the Redemptoris Mater Archdiocesan Missionary Seminary at 672 Passaic Avenue, Kearny (125251), a seminary with no public Mass schedule found: `excluded/redemptoris-mater-seminary-kearny`.

## Website and bulletin provider

https://ststephenkearny.com/ (the directory's link and the masthead's website) is an eCatholic site behind Cloudflare; it links the John Patrick template 628template.pdf and the church-bulletin.org listing. Provider `other`, read with `page-pdfs https://church-bulletin.org/628`; the eCatholic id is left out of `publication` because it identifies the website, not the bulletin. GCatholic's website http://www.thechurchofsaintstephen.com does not resolve (probe url DEAD-DNS, 2026-11-04).

Fetch check (2026-11-04, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/628: current` and picked church-bulletin.org/bulletin/saint-stephen-s-church-kearny-nj-07032/2026-11-01.pdf, the 1 November 2026 issue read above; freshness fresh (3 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
