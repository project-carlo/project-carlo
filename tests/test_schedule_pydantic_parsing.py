import json
from types import SimpleNamespace

from pdf_extract.schedule_extraction import extract_events


def _mock_gemini_response(monkeypatch, text: str) -> None:
    def _generate_content_with_backoff(*args, **kwargs):
        return SimpleNamespace(text=text)

    monkeypatch.setattr(
        "pdf_extract.schedule_extraction._generate_content_with_backoff",
        _generate_content_with_backoff,
    )
    monkeypatch.setattr(
        "pdf_extract.schedule_extraction.genai.Client",
        lambda **_kwargs: SimpleNamespace(),
    )


def test_extract_events_falls_back_on_validation_error(monkeypatch) -> None:
    """One invalid slot should not drop valid slots when Pydantic validation fails."""
    payload = {
        "weekly_schedule": {
            "masses": [
                {"church_slug": "", "day_of_week": "Saturday", "start_time": "5:00 PM"},
                {"church_slug": "st-john", "day_of_week": "Sunday", "start_time": "10:00 AM"},
            ],
            "confessions": [],
            "adorations": [],
        },
        "single_events": {"masses": [], "confessions": [], "adorations": []},
        "cancellations": {"masses": [], "confessions": [], "adorations": []},
        "church_list_needs_review": False,
    }
    _mock_gemini_response(monkeypatch, json.dumps(payload))

    result = extract_events(b"%PDF", churches=[{"name": "St John", "address": "1 Main"}])

    assert len(result["events"]) == 1
    assert result["events"][0]["church_slug"] == "st-john"
