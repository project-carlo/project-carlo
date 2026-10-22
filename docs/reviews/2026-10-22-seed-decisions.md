# Seed decisions from October 22, 2026

The owner reviewed the condensed B1–B10 and E1–E10 brief and authorized saving
the clear decisions and approving the seeds that were ready. Answers made in
this pass name `lyonsl2 (via Codex)`; earlier reviewer answers remain unchanged.

This resolves 63 of the original 72 questions, covering 89 of the 100 open
slots. There are nine questions, covering 11 slots in eight parishes, still open.
Forty-nine seeds have no questions left. Forty-eight were approved immediately;
St. Luke, Schenectady awaits the engineering fix described below before approval.
No published database or website was changed by this review.

The saved seeds keep their original `as_of`, bulletin list, paid-call trail and
draft summary. They describe the schedule at that earlier date, usually October
11, rather than a newly researched October 22 schedule. Dates that have passed
were reviewed against that original scope; they were not silently rewritten as
current events.

## Decisions applied

- **B1 — Parish websites:** usable when the schedule looks real and fits the
  bulletin. Include St. Kateri Latin Mass Community's on-site chapel hours.
  Leave out the reviewed stale, conflicting or incompletely specified website
  times. A copyright year alone does not establish that a schedule is stale.
- **B2 — One omission:** retain St. John of Rochester's repeated chapel and
  Thursday Adoration schedules, and St. Rita's repeated Tuesday Adoration.
  Preserve the Rochester chapel's printed warning that Adoration stops during
  Masses, including weddings and funerals. Do not infer a regular St. Lawrence
  slot from scattered dates without a clear repeating pattern.
- **B3 — Multiple bulletins:** treat matching Mass times in multiple bulletins
  as weekly. This includes Schenectady's Wednesday/Thursday 9 AM Masses, reversing
  the drafter's dated-only preference. At St. Francis, Binghamton, Tuesday and
  Thursday 8 AM recur; the Monday/Wednesday noon times have only one actual
  occurrence each, so they are not promoted. Their explicit dated cancellations
  are preserved separately. Altamont's Sunday 9 AM is supported by its matching
  website schedule under B1.
- **B6 — Overlapping Adoration:** keep Holy Spirit's longer Friday interval
  instead of adding a second Holy Hour slot inside it.
- **B7 — Eucharistic chapel:** include St. Theodore's daily 6 AM–8 PM hours,
  which its parish website explicitly calls Adoration. Do not describe this as
  confirmed exposition.
- **B9 — Unsupported repeating patterns:** exclude alternating-month
  Assumption Adoration and St. Rose's proposed first-Saturday 9 AM start.
  Neither is an accurate recurring entry in the present format.
- **B10 — Blank template lines:** exclude the suspect Fulton and Menands
  entries on the surrounding evidence. This is not a rule that every unfilled
  intention means no Mass.
- **E1–E7, E9–E10:** use the recommended choices. At Christ the King, preserve
  the regular Tuesday 9:30 AM Adoration and represent October 13's reviewed
  9:45 AM exception separately. At Transfiguration, the same bulletin identifies
  its office number and Gathering Area, supporting that church for October 31.
- **Existing rules:** resolve the 31 questions already covered by active rules,
  including older monthly announcements, previously announced future events,
  explicit holiday interruptions, off-site events, the school-Mass exception,
  Holy Hour and Benediction definitions, Confession during Adoration, and
  events without a definite time. Preserve the original evidence and append the
  review's explanation instead of replacing the drafter's reasoning.

## Questions left open

The owner answered “idk” for B4, B5 and B8. Those were not treated as approval.
E8 still needs its recommended venue check.

- **Our Lady of Peace, Clarence — s35 (B4):** October 31, 9 AM remembrance
  Mass invites families and asks for an RSVP. Is that a public Mass?
- **St. Clare, Colonie — s10 (B4):** is the advertised Syro-Malabar community
  Mass public? Its October 11 date has passed.
- **St. Paul's, Webster — s11 (B4):** is the unnamed “Memorial Mass” a public
  service or a private memorial? Its October 13 date has passed.
- **St. Mark, Utica — s6 (B5):** publish 3:15–3:45 PM Confession when the
  bulletin says “Most Saturdays”?
- **St. Anthony, Syracuse — s10/s11 (B5):** publish Saturday noon–1 PM Holy
  Hour and Confession when the parish says to check for changes?
- **St. Joseph–St. Patrick, Utica — s3/s4 (B8):** is the chapel for Monday
  5:30 PM Mass on the church's premises? Its holiday cancellation shares the
  venue question.
- **St. Mary, Nassau — s3 and s4 (B8):** how should Tuesday/Thursday 9:30 AM
  Masses be shown when they move to an unlocated rectory in unspecified winter
  months? These remain two questions in the existing files.
- **St. Michael, South Glens Falls — s13 (E8):** which church hosts the
  November 2, 7 PM remembrance Mass: St. Michael or St. Therese? The available
  parish calendar does not establish the venue.

## Engineering work requested

1. **Allow different hours on different weeks.** St. Luke has Friday Adoration
   at 11:30 AM–1 PM on non-first Fridays and 11:30 AM–4 PM on first Fridays.
   The two patterns do not overlap. Entry identity currently ignores the week
   pattern, so validation and loading reject them as duplicates. Preserve the
   previously reviewed first-Friday decision and support both schedules.
2. **Allow a justified parish-website source.** Let an agent settle a real,
   quoted website schedule after explaining why it fits the bulletin and why
   it appears current. The exact time need not also be in the bulletin.
   Keep live website evidence out of historical evaluations. Code can require
   the explanation and sources; it cannot decide semantic freshness by itself.

## Proposed wording for the guides

These are proposals, not edits to the active prompting guides. Use the next
unused R IDs for any new rules; retain old IDs because saved rationales cite
them. Update conflicting existing rules and candidates at the same time.

1. **Use a parish website when it makes sense.**

   “You may use a schedule on the parish's own website when it clearly describes
   a real service at a known church and fits what you read in the bulletin.
   Quote the page and briefly explain why you trust it. Watch for old priests,
   obsolete restrictions, conflicting schedules and announcements that clearly
   belong to an earlier period. An old copyright year alone does not make a
   schedule stale. Ask if you still doubt the time, place or whether the
   service continues. Do not use a live website in a historical evaluation.”

   Replace the website-only prohibition in R6/R29 and reconcile C9 with this.
   Match the final engineering representation for the explanation.

2. **One missing mention does not cancel a service.**

   “When seeding from several bulletins, keep a clearly established repeating
   service if the newest issue simply omits it once. Keep its older evidence.
   An explicit cancellation or schedule change is different: follow that
   notice. A cancellation of Mass does not automatically cancel Adoration.”

   Add this exception to R29 and retain R18's explicit-interruption rule.

3. **A matching time in multiple bulletins can establish a weekly service.**

   “If the same church, service, weekday and time appear in two or more
   bulletins, you may record the slot as weekly unless the notices identify
   those occurrences as special or one-off. They do not all have to appear
   inside one PDF. A weekend-only schedule box does not disprove weekday
   Masses printed elsewhere. A single dated occurrence is not enough by
   itself. A clear regular schedule or named monthly service follows its own
   rule.”

   Put the cross-bulletin rule in seeding guidance and narrow C1 so it does not
   negate this newly accepted rule merely because a service is in intentions.

4. **Do not list the same availability twice.**

   “If a Holy Hour is entirely inside an Adoration period already recorded at
   the same church, keep the longer period. Mention the Holy Hour in a note
   when useful, rather than adding a second overlapping Adoration slot.”

5. **Adoration can include a parish's Eucharistic chapel hours.**

   “You may include prayer before the Blessed Sacrament in an on-site chapel
   when the parish identifies those hours as Adoration. Do not claim the
   Sacrament is exposed unless the source says so. A building being open for
   prayer, by itself, does not establish an Adoration schedule.”

6. **Do not turn a complicated pattern into the wrong simple one.**

   “Every other month does not mean every month. Saturday after first Friday
   does not always mean first Saturday. A note does not fix an incorrect
   repeating schedule. When the format cannot express the pattern, record
   only future dates the source actually prints and whose time and place are
   clear; otherwise leave it out and explain why.”

   Reconcile R33's current suggestion to offer an inaccurate weekly slot with
   this accepted decision. Do not invent recurrence fields.

7. **Do not guess from an empty intention.**

   “A time with no Mass intention is not proof of either Mass or no Mass.
   Read the headings, surrounding entries and regular schedule. If the line
   appears to be a reused template and contradicts the clear schedule, leave
   it out with that explanation. A generic ‘Morning Liturgy’ label does not
   by itself prove a Communion Service.”

8. **Use the rule before asking the same question again.**

   “Before asking, check the active rules and their exceptions. A named
   monthly service need not appear in a bulletin covering a different week.
   A future event announced earlier need not be reannounced every week.
   Follow explicit POLICY definitions, including the exception allowing
   Confession to use Adoration's hours. Candidates do not override a clear
   active rule. Ask only about the uncertainty that remains.”

9. **Keep recurring changes separate from one-date exceptions.**

   “A dated calendar exception changes that occurrence, not every future
   week. A newer explicit church assignment can correct an older one. A
   church-specific column heading helps establish location; a parish-wide
   heading or office phone number alone is weaker evidence. Distinguish the
   hours a building is open from the hours a service is offered. Still ask
   when current sources genuinely disagree.”

   E10 also supports promoting C3: a specific dated invitation takes priority
   over a generic no-Mass template for that day.

10. **Group only questions that share an answer.**

    “Group the same venue decision across several weekdays. Do not group an
    uncertain weekly pattern with an explicit dated cancellation: rejecting
    the weekly pattern must not discard that cancellation. Preserve earlier
    reviewer answers when repairing a seed.”

Do not add defaults for the unresolved public/private Mass, “most Saturdays,”
or unlocated chapel/rectory cases until the owner decides those questions.
