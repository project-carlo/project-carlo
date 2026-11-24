# Luna's failure modes (Phase 0, both samples)

This combines `verdicts.json` (sample 1, 24 items) with `verdicts-2.json` (sample 2, 40
items), checked against the PDFs. It also covers a scripted sweep of all 258 cached luna
replies (3,739 entries, 11,716 evidence quotes), with about 15 parishes then read by hand.

| | seed right | luna right | judgment | structural |
|---|---:|---:|---:|---:|
| sample 1 (24) | 14 | 1 | 5 | 4 |
| sample 2 (40) | 21 | 2 | 8 | 9 |
| **all (64)** | **35** | **3** | **13** | **13** |

Sample 1 had no failure tags. They were assigned here as follows: #3, #10, #11, #22
nonweekly-as-weekly; #4 regular-slot-recorded-as-dated; #5, #6, #8 missed-line (in the
schedule box); #9 dated-duplicate-of-weekly; #12 signup-or-nonservice-as-service; #18
blended-adjacent-entries; #19 overnight-span-collapsed; #23, #24
ignored-same-bulletin-exception.

## Failure modes, by count (35 seed_right items)

Each suggested instruction is written as a general rule for POLICY or TASK.

### 1. nonweekly-as-weekly: 7 (S1 #3, #10, #11, #22; S2 #4, #20, #23)

Luna turns alternate-week, monthly-rotation and holiday-bounded patterns into every-week
slots. It treats two sightings in different weeks as rule 4's "two or more weeks" even when
the weeks in between lack the slot.

- most-holy-name-of-jesus, B1 p2: "Tuesdays, October 13 & 27, 4:30 to 5:30pm in St.
  Mary's" (and "Wednesdays, October 7 & 21" at St. Patrick's) became weekly Tuesday and
  Wednesday slots.
- northern-points-cluster: "Thursday, October 1st ... followed by Adoration" (B4) and
  "October 15th ... followed by Adoration" (B2). The Oct 8 and Oct 22 issues print the
  same Thursday Mass without Adoration, yet luna recorded weekly Adoration.
- sts-isidore-maria-torribia, p1: a confession rotation ("November 1st / St. Catherine",
  "November 8th / St. Stanislaus", "November 14th / St. Joseph") became weekly Sunday
  slots.

Suggested instruction: *"Rule 4 needs the slot in consecutive weeks. Before calling a slot
weekly, check every week the bulletins cover. If a week they cover lacks it (the same
listing, calendar or intentions print that weekday without it), it is not weekly: record
each printed date on or after today as dated. Dates printed two or four weeks apart
('October 13 & 27'), a rotation table that names a different church each week, and seasons
bounded by a holiday ('Memorial Day to Columbus Day', 'first full weekend') are never
weekly or months-based. Record their printed dates as dated entries."*

### 2. missed-line: 8 (outside the schedule box: S2 #2, #3, #6, #14, #30; inside it: S1 #5, #6, #8)

Luna reads the schedule box well but misses services printed in event lists, sidebars,
notice boxes and prose. It also misses single lines in a box (an exception, a cancellation,
a second relocation). In 134 of 258 replies luna returned no dated entries or
cancellations at all, including 15 parishes whose seed has an included dated entry on or
after today.

- st-catherine-of-siena-ithaca, B1 p8 (prose under a planning-meeting heading): "we will
  be having our Mass of Remembrance on November 2 at 7 p.m."
- catholic-family-holy-rosary, B1 p3 "Upcoming Events": "November 6th First Friday
  Eucharistic Adoration ICC after 8:00 am Mass until noon".
- wheat-family-east-aurora, B1 p2 "Other Faith-Forming Opportunities": "1st Friday Family
  Devotions at St. Vincent's ... 7 Mass".
- parish-of-the-holy-family, B1 p6 calendar: "9:30AM Second Saturday Adoration-CH".
- st-joseph-the-worker-west-winfield (S1): "During the last 2 Mondays of October, Mon. 1
  p.m. - 8 p.m."

Suggested instruction: *"Mass, Confession and Adoration times are often printed outside the
schedule box: in event lists, calendars, sidebars, flyers, the pastor's column and
announcements, including ones whose heading is about something else (a meeting, a
devotion night, a fundraiser). Before answering, go through every page and list every
Mass, Confession, Adoration, Holy Hour or Benediction mentioned with a time, then decide
how to record each one. A service named inside a larger event ('6:15 Confession, 6:30
Rosary, 7 Mass') is a service in its own right."*

### 3. ignored-same-bulletin-exception: 4 (S1 #23, #24; S2 #22, #26)

The bulletin itself qualifies or overrides a regular slot, and luna keeps the plain slot.

- st-luke-schenectady, B1 p2: "Eucharistic Adoration will follow the 11am Mass on Fridays
  and continue until 1pm ... on days other than First Fridays". Luna made it every Friday
  and quoted only the first half.
- ss-columba-and-brigid-buffalo, p1: "Last Sunday of Month: 10 a.m. (bilingual)". The
  intentions for both last Sundays luna saw ("Sunday, September 27 ... Bilingual 10:00
  a.m.") list no 9:00 or 11:00, but luna kept 9:00 every Sunday.
- st-leo-the-great (S1): an intentions template's First Friday 8:30 Mass, against the
  same issue's "Friday - October 2nd 8:30 AM Communion Service".

Suggested instruction: *"Read each regular slot together with its qualifiers and with the
dated listings for the same weekday. A clause in the same sentence or notice ('except',
'other than', 'not on', 'on days other than First Fridays') sets `weeks_of_month`. If a
monthly service is printed for the same weekday ('Last Sunday of Month: 10 a.m.') and the
dated listings for that week show only it, the regular slots skip that week. Quote the
qualifier in the evidence."*

### 4. Time-boundary errors: 6

Luna starts or ends Adoration and Confession at the wrong point.

- **relative-to-mass-not-derived: 2 (S2 #11, #27).** blessed-trinity-st-patrick, p3:
  "available 1/2 hour before weekday Masses" was recorded with no end, although POLICY
  says it ends at the Mass. At sacred-heart-stamford, luna applied "after Mass" on Sunday
  but not "Before or After Mass on Monday".
- **ended-at-following-mass: 1 (S2 #34), plus 6 entries in the sweep.**
  three-catholic-sisters, p3: "Adoration 10:00 am Followed by 11:00 am Mass" ended at
  11:00. hudson-valley-vicariate-west-catskill: "Tuesday, 7:30 AM (followed by Mass)" was
  recorded as 7:30-8:30, and so were five other days.
- **benediction-time-as-start: 1 (S2 #29), plus 2 parishes in the sweep.**
  st-peters-ontario-county, p1: "Adoration ... Following the Noon Mass / Thursday, St.
  Francis, Benediction at 6:00pm" became Adoration at 6:00 PM with no end, at all three
  churches. st-john-greece has the same pattern: "10:00 AM Benediction".
- **overnight-span-collapsed: 1 (S1 #19), plus 1 in the sweep.** transfiguration-syracuse:
  "First Friday ... 7:00am until First Saturday ... 9:00am" became 7:00-9:00.
  light-of-christ-kenmore: "each Wednesday 9am through Thursday 10pm" became Wednesday
  9:00 AM-10:00 PM, with no Thursday entry.
- **missed-end-time-elsewhere: 1 (S2 #35).** st-francis-xavier-marcellus: the box says
  "Penance Tuesday 5:30 pm", and B2 p2's pastor's column says "Confession from 5:30 to 6
  PM". Luna did not merge the two.

Suggested instructions:
- *"'N minutes before Mass' always gets an end: the Mass's start. A clock start followed
  by a Mass ('Adoration 10:00 am followed by 11:00 am Mass', '7:30 AM (followed by Mass)')
  gets no end."*
- *"Benediction closes an Adoration period. When the bulletin gives the period's start
  (a clock time or 'following the noon Mass') and a Benediction time, record one Adoration
  from that start to the Benediction time. Use the Benediction time as a start only when
  Benediction is the whole service."*
- *"A period that runs past midnight ('Wednesday 9am through Thursday 10pm', 'Friday 7am
  until Saturday 9am') is split at midnight into one entry per day: Wednesday 9:00 AM to
  11:59 PM, then Thursday 12:00 AM to 10:00 PM."*
- *"When another passage in any of the bulletins gives the same slot's end time or
  duration, use it and cite both passages."*

### 5. dated-duplicate-of-weekly: 2 (S1 #9; S2 #16), plus 3 in the sweep

cathedral-st-mary-albany, B1 p1: "ALL SOULS SPECIAL MASSES ... 12:05 pm at St. Mary's" is
the regular Monday 12:05, yet luna added it as a dated entry. The sweep found the same in
central-niagara-catholic (Nov 2, 7:30), olg-ic-sj-glenville and catholic-family-cheektowaga.

Suggested instruction (rules 6 and 7 already say this, so add a check): *"Before
answering, compare every dated entry with your weekly entries. If a weekly entry has the
same church, type, weekday and start time, delete the dated entry, whatever the occasion."*

### 6. signup-or-nonservice-as-service: 2 (S1 #12; S2 #24), plus 1 in the sweep

- our-lady-of-hope-whitehall, B1 p5: "Adorers Needed: Wednesdays from 11 a.m. to Noon & 6
  p.m. to 7 p.m."
- holy-spirit-st-josephs (S1): "Hours which need to be filled ... Partner required:
  Friday 2-3 pm".
- spirit-of-hope-oneida (sweep): "Open Hours: Tuesdays 11pm-12am, Thursdays 3am-4am,
  Fridays 10pm-11pm". These are the unfilled hours of a perpetual chapel, which luna
  recorded as its only Adoration slots.

Suggested instruction: *"Hours listed for adorers to sign up ('Adorers needed', 'Open
hours', 'Hours which need to be filled', 'Partner required', 'substitutes needed') are
not Adoration times. Never record them. Take Adoration times only from the schedule of
exposition."*

### 7. Single-item modes: 6

- **blended-adjacent-entries (S1 #18).** niagara-falls-rc-family: two churches'
  confession times ("3pm-3:45pm" and "4:30pm-5:15pm") became "3:45pm-5:15pm".
  *"Take a start and its end from the same line and the same church block. Never join
  times from adjacent blocks."*
- **regular-slot-recorded-as-dated (S1 #4).** assumption-syracuse: a "NO 8:30 AM MASS"
  notice for Monday-Wednesday shows that 8:30 is the regular daily Mass, but luna kept
  Tuesday 8:30 as one date. *"A notice cancelling a time on certain days shows that the
  time is regular on those days."*
- **implied-cancellation-not-recorded (S2 #10).** catholic-family-cheektowaga, B1 p4:
  "November 26 Thanksgiving. The only Mass for our Family of Parishes is at Resurrection
  at 8:30am." *"When the bulletin says a day's only Mass, or only Masses, are X ('the only
  Mass', 'one Mass only', 'combined Mass'), record a cancellation for that date for each
  of your weekly slots of that type on that weekday that X doesn't include."*
- **shared-heading-applied-to-one-line (S2 #7).** st-john-the-baptist-walton, p1:
  "Tuesday, Wednesday & First Friday / 8:00 am at St. Peter's / 9:30 am at St. John's".
  Luna gave First Friday only to St. Peter's, and quoted "Tuesday and Wednesday 9:30 am at
  St. John's", which is not printed. *"A day heading above several church lines applies
  to every line under it."*
- **invalid-church-slug (S2 #17).** st-marys-st-matthew: luna used `st-mary-honeoye` for
  the listed `st-marys-honeoye`. *Make `church_slug` an enum of the parish's slugs in the
  strict schema.* No prompt text needed.
- **silently-repaired-misprint (S2 #31).** st-kateri-tekakwitha, p1 (image): the bulletin
  prints "3:00 pm - 3:4pm", and luna quoted and recorded "3:45pm". *"Quote exactly what
  is printed, including misprints. If a time is cut off or garbled ('3:4pm'), leave that
  time null (an end) or leave the entry out (a start). Never complete it."*

## Systematic issues from the sweep (not counted above)

- **Evidence quotes.** On pages with a text layer, 7,763 quotes match verbatim and 710 have
  all their words on the cited page (stitched from table cells). About 700 do not match,
  but most of these are pypdf font-decoding gaps, so there is no reliable count of
  altered quotes. Two alterations are confirmed by hand: Walton and Kateri, above. Quotes
  are also often cut to the part that supports the entry, dropping the qualifier (St.
  Luke's "on days other than First Fridays"). Suggested instruction: *"Quote the whole
  clause, including any qualifier or exception."*
- **Page numbers.** These are mostly right. One clear pattern: bread-of-life-catholic-community
  cites B4 p11 for its Mass schedule, but B4 has 10 pages, so the page was copied from
  B1-B3. Suggested instruction: *"Give each bulletin's own page. Pages move between
  issues."*
- **24-hour Adoration has three encodings.** Luna writes 12:00 AM-12:00 AM 28 times,
  12:00 AM-11:59 PM 21 times and 12:00 AM with no end 14 times. POLICY should name one
  encoding, for example *"all day: 12:00 AM to 11:59 PM"*, and the matcher should
  normalise all three.
- **Notes carrying schedule.** Notes are mostly fine: no "Vigil Mass", and 1 of 666 notes
  repeats `weeks_of_month`. A few hide schedule facts that should be separate entries:
  bread-of-life's "Perpetual Adoration Chapel; closed Mondays 1:00-2:00 PM for cleaning"
  on a Monday 7-7 entry (it should be split into two), and light-of-christ's note about a
  Thursday Holy Hour on its Wednesday entry. Suggested instruction: *"A note never holds a
  time, a day or an exception. Express it with entries."*
- **Seasons.** Of 26 seasons, most are faithful ("October through June", "Jan-Jun"). Three
  kinds were invented or approximated:
  - a start invented from an end alone: st-mary-crescent, "through mid-January" became
    September-January;
  - a season built from the months seen: our-lady-of-hope-whitehall, "As always ... 2nd
    and 4th Fridays in October/November" became October-November;
  - holiday bounds rounded to months: "Memorial Day - Labor Day" became May-September, and
    "July 4-Labor Day" became July 4-September.

  Suggested instruction: *"Set `season` only from a printed start and end. If either
  bound is missing or is a holiday rather than a date, leave `season` null and record the
  printed dates as dated entries."*
- **Mass end times** never occur, and no entry lacks evidence. Of 666 notes, 11 are over
  60 characters.

## Comparison artefacts (beyond the six in analysis.md)

1. **Orphan cancellations** (S2 #12, #15; 3 luna cancellations in the sweep). A
   cancellation that matches no included weekly slot, on either side, changes nothing.
   Example: luna's "9:00am- No Mass" for days with no weekly Mass, or a seed cancelling a
   slot it excludes. *Matcher:* drop cancellations whose church, type, weekday and time
   match no included weekly slot on that side before comparing.
2. **No pairing when a day has several slots** (S2 #18, #22, #26). `compare` pairs only
   when exactly one unmatched luna entry and one unmatched seed slot share church, type
   and day. With two or three Sunday Masses, or a Friday split into weeks 2-5 and first,
   a weeks or end-time difference becomes "missing" plus "extra". *Matcher:* pair by the
   same start time first, then the nearest start, and report differs with the fields.
3. **24-hour encoding includes "no end", and blocks exclusions too** (S2 #21, #25).
   analysis.md lists 00:00-00:00 against 00:00-23:59. Luna also writes 00:00 with no end,
   and the mismatch keeps a luna entry from matching a settled exclusion (St. Daniel),
   which then shows as "missing". *Matcher:* normalise any 00:00 start with an end of
   00:00, 23:59 or none to all-day before keying both included and excluded slots.
4. **Unknown church slug** (S2 #17). An entry whose `church_slug` is not in the parish's
   list can never match. *Matcher:* report it as a schema error, or map it to the nearest
   listed slug and flag it. Better, enforce an enum in the reply schema.
5. **Slots resting on bulletins luna wasn't given** (S2 #1, #9). The seed's only bulletin
   sources are older issues outside B1..Bn: R12 for a First Friday the shown weeks lack,
   R29 for a box the newer issues dropped. *Matcher:* when none of a slot's agent or
   history sources is among the bulletins luna saw, mark the difference structural (as
   for R6 website slots). Alternatively, give luna the issue the seed cites for a
   weeks-of-month slot.
6. **Slots settled by a reviewer rule or answer outside the bulletins** (S2 #8, and the
   St. Daniel and Utica venue answers). The decision comes from the 2026-10-14 timing
   rule or an R32 venue answer, which luna can't know. *Matcher:* when the slot has an
   `answer` and its rationale cites a reviewer rule or R32, class the difference as
   "settled by reviewer" and show it below unexplained differences, not as a new
   question.

## luna_right: real seed errors for the owner

- **chautauqua-family-catholic s19** (Westfield Saturday 4:00 PM, "every Saturday except
  the first"). The exclusion is wrong. The vigil was held on the first Saturday Oct 3 (B4
  p2: "SATURDAY, OCTOBER 3 - 27TH SUNDAY IN ORDINARY TIME ... [W] 4:00PM"). The Nov 1
  issue (0907add3 p2) lists "[W] 4:00PM" on Saturday Nov 7, the same day "11/7 FIRST
  SATURDAY - NO MASS" refers to. The discontinued "First Saturday Masses" are a separate
  devotional Mass. The slot should be every Saturday, and history agreed.
- **transfiguration-troy s4 and s5** (Sunday 10:00 Confession at Schaghticoke, Saturday
  5:00 PM at Speigletown, both excluded). The exclusion says "no page ... prints
  Confession", but every issue's p5 has an image-only "Sacramental Celebrations" box:
  "Sacrament of Reconciliaion / Available after the 4PM and 9AM Masses" (rendered
  b5eb1494 p5). The text layer of that page holds only the ads. Under POLICY these are 1
  hour after each weekend Mass, so both slots should be included.
- **st-mary-our-mother s12** (sample 1). The Oct 29 Sheen relic Mass has its time, "7:00pm",
  in the Oct 11 issue's p3 graphic.

Two of the three are text-layer blind spots: the drafter grepped, and the content was only
in an image. A drafter rule worth adding: *before excluding for "not printed", render the
pages whose text layer is partial (ads or headers only) and check them.*
