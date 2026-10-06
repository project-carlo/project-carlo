import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

interface MastheadProps {
  /** Optional tagline rendered beneath the wordmark. */
  tagline?: string;
  /** Compact variant hides the tagline, for tight header strips. */
  compact?: boolean;
  /** Set level with the wordmark, at the far end of its row, so the tagline
   *  beneath keeps the full width (e.g. the home card's links). */
  aside?: ReactNode;
  className?: string;
}

/** Site title block — wordmark and optional tagline. The wordmark links
 *  back to the map at `/`. */
export function Masthead({
  tagline = "Mass, Confession & Adoration times near you",
  compact = false,
  aside,
  className = "",
}: MastheadProps) {
  if (compact) {
    return (
      <div className={cn("flex items-baseline gap-4", className)}>
        <Link
          to="/"
          aria-label="Project Carlo — home"
          className="font-display text-lg leading-none font-normal tracking-tight text-ink"
        >
          Project <span className="italic text-rubric">Carlo</span>
        </Link>
      </div>
    );
  }

  // The tagline is the <h1>: it carries the intent keywords ("Mass,
  // Confession & Adoration times near you") that the branded wordmark lacks.
  // Visually unchanged — only the heading semantics are swapped.
  return (
    <header className={cn("space-y-2", className)}>
      <div className="flex items-start justify-between gap-4">
        <p className="font-display text-[2rem] leading-none font-normal tracking-tight text-ink sm:text-[2.5rem]">
          <Link to="/" aria-label="Project Carlo — home">
            Project <span className="italic text-rubric">Carlo</span>
          </Link>
        </p>
        {aside}
      </div>
      {/* A sentence, so it stays in the body serif — small caps is for
          labels. Italic gives it the subtitle voice without shouting. */}
      <h1 className="font-serif text-[1rem] font-normal italic text-ink-soft sm:text-[1.0625rem]">
        {tagline}
      </h1>
    </header>
  );
}
