import { useEffect, useRef, useState, type KeyboardEvent } from "react";

interface Props {
  /** What the field shows when not being edited (the committed value, formatted). */
  display: string;
  /** Parse and apply the text; return false to keep editing (shown as invalid). */
  onCommit: (text: string) => boolean;
  placeholder?: string;
  className?: string;
  title?: string;
  /** Focus (and select) the field when this becomes true. */
  autoFocus?: boolean;
  onFocused?: () => void;
  missing?: boolean;
  testId?: string;
}

/** A text field edited loosely ("530p", "Mon-Fri") and committed on Enter, Tab or blur. */
export function CommitInput({
  display,
  onCommit,
  placeholder,
  className = "",
  title,
  autoFocus,
  onFocused,
  missing,
  testId,
}: Props) {
  const [text, setText] = useState(display);
  const [focused, setFocused] = useState(false);
  const [invalid, setInvalid] = useState(false);
  const ref = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!focused) {
      setText(display);
      setInvalid(false);
    }
  }, [display, focused]);

  useEffect(() => {
    if (autoFocus) {
      ref.current?.focus();
      ref.current?.select();
      onFocused?.();
    }
  }, [autoFocus, onFocused]);

  const commit = (): boolean => {
    if (text === display) {
      setInvalid(false);
      return true;
    }
    const ok = onCommit(text);
    setInvalid(!ok);
    return ok;
  };

  // Leave the field but stay in its row, so a pending multi-day split waits for the row to lose focus.
  const leave = () => {
    const row = ref.current?.closest<HTMLElement>("[data-row-id]");
    if (row) row.focus({ preventScroll: true });
    else ref.current?.blur();
  };

  const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !(e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (commit()) leave();
    } else if (e.key === "Escape") {
      e.preventDefault();
      setText(display);
      setInvalid(false);
      requestAnimationFrame(leave);
    } else if (e.key === "Enter") {
      commit();
    }
  };

  return (
    <input
      ref={ref}
      type="text"
      value={text}
      placeholder={placeholder}
      title={invalid ? `Could not read "${text}"${title ? ` (${title})` : ""}` : title}
      data-testid={testId}
      spellCheck={false}
      autoComplete="off"
      onChange={(e) => setText(e.target.value)}
      onFocus={(e) => {
        setFocused(true);
        e.target.select();
      }}
      onBlur={() => {
        commit();
        setFocused(false);
      }}
      onKeyDown={onKeyDown}
      className={`min-w-0 rounded border px-1 py-0.5 text-sm outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 ${
        invalid
          ? "border-red-500 bg-red-50"
          : missing
            ? "border-amber-400 bg-amber-50"
            : "border-slate-300 bg-white"
      } ${className}`}
    />
  );
}
