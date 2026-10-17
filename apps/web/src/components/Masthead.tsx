import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { useDocumentLinks } from "@/lib/documentLinks";
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
  const documentLinks = useDocumentLinks();
  if (compact) {
    return (
      <div className={cn("flex items-baseline gap-4", className)}>
        <Link
          to="/"
          reloadDocument={documentLinks}
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
  // On a phone it's read but not shown, so the map gets the room.
  return (
    <header className={cn("space-y-2", className)}>
      <div className="flex items-center justify-between gap-4 md:items-start">
        <p className="font-display text-[1.625rem] leading-none font-normal tracking-tight text-ink md:text-[2.5rem]">
          <Link to="/" reloadDocument={documentLinks} aria-label="Project Carlo — home">
            Project <span className="italic text-rubric">Carlo</span>
          </Link>
        </p>
        {aside}
      </div>
      {/* A sentence, so it stays in the body serif — small caps is for
          labels. Italic gives it the subtitle voice without shouting. */}
      <h1 className="sr-only font-serif text-[1.0625rem] font-normal italic text-ink-soft md:not-sr-only">
        {tagline}
      </h1>
    </header>
  );
}
