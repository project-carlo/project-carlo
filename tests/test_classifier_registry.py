import pytest

from pdf_extract.classifiers import (
    REGISTRY,
    Classifier,
    available_classifiers,
    get_classifier,
)


def test_gemini_is_registered():
    assert "gemini-flash" in REGISTRY
    assert "gemini-flash" in available_classifiers()


def test_get_classifier_returns_classifier_instance():
    c = get_classifier("gemini-flash")
    assert isinstance(c, Classifier)
    assert c.name == "gemini-flash"
    assert c.version  # non-empty


def test_get_classifier_unknown_lists_options():
    with pytest.raises(KeyError) as exc:
        get_classifier("does-not-exist")
    assert "gemini-flash" in str(exc.value)


def test_gemini_version_changes_with_the_prompt(monkeypatch) -> None:
    """Cached extractions are keyed by version, so a prompt edit must change it."""
    import importlib

    from pdf_extract import schedule_extraction
    from pdf_extract.classifiers import gemini

    before = gemini.GeminiClassifier(model="m").version
    assert before.startswith("m+prompt-")

    monkeypatch.setattr(
        schedule_extraction, "EVENTS_SYSTEM_PROMPT", schedule_extraction.EVENTS_SYSTEM_PROMPT + "!",
    )
    try:
        assert importlib.reload(gemini).GeminiClassifier(model="m").version != before
    finally:
        monkeypatch.undo()
        importlib.reload(gemini)
