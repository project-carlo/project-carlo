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
}
