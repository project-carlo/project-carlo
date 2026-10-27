"""An attempt's tokens: from the SDK's ResultMessage, or from its session transcript.

Thinking tokens are a part of output tokens, never added to them again. Cache writes keep
their TTL (5 minutes or 1 hour). A transcript repeats an assistant message once per
content block, so messages are counted once by id; a resumed session appends to the same
file, so only the messages from the attempt's start (and not seen before) count.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

FIELDS = ("input", "output", "thinking", "cache_read", "cache_write_5m", "cache_write_1h",
          "web_search")


@dataclass
class Tokens:
    input: int = 0
    output: int = 0  # thinking included
    thinking: int = 0
    cache_read: int = 0
    cache_write_5m: int = 0
    cache_write_1h: int = 0
    web_search: int = 0
    # Per model: the fields above, plus `cache_write` (all TTLs) and `unsplit` (cache
    # writes reported without a TTL, e.g. a side model's).
    per_model: dict[str, dict[str, int]] = field(default_factory=dict)
    messages: int = 0
    duplicates: int = 0
    message_ids: set[str] = field(default_factory=set)
    cli_version: str | None = None
    entrypoint: str | None = None
    gaps: list[str] = field(default_factory=list)

    @property
    def model(self) -> str | None:
        """The main model: the one that wrote the most."""
        return max(self.per_model, key=lambda m: self.per_model[m].get("output", 0),
                   default=None)

    def add(self, model: str, counts: dict[str, int]) -> None:
        mine = self.per_model.setdefault(model, {})
        for k, v in counts.items():
            mine[k] = mine.get(k, 0) + v
            if k in FIELDS:
                setattr(self, k, getattr(self, k) + v)

    def columns(self) -> dict[str, Any]:
        """attempt_meta's token columns."""
        return {"input_tokens": self.input, "output_tokens": self.output,
                "thinking_tokens": self.thinking, "cache_read_tokens": self.cache_read,
                "cache_write_5m_tokens": self.cache_write_5m,
                "cache_write_1h_tokens": self.cache_write_1h,
                "web_search_requests": self.web_search, "per_model": self.per_model,
                "model": self.model, "models": sorted(self.per_model),
                "messages": self.messages, "duplicate_records": self.duplicates}

    def as_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("message_ids")
        return d


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def api_counts(usage: dict[str, Any]) -> dict[str, int]:
    """One API message's usage (snake_case, as in a transcript or the ResultMessage)."""
    details = usage.get("output_tokens_details") or {}
    cache = usage.get("cache_creation") or {}
    written = _int(usage.get("cache_creation_input_tokens"))
    five, hour = _int(cache.get("ephemeral_5m_input_tokens")), \
        _int(cache.get("ephemeral_1h_input_tokens"))
    return {"input": _int(usage.get("input_tokens")), "output": _int(usage.get("output_tokens")),
            "thinking": _int(details.get("thinking_tokens")),
            "cache_read": _int(usage.get("cache_read_input_tokens")),
            "cache_write_5m": five, "cache_write_1h": hour, "cache_write": written,
            "unsplit": max(0, written - five - hour),
            "web_search": _int((usage.get("server_tool_use") or {}).get("web_search_requests"))}


def model_counts(usage: dict[str, Any]) -> dict[str, int]:
    """A per-model total (camelCase, as in ResultMessage.model_usage or a cost-state record).
    Its cache writes come without a TTL."""
    written = _int(usage.get("cacheCreationInputTokens"))
    return {"input": _int(usage.get("inputTokens")), "output": _int(usage.get("outputTokens")),
            "thinking": _int(usage.get("thinkingTokens")),
            "cache_read": _int(usage.get("cacheReadInputTokens")), "cache_write": written,
            "unsplit": written, "web_search": _int(usage.get("webSearchRequests"))}


def _when(value: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_transcript(lines: Iterable[str], since: datetime | None = None,
                     seen: set[str] | None = None) -> Tokens:
    """The tokens of one attempt in a session transcript: assistant messages from `since`
    on, each counted once by id, skipping ids an earlier attempt already counted (`seen`).
    Side calls (a small model summarising) appear only in the session's cost-state record:
    a model there with no assistant message is added from it."""
    seen = seen or set()
    last: dict[str, dict[str, Any]] = {}
    records = 0
    cost_state: dict[str, Any] | None = None
    tokens = Tokens()
    for line in lines:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if not isinstance(r, dict):
            continue
        if r.get("type") == "cost-state":
            started = r.get("startTime")
            if since is None or (started and started / 1000 >= since.timestamp() - 60):
                cost_state = r
            continue
        if r.get("type") != "assistant" or not isinstance(r.get("message"), dict):
            continue
        at = _when(r.get("timestamp"))
        if since is not None and (at is None or at < since):
            continue
        message = r["message"]
        mid = message.get("id") or r.get("uuid")
        if not mid or mid in seen or not isinstance(message.get("usage"), dict):
            continue
        records += 1
        last[mid] = message  # repeats carry the same usage; the last is the final one
        tokens.cli_version = r.get("version") or tokens.cli_version
        tokens.entrypoint = r.get("entrypoint") or tokens.entrypoint
    for mid, message in last.items():
        tokens.add(str(message.get("model") or "unknown"), api_counts(message["usage"]))
    tokens.messages, tokens.duplicates = len(last), records - len(last)
    tokens.message_ids = set(last)
    if cost_state:
        for model, usage in (cost_state.get("modelUsage") or {}).items():
            if model not in tokens.per_model and isinstance(usage, dict):
                tokens.add(model, model_counts(usage))
    _note_unsplit(tokens)
    return tokens


def from_result(usage: dict[str, Any] | None, model_usage: dict[str, Any] | None,
                messages: int = 0, duplicates: int = 0) -> Tokens:
    """An attempt's tokens from its ResultMessage: per model from `model_usage`, the cache
    TTL split and thinking from `usage` (the main model's) when it has them."""
    tokens = Tokens(messages=messages, duplicates=duplicates)
    for model, mu in (model_usage or {}).items():
        if isinstance(mu, dict):
            tokens.add(model, model_counts(mu))
    if usage:
        counts = api_counts(usage)
        main = tokens.model
        if main is None:
            tokens.add("unknown", counts)
        else:
            # Move the main model's TTL split out of `unsplit`, and its thinking if the
            # per-model totals didn't carry it.
            mine = tokens.per_model[main]
            for k in ("cache_write_5m", "cache_write_1h"):
                mine[k] = counts[k]
                setattr(tokens, k, getattr(tokens, k) + counts[k])
            mine["unsplit"] = max(0, mine.get("unsplit", 0) - counts["cache_write_5m"]
                                  - counts["cache_write_1h"])
            if not mine.get("thinking") and counts["thinking"]:
                mine["thinking"] = counts["thinking"]
                tokens.thinking += counts["thinking"]
    _note_unsplit(tokens)
    return tokens


def _note_unsplit(tokens: Tokens) -> None:
    for model, counts in tokens.per_model.items():
        if counts.get("unsplit"):
            tokens.gaps.append(f"{counts['unsplit']} cache-write tokens of {model} without "
                               "a TTL (in per_model only)")
