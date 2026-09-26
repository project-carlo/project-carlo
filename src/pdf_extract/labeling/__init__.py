"""Local ground-truth labeling of bulletins: `python -m pdf_extract label serve`.

A person reads a bulletin PDF beside Gemini's extraction and records what the
bulletin actually says in `data/labels/<parish>/<content_hash>.json`. See
`labels` for the file format, `bulletins` for the queue and Gemini sources,
`server` for the HTTP API and `demo` for the generated demo dataset. The UI is
the `apps/labeler` workspace package.
"""
