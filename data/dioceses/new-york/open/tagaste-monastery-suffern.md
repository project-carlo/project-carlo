---
name: Tagaste Monastery
revisit: Grep the Sacred Heart, Suffern eCatholic issues (files.ecatholic.com/6402/bulletins/) and the
  Tagaste newsletters posted on sacredheartparish.org for a Mass at Tagaste Monastery announced to the
  public, especially around the Feast of St. Augustine (28 August 2027). A dated public Mass makes it
  a church under sacred-heart-suffern; a statement that the chapel is for the community makes it an exclusion
  (no-public-mass).
revisit_after: 2027-08-30
roster: ['gcatholic:39186']
evidence:
- url: https://gcatholic.org/churches/usa-02/39186
  seen: 2026-10-07
  quote: 'GCatholic Church ID: 39186'
  note: Roster identity only, not present public Mass evidence.
- url: https://gcatholic.org/churches/usa-02/39186
  seen: 2026-10-11
  quote: 'Served by: Augustinian Recollects'
  note: Roster reread over HTTP 200. Address 220 Lafayette Avenue and telephone 845-357-0067; linked website
    is http://www.tagastemonastery.org. Nearby Sacred Heart is separately indexed, not an automatic monastery
    publisher match.
- url: http://www.tagastemonastery.org
  seen: 2026-10-11
  note: The actual GCatholic-linked domain failed DNS under verified HTTP and T3 browser navigation (ERR_NAME_NOT_RESOLVED).
    HTTPS failed DNS too. This access failure says nothing about closure or whether monastery Mass is
    public.
- url: https://files.ecatholic.com/6402/bulletins/20261108.pdf
  seen: 2026-11-08
  note: 'Current Sacred Heart, Suffern issue (3 pages, text): no mention of Tagaste, the monastery or
    220 Lafayette Avenue (grep).'
- url: https://sacredheartparish.org/documents/2021/12/Tagaste%20Newsletter%20November%202021%20Revised.pdf
  seen: 2026-11-08
  note: 'Lead from a web search: Sacred Heart parish posts the Augustinian Recollect province''s ''Tagaste
    Newsletter'' (2021 issues found); not read, and a provincial newsletter is not a Mass schedule.'
line1: 220 Lafayette Ave.
city: Suffern
state: NY
postal_code: '10901'
research:
- method: issues.py ecatholic ecatholic:6402 --grep Tagaste/Monastery/220 Lafayette (8 November 2026);
    web search for Tagaste Monastery Mass
  url: https://files.ecatholic.com/6402/bulletins/20261108.pdf
  checked: '2026-11-08'
  outcome: not-found
  next_action: Grep the Sacred Heart issues around 28 August 2027 for a Tagaste Mass
  retry_when: The Sacred Heart, Suffern issues for late August 2027 are posted
  revisit_after: 2027-08-30
---

## What is known

Tagaste Monastery, 220 Lafayette Avenue, Suffern (GCatholic 39186), is a house of the Augustinian Recollects, described by Wikipedia's list of religious orders in the archdiocese as a house of study. Its own domain, tagastemonastery.org, fails DNS (October 11). The Recollects also serve [Sacred Heart, Suffern](../parishes/sacred-heart-suffern.md), whose eCatholic bulletin is read weekly; its 8 November 2026 issue does not mention Tagaste or the monastery. Sacred Heart's site hosts the province's Tagaste Newsletter (2021 issues), and a 2017 Recollect news item reported a St. Augustine feast-day celebration at the monastery.

## Why it is not decided

No source dates a public Mass at the monastery now, and none says it is closed or private. A community house of study may only have community Masses, with occasional public feast-day liturgies. The next check is Sacred Heart's bulletins around the Feast of St. Augustine (28 August).
