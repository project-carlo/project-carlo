"""Registry of bulletin → events classifiers.

Add a new classifier by registering a factory here. The runner and CLI
discover classifiers by name from REGISTRY. A factory that takes keyword
options (reasoning effort, detail level, ...) lists their names in
CLASSIFIER_OPTIONS so `eval run` can offer them; every factory must work
called with none.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pdf_extract.classifiers.base import Classifier, ClassifierOptionError
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.openai_gpt import OpenAIClassifier
from pdf_extract.classifiers.openai_responses import OpenAIResponsesClassifier

REGISTRY: dict[str, Callable[..., Classifier]] = {
    "gemini-flash": lambda: GeminiClassifier(),
    "gpt-5.4-mini": lambda: OpenAIClassifier(model="gpt-5.4-mini"),
    # Qualified schema (weeks of the month, seasons), for scoring against labels.
    "gpt-6-luna": lambda **options: OpenAIResponsesClassifier(model="gpt-6-luna", **options),
    "gpt-6-luna-nonstrict": lambda **options: OpenAIResponsesClassifier(
        model="gpt-6-luna", name="gpt-6-luna-nonstrict", strict=False, **options,
    ),
}

_RESPONSES_OPTIONS = frozenset({"reasoning_effort", "file_detail", "pdf_as_images"})
CLASSIFIER_OPTIONS: dict[str, frozenset[str]] = {
    "gpt-6-luna": _RESPONSES_OPTIONS,
    "gpt-6-luna-nonstrict": _RESPONSES_OPTIONS,
}


def get_classifier(name: str, **options: Any) -> Classifier:
    """The named classifier, built with `options` (None values mean "the default")."""
    if name not in REGISTRY:
        available = ", ".join(sorted(REGISTRY)) or "(none)"
        raise KeyError(f"Unknown classifier {name!r}. Available: {available}")
    options = {k: v for k, v in options.items() if v is not None}
    unsupported = sorted(set(options) - CLASSIFIER_OPTIONS.get(name, frozenset()))
    if unsupported:
        raise ClassifierOptionError(
            f"Classifier {name!r} does not take {', '.join(unsupported)}",
        )
    return REGISTRY[name](**options)


def available_classifiers() -> list[str]:
    return sorted(REGISTRY)


__all__ = [
    "CLASSIFIER_OPTIONS",
    "Classifier",
    "ClassifierOptionError",
    "REGISTRY", "available_classifiers", "get_classifier"]
