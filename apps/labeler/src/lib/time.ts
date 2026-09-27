/**
 * Loose time entry: "530p", "5:30", "17:30", "noon" all become "HH:MM".
 *
 * Without am/pm, 1-6 o'clock reads as afternoon and 7-11 as morning, which is
 * how parish schedules run (a 5:30 is a Saturday vigil, a 7:00 a daily Mass).
 * The editor shows the parsed time straight back, so a wrong guess is visible;
 * add "a" or "p", or type 24-hour time, to be explicit.
 */
export function parseLooseTime(input: string): string | null {
  const raw = input.trim().toLowerCase().replace(/[\s.]/g, "");
  if (!raw) return null;
  if (raw === "noon" || raw === "12n" || raw === "midday") return "12:00";
  if (raw === "midnight" || raw === "12mn") return "00:00";

  const m = /^(\d{1,2})(?::?(\d{2}))?(a|p|am|pm)?$/.exec(raw);
  if (!m) return null;
  let hour = Number(m[1]);
  const minute = m[2] === undefined ? 0 : Number(m[2]);
  const suffix = m[3]?.[0];
  if (minute > 59) return null;

  if (suffix) {
    if (hour < 1 || hour > 12) return null;
    if (suffix === "p" && hour !== 12) hour += 12;
    if (suffix === "a" && hour === 12) hour = 0;
  } else if (m[1].length === 2 && m[1].startsWith("0")) {
    // "0730" or "07:30" is explicit 24-hour time.
  } else if (hour >= 1 && hour <= 6) {
    hour += 12;
  } else if (hour > 23) {
    return null;
  }
  return `${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`;
}

export function minutesOf(hhmm: string | null | undefined): number | null {
  if (!hhmm) return null;
  const m = /^(\d{2}):(\d{2})$/.exec(hhmm);
  return m ? Number(m[1]) * 60 + Number(m[2]) : null;
}

/** "17:30" -> "5:30 PM"; empty for nothing. */
export function formatTime(hhmm: string | null | undefined): string {
  const minutes = minutesOf(hhmm);
  if (minutes === null) return "";
  const h24 = Math.floor(minutes / 60);
  const h12 = h24 % 12 === 0 ? 12 : h24 % 12;
  return `${h12}:${String(minutes % 60).padStart(2, "0")} ${h24 < 12 ? "AM" : "PM"}`;
}

export function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}
