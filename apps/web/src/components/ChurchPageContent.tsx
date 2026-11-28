import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import {
  type ChurchDetail,
  type ContinuousAdoration,
  continuousAccessLine,
  continuousTimes,
  DAY_ORDER,
  describePatternBeyondLabel,
  EVERY_DAY,
  EVENT_TYPE_LABELS,
  EVENT_TYPE_ORDER,
  type EventSummary,
  type EventType,
  formatAddress,
  formatEventDate,
  formatLongDate,
  formatLongMonthDay,
  formatMonthDay,
  formatTimeRange,
  isPlainWeekly,
  patternKey,
  titleCase,
  weekdayLabel,
  WEEKS_OF_MONTH,
} from "@carlo/core";
import {
  CHURCH_LIST,
  churchDisclaimer,
  SOURCE_NAMES,
  UNNAMED_CHURCH,
} from "../copy";
import {
  ExternalLinkIcon,
  FileTextIcon,
  MapPinIcon,
  PencilIcon,
} from "@/components/icons";
import { FeedbackTrigger } from "@/components/FeedbackTrigger";
import { Fleuron } from "@/components/Fleuron";
import { Breadcrumbs, type Crumb } from "@/components/Breadcrumbs";
import { CityMapPreview } from "@/components/CityMapPreview";
import { SiteHeader } from "@/components/SiteHeader";
import { cityPath, type CityLink } from "@/lib/cities";
import type { CityMapConfig } from "@/lib/cityMap";
import type { CityMapData } from "@/lib/cityMapLayout";
import { CHURCH_INDEX_PATH } from "@/lib/seo";
import { LASTMOD_EXEMPT_ATTRIBUTE } from "@/lib/lastmod";

/** Inline annotations on a schedule line — the bulletin page a time came
 *  from, and any qualifier on the slot. One size and one voice for all of
 *  them, so a schedule row doesn't carry three different italics. */
const ANNOTATION_CLASS = "font-serif text-[0.9rem] italic";
const ANNOTATION_LINK_CLASS =
  "text-rubric underline decoration-rubric/40 decoration-from-font underline-offset-[3px] transition-colors hover:text-rubric-deep hover:decoration-rubric-deep";

interface EventsByType {
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
interface PatternedRow {
  key: string;
  label: string;
  qualifier: string | null;
  events: EventSummary[];
  dayIndex: number;
  weekIndex: number;
}

function partitionEventsByType(
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
          label: weekdayLabel(e, day),
          qualifier: describePatternBeyondLabel(e, day),
          events: [],
          dayIndex: (DAY_ORDER as readonly string[]).indexOf(day),
          weekIndex: e.exclude_weeks
            ? WEEKS_OF_MONTH.length
            : Math.min(
                ...e.weeks_of_month.map((week) => WEEKS_OF_MONTH.indexOf(week)),
                WEEKS_OF_MONTH.length,
              ),
        };
        rows.set(key, row);
      }
      row.events.push(e);
    } else {
      typeData.specificDate.push(e);
    }
  }

  for (const type of EVENT_TYPE_ORDER) {
    const typeData = result[type];
    for (const day of DAY_ORDER) {
      typeData.weeklyByDay[day].sort((a, b) => a.start_time - b.start_time);
    }
    typeData.patterned = [...patternedByKey[type].values()].sort(
      (a, b) =>
        a.dayIndex - b.dayIndex ||
        a.weekIndex - b.weekIndex ||
        a.key.localeCompare(b.key),
    );
    for (const row of typeData.patterned) {
      row.events.sort((a, b) => a.start_time - b.start_time);
    }
    typeData.specificDate.sort((a, b) =>
      (a.date ?? "").localeCompare(b.date ?? ""),
    );
  }

  return result;
}

function formatTimeValue(event: EventSummary): string {
  return formatTimeRange(event.start_time, event.end_time);
}

function collectSectionEvents(section: EventsByType): EventSummary[] {
  const all: EventSummary[] = [];
  for (const day of DAY_ORDER) {
    const list = section.weeklyByDay[day];
    if (list) all.push(...list);
  }
  for (const row of section.patterned) all.push(...row.events);
  all.push(...section.specificDate);
  return all;
}

function mostCommonPageNumber(events: EventSummary[]): number | null {
  const counts = new Map<number, number>();
  let bestPage: number | null = null;
  let bestCount = 0;
  for (const e of events) {
    if (e.page_number == null) continue;
    const next = (counts.get(e.page_number) ?? 0) + 1;
    counts.set(e.page_number, next);
    if (next > bestCount) {
      bestCount = next;
      bestPage = e.page_number;
    }
  }
  return bestPage;
}

function SectionPageRef({
  pageNumber,
  bulletinUrl,
}: {
  pageNumber: number;
  bulletinUrl: string | null;
}) {
  const label = `Found on bulletin page ${pageNumber}`;
  const title = `Open bulletin at page ${pageNumber}`;
  const baseClass = `ml-3 ${ANNOTATION_CLASS}`;
  if (bulletinUrl) {
    return (
      <a
        href={`${bulletinUrl}#page=${pageNumber}`}
        target="_blank"
        rel="noopener noreferrer"
        data-track="bulletin_page"
        title={title}
        className={`${baseClass} ${ANNOTATION_LINK_CLASS}`}
      >
        {label}
      </a>
    );
  }
  return (
    <span className={`${baseClass} text-ink-soft`} title={title}>
      {label}
    </span>
  );
}

function EventNote({ note }: { note: string | null }) {
  if (!note) return null;
  return (
    <span className={`ml-2 ${ANNOTATION_CLASS} text-ink-faint`}>
      {note}
    </span>
  );
}

function PageRef({
  event,
  bulletinUrl,
}: {
  event: EventSummary;
  bulletinUrl: string | null;
}) {
  if (event.page_number == null) return null;
  const label = `page ${event.page_number}`;
  const title = `Open bulletin at page ${event.page_number}`;
  if (bulletinUrl) {
    return (
      <a
        href={`${bulletinUrl}#page=${event.page_number}`}
        target="_blank"
        rel="noopener noreferrer"
        data-track="bulletin_page"
        title={title}
        className={`ml-2.5 ${ANNOTATION_CLASS} ${ANNOTATION_LINK_CLASS}`}
      >
        {label}
      </a>
    );
  }
  return (
    <span
      className={`ml-2.5 ${ANNOTATION_CLASS} text-ink-soft`}
      title={title}
    >
      {label}
    </span>
  );
}

/** One row's times, dot-separated, each with its note and its bulletin page
 *  when that isn't the section's. */
function SlotTimes({
  events,
  sectionPage,
  bulletinUrl,
}: {
  events: EventSummary[];
  sectionPage: number | null;
  bulletinUrl: string | null;
}) {
  return events.map((event, idx) => (
    <span key={event.id}>
      {idx > 0 ? <span className="mx-2 text-ink-faint">·</span> : null}
      <span className="tabular-nums">{formatTimeValue(event)}</span>
      <EventNote note={event.note} />
      {event.page_number !== sectionPage ? (
        <PageRef event={event} bulletinUrl={bulletinUrl} />
      ) : null}
    </span>
  ));
}

/**
 * The current bulletin, dated by its week when it has a date: how fresh the
 * times are, beside the bulletin they come from. Exempt from the sitemap's
 * change dates, which would otherwise move every week with the bulletin. One
 * string, so the element holds text only.
 */
function BulletinLabel({ week }: { week: string | null }) {
  return (
    <span {...{ [LASTMOD_EXEMPT_ATTRIBUTE]: "" }}>
      {week ? `Bulletin for the week of ${formatLongMonthDay(week)}` : "Parish bulletin"}
    </span>
  );
}

/**
 * Where a parish with no bulletin posts its times, and when they were last
 * read there: "From the parish website · checked November 16, 2026". Exempt
 * from the sitemap's change dates like the bulletin's week, though it moves
 * only when the parish's page is read again. One string, so the element holds
 * text only.
 */
function SourceLabel({ church }: { church: ChurchDetail }) {
  const from = church.schedule_source
    ? `From ${SOURCE_NAMES[church.schedule_source]}`
    : "";
  const checked = church.checked_on
    ? ` · checked ${formatLongDate(church.checked_on)}`
    : "";
  return <span {...{ [LASTMOD_EXEMPT_ATTRIBUTE]: "" }}>{from + checked}</span>;
}

/** Church list › {City} › {Church}, without the city when the address has none. */
function churchCrumbs(church: ChurchDetail, city: CityLink | null): Crumb[] {
  const crumbs: Crumb[] = [{ label: CHURCH_LIST, to: CHURCH_INDEX_PATH }];
  if (city) crumbs.push({ label: city.label, to: cityPath(city.slug) });
  crumbs.push({ label: church.name ?? UNNAMED_CHURCH });
  return crumbs;
}

/**
 * A chapel open 24 hours, as the first row of the Adoration grid: "Every day
 * — Open 24 hours", its name, and how to get in, in the site's own words.
 */
function ContinuousRow({
  chapel,
  church,
  sectionPage,
}: {
  chapel: ContinuousAdoration;
  church: ChurchDetail;
  sectionPage: number | null;
}) {
  const source = church.schedule_source
    ? titleCase(SOURCE_NAMES[church.schedule_source])
    : "The bulletin";
  const access = continuousAccessLine(chapel, { source });
  const page = chapel.page_number;
  return (
    <div className="grid grid-cols-[6rem_1fr] items-baseline gap-4 py-2.5">
      <dt className="smallcaps text-[0.875rem] text-ink-soft">{EVERY_DAY}</dt>
      <dd className="font-serif text-[1.05rem] leading-snug text-ink">
        <span>{continuousTimes(chapel)}</span>
        <EventNote note={chapel.note} />
        {page != null && page !== sectionPage ? (
          <ChapelPageRef page={page} bulletinUrl={church.bulletin_url} />
        ) : null}
        {access ? (
          <span className={`block ${ANNOTATION_CLASS} text-ink-soft`}>{access}</span>
        ) : null}
      </dd>
    </div>
  );
}

function ChapelPageRef({ page, bulletinUrl }: { page: number; bulletinUrl: string | null }) {
  const title = `Open bulletin at page ${page}`;
  if (!bulletinUrl) {
    return (
      <span className={`ml-2.5 ${ANNOTATION_CLASS} text-ink-soft`} title={title}>
        page {page}
      </span>
    );
  }
  return (
    <a
      href={`${bulletinUrl}#page=${page}`}
      target="_blank"
      rel="noopener noreferrer"
      data-track="bulletin_page"
      title={title}
      className={`ml-2.5 ${ANNOTATION_CLASS} ${ANNOTATION_LINK_CLASS}`}
    >
      page {page}
    </a>
  );
}

interface ChurchPageContentProps {
  church: ChurchDetail;
  /** Its chapel open 24 hours, or null. */
  continuous?: ContinuousAdoration | null;
  /** The city page the church is listed on, as that page names it. */
  city: CityLink | null;
  /** The church's map as it opens; null for a church with no known position. */
  map: CityMapData | null;
  events: EventSummary[];
  /**
   * Makes the map preview live (see CityMapPreview); the prerendered page
   * leaves it out and src/islands/cityMap.ts does the same.
   */
  liveMap?: (config: CityMapConfig) => ReactNode;
}

export function ChurchPageContent({
  church,
  continuous = null,
  city,
  map,
  events,
  liveMap,
}: ChurchPageContentProps) {
  const byType = partitionEventsByType(events);
  const name = church.name ?? UNNAMED_CHURCH;
  // A church whose only Adoration is its chapel open 24 hours still has times.
  const hasTimes = events.length > 0 || continuous !== null;

  return (
    <>
    <main className="min-h-svh bg-paper">
      <SiteHeader />

      <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        <section className="rise-in mx-auto max-w-2xl text-center">
          <Breadcrumbs className="mb-6" crumbs={churchCrumbs(church, city)} />
          <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
            {name}
          </h1>

          {formatAddress(church) ? (
            <p className="mt-4 flex items-center justify-center gap-2 font-serif text-[0.95rem] text-ink-soft">
              <MapPinIcon className="size-3.5 text-brass" />
              {formatAddress(church)}
            </p>
          ) : null}

          <Fleuron className="my-7" />

          <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-3">
            {church.homepage_url ? (
              <a
                href={church.homepage_url}
                target="_blank"
                rel="noopener noreferrer"
                data-track="parish_website"
                className="rubric-link inline-flex items-center gap-2 font-serif text-[0.9375rem]"
              >
                <ExternalLinkIcon className="size-3.5" />
                Visit the parish website
              </a>
            ) : null}
            {church.bulletin_url ? (
              <a
                href={church.bulletin_url}
                target="_blank"
                rel="noopener noreferrer"
                data-track="bulletin"
                className="rubric-link inline-flex items-center gap-2 font-serif text-[0.9375rem]"
              >
                <FileTextIcon className="size-3.5" />
                <BulletinLabel week={church.bulletin_week} />
              </a>
            ) : church.bulletin_week ? (
              <span className="inline-flex items-center gap-2 font-serif text-[0.9375rem] text-ink-soft">
                <FileTextIcon className="size-3.5" />
                <BulletinLabel week={church.bulletin_week} />
              </span>
            ) : church.schedule_source &&
              church.source_url &&
              church.source_url !== church.homepage_url ? (
              <a
                href={church.source_url}
                target="_blank"
                rel="noopener noreferrer"
                data-track="schedule_source"
                className="rubric-link inline-flex items-center gap-2 font-serif text-[0.9375rem]"
              >
                <ExternalLinkIcon className="size-3.5" />
                <SourceLabel church={church} />
              </a>
            ) : church.schedule_source ? (
              // The parish website link above already opens the page.
              <span className="inline-flex items-center gap-2 font-serif text-[0.9375rem] text-ink-soft">
                <FileTextIcon className="size-3.5" />
                <SourceLabel church={church} />
              </span>
            ) : null}
            <FeedbackTrigger
              church={church}
              label="Suggest an edit"
              variant="pill"
              icon={<PencilIcon className="size-3.5" />}
            />
          </div>
        </section>

        {!hasTimes ? (
          <p className="mx-auto mt-6 max-w-2xl text-center font-serif text-sm text-ink-soft md:mt-8">
            {church.schedule_source
              ? `No times listed yet. ${titleCase(SOURCE_NAMES[church.schedule_source])} may not include them, or we couldn’t read it.`
              : "No times listed yet. The parish bulletin may not include them, or we couldn’t read it."}
            {church.homepage_url
              ? " Check the parish website, or suggest an edit."
              : " Check with the parish, or suggest an edit."}
          </p>
        ) : null}

        {hasTimes ? (
          <div className="mx-auto mt-6 max-w-4xl md:mt-8">
            <div className="rise-in space-y-12" style={{ animationDelay: "80ms" }}>
              {EVENT_TYPE_ORDER.map((eventType) => {
                const section = byType[eventType];
                const { weeklyByDay, patterned, specificDate } = section;
                const hasWeekly = DAY_ORDER.some(
                  (d) => (weeklyByDay[d]?.length ?? 0) > 0,
                );
                const chapel = eventType === "adoration" ? continuous : null;
                const hasAny =
                  hasWeekly ||
                  patterned.length > 0 ||
                  specificDate.length > 0 ||
                  chapel !== null;
                if (!hasAny) return null;

                const sectionEvents = collectSectionEvents(section);
                const sectionPage =
                  mostCommonPageNumber(sectionEvents) ?? chapel?.page_number ?? null;

                return (
                  <section key={eventType}>
                    <div className="mb-5 flex flex-wrap items-baseline">
                      <h2 className="font-display text-[1.75rem] leading-none font-normal text-ink">
                        {EVENT_TYPE_LABELS[eventType]}
                      </h2>
                      {sectionPage != null ? (
                        <SectionPageRef
                          pageNumber={sectionPage}
                          bulletinUrl={church.bulletin_url}
                        />
                      ) : null}
                    </div>

                    <dl className="divide-y divide-rule">
                      {chapel ? (
                        <ContinuousRow
                          chapel={chapel}
                          church={church}
                          sectionPage={sectionPage}
                        />
                      ) : null}
                      {DAY_ORDER.map((day) => {
                        const dayEvents = weeklyByDay[day];
                        if (!dayEvents || dayEvents.length === 0)
                          return null;
                        return (
                          <div
                            key={day}
                            className="grid grid-cols-[6rem_1fr] items-baseline gap-4 py-2.5"
                          >
                            <dt className="smallcaps text-[0.875rem] text-ink-soft">
                              {titleCase(day)}
                            </dt>
                            <dd className="font-serif text-[1.05rem] leading-snug text-ink">
                              <SlotTimes
                                events={dayEvents}
                                sectionPage={sectionPage}
                                bulletinUrl={church.bulletin_url}
                              />
                            </dd>
                          </div>
                        );
                      })}

                      {patterned.map((row) => (
                        <div
                          key={row.key}
                          className="grid grid-cols-[6rem_1fr] items-baseline gap-4 py-2.5"
                        >
                          {/* In the one-off rows' red, so every row that
                              doesn't come round each week reads apart from
                              the plain weekday rows above. */}
                          <dt className="smallcaps text-[0.875rem] leading-tight text-rubric">
                            {row.label}
                          </dt>
                          <dd className="font-serif text-[1.05rem] leading-snug text-ink">
                            <SlotTimes
                              events={row.events}
                              sectionPage={sectionPage}
                              bulletinUrl={church.bulletin_url}
                            />
                            {row.qualifier ? (
                              <span className={`block ${ANNOTATION_CLASS} text-ink-faint`}>
                                {row.qualifier}
                              </span>
                            ) : null}
                          </dd>
                        </div>
                      ))}

                      {specificDate.length > 0 ? (
                        <>
                          {specificDate.map((event) => (
                            <div
                              key={event.id}
                              className="grid grid-cols-[6rem_1fr] items-baseline gap-4 py-2.5"
                            >
                              {/* The weekday with its date beneath, so a
                                  one-off service reads apart from the
                                  weekly rows above it. */}
                              <dt className="smallcaps text-[0.875rem] leading-tight text-rubric">
                                {event.date ? (
                                  <>
                                    {formatEventDate(event.date).replace(
                                      /, .+$/,
                                      "",
                                    )}
                                    <span className="block">
                                      {formatMonthDay(event.date)}
                                    </span>
                                  </>
                                ) : (
                                  "Special"
                                )}
                              </dt>
                              <dd className="font-serif text-[1.05rem] leading-snug text-ink">
                                <span className="tabular-nums">
                                  {formatTimeValue(event)}
                                </span>
                                <EventNote note={event.note} />
                                {event.page_number !== sectionPage ? (
                                  <PageRef
                                    event={event}
                                    bulletinUrl={church.bulletin_url}
                                  />
                                ) : null}
                              </dd>
                            </div>
                          ))}
                        </>
                      ) : null}
                    </dl>
                  </section>
                );
              })}
            </div>
          </div>
        ) : null}

        {/* After the times, which are what the page is for: where the church
         *  is, among its neighbours, and the way into the full map. */}
        {map ? (
          <section
            aria-labelledby="church-map-heading"
            className="rise-in mx-auto mt-12 max-w-4xl"
            style={{ animationDelay: "120ms" }}
          >
            <h2
              id="church-map-heading"
              className="mb-5 font-display text-[1.75rem] leading-none font-normal text-ink"
            >
              Map
            </h2>
            {/* Keyed by church: when the app goes from one church's page
             *  straight to another's, the live map starts again on the new
             *  church. */}
            <CityMapPreview
              key={church.id}
              label={name}
              map={map}
              churchId={church.id}
              live={liveMap}
            />
          </section>
        ) : null}

        <div className="mx-auto mt-16 max-w-2xl">
          <Fleuron solo className="text-brass" />
          <p className="mt-4 text-center font-serif text-[0.9rem] text-ink-faint">
            {churchDisclaimer(church)}
          </p>
        </div>
      </div>
    </main>
    <footer className="bg-paper pb-[calc(3rem+var(--safe-area-inset-bottom))] text-center">
      <Link to={CHURCH_INDEX_PATH} className="rubric-link font-serif text-[0.9375rem]">
        {CHURCH_LIST}
      </Link>
    </footer>
    </>
  );
}
