# Seeding decision rules

These are the rules for deciding a seed's slots. `POLICY` in
`src/pdf_extract/classifiers/schedule_policy.py` says what one bulletin shows: which events
count, weekly or dated, times, churches. This file covers what is specific to seeding:
reading across bulletins, history and the website; `as_of`; evidence; and what is settled
and what is asked. The JSON fields are in [file-format.md](file-format.md).

**Apply the rules first; ask about what remains unclear.** Check POLICY and the active
rules below (R…), including their exceptions, before making a question. A named monthly
service need not appear in an issue covering a different week (R12), and a future event
announced earlier need not be repeated in every issue (R19). Confession during Adoration
has the explicit timing exception in POLICY. Do not ask again when a rule settles it.
Everything still unclear is `needs_human`: a short question, the options, exactly one
`"leaning": true`, and why you lean that way. Candidates (C…) are not in force and cannot
override a clear active rule or POLICY. When no active rule settles a candidate's case,
ask and lean as the candidate says. The reviewers (`seed-review`, then the owner in the
factory's PR) work from the seed file and never see your report or handoff. A doubt kept only in the report or a settled slot's rationale is lost.

**Citing.** A settled slot's `rationale` starts with the rule it rests on ("R1: printed in
the schedule box of all three bulletins") or names the POLICY section ("POLICY, Times").
A question's rationale may name the candidate it leans on ("leaning per C5").

**How to change these rules** (maintainer): add a rule under the next unused ID in the
section it belongs to. Never renumber or reuse an ID, since rationales cite them. To
promote a candidate, move it into its section as a new R rule ("was C4"). `pnpm seed
questions` lists answered questions, their leanings and what they cite.

## Evidence and sources

**R1. Clear in the newest bulletin.**
- When: the newest bulletin prints the slot clearly, POLICY is clear about it, and nothing
  you read contradicts it.
- Do: `settled` include, `page` where the newest bulletin prints it, with an `agent` source
  at that page. Every inclusion you settle needs that source, except an assessed website
  schedule under R6, older evidence under R12/R19, or a repeated schedule retained under
  R36. Those exceptions have `page: null`; never invent a newest-bulletin page.

**R2. Read the newest bulletin first, and mark what you read.**
- When: you start a parish, and whenever you read any bulletin.
- Do: read the newest listed bulletin in full and draft every slot POLICY asks for. Run
  `seed mark-read` on every bulletin you read, including one with no schedule and one you
  reject. Don't invent a slot just to show that you read a bulletin. If you read a newer
  bulletin, check the whole draft against it again.

**R3. Read further back when a slot needs it.**
- When: a slot is printed in only one bulletin; a time or day differs from history or
  between bulletins; there is a seasonal hint ("summer schedule", "beginning in Advent");
  or the newest bulletin looks like an old issue or another parish's.
- Do: read the older bulletins on that point and cite each in an `agent` source.

**R4. Model calls are a last resort.**
- When: your reading and history still leave doubt.
- Do: ask a targeted question (`seed ask`). Use a full extraction (`seed extract`) only for
  a bulletin you can't make sense of. Cite the call by its id. A clear parish needs no
  call.

**R5. The website: when to look.**
- When: production only, and a slot needs it: the bulletins disagree, or a slot's location
  or regularity is unclear. Never in a historical eval (`seed check` rejects website
  sources there).
- Do: quote the page in its own words as a `website` source, never a time you worked out.
  If the site can't be read, say so in the rationale and rely on the bulletins.

**R6. The website: what it can settle.**
- When: a website page bears on a slot.
- Do: use the parish's own website when it clearly describes a real service at a known
  church and fits what you read in the bulletin. It may establish a time absent from the
  bulletin, a chapel's location, or a monthly pattern. Quote the page and briefly explain
  why you trust it. Watch for old priests, obsolete restrictions, conflicting schedules
  and announcements clearly belonging to an earlier period. An old copyright year alone
  does not make a schedule stale. A real conflict with the bulletin is still asked; a
  missing mention alone is not a conflict. Ask if you still doubt the time, place or
  whether the service continues. Never use a live website in a historical evaluation.
- For an agent-settled website-backed inclusion, set `page: null` and record the website
  source's `schedule_check`: when checked, why it appears current, the newest read
  bulletin, and why it fits that bulletin. Use paired `--website-current` and
  `--website-context` with `web URL: quote` (file-format.md). Code checks this evidence's
  shape and provenance; judging whether the schedule is real remains your job.
- This promotes C9. Its old case remains evidence, not an automatic instruction to
  restore a previously excluded slot.

## History

**R7. History is a hint, not a vote.**
- When: extract mode's history (written with an older prompt) disagrees with your clear
  reading of the bulletins under POLICY.
- Do: settle by your reading, and say in the rationale what history got wrong. A
  difference is a reason to look closer (R3). POLICY, not history, decides which events
  count.

**R8. History reads one of your slots at another time.**
- When: a history event differs from one of your slots only in its time (`seed diff` lists
  it separately). For example, history says 11:30 or 12:15 for a slot POLICY times at 12:00.
- Do: check your time. The event needs no slot of its own; `finalize` cites it.

**R9. A history event you leave out gets its own slot.**
- When: a history event that no slot or option covers, which you leave out.
- Do: record it as its own excluded slot (or a question) so `seed diff` can match it.
  Naming it in another slot's rationale doesn't count. Deal with every `!` warning from
  `finalize`.

## Times

**R10. A time POLICY works out.**
- When: the bulletin times an event relative to a Mass or to Adoration and gives no clock
  time.
- Do: settle it at POLICY's time (POLICY, Times). After a weekday Mass, 30 minutes after it
  starts ("after the 11:30 AM Mass" is 12:00). After a weekend Mass, an hour after it
  starts. "An hour before each Mass" runs from an hour before to the Mass's start.
  Confession during Adoration takes the Adoration's hours, with the note
  `During Adoration`.

## Recurrence

**R11. Check before calling a weeks-of-the-month slot "seen once".**
- When: a weeks-of-the-month slot ("First Friday Holy Hour") appears in only one bulletin.
- Do: first check whether the other bulletins' weeks include a week it falls in.
  `seed brief` prints the weeks of the month the newest bulletin's week holds.

**R12. A weeks-of-the-month slot the newest bulletin can't show.**
- When: the slot is named by its week of the month ("First Friday Adoration", "First
  Saturday Mass") and the newest bulletin's week holds none of those weeks.
- Do: `settled` include with `page: null` and an `agent` source at a page of an older
  bulletin that prints it. If any read bulletin's week holds one of those weeks, cite the
  newest such bulletin, since that issue would print it.

**R13. A dated time that happens to fall on a named week.**
- When: a time is printed only as a dated item that falls on, say, a first Friday, and the
  bulletin doesn't say "First Friday".
- Do: it is dated (POLICY, Weekly or dated, rule 2). Once its date is before `as_of`, it is
  out of scope (R16).

**R14. Every other week, with the dates printed.**
- When: the schedule can't be written as a weekly slot ("every other Tuesday") and the
  bulletin prints the next dates.
- Do: record the dated occurrences on or after `as_of`.

**R15. A season given only by its start or its end is not a season.**
- When: the bulletin gives only one end of a season ("from October").
- Do: record no `season`.

**R35. Matching times in multiple bulletins can be weekly.**
- When: the same church, service, weekday and time appear in two or more bulletins
  covering different weeks, without being marked special or one-off.
- Do: record it as weekly and cite each reading. They need not all appear inside one
  PDF: this is seeding's extension of POLICY, Weekly or dated rule 4. A weekend-only
  schedule box does not disprove weekday Masses printed elsewhere. A single dated
  occurrence is not enough by itself; a clear regular schedule, a credible website
  schedule (R6), or a named monthly service follows its own rule. Do not restore a
  reviewer-excluded slot without new evidence addressing why it was excluded.

**R33. A pattern the file cannot express.**
- When: for example, every other Wednesday, alternating months, or Saturday after first
  Friday, and the format cannot express the actual pattern.
- Do: record only occurrences on or after `as_of` whose dates, times and places the
  source actually prints (R14). Otherwise settle the unrepresentable recurring entry as
  excluded and explain why. Every other month is not every month; Saturday after first
  Friday is not always first Saturday. A note cannot repair a false repeating schedule.
  Never invent recurrence fields or dates. If a needed fact itself is unclear, ask about
  that fact rather than offering an inaccurate weekly approximation.

## Changes over time

**R16. Seed scope.**
- When: deciding whether a dated entry or a cancellation belongs in the seed.
- Do: a seed holds weekly slots, plus dated entries and cancellations on or after
  `as_of`'s date. Record every such cancellation: update mode never reads a bulletin
  fetched on or before `as_of`, so a cancellation left out never reaches the site. Leave
  out dated entries before `as_of`.

**R17. A cancellation the bulletin doesn't state.**
- When: a holiday listing shows a 9:00 AM Mass and not the usual 6:45.
- Do: record the dated 9:00 AM Mass and leave the weekly slot alone. Record a cancellation
  only when the bulletin says a Mass is cancelled, moved, or replaced by a Communion
  Service.

**R18. A weekly slot the newest bulletin skips for a reason it gives.**
- When: for example, "No Mass Monday, Columbus Day", or a retreat day.
- Do: the weekly slot is confirmed. Settle it as included, with `page` set to the newest
  bulletin's page for that line, citing that line and the older bulletins that print the
  slot. Add the dated cancellation if its date is on or after `as_of`.

**R19. A dated event an older bulletin announced.**
- When: an older bulletin announced a dated entry or cancellation on or after `as_of` (an
  All Souls Mass on November 2), and nothing newer contradicts it.
- Do: `settled` with `page: null` and an `agent` source at the older bulletin's page.

**R20. A change announced for later.**
- When: for example, "From November 1, the Friday Mass moves to Tuesday".
- Do: keep the current schedule, leave the future one out, and say so in the rationale.
  Update mode will read the bulletins that show the change.

**R36. One omission does not remove an established weekly service.**
- When: readings of older bulletins establish the same weekly service, and the newest
  issue simply omits it once, with no service-specific cancellation or change.
- Do: retain it with `page: null`, cite the matching readings in older issues, including
  the immediately preceding read issue, and explain the omission in the rationale.
  Record `weekly_omission` with `--weekly-omission "why this is only an omission"` and
  `--page -`. The checker needs paged agent evidence from two older issue weeks and
  the preceding read issue exactly one week before newest, with valid publication
  dates. If that evidence is unavailable, ask rather than inventing citations.
  Repeated fetches of the same issue do not establish cross-week recurrence. A named
  monthly service still follows R11/R12; do not use this rule to skip its relevant week.
  Ask if a continuing pattern is not established or there is a real contradiction.
  Follow explicit cancellations and changes. A cancellation of Mass does not by itself
  cancel independently scheduled Adoration. Follow explicit dependency wording when a
  service is offered only with a particular Mass. Preserve qualifications such as
  "No Adoration during Masses".

**R40. Separate a standing schedule from one-date exceptions.**
- When: a dated calendar listing differs from a standing schedule, or a newer source
  clearly corrects an older church assignment or time.
- Do: a dated exception changes that occurrence, not every future week. Keep the
  standing schedule and record the dated exception within seed scope; a reviewed move
  is a cancellation of the old occurrence plus the new one. A newer explicit church
  assignment can correct an older one. Distinguish building-access hours from the
  hours a service is offered. Still ask when current, service-specific sources genuinely
  disagree and neither explains the difference. Do not infer a change merely from a
  missing listing (R17).

**R41. A specific dated invitation against a generic no-Mass template (was C3).**
- When: a specific dated notice invites people to Mass while the same bulletin's generic
  recurring line says no Mass for that day.
- Do: use the specific dated invitation when its date, time and church are clear. A
  direct conflict between two equally specific current notices remains a question.
- Evidence: mater-christi-albany s18 and st-michael-the-archangel-south-glens-falls s12.

## Location and churches

**R21. Look a church up before deciding it's missing.**
- When: a bulletin names a church or chapel.
- Do: `seed church` with its name and town ("Immaculate Conception Ithaca"), then with the
  town alone. It tells you whether the church is in `data/churches.csv` and which parish
  it belongs to.

**R22. Elsewhere, unclear, or another parish's.**
- When: a chapel or church elsewhere, one whose location is unclear (POLICY, Churches and
  chapels), or another parish's listed church.
- Do: `settled` exclude, saying why. The excluded entry may keep that church's own slug.
  Another parish's church is not a church-list issue: its events belong to that parish.

**R23. A church or chapel the church list lacks.**
- When: the bulletins give times for a church or chapel that `data/churches.csv` lacks or
  can't place (the parish's chapel at a mall, a mission church, an adoration chapel with
  no address), other than the case in R34.
- Do: don't ask about it. Settle its slots as excluded, say why, and list the church once
  in the file's `church_list_issues`.

When resolving a venue under R21–R23, a church-specific column heading is useful evidence.
A parish-wide heading or office phone number alone is weaker evidence; do not invent a
venue from it. Ask when it is unclear which listed church is intended (R32).

## What to leave out

**R24. What POLICY leaves out.**
- When: a devotion that is not Mass, Confession or Adoration (a Rosary, Anointing of the
  Sick); a wedding, funeral or memorial Mass for one person; an event with no definite
  time.
- Do: `settled` exclude, saying why.

**R25. Record what you leave out on purpose.**
- When: you leave out something a reviewer would expect to see (a Communion Service, a
  chapel at another address, a school Mass).
- Do: give it an excluded slot with its reason. Excluded slots left out for the same
  reason can share one rationale.

**R26. Nothing to record.**
- When: something you leave out has no time (a chapel open only by arrangement,
  confession by appointment).
- Do: `"entry": null`. Never make up a time to fill it.

**R37. A Holy Hour inside an Adoration period already recorded.**
- When: the Holy Hour is entirely inside Adoration at the same church on the same days.
- Do: keep the longer Adoration period. Mention the Holy Hour in a note when useful;
  do not add a second overlapping Adoration slot for the same availability.

**R38. A parish's Eucharistic chapel hours can be Adoration.**
- When: the parish identifies prayer before the Blessed Sacrament in an on-site chapel
  as Adoration and gives its hours.
- Do: include those hours at the listed church, naming the chapel in a note. Do not
  claim the Sacrament is exposed unless the source says so. A building being open for
  prayer alone does not establish an Adoration schedule. R6 covers website evidence;
  unclear or off-site locations still follow R22/R23/R32.

**R39. An empty intention is not proof of Mass or no Mass.**
- When: a time is printed with no Mass intention or a generic "Morning Liturgy" label.
- Do: read the headings, surrounding entries and regular schedule. If the line appears
  to be a reused template and contradicts the clear schedule, leave it out and explain
  the evidence. A blank intention alone proves neither a service nor a cancellation.
  "Morning Liturgy" alone does not prove a Communion Service replacing Mass (R17).

## Asking

**R27. One decision, one question.**
- When: one answer decides several slots (the seven days of a chapel, a confession window
  before every Mass).
- Do: give the slots one `group`, with the same question and the same options in the
  same order, leaning the same way. Do not group uncertain weekly recurrence with an
  explicit dated cancellation: rejecting the weekly pattern must not discard that
  cancellation. Preserve earlier reviewer answers when repairing a seed.

## Always ask

These cases are always `needs_human`. They are the standing examples of the default.

**R28. The bulletins contradict each other and don't settle it.**

**R29. The newest bulletin doesn't print it.**
- When: a slot backed only by older bulletins or the website (a weekly Mass missing with no
  reason given), and R6, R12, R18, R19 and R36 do not settle it.
- Do: ask, with `page: null`. If the reviewer answers to include it, it is included.

**R30. POLICY leaves it a judgment call.**

**R31. The print is unreadable.**

**R32. It's unclear which listed church it belongs to.**

## Blocked parishes

**R34. Blocked.**
- When: there is no usable bulletin (the newest is unusable and the rest of the evidence
  can't support explicit questions); the bulletins print no schedule;
  `data/churches.csv` lacks the parish's own church or churches, so no slot can be
  attached; or `finalize` reports a problem you can't resolve.
- Do: set `"status": "blocked"` with a `blocked_reason`, keep the evidence, and move on.
  `finalize` leaves a blocked status alone. Any other church the list lacks falls under
  R23.

## Candidates (not in force — ask, leaning as shown)

These come from reviewers' answers. Ask them as `needs_human`, lean as shown, and cite the
C rule. The owner promotes them to R rules.

**C1. A Mass only in the intentions.**
- When: a Mass appears only in intentions and there is an unresolved conflict with a
  clearly stated regular schedule or public venue. A missing header or website mention
  alone does not create this conflict; matching occurrences follow R35.
- Lean: leave it out.
- Evidence: all-saints-corning s5. Every week's intentions list a Saturday 4:00 PM Mass,
  but the schedule header and the website give only the 5 PM vigil. The agent leaned
  toward leaving it out, and the reviewer left it out (dropped).

**C2. A weekly slot suspended or moved for a stated period that covers `as_of`.**
- When: for example, "Friday Mass at St. Mary's until early January".
- Lean: leave the regular slot out. Record a temporary slot only if it is at one of the
  parish's own churches.
- Evidence: st-edward-the-confessor-clifton-park s8. Friday 9:00 AM Mass was at St. Mary's,
  Crescent (another parish) until early January. The agent leaned toward keeping it weekly
  with the dated cancellation; the reviewer chose to leave it out until it returns.

**C4. A weeks-of-the-month service that replaces the regular weekday one.**
- When: for example, a 7 PM First Friday Mass in place of the 8 AM Friday Mass.
- Lean: keep the regular slot on the remaining weeks.
- Evidence: our-lady-of-good-counsel-verona s10. The reviewer chose "Fridays 8 AM except
  first Fridays", which was the leaning, over "every Friday" and "leave out".

**C5. Confession after Mass on request ("let Father know").**
- Lean: include it at the time POLICY works out (R10), with a note. Only "by appointment"
  or "call the office" has no time.
- Evidence: immaculate-conception-greene s4. Sunday confession after the 10:00 AM Mass,
  where penitents are asked to tell Father first (the website gives it without that
  condition). The agent leaned toward 11:00 AM, and the reviewer included it.

**C7. "For members of X" under a heading that says all events are open.**
- Lean: include it.
- Evidence: blessed-trinity-buffalo s8. An October 28 Healing Mass "for members of HOBCCE",
  in a section that says its events are open to members of any parish. The agent leaned
  toward including it, and the reviewer included it.

**C8. Conflicting standing times that R40 does not resolve.**
- When: two service-specific schedule statements conflict and neither explains a dated
  exception or correction. Apply R40 first; do not ask solely because an old dated
  occurrence differs from the current standing schedule.
- Lean: not fixed. Lean as you judge, and say why.
- Evidence: parish-of-the-holy-family s19. Second-Saturday Adoration was at 9:30 AM in the
  newest bulletin and 9:00 AM in the September 6 one. The agent leaned toward 9:30, and
  the reviewer left it out (dropped).

## Former candidates

These IDs remain here so earlier rationales can be understood; do not reuse them.

- **C3:** promoted to R41, specific dated invitation over a generic no-Mass template.
- **C6:** settled by POLICY, Final source checks, and R24/R26 when Adoration attached to
  Mass has no separate or permitted relative start time. Evidence:
  our-lady-of-the-assumption-latham s10, "Simple Adoration" on the Friday 9 AM Mass line.
- **C9:** promoted into R6. Evidence: st-anthony-st-agnes-utica s8, website-only Saturday
  3:45 PM Confession supported by the site's otherwise matching Mass schedule.

Public/private Masses not already covered by POLICY, hedged availability such as "most
Saturdays", and unlocated chapels or winter rectories still need a human decision. The
new rules do not supply a default for those unresolved cases.
