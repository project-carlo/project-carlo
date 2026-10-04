import { useEffect, useState } from "react";

/** The current time, refreshed every `intervalMs` so "Soon" badges and relative days stay true. */
export function useNow(intervalMs: number = 30_000): Date {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = window.setInterval(() => setNow(new Date()), intervalMs);
    return () => window.clearInterval(id);
  }, [intervalMs]);
  return now;
}
