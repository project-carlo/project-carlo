export type EventType = "mass" | "confession" | "adoration";

/**
 * A week of the month a weekly slot keeps: "first" is days 1–7, "second"
 * 8–14, "third" 15–21, "fourth" 22–28, "fifth" 29–31, and "last" the month's
 * last such weekday.
 */
export type WeekOfMonth = "first" | "second" | "third" | "fourth" | "fifth" | "last";

/**
 * The part of the year a weekly slot runs: from start_month/start_day (null:
 * the 1st) through end_month/end_day (null: the month's last day), both
 * inclusive, wrapping the new year when the start comes after the end.
 */
export interface Season {
  start_month: number;
  start_day: number | null;
  end_month: number;
  end_day: number | null;
}

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
  /** Weekly slots only: the weeks of the month it keeps; empty for every week. */
  weeks_of_month: WeekOfMonth[];
  /** Weekly slots only: `weeks_of_month` are the weeks it skips instead. */
  exclude_weeks: boolean;
  /** Weekly slots only: the part of the year it runs; null for all year. */
  season: Season | null;
  /** Inclusive absolute dates, distinct from an annually repeating season. */
  valid_from?: string | null;
  valid_until?: string | null;
}

/** The church fields every view reads. */
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
  /** The parish's current bulletin: the one this church's times come from. */
  bulletin_url: string | null;
  /** YYYY-MM-DD: the Sunday of the week that bulletin is for, or null if it has no date. */
  bulletin_week: string | null;
}

/** A snapshot event as the data layer filters it; `occurrence` is its next occurrence. */
export interface RawEvent {
  id: number;
  church_id: number;
  event_type: EventType;
  event_kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
  end_time: number | null;
  cancelled: boolean;
  occurrence: string | null;
  page_number: number | null;
  note: string | null;
  /** Weekly rows only: the weeks of the month it keeps; empty for every week. */
  weeks_of_month: WeekOfMonth[];
  /** Weekly rows only: `weeks_of_month` are the weeks it skips instead. */
  exclude_weeks: boolean;
  /** Weekly rows only: the season (see `Season`); all four null for all year. */
  season_start_month: number | null;
  season_start_day: number | null;
  season_end_month: number | null;
  season_end_day: number | null;
  /**
   * On a cancelled dated row: the id of the weekly row whose occurrence on
   * `date` it cancels. Null on every other row.
   */
  cancels_event_id: number | null;
  valid_from?: string | null;
  valid_until?: string | null;
}
