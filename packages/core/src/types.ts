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

/**
 * What a church row is: a place of public Mass, or a parish's Adoration
 * chapel at an address of its own, which has no Mass or Confession.
 */
export type ChurchKind = "church" | "adoration_chapel";

/**
 * How a visitor gets into a chapel open 24 hours: the source says nothing; a
 * door code is needed outside its unlocked hours; a code is needed at every
 * hour; or only by arrangement with the parish. The site words each itself, so
 * nothing stored ever carries a contact or a code.
 */
export type ChapelAccess = "not_stated" | "code_after_hours" | "code" | "arrangement";

/**
 * A standing Adoration chapel open every day around the clock: one per church
 * (two only when a closure ends one and another starts later). It has no day
 * or time, so it is kept apart from the timed events, which all have a
 * numeric `start_time`.
 */
export interface ContinuousAdoration {
  id: number;
  church_id: number;
  access: ChapelAccess;
  /** `code_after_hours` only: the hours it is unlocked, minutes after midnight. */
  open_from: number | null;
  open_until: number | null;
  /** A short location or exception ("Adoration Chapel"), never a contact. */
  note: string | null;
  page_number: number | null;
  /** Inclusive absolute dates, as on a weekly slot (a closure, a reopening). */
  valid_from: string | null;
  valid_until: string | null;
}

/** The church fields every view reads. */
export interface ChurchBase {
  id: number;
  parish_id: number;
  slug: string;
  /** A church, or an Adoration chapel at its own address. */
  kind: ChurchKind;
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
  /** The church's chapel open 24 hours, when Adoration is shown and it has one. */
  continuous: ContinuousAdoration | null;
}

export interface ChurchDetail extends ChurchBase {
  homepage_url: string | null;
  /** The parish's current bulletin: the one this church's times come from. */
  bulletin_url: string | null;
  /** YYYY-MM-DD: the Sunday of the week that bulletin is for, or null if it has no date. */
  bulletin_week: string | null;
  /**
   * Where a parish with no bulletin posts its times: its own website or its
   * Facebook page. Null for a church whose times come from its bulletin.
   */
  schedule_source: ScheduleSource | null;
  /** The page the times were read from, when `schedule_source` is set. */
  source_url: string | null;
  /** YYYY-MM-DD: when that page was last read, when `schedule_source` is set. */
  checked_on: string | null;
}

/** Where a parish with no bulletin posts its times. */
export type ScheduleSource = "website" | "facebook";

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
