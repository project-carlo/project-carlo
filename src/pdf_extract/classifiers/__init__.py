"""Registry of bulletin → events classifiers.

Add a new classifier by registering a zero-arg factory here. The runner and CLI
discover classifiers by name from REGISTRY.
"""

from __future__ import annotations

from collections.abc import Callable

from pdf_extract.classifiers.base import Classifier
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.openai_gpt import (
    FileDetail,
    ImageDetail,
    OpenAIClassifier,
    PdfInput,
)
from pdf_extract.classifiers.text_llm import (
    DEFAULT_REASONING_EFFORT,
    DEFAULT_TEXT_MODEL,
    TextLLMClassifier,
)

# ── Benchmark stacks (see `pnpm bench`) ─────────────────────────────────────
# Stack -> text extractor that feeds the model; None: the model reads the PDF
# itself, the control, sent at each `detail`, schema mode and input under test.
STACKS: dict[str, str | None] = {
    "pymupdf": "pymupdf-layout",
    "docling": "docling",
    "ocr": "ocr-layout",
    "pdf": None,
}
PDF_DETAILS: tuple[FileDetail, ...] = ("low", "high")
# How the pdf stack sends the bulletin: the PDF file, or one image per page.
# Page images also take `original` detail (full resolution).
PDF_INPUTS: tuple[PdfInput, ...] = ("file", "images")
IMAGE_DETAILS: tuple[ImageDetail, ...] = ("low", "high", "original")
# How the pdf stack asks for JSON: Gemini's exact schema (non-strict), or the
# OpenAI SDK's strict rewrite of it with strict decoding. The text stacks
# always use the SDK's strict `text_format`.
SCHEMA_MODES = ("exact", "strict")
# Short names for run directories; other models go by their model id.
MODEL_PREFIXES = {"gpt-6-luna": "luna", "gpt-5.6-luna": "luna5.6"}
BENCH_MODELS = tuple(MODEL_PREFIXES)


def details_for(pdf_input: PdfInput) -> tuple[ImageDetail, ...]:
    """The `detail` levels an input takes."""
    return IMAGE_DETAILS if pdf_input == "images" else PDF_DETAILS


def stack_name(
    stack: str,
    *,
    model: str = DEFAULT_TEXT_MODEL,
    detail: ImageDetail = "low",
    schema: str = "exact",
    effort: str | None = DEFAULT_REASONING_EFFORT,
    pdf_input: PdfInput = "file",
) -> str:
    """The run name (data/runs/<name>/) of one stack configuration."""
    name = f"{MODEL_PREFIXES.get(model, model)}-{stack}"
    if STACKS[stack] is None:
        if pdf_input == "images":
            name += "-images"
        name += f"-{detail}"
        if schema == "strict":
            name += "-strict"
    if effort != DEFAULT_REASONING_EFFORT:
        name += f"-{effort or 'default'}"
    return name


def stack_classifier(
    stack: str,
    *,
    model: str = DEFAULT_TEXT_MODEL,
    detail: ImageDetail = "low",
    schema: str = "exact",
    effort: str | None = DEFAULT_REASONING_EFFORT,
    pdf_input: PdfInput = "file",
) -> Classifier:
    """The classifier for one stack configuration, named by `stack_name`."""
    if schema not in SCHEMA_MODES:
        raise ValueError(f"Unknown schema mode {schema!r}. Available: {', '.join(SCHEMA_MODES)}")
    name = stack_name(
        stack, model=model, detail=detail, schema=schema, effort=effort, pdf_input=pdf_input,
    )
    extractor = STACKS[stack]
    if extractor is None:
        return OpenAIClassifier(
            model=model, name=name, reasoning_effort=effort, file_detail=detail,
            strict=schema == "strict", pdf_input=pdf_input,
        )
    return TextLLMClassifier(extractor=extractor, name=name, model=model, reasoning_effort=effort)


def _stack_factory(
    stack: str, model: str, detail: ImageDetail, schema: str, pdf_input: PdfInput,
) -> Callable[[], Classifier]:
    return lambda: stack_classifier(
        stack, model=model, detail=detail, schema=schema, pdf_input=pdf_input,
    )


REGISTRY: dict[str, Callable[[], Classifier]] = {
    "gemini-flash": lambda: GeminiClassifier(),
    "gpt-5.4-mini": lambda: OpenAIClassifier(model="gpt-5.4-mini"),
    # Every benchmark stack at the default effort, for `pnpm extract --classifier`.
    **{
        stack_name(
            stack, model=model, detail=detail, schema=schema, pdf_input=pdf_input,
        ): _stack_factory(stack, model, detail, schema, pdf_input)
        for model in BENCH_MODELS
        for stack, extractor in STACKS.items()
        for pdf_input in (PDF_INPUTS if extractor is None else ("file",))
        for detail in (details_for(pdf_input) if extractor is None else ("low",))
        for schema in (SCHEMA_MODES if extractor is None else ("exact",))
    },
}


def get_classifier(name: str) -> Classifier:
    if name not in REGISTRY:
        available = ", ".join(sorted(REGISTRY)) or "(none)"
        raise KeyError(f"Unknown classifier {name!r}. Available: {available}")
    return REGISTRY[name]()


def available_classifiers() -> list[str]:
    return sorted(REGISTRY)


__all__ = [
    "BENCH_MODELS",
    "Classifier",
    "IMAGE_DETAILS",
    "PDF_DETAILS",
    "PDF_INPUTS",
    "REGISTRY",
    "SCHEMA_MODES",
    "STACKS",
    "available_classifiers",
    "details_for",
    "get_classifier",
    "stack_classifier",
    "stack_name",
]
