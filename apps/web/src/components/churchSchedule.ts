import {
  comparePatterns,
  DAY_ORDER,
  describePatternBeyondLabel,
  EVENT_TYPE_ORDER,
  type EventSummary,
  type EventType,
  isPlainWeekly,
  patternKey,
  weekdayLabel,
} from "@carlo/core";

/** One section of the church page (Mass, Confession, Adoration), by row. */
export interface EventsByType {
  /** Slots that run every week of the year, by weekday. */
  weeklyByDay: Record<string, EventSummary[]>;
  /** Weekly slots that keep only some weeks, or part of the year. */
  patterned: PatternedRow[];
  specificDate: EventSummary[];
}

/**
 * The slots on one weekday that share one schedule beyond it ("4th Sunday",
 * "Tuesday, October through June"), as a row of their own under the
 * every-week rows.
 *
 * The church page lists a slot whether or not it is running today (someone
 * looking up a parish wants its whole schedule). A slot set among the
 * every-week times of its day, with its qualifier in a note, read as one more
 * time every week: the 4th-Sunday Mass between the Sunday 12 and 5 read as a
 * Sunday 1:30. On a row of its own, its label says when it runs, and the
 * note says what the label can't, such as the months it runs, which tells a
 * reader why the map did not show it today.
 */
export interface PatternedRow {
  key: string;
  /** Lower-case weekday, as in `DAY_ORDER`. */
  day: string;
  label: string;
  qualifier: string | null;
  events: EventSummary[];
}

export function partitionEventsByType(
  events: EventSummary[],
): Record<EventType, EventsByType> {
  const result: Record<EventType, EventsByType> = {
    mass: { weeklyByDay: {}, patterned: [], specificDate: [] },
    confession: { weeklyByDay: {}, patterned: [], specificDate: [] },
    adoration: { weeklyByDay: {}, patterned: [], specificDate: [] },
  };

  for (const type of EVENT_TYPE_ORDER) {
    for (const d of DAY_ORDER) {
      result[type].weeklyByDay[d] = [];
    }
  }

  const patternedByKey: Record<EventType, Map<string, PatternedRow>> = {
    mass: new Map(),
    confession: new Map(),
    adoration: new Map(),
  };

  for (const e of events) {
    const typeData = result[e.type];
    if (e.kind === "weekly" && e.day_of_week) {
      const day = e.day_of_week.toLowerCase();
      if (!(day in typeData.weeklyByDay)) continue;
      if (isPlainWeekly(e)) {
        typeData.weeklyByDay[day].push(e);
        continue;
      }
      const key = `${day}:${patternKey(e)}`;
      const rows = patternedByKey[e.type];
      let row = rows.get(key);
      if (!row) {
        row = {
          key,
          day,
          label: weekdayLabel(e, day),
          qualifier: describePatternBeyondLabel(e, day),
          events: [],
        };
        rows.set(key, row);
      }
      row.events.push(e);
    } else {
      typeData.specificDate.push(e);
    }
  }

  const dayIndex = (day: string) =>
    (DAY_ORDER as readonly string[]).indexOf(day);
  for (const type of EVENT_TYPE_ORDER) {
    const typeData = result[type];
    for (const day of DAY_ORDER) {
      typeData.weeklyByDay[day].sort((a, b) => a.start_time - b.start_time);
    }
    for (const row of patternedByKey[type].values()) {
      row.events.sort((a, b) => a.start_time - b.start_time);
    }
    // A row's slots share one pattern, so its first slot stands for the row.
    typeData.patterned = [...patternedByKey[type].values()].sort(
      (a, b) =>
        dayIndex(a.day) - dayIndex(b.day) ||
        comparePatterns(a.events[0], b.events[0]),
    );
    typeData.specificDate.sort((a, b) =>
      (a.date ?? "").localeCompare(b.date ?? ""),
    );
  }

  return result;
}

/** Every slot in a section, in the order the page shows them. */
export function collectSectionEvents(section: EventsByType): EventSummary[] {
  const all: EventSummary[] = [];
  for (const day of DAY_ORDER) {
    const list = section.weeklyByDay[day];
    if (list) all.push(...list);
  }
  for (const row of section.patterned) all.push(...row.events);
  all.push(...section.specificDate);
  return all;
}
