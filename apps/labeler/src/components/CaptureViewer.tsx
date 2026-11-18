import { useEffect, useState } from "react";
import { captureUrl } from "../api";
import type { SeedCapture } from "../types";

interface Props {
  parish: string;
  capture: SeedCapture;
}

/**
 * A source seed's capture: the page as it looked (its screenshot), or the text
 * its quotes are checked against. Where a bulletin seed shows a PDF.
 */
export function CaptureViewer({ parish, capture }: Props) {
  const [view, setView] = useState<"screenshot" | "text">(
    capture.screenshot_hash ? "screenshot" : "text",
  );
  const [text, setText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [imageMissing, setImageMissing] = useState(false);

  useEffect(() => {
    if (view !== "text" || text !== null) return;
    let cancelled = false;
    fetch(captureUrl(parish, capture.content_hash, "text"))
      .then((r) => (r.ok ? r.text() : Promise.reject(new Error(`${r.status} ${r.statusText}`))))
      .then((t) => !cancelled && setText(t))
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => {
      cancelled = true;
    };
  }, [view, text, parish, capture.content_hash]);

  return (
    <div className="flex h-full min-h-0 flex-col bg-slate-800">
      <div className="flex shrink-0 items-center gap-2 px-2 py-1 text-xs text-slate-300">
        <button
          className={view === "screenshot" ? "font-semibold text-white" : "hover:text-white"}
          disabled={!capture.screenshot_hash}
          onClick={() => setView("screenshot")}
        >
          Screenshot
        </button>
        <button
          className={view === "text" ? "font-semibold text-white" : "hover:text-white"}
          onClick={() => setView("text")}
        >
          Text
        </button>
        <a
          href={capture.url}
          target="_blank"
          rel="noreferrer"
          className="ml-auto truncate text-sky-300 hover:underline"
          title="The live page, which may have changed since"
        >
          {capture.url}
        </a>
        <span className="whitespace-nowrap text-slate-400">captured {capture.captured_at.slice(0, 16).replace("T", " ")}</span>
      </div>
      <div className="min-h-0 flex-1 overflow-auto" data-testid="capture-viewer">
        {view === "screenshot" && capture.screenshot_hash && imageMissing ? (
          <p className="p-4 text-sm text-slate-300">
            The screenshot isn't here: it is committed only when a quote was read from it,
            and otherwise reaches R2 only from a machine that writes there. The text is
            committed.
          </p>
        ) : view === "screenshot" && capture.screenshot_hash ? (
          <img
            onError={() => setImageMissing(true)}
            key={capture.screenshot_hash}
            src={captureUrl(parish, capture.content_hash, "image", capture.screenshot_hash)}
            alt={`Screenshot of ${capture.url}`}
            className="w-full"
          />
        ) : error ? (
          <p className="p-4 text-sm text-red-300">Couldn't load the text: {error}</p>
        ) : (
          <pre className="whitespace-pre-wrap p-4 font-sans text-sm text-slate-100">{text ?? "Loading…"}</pre>
        )}
      </div>
    </div>
  );
}
