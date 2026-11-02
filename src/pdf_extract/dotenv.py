"""`.env`: KEY=VALUE lines with the keys a command needs (R2_*, GEMINI_API_KEY...)."""

from __future__ import annotations

from pathlib import Path


def read_dotenv(path: Path = Path(".env")) -> dict[str, str]:
    """The file's entries; none when it doesn't exist. `export ` and quotes are dropped."""
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values.setdefault(key, value)
    return values
