---
name: Saint John Bosco Parish
website: https://sites.google.com/view/stjohnboscochurchconyngham/home
bulletin_provider: other
provider_id: page-pdfs https://sites.google.com/view/stjohnboscochurchconyngham/2026-bulletins
publication: ['url:https://sites.google.com/view/stjohnboscochurchconyngham/2026-bulletins']
group: Saint John Bosco Parish
evidence:
- url: https://drive.google.com/uc?export=download&id=1r5dPEcvgX8y3IzuuSMkP8dLDwF1nVCBZ
  seen: 2026-10-16
  quote: SAINT JOHN BOSCO PARISH C O N Y N G H A M , P E N N S Y L V A N I A Sacred Heart of Jesus Church,
    Weston + Saint John Bosco Church, Conyngham
  note: Masthead, page 1 of the 11 October 2026 issue ("10/11-28th Sunday in Ordinary Time" on the parish's
    2026 Bulletins page).
- url: https://drive.google.com/uc?export=download&id=1r5dPEcvgX8y3IzuuSMkP8dLDwF1nVCBZ
  seen: 2026-10-16
  quote: 'WEEKEND Saint John Bosco Church: Saturday, Vigil Mass: 4:00 pm Sunday: 7:30, 9:00 & 11:30 am'
- url: https://drive.google.com/uc?export=download&id=1r5dPEcvgX8y3IzuuSMkP8dLDwF1nVCBZ
  seen: 2026-10-16
  quote: 'Sacred Heart of Jesus Church: Sunday: 9:00 am'
- url: https://sites.google.com/view/stjohnboscochurchconyngham/2026-bulletins
  seen: 2026-10-16
  note: Lists the 2026 issues as Google Drive file links titled by date and Sunday ("10/4-27th Sunday
    in Ordinary Time", "10/11-28th Sunday in Ordinary Time", ...); newest 11 October on 2026-10-16. Its
    Drive file ids differ from the Good Shepherd/Immaculate Conception bulletin's.
revisit: Check that the 2026-bulletins page (or its 2027 successor) still lists new issues and repin the
  recipe if the page moved.
revisit_after: 2027-01-15
promoted: 2026-10-17
---

## Publisher

Saint John Bosco Parish publishes its own weekly bulletin, posted as Google Drive PDFs on
its Google Site. The 11 October 2026 issue's masthead reads "SAINT JOHN BOSCO PARISH,
CONYNGHAM ... Sacred Heart of Jesus Church, Weston + Saint John Bosco Church, Conyngham",
with Rev. Richard J. Polmounter as pastor and a Mass schedule for both churches. Not
shared: the neighbouring Good Shepherd, Drums has a different bulletin (different Drive
files, its own content), and Holy Rosary, Hazleton (whose sacramental minister is SJB's
associate pastor) publishes through Discover Mass.

## Worship sites

Two, both with Sunday Mass in the 11 October 2026 schedule:
- Saint John Bosco Church, 573 State Route 93, Sugarloaf Township (Conyngham)
  (`st-john-bosco-conyngham`).
- Sacred Heart of Jesus Church, 554 Main Street, Weston (`sacred-heart-of-jesus-weston`),
  Sunday 9 am. The diocese's consolidated-parishes list says "Weston Sacred Heart of Jesus
  (closed 2021)", i.e. the parish was merged in 2021; the current bulletin shows the church
  still has Sunday Mass, and the bulletin wins.

The same list gives "Nuremberg St. Joseph Misson Church (closed 6/26/2010)" with records
here; it is in neither roster and has no record.

## Website and bulletin provider

The parish's Google Site (the diocese finder's link). Its "2026 Bulletins" page links one
Google Drive PDF per week, so provider `other` (its resolver reads Drive file links), with
recipe `page-pdfs https://sites.google.com/view/stjohnboscochurchconyngham/2026-bulletins`
pinned by inspection; `fetch:check` (run on 2026-10-17 against a temporary parishes.csv holding this row) picked the 4 October issue, not the newest (11 October): it read the label "10/4-27th Sunday" as 2027-10-04 ("first-listed, dated 2027-10-04"). The chooser needs to stop reading "27th" as a year, or the parish to drop the Sunday name from its labels. As
with Freeland's site, the yearly page will likely move in January 2027 (the 2025 page now
sits at /2026-bulletins/2025-bulletins). The PDFs have text.

## Not yet confirmed

Whether a 2027 bulletins page replaces this one (see `revisit`).
