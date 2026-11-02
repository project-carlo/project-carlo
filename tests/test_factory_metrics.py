"""The factory's measurement: quota attribution from readings, tokens from results and
transcripts, and the reports on them (docs/factory-quota.md). Readings taken by a running
dispatcher are tested with it, in test_factory.py."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from pdf_extract.factory.config import FactoryError
from pdf_extract.factory.ledger import Ledger
from pdf_extract.factory.metrics import report
from pdf_extract.factory.metrics.attempt_meta import work_units
from pdf_extract.factory.metrics.quota import (
    IMMEDIATE,
    INCONSISTENT,
    MISSING,
    RESET,
    SETTLED,
    SHARED,
    Analysis,
    Reading,
    Span,
    combine,
)
from pdf_extract.factory.metrics.tokens import from_result, parse_transcript

T0 = datetime(2026, 11, 2, 12, tzinfo=UTC)
FIVE_RESETS = T0 + timedelta(hours=4)
WEEK_RESETS = T0 + timedelta(days=3)
SETTLE = timedelta(seconds=150)


def reading(rid: int, minutes: float, five: float, week: float = 20, *,
            five_resets: datetime = FIVE_RESETS, account: str = "a") -> Reading:
    return Reading(rid, account, T0 + timedelta(minutes=minutes),
                   {"five_hour": five, "seven_day": week},
                   {"five_hour": five_resets, "seven_day": WEEK_RESETS})


def span(sid: int, start: float, end: float | None, account: str = "a") -> Span:
    return Span(sid, sid, account, T0 + timedelta(minutes=start),
                None if end is None else T0 + timedelta(minutes=end))


def test_back_to_back_attempts_share_their_measurement() -> None:
    # B starts 5 s after A ends, and the meter rises during B: no exact share for either.
    spans = [span(1, 0, 10), span(2, 10.1, 20)]
    reads = [reading(1, -0.01, 10), reading(2, 10.05, 12), reading(3, 24, 21)]
    an = Analysis(spans, reads, SETTLE)
    a, b = an.measure(spans[0], "five_hour"), an.measure(spans[1], "five_hour")
    assert a.label == b.label == SHARED and a.group == b.group == [1, 2]
    assert (a.group_low, a.group_high) == (10, 12)  # 21 - 10 ± 1, settled
    assert a.low == 1 and a.high == 12  # A's early reading: at least 12 - 10 - 1
    assert b.low == 0 and b.high == 12
    # One job running both: the group's upper bound counts once, not once per attempt.
    job = combine([a, b])
    assert (job["label"], job["low"], job["high"]) == (SHARED, 1, 12)
    totals = {(w["window"]): w for w in an.window_totals()}
    assert totals["five_hour"]["shared"] == 11 and totals["five_hour"]["unexplained"] == 10


def test_an_idle_gap_gives_a_settled_range_and_zero_is_below_one() -> None:
    spans = [span(1, 0, 10)]
    an = Analysis(spans, [reading(1, 0, 10, 20), reading(2, 13, 15, 20)], SETTLE)
    five, week = an.measure(spans[0], "five_hour"), an.measure(spans[0], "seven_day")
    assert (five.label, five.low, five.high) == (SETTLED, 4, 6)
    assert (week.label, week.low, week.high) == (SETTLED, 0, 1) and week.as_dict()["text"] == "<1"
    # Read sooner than the meter settles: a minimum only.
    early = Analysis(spans, [reading(1, 0, 10), reading(2, 10.5, 15)], SETTLE)
    m = early.measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (IMMEDIATE, 4, None)
    assert combine([m])["text"] == "≥4"


def test_a_reset_during_a_job_is_a_minimum_and_jitter_is_not_a_reset() -> None:
    spans = [span(1, 0, 10)]
    before = reading(1, 0, 70, five_resets=T0 + timedelta(minutes=5))
    after = reading(2, 13, 4, five_resets=T0 + timedelta(hours=5, minutes=5))
    m = Analysis(spans, [before, after], SETTLE).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (RESET, 3, None)
    jitter = reading(2, 13, 72, five_resets=FIVE_RESETS + timedelta(seconds=0.6))
    m = Analysis(spans, [reading(1, 0, 70), jitter], SETTLE).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (SETTLED, 1, 3)


def test_missing_or_inconsistent_readings_give_no_number() -> None:
    spans = [span(1, 0, 10)]
    for reads in ([reading(2, 13, 15)], [reading(1, 0, 10)]):
        m = Analysis(spans, reads, SETTLE).measure(spans[0], "five_hour")
        assert m.label == MISSING and m.low is None and m.high is None
    fell = Analysis(spans, [reading(1, 0, 10), reading(2, 13, 8)], SETTLE)
    m = fell.measure(spans[0], "five_hour")
    assert m.label == INCONSISTENT and m.low is None
    assert combine([m])["low"] is None


def test_a_meter_rising_while_idle_flags_nearby_attempts() -> None:
    spans = [span(1, 0, 10)]
    reads = [reading(1, -60, 5), reading(2, -30, 9), reading(3, 0, 9), reading(4, 13, 12)]
    an = Analysis(spans, reads, SETTLE)
    assert an.measure(spans[0], "five_hour").outside_use
    assert an.rises[0]["points"] == 4
    quiet = Analysis(spans, [reading(1, -60, 9), reading(3, 0, 9), reading(4, 13, 12)], SETTLE)
    assert not quiet.measure(spans[0], "five_hour").outside_use


def test_historical_readings_are_a_minimum_at_best() -> None:
    spans = [span(1, 0, 10)]
    reads = [reading(1, 0, 10), reading(2, 13, 15)]
    m = Analysis(spans, reads, SETTLE, approximate={1}).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high, m.approximate) == (IMMEDIATE, 4, None, True)


def assistant(mid: str, at: str, model: str = "claude-opus-5-5", out: int = 100,
              thinking: int = 40, five: int = 0, hour: int = 50) -> str:
    return json.dumps({"type": "assistant", "timestamp": at, "version": "2.1.310",
                       "entrypoint": "sdk-py", "sessionId": "s1", "message": {
                           "id": mid, "model": model, "usage": {
                               "input_tokens": 3, "output_tokens": out,
                               "output_tokens_details": {"thinking_tokens": thinking},
                               "cache_read_input_tokens": 1000,
                               "cache_creation_input_tokens": five + hour,
                               "cache_creation": {"ephemeral_5m_input_tokens": five,
                                                  "ephemeral_1h_input_tokens": hour}}}})


def cost_state(start: datetime) -> str:
    return json.dumps({"type": "cost-state", "startTime": start.timestamp() * 1000,
                       "modelUsage": {"claude-haiku-5-5": {
                           "inputTokens": 2000, "outputTokens": 20, "thinkingTokens": 0,
                           "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0}}})


TRANSCRIPT = [
    # Attempt 1 (12:00): m1 recorded three times, m2 once, and its cost-state.
    assistant("m1", "2026-11-02T12:00:05Z"), assistant("m1", "2026-11-02T12:00:05Z"),
    assistant("m1", "2026-11-02T12:00:06Z"), assistant("m2", "2026-11-02T12:01:00Z", five=7),
    cost_state(T0), "not json",
    # Attempt 2 (13:00), resuming the session in the same file.
    assistant("m3", "2026-11-02T13:00:05Z", out=10, thinking=0, hour=0),
    assistant("m3", "2026-11-02T13:00:05Z", out=10, thinking=0, hour=0),
]


def test_transcript_tokens_count_each_message_once() -> None:
    first = parse_transcript(TRANSCRIPT, since=T0)
    assert first.messages == 3 and first.duplicates == 3  # m1, m2, m3
    one = parse_transcript(TRANSCRIPT[:6], since=T0)
    assert (one.messages, one.duplicates) == (2, 2)
    assert one.output == 200 + 20 and one.thinking == 80  # thinking not added to output
    assert (one.cache_write_5m, one.cache_write_1h) == (7, 100)
    assert one.per_model["claude-haiku-5-5"]["input"] == 2000  # the side call
    assert one.input == 6 + 2000 and one.model == "claude-opus-5-5"
    assert one.cli_version == "2.1.310" and one.entrypoint == "sdk-py"
    # A resumed session appends to the same file: each attempt counts only its own time.
    later = parse_transcript(TRANSCRIPT, since=T0 + timedelta(hours=1))
    assert (later.messages, later.output, later.cache_write_1h) == (1, 10, 0)
    assert "claude-haiku-5-5" not in later.per_model  # attempt 1's cost-state
    earlier = parse_transcript(TRANSCRIPT, since=T0, until=T0 + timedelta(minutes=10))
    assert (earlier.messages, earlier.output) == (2, 220)  # m1, m2 only
    assert "claude-haiku-5-5" in earlier.per_model


def test_result_tokens_keep_the_cache_ttl_and_side_models() -> None:
    t = from_result(
        {"input_tokens": 5, "output_tokens": 90, "cache_creation_input_tokens": 30,
         "cache_creation": {"ephemeral_5m_input_tokens": 10, "ephemeral_1h_input_tokens": 20},
         "output_tokens_details": {"thinking_tokens": 40}},
        {"claude-opus-5-5": {"inputTokens": 5, "outputTokens": 90,
                             "cacheCreationInputTokens": 30, "cacheReadInputTokens": 9},
         "claude-haiku-5-5": {"inputTokens": 100, "outputTokens": 2}})
    assert (t.output, t.thinking, t.cache_write_5m, t.cache_write_1h) == (92, 40, 10, 20)
    assert t.input == 105 and t.model == "claude-opus-5-5" and not t.gaps


def test_an_unknown_time_zone_is_a_clear_error(tmp_path: Path) -> None:
    with pytest.raises(FactoryError, match="unknown time zone 'US/Eastrn'"):
        report.quota(Ledger(tmp_path / "l.db"), by="hour", tz="US/Eastrn")


def test_work_units_count_what_a_job_completes() -> None:
    batches = [{"id": "b1", "entries": ["r1", "r2"]}]
    assert work_units("map", {"batch": "b1"}, batches) == 2
    assert work_units("map", {"batch": "b9"}, batches) is None
    assert work_units("seed-review", {"parishes": ["a", "b", "c"]}) == 3
    assert work_units("seed", {"parish": "a"}) == 1
    assert work_units("survey", {}) == 1
