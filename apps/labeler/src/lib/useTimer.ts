import { useEffect, useRef, useState, type RefObject } from "react";

/** Seconds spent on the page, counting only while the tab is visible. */
export function useTimer(initial: number): [number, RefObject<number>] {
  const [seconds, setSeconds] = useState(initial);
  const ref = useRef(initial);
  useEffect(() => {
    const id = window.setInterval(() => {
      if (document.visibilityState !== "visible") return;
      ref.current += 1;
      setSeconds(ref.current);
    }, 1000);
    return () => window.clearInterval(id);
  }, []);
  return [seconds, ref];
}
