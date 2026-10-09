import { useCallback, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { buildFeedbackContext } from "@/lib/feedbackContext";
import { getTallyFormId, openFeedbackPopup } from "@/lib/tally";
import { track } from "@/lib/analytics";

interface FeedbackTriggerProps {
  /** Shown on church pages so the church is attached to the submission. */
  church?: { slug: string; name: string | null };
  label?: string;
  icon?: ReactNode;
  variant?: "link" | "pill";
  className?: string;
}

/** Opens the Tally feedback popup with page and church context. */
export function FeedbackTrigger({
  church,
  label = "Share feedback",
  icon,
  variant = "link",
  className,
}: FeedbackTriggerProps) {
  const formId = getTallyFormId();

  const handleClick = useCallback(() => {
    track("feedback_open", { target: church?.slug });
    const context = buildFeedbackContext(church);
    void openFeedbackPopup(context);
  }, [church]);

  if (!formId) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className={cn(
        variant === "pill"
          ? "rubric-link inline-flex items-center gap-2 font-serif text-[0.9375rem]"
          : "rubric-link font-serif text-[0.9375rem] text-rubric hover:text-rubric-deep",
        className,
      )}
    >
      {icon}
      {label}
    </button>
  );
}
