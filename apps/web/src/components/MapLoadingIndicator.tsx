/** The serif stack's system fallbacks (see --font-serif in app.css). */
const SYSTEM_SERIF = '"Iowan Old Style", Georgia, serif';

/**
 * "Loading map…", centred over where the map will be. index.html carries a
 * static copy, shown before any script has run; keep the two in step so the
 * page doesn't shift when React takes over.
 *
 * `systemFont` is for the first load, before the map's code has arrived: the
 * text then skips the web font, which would otherwise download ahead of that
 * code and hold the map back.
 */
export function MapLoadingIndicator({
  systemFont = false,
}: {
  systemFont?: boolean;
}) {
  return (
    <div className="pointer-events-none absolute inset-0 z-[800] flex items-center justify-center">
      <div className="pointer-events-auto flex items-center gap-3 border border-rule-strong bg-paper/95 px-5 py-3 shadow-missal-loading">
        <span
          className="h-2 w-2 animate-pulse rounded-full bg-rubric"
          aria-hidden
        />
        <span
          className={
            systemFont
              ? "text-sm text-ink-soft"
              : "font-serif text-sm text-ink-soft"
          }
          style={systemFont ? { fontFamily: SYSTEM_SERIF } : undefined}
        >
          Loading map…
        </span>
      </div>
    </div>
  );
}
