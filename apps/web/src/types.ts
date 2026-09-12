import type { WeekOfMonth } from "./lib/schedulePattern";

export type EventType = "mass" | "confession" | "adoration";

export interface EventSummary {
  id: number;
  type: EventType;
  kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
  end_time: number | null;
  cancelled: boolean;
  next_occurrence: string | null;
  page_number: number | null;
  note: string | null;
  /** Weeks of the month a weekly slot falls on; empty means every week. */
  weeks_of_month: WeekOfMonth[];
  /** Inclusive range of the year a weekly slot runs in; null means all year. */
  season_start_month: number | null;
  season_start_day: number | null;
  season_end_month: number | null;
  season_end_day: number | null;
}

/** The church columns every view reads; see `CHURCH_COLUMNS` in lib/churchRow. */
export interface ChurchBase {
  id: number;
  parish_id: number;
  slug: string;
  name: string | null;
  address_line1: string | null;
  address_line2: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface ChurchMapItem extends ChurchBase {
  event_types: EventType[];
  upcoming_events: EventSummary[];
}

export interface ChurchDetail extends ChurchBase {
  homepage_url: string | null;
  bulletin_url: string | null;
}
