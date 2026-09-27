import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from "react";
import {
  GlobalWorkerOptions,
  TextLayer,
  getDocument,
  type PDFDocumentProxy,
  type RenderTask,
} from "pdfjs-dist";
import workerUrl from "pdfjs-dist/build/pdf.worker.min.mjs?url";
import { markKeywords } from "../lib/keywords";

GlobalWorkerOptions.workerSrc = workerUrl;

export interface ScrollRequest {
  page: number;
  nonce: number;
}

interface Props {
  url: string;
  scrollTo: ScrollRequest | null;
  onPageChange: (page: number) => void;
}

const ZOOM_STEP = 1.2;

function pdfLoadError(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  if (/\b404\b/.test(message)) return "This bulletin PDF is not in storage.";
  return `Could not load the PDF: ${message}`;
}

export function PdfViewer({ url, scrollTo, onPageChange }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [doc, setDoc] = useState<PDFDocumentProxy | null>(null);
  const [sizes, setSizes] = useState<{ width: number; height: number }[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [zoom, setZoom] = useState<number | "fit">("fit");
  const [viewWidth, setViewWidth] = useState(0);
  const [highlight, setHighlight] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    let cancelled = false;
    const task = getDocument({ url });
    setDoc(null);
    setSizes([]);
    setError(null);
    task.promise
      .then(async (loaded) => {
        const dims = [];
        for (let i = 1; i <= loaded.numPages; i++) {
          const p = await loaded.getPage(i);
          const vp = p.getViewport({ scale: 1 });
          dims.push({ width: vp.width, height: vp.height });
        }
        if (!cancelled) {
          setSizes(dims);
          setDoc(loaded);
        }
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(pdfLoadError(e));
      });
    return () => {
      cancelled = true;
      void task.destroy();
    };
  }, [url]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const observer = new ResizeObserver(() => setViewWidth(el.clientWidth));
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const widest = Math.max(1, ...sizes.map((s) => s.width));
  const fitScale = viewWidth > 0 ? Math.max(0.2, (viewWidth - 32) / widest) : 1;
  const scale = zoom === "fit" ? fitScale : zoom;

  const updatePage = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const mark = el.scrollTop + el.clientHeight * 0.3;
    let current = 1;
    for (const child of el.querySelectorAll<HTMLElement>("[data-page]")) {
      if (child.offsetTop <= mark) current = Number(child.dataset.page);
    }
    setPage((prev) => (prev === current ? prev : current));
  }, []);

  useEffect(() => onPageChange(page), [page, onPageChange]);
  useEffect(updatePage, [scale, sizes, updatePage]);

  const goTo = useCallback((target: number, smooth = true) => {
    const el = scrollRef.current;
    const pageEl = el?.querySelector<HTMLElement>(`[data-page="${target}"]`);
    if (el && pageEl) el.scrollTo({ top: pageEl.offsetTop - 8, behavior: smooth ? "smooth" : "auto" });
  }, []);

  useEffect(() => {
    if (scrollTo && sizes.length) goTo(Math.min(Math.max(1, scrollTo.page), sizes.length));
  }, [scrollTo, sizes.length, goTo]);

  // Zooming keeps the same part of the document in view.
  const anchor = useRef<number | null>(null);
  const changeZoom = (next: number | "fit") => {
    const el = scrollRef.current;
    if (el) anchor.current = el.scrollTop / Math.max(1, el.scrollHeight);
    setZoom(next);
  };
  useLayoutEffect(() => {
    const el = scrollRef.current;
    if (el && anchor.current !== null) el.scrollTop = anchor.current * el.scrollHeight;
    anchor.current = null;
  }, [scale]);

  const zoomBy = (factor: number) =>
    changeZoom(Math.min(5, Math.max(0.25, Math.round(scale * factor * 100) / 100)));

  return (
    <div className="flex h-full flex-col bg-slate-600">
      <div className="flex items-center gap-2 border-b border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-100">
        <button className="toolbar-btn" onClick={() => goTo(page - 1)} disabled={page <= 1} title="Previous page">
          ‹
        </button>
        <span className="tabular-nums" data-testid="page-indicator">
          Page {page} / {sizes.length || "…"}
        </span>
        <button className="toolbar-btn" onClick={() => goTo(page + 1)} disabled={page >= sizes.length} title="Next page">
          ›
        </button>
        <span className="mx-2 h-4 w-px bg-slate-600" />
        <button className="toolbar-btn" onClick={() => zoomBy(1 / ZOOM_STEP)} title="Zoom out">
          −
        </button>
        <span className="w-12 text-center tabular-nums">{Math.round(scale * 100)}%</span>
        <button className="toolbar-btn" onClick={() => zoomBy(ZOOM_STEP)} title="Zoom in">
          +
        </button>
        <button
          className={`toolbar-btn ${zoom === "fit" ? "bg-slate-600" : ""}`}
          onClick={() => changeZoom("fit")}
          title="Fit width"
        >
          Fit
        </button>
        <span className="mx-2 h-4 w-px bg-slate-600" />
        <label className="flex cursor-pointer items-center gap-1.5 select-none" title="Highlight Mass, Confession, Reconciliation, Adoration, Holy Hour and cancellations">
          <input type="checkbox" checked={highlight} onChange={(e) => setHighlight(e.target.checked)} />
          Highlight keywords
        </label>
        <a className="ml-auto text-slate-300 underline hover:text-white" href={url} target="_blank" rel="noreferrer">
          Open PDF
        </a>
      </div>
      <div
        ref={scrollRef}
        onScroll={updatePage}
        className={`relative flex-1 overflow-auto p-4 ${highlight ? "highlight-on" : ""}`}
        data-testid="pdf-scroll"
      >
        {error && (
          <div className="rounded bg-white p-4 text-slate-800">{error}</div>
        )}
        {!error && !doc && <div className="p-4 text-slate-200">Loading PDF…</div>}
        {doc &&
          sizes.map((size, i) => (
            <PdfPage
              key={i}
              doc={doc}
              index={i + 1}
              scale={scale}
              width={size.width * scale}
              height={size.height * scale}
              root={scrollRef}
            />
          ))}
      </div>
    </div>
  );
}

interface PageProps {
  doc: PDFDocumentProxy;
  index: number;
  scale: number;
  width: number;
  height: number;
  root: React.RefObject<HTMLDivElement | null>;
}

function PdfPage({ doc, index, scale, width, height, root }: PageProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { root: root.current, rootMargin: "100% 0px" },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [root]);

  useEffect(() => {
    if (!visible) return;
    let cancelled = false;
    let renderTask: RenderTask | null = null;
    let textLayer: TextLayer | null = null;
    (async () => {
      const pdfPage = await doc.getPage(index);
      const viewport = pdfPage.getViewport({ scale });
      const ratio = window.devicePixelRatio || 1;
      const canvas = document.createElement("canvas");
      canvas.width = Math.floor(viewport.width * ratio);
      canvas.height = Math.floor(viewport.height * ratio);
      canvas.style.width = `${viewport.width}px`;
      canvas.style.height = `${viewport.height}px`;
      canvas.className = "absolute inset-0";
      renderTask = pdfPage.render({
        canvas,
        viewport,
        transform: ratio !== 1 ? [ratio, 0, 0, ratio, 0, 0] : undefined,
      });
      await renderTask.promise;
      if (cancelled) return;
      const textDiv = document.createElement("div");
      textDiv.className = "textLayer";
      textLayer = new TextLayer({
        textContentSource: pdfPage.streamTextContent(),
        container: textDiv,
        viewport,
      });
      await textLayer.render();
      if (cancelled) return;
      markKeywords(textDiv);
      ref.current?.replaceChildren(canvas, textDiv);
    })().catch((e: unknown) => {
      if (!cancelled && !(e instanceof Error && e.name === "RenderingCancelledException")) {
        console.error(`Rendering page ${index} failed`, e);
      }
    });
    return () => {
      cancelled = true;
      renderTask?.cancel();
      textLayer?.cancel();
    };
  }, [visible, scale, doc, index]);

  const style = { width, height, "--total-scale-factor": scale } as CSSProperties;
  return (
    <div
      ref={ref}
      data-page={index}
      className="pdf-page relative mx-auto mb-4 bg-white shadow-lg"
      style={style}
    />
  );
}
