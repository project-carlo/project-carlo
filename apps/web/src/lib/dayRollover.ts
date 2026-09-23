import { todayDate } from "./schedule";

/**
 * Call `onChange` whenever the local date changes while the page is open.
 *
 * A timer is armed for the next local midnight, but a suspended tab (a phone
 * in a pocket) doesn't run timers and resumes them late, so the date is also
 * re-checked whenever the page becomes visible again. A timer that fires a
 * little early just re-arms itself for the remainder. Browser-only; returns a
 * function that stops watching.
 */
export function onLocalDayChange(onChange: () => void): () => void {
  let day = todayDate().getTime();
  let timer: ReturnType<typeof setTimeout> | undefined;

  function arm(today: Date): void {
    clearTimeout(timer);
    const tomorrow = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate() + 1,
    );
    timer = setTimeout(check, tomorrow.getTime() - Date.now());
  }

  function check(): void {
    const today = todayDate();
    if (today.getTime() !== day) {
      day = today.getTime();
      onChange();
    }
    arm(today);
  }

  function onVisibilityChange(): void {
    if (document.visibilityState === "visible") check();
  }

  arm(new Date(day));
  document.addEventListener("visibilitychange", onVisibilityChange);
  return () => {
    clearTimeout(timer);
    document.removeEventListener("visibilitychange", onVisibilityChange);
  };
}
