"""Registry of bulletin → events classifiers.

Add a new classifier by registering a zero-arg factory here. The runner and CLI
discover classifiers by name from REGISTRY.
"""

from __future__ import annotations

from collections.abc import Callable

from pdf_extract.classifiers.base import Classifier
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.openai_gpt import OpenAIClassifier
from pdf_extract.classifiers.openai_responses import OpenAIResponsesClassifier

REGISTRY: dict[str, Callable[[], Classifier]] = {
    "gemini-flash": lambda: GeminiClassifier(),
    "gpt-5.4-mini": lambda: OpenAIClassifier(model="gpt-5.4-mini"),
    # Qualified schema (weeks of the month, seasons), for scoring against labels.
    "gpt-6-luna": lambda: OpenAIResponsesClassifier(model="gpt-6-luna"),
    "gpt-6-luna-nonstrict": lambda: OpenAIResponsesClassifier(
        model="gpt-6-luna", name="gpt-6-luna-nonstrict", strict=False,
    ),
}


def get_classifier(name: str) -> Classifier:
    if name not in REGISTRY:
        available = ", ".join(sorted(REGISTRY)) or "(none)"
        raise KeyError(f"Unknown classifier {name!r}. Available: {available}")
    return REGISTRY[name]()


def available_classifiers() -> list[str]:
    return sorted(REGISTRY)


__all__ = ["Classifier", "REGISTRY", "available_classifiers", "get_classifier"]
