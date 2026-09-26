FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
# Keep the venv off /workspace so a bind mount of the repo does not hide it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_LINK_MODE=copy

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates xvfb xauth ghostscript \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Lockfiles only. The weekly pipeline is Python: Playwright Chromium, xvfb, and
# Ghostscript. Node is not installed. README stays out of this layer so a doc
# edit does not reinstall Chromium (`uv sync --no-install-project` does not need it).
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project
# --no-sync: the project is not installed yet, and a plain `uv run` would
# also pull the dev group into this image.
RUN uv run --no-dev --no-sync playwright install --with-deps chromium

COPY . .

RUN uv sync --frozen --no-dev

CMD ["bash", "docker/weekly-run.sh"]
