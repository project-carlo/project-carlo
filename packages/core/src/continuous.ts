import type { ScheduleRollupRow } from "./eventRollup";
import { dateInValidity } from "./schedulePattern";
import type { ContinuousAdoration } from "./types";
import { formatMinutesMissal } from "./utils";

/**
 * Chapels open 24 hours: which one a church has today, and how the site words
 * it. Every sentence here is the site's own: a chapel stores only its access
 * (`ChapelAccess`) and unlocked hours, never a contact or a code, and the site
 * never says that no code is needed, since a bulletin's silence does not prove
 * that. Pure; no DOM or React dependencies.
 */

/** The day heading a chapel's row goes under, in every schedule layout. */
export const EVERY_DAY = "Every day";

const CONTACT = "Contact the parish office for details.";

export interface ContinuousRowOptions {
  /** The map popup and city card: no line for a silent source, the locked hours. */
  compact?: boolean;
  /** Where the times were read, starting a sentence: "The bulletin" by default. */
  source?: string;
}

/**
 * The church's chapel open on `today`, or null. A closure ends one record
 * (`valid_until`) and a reopening starts another (`valid_from`), so at most
 * one is open on any one day.
 */
export function currentContinuous(
  chapels: readonly ContinuousAdoration[],
  today: Date = new Date(),
): ContinuousAdoration | null {
  return chapels.find((chapel) => dateInValidity(today, chapel)) ?? null;
}

/** The main text beside "Every day": "Open 24 hours", "By arrangement"... */
export function continuousTimes(chapel: ContinuousAdoration): string {
  switch (chapel.access) {
    case "code":
      return "24 hours with code";
    case "arrangement":
      return "By arrangement";
    default:
      return "Open 24 hours";
  }
}

/** "6 a.m. – 9 p.m.", ending a sentence: "a.m." and "p.m." already end in a stop. */
function hours(from: number, until: number): string {
  return `${formatMinutesMissal(from)} – ${formatMinutesMissal(until)}`;
}

/**
 * The line under the chapel's row, saying how to get in: shorter on the map
 * popup and city card (`compact`), fuller on the church page. `source` names
 * where the times were read ("The bulletin", "The parish website"), for a
 * chapel whose source says nothing about getting in; that line is the church
 * page's only.
 */
export function continuousAccessLine(
  chapel: ContinuousAdoration,
  { compact = false, source = "The bulletin" }: ContinuousRowOptions = {},
): string | null {
  switch (chapel.access) {
    case "not_stated":
      return compact ? null : `${source} gives no access details.`;
    case "code_after_hours": {
      const { open_from: from, open_until: until } = chapel;
      if (from == null || until == null) {
        return `Door code needed after hours. ${CONTACT}`;
      }
      return compact
        ? `Door code needed ${hours(until, from)} ${CONTACT}`
        : `Unlocked ${hours(from, until)} Door code needed at other hours. ${CONTACT}`;
    }
    default:
      return CONTACT;
  }
}

/**
 * The chapel as one schedule row, the `{label, times, note}` shape the map
 * popup and the city card already lay out: "Every day ..... Open 24 hours",
 * then how to get in.
 */
export function continuousRow(
  chapel: ContinuousAdoration,
  options: ContinuousRowOptions = {},
): ScheduleRollupRow {
  return {
    key: `continuous:${chapel.id}`,
    label: EVERY_DAY,
    times: [continuousTimes(chapel)],
    note: continuousAccessLine(chapel, options),
  };
}
