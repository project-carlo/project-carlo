import { RefreshCwIcon } from "@/components/icons";
import { cn } from "@/lib/utils";

export interface InlineQueryErrorProps {
  message: string;
  onRetry: () => void;
  /** Optional smallcaps rubric heading (e.g. overlay error title). */
  title?: string;
  className?: string;
  /** Center text and retry control (full-page / card overlays). */
  centered?: boolean;
}

export function InlineQueryError({
  message,
  onRetry,
  title,
  className,
  centered,
}: InlineQueryErrorProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-3",
        centered ? "text-center" : "items-start",
        className,
      )}
    >
      {title ? (
        <p className="smallcaps text-[0.8125rem] text-rubric">{title}</p>
      ) : null}
      <p className="font-serif text-sm text-ink-soft">{message}</p>
      <button
        type="button"
        onClick={onRetry}
        className={cn(
          "rubric-link inline-flex items-center gap-1.5 font-serif text-[0.9375rem]",
          centered && "mx-auto mt-1",
        )}
      >
        <RefreshCwIcon className="size-3" />
        Try again
      </button>
    </div>
  );
}
