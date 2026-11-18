"""The blind second reading of a seed: reading the reply, and comparing it with the slots."""

from __future__ import annotations

import json

from pdf_extract.classifiers.seed_opinion import opinion_entries, parse_reply
from pdf_extract.seeding import opinion

CHURCH = "st-marys-oswego"


def entry(day="Saturday", start="16:00", **extra):
    base = {"church_slug": CHURCH, "event_type": "mass", "event_kind": "weekly",
            "day_of_week": day, "date": None, "start_time": start, "end_time": None,
            "cancelled": False, "weeks_of_month": [], "exclude_weeks": False, "season": None}
    return {**base, **extra}


def slot(sid, e, decision="include", rationale="R1: printed."):
    return {"id": sid, "decision": decision, "status": "settled", "entry": e,
            "rationale": rationale}


def kinds(result):
    return sorted(d["kind"] for d in result["differences"])


def test_reply_becomes_seed_entries_with_evidence():
    reply = {
        "bulletins": [{"bulletin": "B1", "published_date": "2026-10-25", "wrong_bulletin": False}],
        "weekly_schedule": {"masses": [{
            "church_slug": CHURCH, "day_of_week": "Saturday", "start_time": "4:00 PM",
            "end_time": None, "weeks_of_month": [], "exclude_weeks": False, "season": None,
            "note": None, "evidence": [{"bulletin": "B1", "page": 2, "quote": "Sat 4 PM"}]}],
            "confessions": [], "adorations": []},
        "single_events": {"masses": [], "confessions": [], "adorations": []},
        "cancellations": {"masses": [{
            "church_slug": CHURCH, "date": "2026-11-02", "start_time": "8:00 AM",
            "end_time": None, "note": None,
            "evidence": [{"bulletin": "B1", "page": 3, "quote": "No 8 AM Mass"}]}],
            "confessions": [], "adorations": []},
        "church_list_needs_review": False,
    }
    payload, status = parse_reply(json.dumps(reply))
    assert status == "ok"
    weekly, cancelled = opinion_entries(payload)
    assert weekly["start_time"] == "16:00" and weekly["event_kind"] == "weekly"
    assert weekly["evidence"][0]["page"] == 2
    assert cancelled["cancelled"] is True and cancelled["date"] == "2026-11-02"


def test_agreement_and_each_kind_of_difference():
    seed = {"slots": [
        slot("s1", entry()),                                    # luna agrees
        slot("s2", entry("Sunday", "10:00")),                   # luna: 10:30 -> differs
        slot("s3", entry("Monday", "08:00")),                   # luna silent -> extra
        slot("s4", entry("Friday", "12:15", church_slug="chapel"), decision="exclude",
             rationale="R23: not on the church list."),         # luna includes -> excluded
    ]}
    luna = [
        entry(), entry("Sunday", "10:30"), entry("Friday", "12:15", church_slug="chapel"),
        entry("Wednesday", "19:00"),                            # nowhere in the seed -> missing
        entry(event_kind="specific_date", day_of_week=None, date="2026-01-01"),  # before today
    ]
    result = opinion.compare(seed, luna, "2026-10-25")
    assert len(result["agree"]) == 1
    assert result["out_of_scope"] == 1
    assert kinds(result) == ["differs", "excluded", "extra", "missing"]
    differs = next(d for d in result["differences"] if d["kind"] == "differs")
    assert differs["fields"] == ["start time"] and differs["slot"] == "s2"
    excluded = next(d for d in result["differences"] if d["kind"] == "excluded")
    assert excluded["policy_exclusion"] is True


def test_equivalent_weeks_match_and_mass_end_time_is_ignored():
    seed = {"slots": [slot("s1", entry("Sunday", weeks_of_month=["last"], exclude_weeks=True))]}
    same = entry("Sunday", weeks_of_month=["last"], exclude_weeks=True, end_time="17:00")
    assert opinion.compare(seed, [same], "2026-10-25")["differences"] == []
    every_week = entry("Sunday")
    result = opinion.compare(seed, [every_week], "2026-10-25")
    assert [(d["kind"], d["fields"]) for d in result["differences"]] == [
        ("differs", ["weeks/season"])]


def test_question_leaning_agrees_and_other_option_differs():
    question = {"id": "s1", "status": "needs_human", "entry": None, "options": [
        {"label": "Fridays 9:45", "leaning": True, "entry": entry("Friday", "09:45")},
        {"label": "First Fridays", "entry": entry("Friday", "09:45", weeks_of_month=["first"])},
        {"label": "Leave out", "entry": None}]}
    seed = {"slots": [question]}
    assert opinion.compare(seed, [entry("Friday", "09:45")], "2026-10-25")["differences"] == []
    other = opinion.compare(
        seed, [entry("Friday", "09:45", weeks_of_month=["first"])], "2026-10-25")
    assert kinds(other) == ["question"]


def test_weekday_differences_group_into_one():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    seed = {"slots": [slot(f"s{i}", entry(d, "08:00")) for i, d in enumerate(days)]}
    luna = [entry(d, "08:30") for d in days]
    result = opinion.compare(seed, luna, "2026-10-25")
    assert len(result["differences"]) == 5
    assert len(result["groups"]) == 1


def dated(day, start, **extra):
    return entry(None, start, event_kind="specific_date", day_of_week=None, date=day, **extra)


def adoration(day="Monday", start="00:00", end=None, **extra):
    return entry(day, start, event_type="adoration", end_time=end, **extra)


def test_24_hour_adoration_matches_however_it_is_written():
    for seed_end, luna_end in (("23:59", "00:00"), ("23:59", None), ("00:00", None)):
        seed = {"slots": [slot("s1", adoration(end=seed_end))]}
        result = opinion.compare(seed, [adoration(end=luna_end)], "2026-10-25")
        assert result["differences"] == [] and len(result["agree"]) == 1
    # ...and an excluded 24-hour slot is matched as excluded, not missing.
    seed = {"slots": [slot("s1", adoration(end="23:59"), decision="exclude",
                           rationale="Owner: the chapel's location is unknown.")]}
    assert kinds(opinion.compare(seed, [adoration(end="00:00")], "2026-10-25")) == ["excluded"]
    # A midnight start with a real end is not all day.
    seed = {"slots": [slot("s1", adoration(end="23:59"))]}
    result = opinion.compare(seed, [adoration(end="06:00")], "2026-10-25")
    assert [d["fields"] for d in result["differences"]] == [["end time"]]


def test_end_time_or_no_end_on_the_same_slot_is_one_differs():
    seed = {"slots": [slot("s1", entry(event_type="confession", end_time="16:15", start="15:30")),
                      slot("s2", entry("Sunday", "10:35", event_type="confession", end_time="11:15"))]}
    luna = [entry(event_type="confession", start="15:30", end_time="16:30"),
            entry("Sunday", "10:35", event_type="confession")]
    result = opinion.compare(seed, luna, "2026-10-25")
    assert [(d["kind"], d["slot"], d["fields"]) for d in result["differences"]] == [
        ("differs", "s1", ["end time"]), ("differs", "s2", ["end time"])]


def test_several_slots_on_a_day_pair_by_same_then_nearest_start():
    seed = {"slots": [
        slot("s1", entry("Sunday", "09:00", weeks_of_month=["last"], exclude_weeks=True)),
        slot("s2", entry("Sunday", "10:00", weeks_of_month=["last"])),
        slot("s3", entry("Sunday", "11:00", weeks_of_month=["last"], exclude_weeks=True)),
        slot("s4", entry("Sunday", "17:00")),
    ]}
    luna = [entry("Sunday", "09:00"), entry("Sunday", "11:00", weeks_of_month=["last"],
                                            exclude_weeks=True), entry("Sunday", "17:30")]
    result = opinion.compare(seed, luna, "2026-10-25")
    got = sorted((d["kind"], d["slot"], tuple(d.get("fields") or ())) for d in result["differences"])
    assert got == [("differs", "s1", ("weeks/season",)), ("differs", "s4", ("start time",)),
                   ("extra", "s2", ())]
    # Starts further apart than the window stay unpaired when the day has several slots.
    seed = {"slots": [slot("s1", entry("Sunday", "08:00")), slot("s2", entry("Sunday", "10:00"))]}
    result = opinion.compare(seed, [entry("Sunday", "13:00"), entry("Sunday", "18:00")],
                             "2026-10-25")
    assert kinds(result) == ["extra", "extra", "missing", "missing"]


def test_a_dated_entry_an_included_weekly_slot_covers_is_no_difference():
    # 2026-11-02 is a Monday, the first of the month.
    seed = {"slots": [slot("s1", entry("Monday", "12:05"))]}
    luna = [entry("Monday", "12:05"), dated("2026-11-02", "12:05")]
    result = opinion.compare(seed, luna, "2026-10-25")
    assert result["differences"] == []
    assert [d["why"] for d in result["dropped"]] == ["covered-by-weekly"]
    # Not when the weekly slot's weeks leave that date out, or the time differs.
    seed = {"slots": [slot("s1", entry("Monday", "12:05", weeks_of_month=["second"]))]}
    assert kinds(opinion.compare(seed, [dated("2026-11-02", "12:05")], "2026-10-25")) == [
        "extra", "missing"]
    seed = {"slots": [slot("s1", entry("Monday", "12:05"))]}
    assert kinds(opinion.compare(seed, [entry("Monday", "12:05"), dated("2026-11-02", "19:00")],
                                 "2026-10-25")) == ["missing"]
    # The seed's own duplicate of luna's weekly slot is dropped the same way.
    seed = {"slots": [slot("s1", entry("Monday", "12:05")), slot("s2", dated("2026-11-02", "12:05"))]}
    assert opinion.compare(seed, [entry("Monday", "12:05")], "2026-10-25")["differences"] == []


def test_a_cancellation_that_cancels_nothing_on_either_side_is_dropped():
    # 2026-10-14 is a Wednesday.
    nothing = dated("2026-10-14", "09:00", cancelled=True)
    seed = {"slots": [slot("s1", entry("Sunday", "10:00"))]}
    result = opinion.compare(seed, [entry("Sunday", "10:00"), nothing], "2026-10-11")
    assert result["differences"] == [] and result["dropped"][0]["why"] == "cancels-nothing"
    # The seed cancelling a slot it excludes changes nothing either.
    seed = {"slots": [slot("s1", entry("Wednesday", "12:00"), decision="exclude"),
                      slot("s2", dated("2026-10-14", "12:00", cancelled=True))]}
    assert opinion.compare(seed, [], "2026-10-11")["differences"] == []
    # A cancellation of a weekly slot on either side is kept.
    seed = {"slots": [slot("s1", entry("Wednesday", "09:00"))]}
    result = opinion.compare(seed, [entry("Wednesday", "09:00"), nothing], "2026-10-11")
    assert kinds(result) == ["missing"]


def test_an_excluded_slot_with_another_season_or_weeks_is_excluded_not_missing():
    seed = {"slots": [slot("s1", entry(start="17:30"), decision="exclude",
                           rationale="R33: Memorial Day to Columbus Day can't be a season.")]}
    luna = [entry(start="17:30", season={"start_month": 5, "start_day": None,
                                         "end_month": 10, "end_day": None})]
    result = opinion.compare(seed, luna, "2026-10-11")
    assert [(d["kind"], d["slot"], d["fields"]) for d in result["differences"]] == [
        ("excluded", "s1", ["weeks/season"])]
    assert result["counted"]  # R33 is not one of the policy exclusions: still counted


def with_sources(s, *sources, rationale=None):
    s["sources"] = [{"source": kind, "bulletin": ref, "page": 1, "said": "x"} if ref else
                    {"source": kind, "url": "https://parish.example", "said": "x"}
                    for kind, ref in sources]
    if rationale:
        s["rationale"] = rationale
    return s


def test_differences_the_opinion_could_not_see_are_resolved():
    seen = ["aaaa1111" + "0" * 56, "bbbb2222" + "0" * 56]
    seed = {"slots": [
        # Settled from an older issue luna wasn't given (R12), though history saw a newer one.
        with_sources(slot("s1", entry("Friday", "13:00", weeks_of_month=["first"])),
                     ("agent", "cccc3333"), ("history", "aaaa1111")),
        # The website set its end time (R6).
        with_sources(slot("s2", entry(event_type="confession", start="16:15", end_time="17:00")),
                     ("agent", "aaaa1111"), ("website", None),
                     rationale="R6: the parish site gives the end."),
        # Website-only.
        with_sources(slot("s3", entry("Thursday", "18:00")), ("website", None)),
        # C9, the rule R6 was promoted from.
        with_sources(slot("s6", entry("Saturday", "09:00", weeks_of_month=["first"])),
                     ("agent", "aaaa1111"), ("website", None),
                     rationale="R29: only the website gives the time. Leaning include per C9."),
        # Printed in a bulletin luna read, the website merely agreeing: luna's miss counts.
        with_sources(slot("s4", entry("Monday", "08:00")), ("agent", "bbbb2222"), ("website", None),
                     rationale="R1: printed; the website agrees."),
        slot("s5", entry("Tuesday", "12:15", church_slug="chapel"), decision="exclude",
             rationale="R23: not on the church list."),
    ]}
    luna = [entry(event_type="confession", start="16:15"),
            entry("Tuesday", "12:15", church_slug="chapel")]
    result = opinion.compare(seed, luna, "2026-10-25", seen_bulletins=seen)
    resolved = {d["slot"]: d["resolved"] for d in result["differences"]}
    assert resolved == {"s1": "unseen-bulletins", "s2": "website", "s3": "website", "s4": None,
                        "s5": "policy-exclusion", "s6": "website"}
    assert [g[0]["slot"] for g in result["counted"]] == ["s4"]
    # Without the bulletins luna saw, only the R6 and R22-R26 cases are resolved.
    result = opinion.compare(seed, luna, "2026-10-25")
    assert {d["slot"]: d["resolved"] for d in result["differences"]}["s1"] is None


def test_an_unlisted_slug_that_plainly_means_a_listed_one_is_mapped():
    luna = [entry(church_slug="st-mary-honeoye"), entry(church_slug="somewhere-else")]
    assert opinion.fix_church_slugs(luna, ["st-marys-honeoye", "st-matthew"]) == 1
    assert [e["church_slug"] for e in luna] == ["st-marys-honeoye", "somewhere-else"]
    assert luna[0]["problems"] == ["unlisted church slug 'st-mary-honeoye'"]


def test_a_period_past_midnight_matches_its_two_days_written_apart():
    overnight = adoration("Friday", "20:00", "06:00", weeks_of_month=["first"])
    split = [adoration("Friday", "20:00", "23:59", weeks_of_month=["first"]),
             adoration("Saturday", "00:00", "06:00", weeks_of_month=["first"])]
    seed = {"slots": [slot("s1", overnight)]}
    assert opinion.compare(seed, split, "2026-10-25")["differences"] == []
    seed = {"slots": [slot("s1", split[0]), slot("s2", split[1])]}
    assert opinion.compare(seed, [overnight], "2026-10-25")["differences"] == []
    # Ending at midnight is not ending at 6 AM: the seed's slot is still unmatched.
    seed = {"slots": [slot("s1", overnight)]}
    assert kinds(opinion.compare(seed, split[:1], "2026-10-25")) == ["extra"]
    # A reading past midnight that matches nothing is one item, not two.
    result = opinion.compare({"slots": []}, [overnight], "2026-10-25")
    assert kinds(result) == ["missing", "missing"] and len(result["groups"]) == 1
    # Ending at midnight is the same day.
    assert opinion.overnight_parts(adoration("Tuesday", "23:00", "00:00")) == [
        adoration("Tuesday", "23:00", "00:00")]
    seed = {"slots": [slot("s1", adoration("Tuesday", "23:00", "23:59"))]}
    assert opinion.compare(seed, [adoration("Tuesday", "23:00", "00:00")],
                           "2026-10-25")["differences"] == []
