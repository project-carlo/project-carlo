---
name: St. Anthony of Padua
website: https://sapde.org/
bulletin_provider: other
provider_id: page-pdfs https://sapde.org/bulletin-archive/ filename=Bulletin-*.pdf
publication: ['url:https://sapde.org/bulletin-archive/']
group: City Deanery
evidence:
- url: https://sapde.org/wp-content/uploads/2026/10/Bulletin-October-25-2026.pdf
  seen: 2026-10-27
  quote: 901 N. DuPont St., Wilmington, DE 19805
  note: 'Page 1 of the 25 October 2026 issue (6 pages): masses Sunday 9:00, 11:00 am and 5:00 pm, Monday-Friday
    6:45 am, Saturday 5:00 pm; rectory 901 N. DuPont St.; school and Padua Academy contacts; web address
    www.sapde.org. Page 2 lists St. Anthony''s own Mass intentions for 26 October-1 November (e.g. ''THANKSGIVING
    TO ST. ANTHONY MR. & MRS. ROBERTO QUEZON''). It names no other parish. Pages 5-6 carry the Bon Venture
    Services ad footer (''D86910 (JB) - St. Anthony of Padua, Wilmington''): Bon Venture only sells the
    ads, the PDF is hosted on the parish site.'
- url: https://sapde.org/bulletin-archive/
  seen: 2026-10-27
  note: 'probe url: HTTP 200, ''Bulletin Archive – Welcome to St. Anthony of Padua Roman Catholic Church''.
    The page links dated PDFs under /wp-content/uploads/YYYY/MM/Bulletin-<Month>-<DD>-<YYYY>.pdf, newest
    first (November 01 2026, October 25, 18, 11, 04, September 27, 20), along with unrelated forms and
    calendars that do not match the Bulletin- name. stanthonynet.org (GCatholic''s old domain, and the
    e-mail domain in the bulletin) is the same parish.'
---

## Publisher

St. Anthony of Padua self-hosts its weekly bulletin on sapde.org (WordPress). /bulletin-archive/ lists one PDF per Sunday, newest first, named Bulletin-<Month>-<DD>-<YYYY>.pdf. The next Sunday's issue (1 November 2026) was already posted on 27 October. The 25 October issue names this parish alone: its own Masses, rectory and school.

## Worship sites

One church, 901 N. Dupont St. (at W. 9th St.), Wilmington. The bulletin lists Sunday 9:00 and 11:00 am and 5:00 pm, Saturday 5:00 pm and weekdays 6:45 am, matching the diocese map. It names no other building. See the church record.

## Website and bulletin provider

`other`, pinned to the archive page with a `Bulletin-*.pdf` filter so the calendars and forms on the same page are never picked. The Bon Venture footer on pages 5-6 is the ad seller, not a feed; the Bonventure bulletin-page feed in the playbook is not used here.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-anthony-of-padua-wilmington` (2026-10-27): the pinned recipe picked Bulletin-November-01-2026.pdf (8.8 MB); transport ok, document type PDF, freshness `future` (the 1 November issue goes up before its Sunday, as the playbook notes; the 25 October issue read above is the current one in force). The tool leaves identity 'unverified'; the 25 October masthead read above settles it. The recipe is already in `provider_id`.

## Not yet confirmed

Nothing outstanding.
