---
name: St. Joseph the Worker Parish
website: https://www.stjoesfrackville.com/
bulletin_provider: other
provider_id: page-pdfs https://www.stjoesfrackville.com/services-9
publication:
- url:https://www.stjoesfrackville.com/services-9
group: St. Joseph the Worker Parish
evidence:
- url: https://www.stjoesfrackville.com/_files/ugd/23b1db_dff889f82b4142f098cf8eb5635b0c90.pdf
  seen: 2026-10-18
  note: 'Page 1 of the 18 October 2026 issue (six image pages; read by rendering them): "St. Joseph the
    Worker Parish / Twenty-Ninth Sunday in Ordinary Time / October 18, 2026 / Father Christopher M. Zelonis,
    Pastor"; "Parish Office 99 North Line Street, Frackville"; "St. Joseph Complex Locations 49 North
    Line Street & 33 South Broad Mountain Avenue".'
- url: https://www.stjoesfrackville.com/_files/ugd/23b1db_dff889f82b4142f098cf8eb5635b0c90.pdf
  seen: 2026-10-18
  note: 'Page 2 "Mass Intentions": Saturday 5:30 PM SJWP, Sunday 11:00 AM SJWP, Monday 5:30 PM SJWP, Thursday
    8:30 AM SJWP; St. Charles Borromeo-Ashland''s Masses are listed alongside in italics.'
- url: https://www.stjoesfrackville.com/services-9
  seen: 2026-10-18
  quote: Sunday, October 18, 2026 Twenty-Ninth Sunday in Ordinary Time view
  note: The Wix "2026 Bulletins" page; the first "view" link is the 18 October file.
- url: https://www.stjoesfrackville.com/copy-of-mass-times
  seen: 2026-10-18
  quote: Saturday Vigil 5:30 pm
  note: 'The parish site''s Mass Times page: Saturday Vigil 5:30 pm, Sunday 11:00 am, Monday 5:30 pm,
    Thursday 8:30 am.'
---

## Publisher

St. Joseph the Worker Parish, Frackville (formed from Annunciation B.V.M., St. Ann and St.
Joseph, Frackville; the diocese's map: "St. Joseph is the repository for records of
Annunciation B.V.M. and St. Ann, Frackville") publishes its own weekly bulletin on its Wix
site. The 18 October 2026 issue is six image pages: page 1 is the masthead ("St. Joseph the
Worker Parish ... October 18, 2026", Fr. Christopher M. Zelonis, pastor), page 2 the Mass
intentions (Saturday 5:30 pm, Sunday 11 am, Monday 5:30 pm, Thursday 8:30 am, all "SJWP").

Same pastor and webmaster as St. Charles Borromeo, Ashland, which prints its own bulletin
(`st-charles-borromeo-ashland`); each lists the other's Masses for convenience. Two rows.

## Worship sites

- `st-joseph-the-worker-frackville`: the one church whose Masses the bulletin lists, at 49
  North Line Street (the diocese's map address for the parish, and the first of the bulletin's
  "St. Joseph Complex Locations"). GCatholic puts its St. Ann church at the same address, so
  the parish church is the former St. Ann building (inferred from the addresses; no source
  says so in words).

Ruled out: St. Joseph, 237 W. Frack St. (`excluded/`, named among closed churches in 2019);
Annunciation B.V.M., 7 S. Broad Mountain Ave. (`open/`: no Mass in the bulletin, but no
source says the building closed; the parish home page still says "Churches of St. Ann,
Annunciation B.V.M, St. Joseph"). St. Michael (Ukrainian Catholic, 45 S. 2nd St.) is another
jurisdiction.

## Website and bulletin provider

`other`: stjoesfrackville.com (the diocese map's website) lists the PDFs on "2026 Bulletins"
(/services-9), one Wix card per issue (date, Sunday, "view" link to a hash-named PDF). The
first `fetch_check_rows.py` run on 2026-10-18 picked
`23b1db_ede965826aac4635ad5cecf39b338d0f.pdf` ("first-listed"), the header's "Coat of Arms"
PDF (the same Wix pattern as St. Charles Borromeo). With the resolver now dating a link by
its card, and reading the page again when its cards render late, three runs on 2026-10-19
each picked `23b1db_dff889f82b4142f098cf8eb5635b0c90.pdf`, the 18 October issue ("current");
that recipe is pinned. The bulletin is image-only, so the pipeline must also read it as images.

## Not yet confirmed

Which former church the 49 N. Line St. building was (St. Ann per GCatholic's address);
the Annunciation building's status (`open/annunciation-bvm-frackville`).
