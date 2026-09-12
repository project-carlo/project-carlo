/** Format minutes since midnight for display: e.g. `7:30 a.m.` — lowercase
 *  meridiem. Omits `:00` for on-the-hour times so `8 a.m.` reads naturally. */
export function formatMinutesMissal(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  const meridiem = h < 12 ? "a.m." : "p.m.";
  const displayH = h === 0 ? 12 : h > 12 ? h - 12 : h;
  if (m === 0) return `${displayH} ${meridiem}`;
  return `${displayH}:${m.toString().padStart(2, "0")} ${meridiem}`;
}

/** Capitalize the first letter of a string. */
export function titleCase(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

// Formatters built once and reused: constructing an Intl formatter costs far
// more than formatting with it, and a parish page formats one date per listed
// service. (Weekday and month stay separate formatters — asking for both at
// once yields "March Tuesday" in en-US.)
const LONG_WEEKDAY_FORMATTER = new Intl.DateTimeFormat("en-US", {
  weekday: "long",
});
const LONG_MONTH_FORMATTER = new Intl.DateTimeFormat("en-US", { month: "long" });
const eventDateCache = new Map<string, string>();

/** Format YYYY-MM-DD to "Tuesday, March 17th" style. */
export function formatEventDate(dateStr: string): string {
  const cached = eventDateCache.get(dateStr);
  if (cached !== undefined) return cached;
  const d = new Date(dateStr + "T12:00:00");
  const weekday = LONG_WEEKDAY_FORMATTER.format(d);
  const month = LONG_MONTH_FORMATTER.format(d);
  const day = d.getDate();
  const suffix =
    day >= 11 && day <= 13
      ? "th"
      : { 1: "st", 2: "nd", 3: "rd" }[day % 10] ?? "th";
  const formatted = `${weekday}, ${month} ${day}${suffix}`;
  eventDateCache.set(dateStr, formatted);
  return formatted;
}

/** Format structured address fields into a single display string. */
export function formatAddress(church: {
  address_line1: string | null;
  address_line2: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
}): string | null {
  const parts: string[] = [];
  if (church.address_line1) parts.push(church.address_line1);
  if (church.address_line2) parts.push(church.address_line2);
  const stateZip = [church.state, church.postal_code].filter(Boolean).join(" ");
  const cityStateZip = [church.city, stateZip].filter(Boolean).join(", ");
  if (cityStateZip) parts.push(cityStateZip);
  return parts.length > 0 ? parts.join(", ") : null;
}
