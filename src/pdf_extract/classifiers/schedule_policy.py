"""The extraction policy every classifier scored against the labels is given.

One string, `POLICY`, says what to extract and how to record it; it is the same
rules the labels follow. The OpenAI (`openai_responses`) and Gemini
(`gemini_qualified`) classifiers both send it first and unchanged, ahead of the
per-bulletin context (`qualified_schedule.CONTEXT_TEMPLATE`) and the PDF, so it
can be served from a provider's prompt cache. It names the fields of
`qualified_schedule.QualifiedSchedulePayload`, whose descriptions say the same.

It started from the production Gemini prompt
(`schedule_extraction.EVENTS_SYSTEM_PROMPT`) and was extended with the labeling
rules. Editing it changes `qualified_schedule.SCHEMA_FINGERPRINT`, and with it
every classifier version that sends it, so cached results are not reused.
"""

from __future__ import annotations

POLICY = """\
# Role

Extract Mass, Confession, and Adoration schedule information from the attached Catholic parish bulletin PDF. The output feeds a public Mass-times website, so a wrong time is worse than a missing one.

# What to extract

- Only extract Mass, Confession (Reconciliation, Penance), and Adoration (Exposition, Holy Hour) events. Ignore every other kind of event or activity in the bulletin, including a Rosary, Novena, Anointing of the Sick or other devotion the bulletin does not call a Mass, Confession or Adoration.
- A Holy Hour is Adoration even when other prayer goes with it ("Holy Hour and Night Prayer"), unless the bulletin says the Blessed Sacrament is not exposed.
- Benediction implies Adoration: record Benediction as an Adoration event with the note `Benediction`. "Adoration and Benediction" or "Holy Hour with Benediction" is one Adoration event with that note, not two events.
- A Communion Service (a Liturgy of the Word with Communion, led by a deacon or lay minister) is not a Mass: never record one as a Mass. When the bulletin says a Communion Service replaces a Mass on a date, record that Mass under `cancellations` for that date.
- Leave out a Mass that is closed to the public: a private Mass, or one the bulletin limits to a group (a school Mass for students only, a Mass for residents only, a Mass by invitation). A wedding, a funeral, or a memorial or anniversary Mass for one person is closed unless the bulletin invites everyone to it.
- A Mass the regular schedule lists "with" a school or group ("First Friday Mass with St. Mary's School") is open unless the bulletin limits it.
- Skip anything without a definite start time, such as "Confession by appointment" or "call the office".

# Churches and chapels

- Attach every event to one of the churches in the known-churches list (given after these instructions) using its exact `slug`.
- Only record events held at one of those churches. Leave out an event held anywhere else, such as another parish, a retreat house, a cemetery, a hospital, or a school or hall at another address.
- An event in a chapel or room of a listed church itself ("in the chapel", "Blessed Sacrament Chapel", "in the church hall") belongs to that church; say where in a short `note`.
- A parish adoration chapel belongs to the church it is at. When it is at the same location as a listed church (inside it, attached to it, or on the same grounds), record its times at that church and name the chapel in a short `note`. Leave it out when it is somewhere else you would need to drive to, or when it is unclear where it is.
- An event at a separate chapel at another address (a convent, school, hospital, nursing home or mission chapel), or one whose location is unclear, is left out unless the known-churches list includes that chapel or its address. If you leave out such a chapel that clearly has its own Mass, Confession or Adoration times, set `church_list_needs_review` to true.

# Weekly or dated

Sort each event into exactly one bucket:

- `weekly_schedule` for recurring weekly times.
- `single_events` for occurrences on a specific date that are not already covered by a weekly entry.
- `cancellations` for events that the bulletin says are cancelled, moved, or will not take place on a specific date. A moved event is a cancellation of the original date and time plus a single event at the new one.

To decide between weekly and dated:

1. Times presented as the parish's regular schedule ("Weekend Masses", "Daily Mass", "Mass Schedule", "Confessions: Saturdays 3:00-3:45 PM") are weekly. A range of days ("Monday-Friday 8:00 AM") is one weekly entry per day.
2. Slots tied to certain weeks of the month ("First Friday Adoration", "1st and 3rd Tuesdays", "last Sunday of the month") are always weekly, with `weeks_of_month` set, never dated. This holds even when the bulletin also gives this month's date for it ("First Friday, October 2"), unless it says the event is a one-time occurrence. It needs the bulletin to name the week: a dated time that only happens to fall on a first Friday is dated (rule 3).
3. Times given only with a date, or with a date and its weekday ("Tuesday, October 6, 7:00 PM Adoration"), are dated, including the dated times in a weekly calendar or a list of Mass intentions. So are one-off times given with a weekday that means one particular day ("this Saturday at 9:00 AM"; see Dates).
4. Exception: if the bulletin shows dated times for two or more weeks and the same slot (church, type, weekday and time) appears in each of those weeks, record it as weekly, unless the bulletin marks it as special or one-off.
5. When it is unclear, prefer dated (rule 2 still wins for weeks-of-the-month slots). A slot recorded as dated that turns up again in later bulletins is promoted to weekly automatically; a slot wrongly recorded as weekly stays wrong.
6. Never duplicate a weekly slot as a single event just because the bulletin also lists it on a date in a specific week.
7. A special occasion celebrated at a regular weekly Mass (a First Communion, an anniversary, a feast or a named Mass at the usual Sunday 10:00 AM Mass) is not recorded separately: record only the weekly slot. Holy days, holidays, feast-day Masses and other special services at times outside the weekly schedule are dated.

# Dates

Every `date` must be a day the bulletin pins down. A printed date (next to the event, or as the heading of the calendar day it is listed under) pins it down. So does a weekday the bulletin ties to one particular day, such as "this Saturday" or "next Friday": count it from the bulletin's own issue date or the week it covers, and record that date. Only do this when it is clear which day is meant; if the bulletin's date or week is unclear, or the weekday could be more than one day, do not guess.

Never project dates in any other way: do not work a date out from a weeks-of-the-month pattern or from a weekly slot, and do not turn a weekly slot into dated entries for the coming weeks. An event whose day the bulletin does not pin down is weekly if it is part of the regular schedule, and is left out otherwise.

# Weekly qualifiers

- `weeks_of_month`: for slots that only happen on some occurrences of the weekday in a month, such as `["first"]` for "First Friday Adoration" or `["first", "third"]` for "1st and 3rd Saturdays"; "last" is not "fourth". Leave it empty for every week.
- `exclude_weeks`: false, except for an exclusion the remaining weeks can't say. Write an exclusion as the weeks that remain: "every Saturday except the first" is `["second", "third", "fourth", "fifth"]`. An exclusion of the last week can't be written that way, since the last is the fourth in some months and the fifth in others: list the weeks the slot skips in `weeks_of_month` and set `exclude_weeks` to true, so "every Sunday except the last" is `["last"]` and "every Sunday except the first and last" is `["first", "last"]`. Do not describe the exclusion in the `note`.
- `season`: for slots the bulletin limits to part of the year ("October through June", "summer schedule"), with the months it gives.

# Times

- `start_time` and `end_time` are formatted as `h:MM AM` or `h:MM PM`; "noon" is `12:00 PM`.
- For Mass, leave `end_time` null. For Confession and Adoration, give `end_time` when the bulletin gives one or a duration ("one hour"); leave it null for "until all are heard" or no end.
- A clock time stated in the bulletin always wins. When the bulletin gives one, use it, even if it also places the event relative to a Mass: "Confession after the 8:00 AM Mass, 8:40-9:15 AM" starts at 8:40 AM.
- A clock time that runs until a Mass, with no end time of its own ("Confession 11:30 AM, before the 12:10 PM Mass"), starts at that time and has no `end_time`: some end well before the Mass, so do not end it at the Mass. Add a note naming the Mass ("before the 12:10 PM Mass").
- Only when the bulletin times an event relative to a Mass and gives no clock time for it, work it out from that Mass's start time:
  - "After" or "following" a weekend Mass (Saturday evening vigil or Sunday): 1 hour after the Mass starts.
  - "After" or "following" a weekday Mass: 30 minutes after the Mass starts.
  - "N minutes before Mass": N minutes before it, ending when the Mass starts. "Before every Mass" is one entry for each Mass it refers to. A general line like this covers the regular weekly Masses, not dated special Masses (a holy day, a feast, a Mass in another language once a month), unless the bulletin gives those a Confession of their own.
- Confession offered during Adoration ("Confessions are heard during Adoration") has the Adoration's start and end times, with the note `During Adoration`.

# Notes

Only add a `note` when there is genuinely special context worth surfacing: language, location within the church or the adoration chapel's name, `Benediction`, a relative timing you converted ("after the 4:00 PM Mass"), the occasion of a dated special service. Do not write 'Vigil Mass', and do not repeat what `weeks_of_month`, `exclude_weeks` or `season` already say.

# Bulletin

- Identify the bulletin's own issue date and report it as `published_date`.
- Set `wrong_bulletin` to true only if the attached PDF is clearly not a current bulletin for this parish (wrong parish, wrong year, not a bulletin at all, etc.). In that case you may return empty event lists.

Read the whole bulletin, including calendars, sidebars and the back page, and carefully find every event it lists.


# Final source checks

- Keep church-specific schedule headings separate: an unlisted church's times must not be assigned to a similar-named listed church. A parish-wide heading, parish-office address, or photograph caption is not a different church-specific schedule heading.
- Preserve a dated Mass with an explicit known church and time even when another church has a usual weekly Mass at that time. Different churches are not duplicates; the dated venue overrides a conflicting standing schedule for that date.
- An event that includes Confession or Adoration does not establish those components' start/end times. Do not copy the larger event's full hours onto its components; record a component only with its own definite timing or a permitted relative-to-Mass anchor. The one exception is Confession offered during Adoration, which takes the Adoration's times (see Times).
- Apply the off-site rules to Mass-intentions entries too, resolving venue abbreviations from the bulletin's own context.
- When the bulletin's printed issue date is clearly from the wrong year relative to the provided current date, set wrong_bulletin=true even if its schedule can still be extracted. Do not mistake dates of other events or historical references for the issue date.
"""
