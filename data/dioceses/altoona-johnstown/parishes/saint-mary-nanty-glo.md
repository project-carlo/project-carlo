---
name: Saint Mary Parish, Nanty Glo
website: https://stmarysnantyglo.org
bulletin_provider: other
provider_id: page-pdfs https://stmarysnantyglo.org
publication: ['url:https://stmarysnantyglo.org']
group: ''
evidence:
- url: https://stmarysnantyglo.org/wp-content/uploads/2026/10/Oct-18.pdf
  seen: 2026-10-21
  note: 'Image-only PDF (4 pages, no text layer; `probe pdf` reports "scanned images"), so this is a note
    from the rendered page 1 (pdftoppm -r 80), not a quote. Masthead "SAINT MARY''S PARISH COMMUNITY,
    1020 CAROLINE STREET, NANTY GLO, PA 15943", "October 18, 2026 29th Sunday in Ordinary Time", pastor
    Father Kevin Queally, T.O.R., Deacon James J. Janosik, rectory 749-9103. MASS SCHEDULE: Daily Monday
    through Friday 8:30 AM; Saturday 4:30 PM; Sunday 8:00 AM & 10:30 AM; Sacrament of Penance Friday 8:00
    AM, Saturday 3:30 PM - 4:15 PM. It names St. Mary alone (the Elementary Religious Education line mentions
    St. John Vianney, a school/program, not a Mass site).'
- url: https://stmarysnantyglo.org
  seen: 2026-10-21
  note: 'WordPress parish site (title "Saint Mary Parish | A Catholic Faith Community"). `probe url` lists
    bulletin PDFs under wp-content/uploads/2026/10/ (October-11.pdf, Oct-18.pdf); `fetch:check` picked
    Oct-18.pdf ("page-pdfs on https://stmarysnantyglo.org: current", url_date 2026-10-18, status ok).'
- url: https://discovermass.com/church/st-mary-nanty-glo-pa/
  seen: 2026-10-21
  quote: Shucks! There are no bulletins available.
  note: Discover Mass page for St. Mary, Nanty Glo has an empty Bulletins tab; not a channel.
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory: Saint Mary Parish, Nanty Glo, 1020 Caroline Street 15943, homepage stmarysnantyglo.org;
    Masses Sat 4:30 PM, Sun 8:00 AM and 10:30 AM, Mon-Fri 8:30 AM; Confession Sat 3:30 PM, Fri 8:00 AM.
    Matches the bulletin.'
promoted: 2026-10-21
---

## Publisher

Saint Mary Parish (Father Kevin Queally, T.O.R.) publishes its own weekly bulletin as a PDF on its WordPress site, `stmarysnantyglo.org` (`wp-content/uploads/<YYYY>/<MM>/Oct-18.pdf`, `October-11.pdf`). The 18 Oct 2026 issue is an image-only PDF; read from a rendering on 2026-10-21 it is headed "SAINT MARY'S PARISH COMMUNITY, 1020 CAROLINE STREET, NANTY GLO" and carries one Mass schedule. It is not shared with another parish. Whether the pipeline can extract Mass times from an image-only bulletin is for the later stages; the fetch is fine.

## Worship sites

One: St. Mary, 1020 Caroline Street (see `churches/saint-mary-nanty-glo.md`). GCatholic's St. Nicholas of Myra, Nanty Glo (17304) is Eastern Catholic and belongs to another batch; it is not in this bulletin.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stmarysnantyglo.org`: `fetch:check` on 2026-10-21 picked `Oct-18.pdf` as "current" (url_date 2026-10-18). The same page also links a July 2026 flyer ("The-Pardon-of-Assisi") and a 2022 windows brochure, so a "current" pick relies on the dated file name; check it again if the parish renames files.

## Not yet confirmed

Nothing blocking.
