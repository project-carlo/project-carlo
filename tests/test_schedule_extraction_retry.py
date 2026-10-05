from types import SimpleNamespace

import httpx
import pytest
from google.genai import errors, types

import pdf_extract.schedule_extraction as schedule_extraction
from pdf_extract.schedule_extraction import (
    GEMINI_HTTP_TIMEOUT_MS,
    _generate_content_with_backoff,
    gemini_client,
)


def _patch_backoff_clock(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Fake monotonic clock so gate waits exit in one sleep, not a spin loop."""
    clock = [1000.0]
    sleep_delays: list[float] = []

    def _fake_monotonic() -> float:
        return clock[0]

    def _fake_sleep(delay: float) -> None:
        sleep_delays.append(delay)
        clock[0] += delay

    schedule_extraction._pause_until = 0.0
    monkeypatch.setattr(schedule_extraction.time, "monotonic", _fake_monotonic)
    monkeypatch.setattr(schedule_extraction.time, "sleep", _fake_sleep)
    return sleep_delays


def test_generate_content_with_backoff_retries_on_503(monkeypatch) -> None:
    attempts = 0
    sleep_delays = _patch_backoff_clock(monkeypatch)
    monkeypatch.setattr(schedule_extraction.random, "uniform", lambda _a, _b: 0.0)

    def _generate_content(**kwargs):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise errors.ServerError(503, {"error": {"status": "UNAVAILABLE"}})
        return SimpleNamespace(text="{}")

    client = SimpleNamespace(models=SimpleNamespace(generate_content=_generate_content))
    response = _generate_content_with_backoff(
        client,
        model="gemini-3-flash-preview",
        contents=["prompt"],
        config=SimpleNamespace(),
    )

    assert response.text == "{}"
    assert attempts == 3
    assert sleep_delays == [2.0, 4.0]


def test_generate_content_with_backoff_does_not_retry_non_retryable(monkeypatch) -> None:
    sleep_delays = _patch_backoff_clock(monkeypatch)

    def _generate_content(**kwargs):
        raise errors.ClientError(400, {"error": {"status": "INVALID_ARGUMENT"}})

    client = SimpleNamespace(models=SimpleNamespace(generate_content=_generate_content))
    with pytest.raises(errors.ClientError):
        _generate_content_with_backoff(
            client,
            model="gemini-3-flash-preview",
            contents=["prompt"],
            config=SimpleNamespace(),
        )

    assert sleep_delays == []


def test_generate_content_with_backoff_retries_connection_reset(monkeypatch) -> None:
    attempts = 0
    sleep_delays = _patch_backoff_clock(monkeypatch)
    monkeypatch.setattr(schedule_extraction.random, "uniform", lambda _a, _b: 0.0)

    def _generate_content(**kwargs):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise httpx.ReadError("[Errno 104] Connection reset by peer")
        return SimpleNamespace(text="{}")

    client = SimpleNamespace(models=SimpleNamespace(generate_content=_generate_content))
    response = _generate_content_with_backoff(
        client,
        model="gemini-3-flash-preview",
        contents=["prompt"],
        config=SimpleNamespace(),
    )

    assert response.text == "{}"
    assert attempts == 3
    assert sleep_delays == [2.0, 4.0]


def test_gemini_client_sets_request_timeout(monkeypatch) -> None:
    captured: dict = {}

    def _client(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace()

    monkeypatch.setattr(schedule_extraction.genai, "Client", _client)
    gemini_client()

    http_options = captured["http_options"]
    assert isinstance(http_options, types.HttpOptions)
    assert http_options.timeout == GEMINI_HTTP_TIMEOUT_MS
