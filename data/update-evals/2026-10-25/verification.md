# October 25 seeded-parish error verification

Reviewed October 26, 2026. This records the investigation before implementation. See [implementation.md](implementation.md) for subsequent code and data repairs; published data was not changed by the investigation.

## Evidence and scope

The weekly run is `20261025T131034Z-gh40196397303` (October 25, 13:11–14:25 UTC). Its stored results say 264 update calls, 203 applied proposals, and two rejected proposals. A later October 25 manual run made no update calls. This audit uses the local database's actual calls, stored input views and policy, current entries, and the stored PDFs read by the pipeline. It does not establish which snapshot is currently published.

The October 25 run also processed October 18 bulletins. Distinguish those historical dates from upcoming dates in the October 25 bulletin. All listed parishes' latest calls used policy hash `98c73111f1b85b984d6aae8363dafaa79001a98138a6eae28225f695045c5f79`.

## Findings and repairs

### St. Vincent de Paul Blessed Sacrament, Vestal — confirmed false cancellation

Call **342**, proposal 1, added cancelled entry **2072**, October 31 at 4 PM. Page 3 prints two separate 4 PM lines: the sister church's Mass, then this parish's intentions under the STVBS heading. Page 2 also assigns ministers to the October 31 4 PM service. There is no relocation or cancellation of STVBS's service.

**Repair:** delete entry 2072 through an audited human schedule revision. Keep weekly entry 1845 and the valid November 2 memorial Mass, entry 2073. Do not re-seed the parish.

**Prevention:** both a short parish clarification and a general prompt clarification. Suggested parish context: “The intentions list includes Sts. John & Andrew services alongside STVBS services. Two lines with the same time can be distinct services at the two churches. An off-site line does not relocate or cancel the STVBS line.” Existing reviewed exclusion s8 already explains that Sts. John & Andrew is off-site; expand that rationale rather than relying on a free-form seed summary. The general relocation rule should require evidence that the particular local service is moved, and check for a separate local line at the same time before cancelling it.

[October 25 PDF, pp. 2–3](https://container.parishesonline.com/bulletins/03/1214/20261025B.pdf)

### Whitney Point community / St. Stephen, Marathon — confirmed transition gap, including Confession

Call **148** adds October 31 exceptions, entries **1940–1943**, but retains weekly Mass **615** at 5 PM and Confession **614** at 4–4:45 PM. Page 2 explicitly announces an ongoing winter change beginning October 31: Mass 4 PM, Confession 3–3:45 PM. Thus the stored schedule shows the old times again on November 7 unless another update intervenes. That is a projection of the current state, not proof the next weekly run will fail.

**Repair:** ensure the weekly slots change effective October 31. With today's schema, retain the valid October 31 exceptions and apply an audited weekly modification when effective, removing redundant dated exceptions if necessary. There is no printed winter end date, so do not invent an annual season or a spring return date.

**Prevention:** general future-change support, rather than a permanent parish note. The current prompt says weekly changes wait until effective; reviewed seed exclusions s16/s17 likewise preserve the summer times until then. Persist a future change with its effective date and apply/render it when due, independently of whether a later bulletin repeats the announcement. A dated first occurrence alone does not implement an ongoing transition. Clarify whether “bulletin's week” includes a change starting at its ending weekend.

[October 25 PDF, pp. 2–3](https://container.parishesonline.com/bulletins/03/1424/20261025B.pdf)

### Transfiguration, Syracuse — missing Wednesday Mass confirmed; cancellation claim needs correction

Call **346** misses **Wednesday, October 28, 6:30 AM Mass**, printed on page 2. The **6:10–6:25 AM Confession** beside it is also missing. Call **345** had similarly missed the October 21 6:30 AM Mass; that date was already past by the October 25 call.

The October 25 bulletin explicitly prints 6:30 AM Mass on **Thursday October 29 and Friday October 30**. Do not cancel those services or their morning Confessions. The October 18 table instead prints Thursday October 22 at 12:10 PM and Friday October 23 at 6 PM, omitting the 6:30 AM services. That is a historical timetable discrepancy, not explicit cancellation text; the current policy forbids inferring cancellation from silence. It warrants review if treating that calendar as an exhaustive replacement, but does not justify upcoming cancellations or permanent deletion of the weekly slots.

**Repair:** add the October 28 Mass and Confession as dated entries. Historical October 21 can be repaired in history if desired; it does not affect future availability. Keep October 29/30 6:30 AM Masses.

**Prevention:** clarify the general reviewed-context rule: an exclusion of a *weekly interpretation* does not exclude a newly printed *dated occurrence*. Seed s51 rejects Wednesday 6:30 AM as weekly and records the service as dated; it does not reject the service itself. The same distinction applies to s50's Confession. A regression replay should exercise this distinction. The existing separate-calendar-pass instruction already covers recall; repeating it as a parish note is unlikely to add much. A parish note should explain a recurring source convention only if one is established, not declare that every missing table row is cancelled.

[October 25 PDF, p. 2](https://files.ecatholic.com/29735/bulletins/20261025.pdf?t=1792786413000) · [October 18 PDF, p. 2](https://files.ecatholic.com/29735/bulletins/20261018.pdf?t=1792181947000)

### Sacred Heart, Lake George — correct current location, missing future transition

Call **114** changes Wednesday Mass, Wednesday Adoration, and Friday Mass to note “Chapel,” entries **1921–1923**. Page 2 says the chapel closes **November 1 until June 1**, and those services resume in the main church. “Chapel” therefore describes October 28/30 reasonably; it is misleading for services after November 1. Calling the notes simply backwards misses the effective-date distinction.

**Repair:** remove “Chapel” from the three weekly entries effective November 1 (or explicitly say “Main church” if useful). Preserve the times: Wednesday and Friday Mass 8:30 AM; Wednesday Adoration 9 AM–3 PM. Do not cancel the services when the chapel closes.

**Prevention:** the same general future-change mechanism as Whitney Point, including effective changes to notes/location. A time-bounded parish clarification can help while that mechanism is absent. Do not encode “main church” as a permanent instruction, or invent a June service schedule from the reopening date alone.

[October 25 PDF, p. 2](https://container.parishesonline.com/bulletins/03/1267/20261025B.pdf)

### Holy Spirit / St. Joseph's — confirmed end-time error

Call **161** changed the note on Friday Holy Spirit Adoration, producing entry **1953**, but kept its 10 AM–9 PM interval. Page 6 describes the **closing** Knights of Columbus Holy Hour changing from 8–9 PM to 7–8 PM, starting October 23. The closing interval supplies the new overall end, 8 PM.

**Repair:** modify entry 1953 to Friday **10 AM–8 PM**, keeping the 7–8 PM Holy Hour note if useful. Do not add a second overlapping Adoration event.

**Prevention:** a narrow general clarification: moving an explicitly closing segment changes the enclosing Adoration period's end; moving an ordinary embedded segment does not necessarily change that boundary. The existing seed review s30 correctly avoids a duplicate interval; no permanent parish exception is needed. A replay should verify that the model updates the end time as well as the note.

[October 25 PDF, p. 6](https://container.parishesonline.com/bulletins/06/0030/20261025B.pdf)

### St. Bartholomew, Norwich — announced future change, not an ordinary recall miss

Call **123** proposes no changes. Page 2 announces the new daily rotation starting **Monday November 2**: St. Bartholomew Monday 9 AM; Tuesday St. Malachy; Wednesday St. Theresa; Friday St. Paul. The believed schedule still has Tuesday 9 AM, entry **434**. The seed context already explicitly discusses this pending transition.

**Repair:** effective November 2, replace this parish's Tuesday 9 AM weekly Mass with Monday 9 AM. Do not assign the other churches' services to St. Bartholomew. Their owning parishes should be checked separately.

**Prevention:** future-change support, shared with Whitney Point and Lake George. Deferring the weekly replacement follows the present prompt; it is inaccurate to call that alone a model recall failure. A stored effective change avoids relying on the next issue to repeat the notice. Another permanent parish note is unnecessary.

[October 25 PDF, p. 2](https://designrr.s3.amazonaws.com/kathy_at_thebestva.com_52279/kathythebestvacom_25October20261792673248.pdf)

### St. Michael, South Glens Falls — confirmed dated recall miss

Call **302** proposes no changes. Page 5's parish calendar lists **November 2, All Souls' Day Mass of Remembrance, 7 PM**; no corresponding current entry exists.

**Repair:** add a dated November 2, 7 PM Mass at St. Michael the Archangel, with an optional remembrance note. Do not add a weekly Monday slot.

**Prevention:** one-off repair plus a regression case under the existing calendar-pass rule. No parish-specific note or new scheduling rule is justified by this single miss. Replays should test whether input detail or a separate calendar extraction/check improves recall before changing the model configuration globally.

[October 25 PDF, p. 5](https://container.parishesonline.com/bulletins/03/0901/20261025B.pdf)

### Sacred Heart, Cicero — suspicious source time, accurately copied

Call **186** adds entry **1981**, November 15, 2 AM First Penance. Page 7 really prints **2:00 AM** and explicitly invites adults to receive Reconciliation too, so the event is not excluded merely as a children's preparation session. An afternoon typo is plausible but unverified.

**Repair:** obtain corroboration before changing to 2 PM. If it cannot be corroborated before publication, omit/hold this disputed dated entry rather than guess a replacement time. A later correction should be a dated human fix with evidence.

**Prevention:** a general review flag for unusual overnight, non-overnight services, without banning genuine night services or automatically flipping AM/PM. No lasting parish note.

[October 25 PDF, p. 7](https://container.parishesonline.com/bulletins/06/0003/20261025B.pdf)

### St. Jerome, East Rochester — 3 AM is supported, not a verified error

Call **204** adds entry **1996**, October 31, 3 AM Adoration/Benediction. The October 18 announcement explicitly prints 3 AM. The October 25 issue repeats **3 AM** in both its event calendar and prayer announcement. Thus there is no basis to change this to 3 PM. The website's ordinary 3 PM Saturday Confessions are a different event and do not correct the special service.

**Repair:** none without contradictory evidence. Keep 3 AM; optional manual confirmation is reasonable. Do not fabricate a one-hour duration from the special service's name when the bulletin gives none.

**Prevention:** only the same general unusual-time review flag, with corroborated exceptions. No permanent parish note and no automatic AM/PM correction.

[October 18 PDF, p. 3](https://files.ecatholic.com/22370/bulletins/20261018.pdf?t=1792067072000) · [October 25 source PDF, pp. 2–3](https://files.ecatholic.com/22370/bulletins/20261025.pdf?t=1792674729000) · [Parish web calendar: ordinary Confessions](https://www.stjeromerochester.org/calendar)

## Where guidance belongs

The updater currently receives selected, approved seed **slot** decisions through `reviewed_seed_context`, not a parish's seed `summary`, a human revision's `note`, or arbitrary Markdown. `schedule/context.py` selects settled exclusions, answered decisions, and monthly/seasonal slots; it verifies that the seed matches the imported seed revision. Changing only a selected slot's rationale/sources does not change the imported schedule digest; it does change the rendered context/hash for future requests. Changing included seed entries is different and can cause re-import: repair live schedules through human revisions instead.

Use parish context for lasting source conventions such as Vestal's mixed intentions list. Use the general prompt for shared interpretation rules. Use code/data support for effective dates and review flags. The deterministic decision policy currently checks structure, identity, date validity, and whole-call guards; it cannot verify whether a PDF actually cancels a Mass. More structural guards alone will not repair these source-reading failures.

Recommended implementation priority:

1. Repair the confirmed current errors through audited human revisions: Vestal cancellation, Holy Spirit end time, Transfiguration October 28 entries, and St. Michael November 2 Mass. Resolve/hold Cicero's disputed time.
2. Preserve and enact the three pending transitions: St. Stephen October 31, Lake George November 1, St. Bartholomew November 2. Do not depend solely on later bulletins.
3. Clarify mixed-venue cancellations, weekly-versus-dated exclusions, and closing-service boundaries in the shared prompt; add focused replays against the historical calls before claiming improvement.
4. Add effective-date/deferred-change support and unusual-time review. Effective dates are explicitly outside the current v1 design; a parish note is only a temporary reminder, not an implementation of that feature.
