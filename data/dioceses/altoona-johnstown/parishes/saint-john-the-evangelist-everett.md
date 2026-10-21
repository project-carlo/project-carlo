---
name: Saint John the Evangelist Parish, Everett
website: http://stjohneverettpa.org/
bulletin_provider: other
provider_id: page-pdfs http://stjohneverettpa.org/Bulletins/
publication: ['url:http://stjohneverettpa.org/Bulletins/']
group: ''
evidence:
- url: http://stjohneverettpa.org/gallery/Bulletin%20October%2018%202026.pdf
  seen: 2026-10-21
  quote: Fr. Derek Fairman, Pastor
  note: 'The bulletin for 18 October 2026 (2 pages), page 1 masthead: "ST. JOHN THE EVANGELIST CATHOLIC
    CHURCH ... 161 East First Avenue, Everett, PA 15537 ... Website: stjohneverettpa.org"; Mass times
    M, W, Th, F 8:30 a.m., Saturday 5:30 p.m., Sunday 9:00 a.m. Searched both pages for "McConnellsburg",
    "Fulton" and "Stephen": no hit.'
- url: http://stjohneverettpa.org/Bulletins/
  seen: 2026-10-21
  note: 'The parish site''s Bulletins page lists four dated PDFs under /gallery/: "Bulletin September
    27 2026.pdf", "Bulletin October 4 2026.pdf", "Bulletin October 11 2026.pdf", "Bulletin October 18
    2026.pdf". The page declares <base href="http://stjohneverettpa.org/">, so its relative links resolve
    under the site root, not under /Bulletins/.'
- url: https://www.fultoncatholic.com/uploads/1/2/2/0/122079007/2026-10-11.pdf
  seen: 2026-10-21
  quote: 'Phone Number: 814-652-5854 (Everett Parish Office)'
  note: The McConnellsburg bulletin names Fr. Fairman and uses Everett's office number, but is a separate
    publication on a separate site (see parishes/saint-stephen-mcconnellsburg).
- url: https://discovermass.com/church/st-john-the-evangelist-everett-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for St. John the Evangelist.
  note: Discover Mass page exists but carries no bulletin; not a live channel.
promoted: 2026-10-21
---

## Publisher

St. John the Evangelist Parish, Everett publishes its own weekly bulletin as PDFs on its parish site
(stjohneverettpa.org, a 2MHost site). The newest issue read on 2026-10-21 is
`http://stjohneverettpa.org/gallery/Bulletin%20October%2018%202026.pdf`, dated 18 October 2026, with the
masthead "ST. JOHN THE EVANGELIST CATHOLIC CHURCH, Fr. Derek Fairman, Pastor, 161 East First Avenue, Everett"
and a Mass schedule for Everett alone.

**Everett and McConnellsburg: two bulletins.** The lead was that the two share a pastor (Fr. Derek Fairman).
They do: the McConnellsburg bulletin of 11 October 2026 names him and gives Everett's office number. But
each parish keeps its own site and its own weekly bulletin: Everett's carries only Everett's Masses and
intentions (no hit for "McConnellsburg", "Fulton" or "Stephen" on either page), and McConnellsburg's
(fultoncatholic.com) is a different PDF series with its own masthead and Mass times (Saturday 4:00 p.m.,
Sunday noon). Two live channels, so two rows.

## Worship sites

St. John the Evangelist, 161 East First Avenue, Everett (churches/st-john-the-evangelist-everett). The
bulletin's schedule lists no other place; the directory and GCatholic list this one church for the parish.

## Website and bulletin provider

`other`. The directory homepage http://www.stjohneverettpa.org/ is live. Its Bulletins page lists the
PDFs. The recipe in `provider_id` is the one that describes it: `page-pdfs http://stjohneverettpa.org/Bulletins/`.

The Bulletins page declares `<base href="http://stjohneverettpa.org/">` and links its PDFs as
`gallery/Bulletin October 18 2026.pdf`, which resolve to `/gallery/...`, not `/Bulletins/gallery/...`.
The first `fetch:check` on 2026-10-21 picked the right issue but resolved the link against the page
URL and got HTTP 404; the fetch code now honours `<base href>`. Rerun the same day:
`ok`, "page-pdfs on http://stjohneverettpa.org/Bulletins/: current",
`http://stjohneverettpa.org/gallery/Bulletin October 18 2026.pdf` (360,776 bytes), dated 2026-10-18.

## Not yet confirmed

Nothing open.
