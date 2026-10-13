# Seeding decision rules

These are the rules for deciding a seed's slots. `POLICY` in
`src/pdf_extract/classifiers/schedule_policy.py` says what one bulletin shows: which events
count, weekly or dated, times, churches. This file covers what is specific to seeding:
reading across bulletins, history and the website; `as_of`; evidence; and what is settled
and what is asked. The JSON fields are in [file-format.md](file-format.md).

**The default is to ask.** Settle a slot only when a rule below (R…) or POLICY clearly
covers it. Everything else is `needs_human`: a short question, the options, exactly one
`"leaning": true`, and in the rationale why you lean that way. Candidates (C…) are not in
force: ask them too, and lean the way they say. The reviewer works in the labeler and
never sees your report. A doubt kept only in the report or in a settled slot's rationale
is lost, and the slot is approved as settled.

**Citing.** A settled slot's `rationale` starts with the rule it rests on ("R1: printed in
the schedule box of all three bulletins") or names the POLICY section ("POLICY, Times").
A question's rationale may name the candidate it leans on ("leaning per C3").

**How to change these rules** (maintainer): add a rule under the next unused ID in the
section it belongs to. Never renumber or reuse an ID, since rationales cite them. To
promote a candidate, move it into its section as a new R rule ("was C4"). `pnpm seed
questions` lists answered questions, their leanings and what they cite.

## Evidence and sources

**R1. Clear in the newest bulletin.**
- When: the newest bulletin prints the slot clearly, POLICY is clear about it, and nothing
  you read contradicts it.
- Do: `settled` include, `page` where the newest bulletin prints it, with an `agent` source
  at that page. Every inclusion you settle, under any rule, needs that source, except
  under R12 and R19. `seed check` enforces this.

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
- Do: it can back up a reading, or settle where a chapel is or that a "First Saturday" Mass
  is monthly. It never outweighs the newest bulletin, because websites go stale. A slot
  found only on the website is asked (R29).

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

## Asking

**R27. One decision, one question.**
- When: one answer decides several slots (the seven days of a chapel, a confession window
  before every Mass).
- Do: give the slots one `group`, with the same question and the same options in the
  same order, leaning the same way.

## Always ask

These cases are always `needs_human`. They are the standing examples of the default.

**R28. The bulletins contradict each other and don't settle it.**

**R29. The newest bulletin doesn't print it.**
- When: a slot backed only by older bulletins or the website (a weekly Mass missing with no
  reason given), and R12, R18 and R19 don't cover it.
- Do: ask, with `page: null`. If the reviewer answers to include it, it is included.

**R30. POLICY leaves it a judgment call.**

**R31. The print is unreadable.**

**R32. It's unclear which listed church it belongs to.**

**R33. A schedule the file can't express, with no dates printed.**
- When: for example, "every other Wednesday".
- Do: offer weekly with a note that says so, and leaving it out. Don't invent a field for
  it.

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
- When: a Mass appears in the Mass intentions every week but is missing from the parish's
  regular schedule box, and from its website.
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

**C3. A dated special listing against a general "NO MASS" line for the same day.**
- Lean: the specific dated listing.
- Evidence: mater-christi-albany s18. A notice gave a 5:30 PM Mass on Monday, October 5,
  while the intentions' template line said "NO MASS" for that day. The agent leaned toward
  including the dated Mass, and the reviewer included it.

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

**C6. Adoration "with" a Mass, with no clock time and no "before" or "after".**
- Lean: leave it out, since it has no definite time.
- Evidence: our-lady-of-the-assumption-latham s10. "Simple Adoration" is attached to the
  Friday 9:00 AM Mass line. The agent leaned toward leaving it out, and the reviewer
  agreed.

**C7. "For members of X" under a heading that says all events are open.**
- Lean: include it.
- Evidence: blessed-trinity-buffalo s8. An October 28 Healing Mass "for members of HOBCCE",
  in a section that says its events are open to members of any parish. The agent leaned
  toward including it, and the reviewer included it.

**C8. The same slot at different times in the newest and an older bulletin.** (The owner
hasn't decided.)
- Lean: not fixed. Lean as you judge, and say why.
- Evidence: parish-of-the-holy-family s19. Second-Saturday Adoration was at 9:30 AM in the
  newest bulletin and 9:00 AM in the September 6 one. The agent leaned toward 9:30, and
  the reviewer left it out (dropped).

**C9. A slot only on the parish website, with nothing in the bulletins against it.** (The
owner hasn't decided.)
- Lean: not fixed. Lean as you judge, and say why.
- Evidence: st-anthony-st-agnes-utica s8. Saturday 3:45 PM Confession appears only on the
  website, whose Mass times match the bulletins. The agent leaned toward including it, and
  the reviewer included it. `seed check` doesn't allow a settled inclusion without a
  newest-bulletin citation (R1), so promoting this would need a code change.
