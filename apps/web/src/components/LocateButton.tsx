import { CrosshairIcon } from "@/components/icons";

export type LocateStatus = "idle" | "requesting" | "error";

interface LocateButtonProps {
  status: LocateStatus;
  /** Why the last request failed, shown beside the button. */
  error: string | null;
  onLocate: () => void;
}

/**
 * The map's "go to my exact location" control, in the corner where maps keep
 * it. It asks the browser for the visitor's position, which is far closer
 * than the IP estimate the map may have started from.
 */
export function LocateButton({ status, error, onLocate }: LocateButtonProps) {
  const requesting = status === "requesting";
  return (
    <div className="flex items-center justify-end gap-2">
      {status === "error" && error ? (
        <p
          role="status"
          className="max-w-[16rem] border border-rule-strong bg-paper/96 px-3 py-1.5 font-serif text-sm text-ink-soft shadow-missal-loading"
        >
          {error}
        </p>
      ) : null}
      <button
        type="button"
        onClick={onLocate}
        disabled={requesting}
        aria-label={
          requesting ? "Finding your location…" : "Go to my exact location"
        }
        title="Go to my exact location"
        className="missal-focus flex size-11 shrink-0 items-center justify-center border border-rule-strong bg-paper/96 text-ink-soft shadow-missal-floating backdrop-blur-sm transition-colors hover:text-rubric disabled:cursor-wait"
      >
        <CrosshairIcon
          className={`size-5 ${requesting ? "animate-pulse text-rubric" : ""}`}
          aria-hidden
        />
      </button>
    </div>
  );
}
