/** The label file format (schema_version 1); see src/pdf_extract/labeling/labels.py. */

export const EVENT_TYPES = ["mass", "confession", "adoration"] as const;
export type EventType = (typeof EVENT_TYPES)[number];

export type EventKind = "weekly" | "specific_date";

export const DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
] as const;
export type Day = (typeof DAYS)[number];

export const WEEKS_OF_MONTH = ["first", "second", "third", "fourth", "fifth", "last"] as const;
export type WeekOfMonth = (typeof WEEKS_OF_MONTH)[number];

export type Origin = "human" | "gemini" | "gemini-edited";

/**
 * An optional event is a judgment call whether it belongs in the schedule at
 * all; the value is the preferred answer. Scoring leaves optional events out
 * and reports how often a classifier made the preferred choice.
 */
export type OptionalPreference = "include" | "exclude";

export type Status = "in_progress" | "done" | "skipped";

export const FLAG_NAMES = ["wrong_bulletin", "unreadable", "no_schedule", "church_missing", "conflicting_info"] as const;
export type FlagName = (typeof FLAG_NAMES)[number];
export type Flags = Record<FlagName, boolean>;

export interface Season {
  start_month: number;
  start_day: number | null;
  end_month: number;
  end_day: number | null;
}

export interface LabelEvent {
  church_slug: string;
  event_type: EventType;
  event_kind: EventKind;
  day_of_week: Day | null;
  date: string | null;
  start_time: string;
  end_time: string | null;
  cancelled: boolean;
  weeks_of_month: WeekOfMonth[];
  season: Season | null;
  page_number: number | null;
  note: string | null;
  origin: Origin;
  /** Null for a required event. Labels saved before this existed lack it. */
  optional: OptionalPreference | null;
}

export interface Label {
  schema_version: 1;
  parish_slug: string;
  content_hash: string;
  source_url: string;
  status: Status;
  flags: Flags;
  published_date: string | null;
  note: string;
  labeler: string;
  seconds_spent: number;
  updated_at: string;
  events: LabelEvent[];
}

/** A ground-truth row being edited: a label event that may still be incomplete. */
export interface EditorRow extends Omit<LabelEvent, "church_slug" | "start_time"> {
  id: string;
  church_slug: string;
  start_time: string;
  /** The Gemini row this came from, while this browser remembers it. */
  gemini_id?: string;
  /**
   * Several days or dates typed into one row. The row becomes one row each
   * when focus leaves it, so the times typed next apply to all of them.
   */
  pending_split?: { days?: Day[]; dates?: string[] };
}

/** One of Gemini's events, in the label's row shape (read-only). */
export interface GeminiRow {
  id: string;
  church_slug: string;
  event_type: EventType | null;
  event_kind: EventKind | null;
  day_of_week: Day | null;
  date: string | null;
  start_time: string | null;
  end_time: string | null;
  cancelled: boolean;
  weeks_of_month: WeekOfMonth[];
  season: Season | null;
  page_number: number | null;
  note: string | null;
  raw: Record<string, string>;
  problems: string[];
}

export interface GeminiSource {
  kind: "cache" | "post-processing" | "update" | "none";
  classifier: string;
  /** For an update-mode parish ("update"): the call whose view and applied changes are shown. */
  llm_call_id?: number;
  model?: string | null;
  prompt_version?: string | null;
  version_dir?: string;
  is_current_version?: boolean;
  church_list_matches?: boolean;
  processed_at?: string | null;
}

export interface Church {
  slug: string;
  name: string;
  address: string;
}

export interface BulletinSummary {
  parish_slug: string;
  parish_name: string;
  content_hash: string;
  source_url: string;
  published_date: string | null;
  fetched_at: string | null;
  processed_at: string | null;
  rank: number;
  status: Status | "unlabeled";
}

export interface Progress {
  latest_total: number;
  latest_done: number;
  /** Parishes with at least one bulletin labeled (in progress, done, or skipped). */
  parishes_labeled: number;
  total: number;
  unlabeled: number;
  in_progress: number;
  done: number;
  skipped: number;
}

/** One bulletin of the parish open in the editor, for switching among them. */
export interface ParishBulletin {
  content_hash: string;
  published_date: string | null;
  fetched_at: string | null;
  rank: number;
  status: BulletinSummary["status"];
}

export interface BulletinDetail {
  parish: { slug: string; name: string; homepage_url: string };
  churches: Church[];
  bulletin: {
    source_url: string;
    content_hash: string;
    published_date: string | null;
    fetched_at: string | null;
    processed_at: string | null;
  };
  gemini: {
    source: GeminiSource;
    published_date: string | null;
    wrong_bulletin: boolean | null;
    church_list_needs_review: boolean | null;
    events: GeminiRow[];
  };
  label: Label | null;
  progress: Progress;
  parish_bulletins: ParishBulletin[];
}

export interface Config {
  mode: "live" | "demo";
  classifier: string;
  classifier_version: string;
  remote: boolean;
  labels_dir: string;
  seeds_dir: string;
  default_labeler: string;
}

// ── Seeds (docs/seeding-plan.md; src/pdf_extract/seeding/files.py) ──────────

/** A schedule entry in a seed: a label event without page, origin and optional. */
export type SeedEntry = Omit<LabelEvent, "page_number" | "origin" | "optional">;

export type SeedStatus = "drafting" | "needs_review" | "ready" | "approved" | "blocked";

export interface SeedBulletin {
  content_hash: string;
  fetched_at: string;
  published_date: string | null;
  read: boolean;
}

export interface SeedSource {
  /** "agent", "history", or the id of one of the file's calls. */
  source: string;
  bulletin?: string | null;
  page?: number | null;
  said: string;
}

export interface SeedOption {
  label: string;
  entry: SeedEntry | null;
  leaning?: boolean;
}

export interface SeedAnswer {
  choice: number | "edited" | "dropped";
  by: string;
  at: string;
}

export interface SeedSlot {
  id: string;
  decision: "include" | "exclude" | null;
  status: "settled" | "needs_human";
  entry: SeedEntry | null;
  page: number | null;
  sources: SeedSource[];
  rationale: string;
  question: string | null;
  options: SeedOption[] | null;
  answer: SeedAnswer | null;
}

export interface SeedCall {
  id: string;
  kind: "extract" | "ask";
  model: string;
  bulletin: string;
  cached: boolean;
  cost_usd: number | null;
  question?: string;
  answer?: string;
  page?: number | null;
  quote?: string;
  events?: GeminiRow[];
}

export interface SeedFile {
  schema_version: 1;
  parish_slug: string;
  status: SeedStatus;
  as_of: string | null;
  drafted_by: string;
  drafted_at: string | null;
  reviewer: string | null;
  approved_at: string | null;
  summary: string;
  blocked_reason: string | null;
  bulletins: SeedBulletin[];
  calls: SeedCall[];
  slots: SeedSlot[];
}

export interface SeedQueueRow {
  parish_slug: string;
  parish_name: string;
  status: SeedStatus | "invalid";
  open_questions: number;
  slots: number;
  included: number;
  calls: number;
  cost_usd: number;
  as_of: string | null;
  reviewer: string | null;
  summary: string;
  blocked_reason: string | null;
  problem: string | null;
  loaded: boolean;
}

export interface SeedDetail {
  seed: SeedFile;
  parish: { slug: string; name: string };
  churches: Church[];
  bulletins_in_db: string[];
  problems: string[];
  loaded: boolean;
}
