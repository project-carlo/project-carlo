/**
 * Building blocks shared by the browse pages (diocese index, diocese, state
 * hub, city). Pure presentational components over the data models in
 * src/lib/browse.ts: no hooks, no router hooks, so they render identically in
 * the SPA and in the static prerender.
 */
import type { ReactNode } from "react";
import { Breadcrumbs, type BreadcrumbLink } from "@/components/Breadcrumbs";
import { Fleuron } from "@/components/Fleuron";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteLink } from "@/components/SiteLink";
import { churchPath } from "@/lib/places";
import {
  formatSlot,
  type ChurchListItem,
  type DioceseCard,
  type Highlight,
  type NearbyItem,
  type ServiceDay,
  type WeekendRow,
} from "@/lib/browse";

/** Keep "4:30 p.m." on one line in a narrow table cell. */
function nbsp(times: string): string {
  return times.replace(/ ([ap]\.m\.)/g, "\u00a0$1");
}

const FAINT_DASH = <span className="text-ink-faint">—</span>;

/** Header, main column and footer common to every browse page. */
export function BrowseShell({
  mapHref,
  showAbout,
  children,
}: {
  mapHref?: string;
  showAbout?: boolean;
  children: ReactNode;
}) {
  return (
    <div className="bg-paper">
      <SiteHeader sticky mapHref={mapHref} showAbout={showAbout} />
      <main className="mx-auto w-full max-w-4xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        {children}
      </main>
      <SiteFooter mapHref={mapHref} showAbout={showAbout} />
    </div>
  );
}

/** Breadcrumbs, the page's single `<h1>`, a lede and a fleuron. */
export function PageHeader({
  crumbs,
  title,
  lede,
  children,
}: {
  crumbs: BreadcrumbLink[];
  title: ReactNode;
  lede?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <header className="rise-in text-center">
      <Breadcrumbs items={crumbs} className="mb-6 flex justify-center" />
      <h1 className="font-display text-[clamp(2rem,5.5vw,3.25rem)] leading-[1.06] font-normal tracking-tight text-ink">
        {title}
      </h1>
      {lede ? (
        <p className="mx-auto mt-5 max-w-2xl font-serif text-[1.05rem] leading-relaxed text-ink-soft">
          {lede}
        </p>
      ) : null}
      {children}
      <Fleuron className="my-8" />
    </header>
  );
}

export interface JumpLink {
  href: string;
  label: string;
}

/** In-page anchors: #mass, #confession, #adoration and friends. */
export function JumpLinks({ links }: { links: JumpLink[] }) {
  if (links.length === 0) return null;
  return (
    <nav aria-label="On this page" className="mb-10">
      <ul className="flex flex-wrap justify-center gap-x-6 gap-y-2">
        {links.map((l) => (
          <li key={l.href}>
            <a href={l.href} className="rubric-link smallcaps text-[0.95rem]">
              {l.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export function SectionHeading({
  id,
  children,
  aside,
}: {
  id?: string;
  children: ReactNode;
  aside?: ReactNode;
}) {
  return (
    <div className="mb-5 flex flex-wrap items-baseline gap-x-4 gap-y-1">
      <h2
        id={id}
        className="scroll-mt-20 font-display text-[1.75rem] leading-none font-normal text-ink"
      >
        {children}
      </h2>
      {aside ? (
        <p className="font-serif text-[0.9rem] italic text-ink-faint">{aside}</p>
      ) : null}
    </div>
  );
}

/** Data-driven headline figures: earliest Sunday Mass, daily-Mass count, ... */
export function HighlightGrid({ highlights }: { highlights: Highlight[] }) {
  if (highlights.length === 0) return null;
  return (
    <section aria-label="At a glance" className="mb-12">
      <dl className="grid grid-cols-2 border-t border-l border-rule-strong md:grid-cols-4">
        {highlights.map((h) => (
          <div
            key={h.id}
            className="border-r border-b border-rule-strong px-4 py-4"
          >
            <dt className="smallcaps text-[0.8125rem] leading-tight text-ink-soft">
              {h.label}
            </dt>
            <dd className="mt-2 font-display text-[1.75rem] leading-none text-ink">
              {h.value}
            </dd>
            {h.detail ? (
              <dd className="mt-1.5 font-serif text-[0.875rem] leading-snug text-ink-soft">
                {h.church ? (
                  <>
                    {h.detail.slice(0, h.detail.indexOf(h.church.name))}
                    <SiteLink
                      spa
                      href={churchPath(h.church.slug)}
                      className="rubric-link"
                    >
                      {h.church.name}
                    </SiteLink>
                    {h.detail.slice(
                      h.detail.indexOf(h.church.name) + h.church.name.length,
                    )}
                  </>
                ) : (
                  h.detail
                )}
              </dd>
            ) : null}
          </div>
        ))}
      </dl>
    </section>
  );
}

const TH = "smallcaps pb-2 pr-3 text-left text-[0.875rem] font-normal text-ink-soft";
const TD = "py-2.5 pr-3 align-baseline font-serif text-[1rem] leading-snug text-ink";

/** "This weekend": Saturday vigil and Sunday Masses, one row per church. */
export function WeekendTable({
  rows,
  showCity = false,
}: {
  rows: WeekendRow[];
  showCity?: boolean;
}) {
  return (
    <table className="w-full border-collapse">
      <caption className="sr-only">
        Saturday vigil, Sunday and weekday Mass times by church
      </caption>
      <thead>
        <tr className="border-b border-rule-strong">
          <th scope="col" className={TH}>
            Church
          </th>
          <th scope="col" className={TH}>
            Sat. vigil
          </th>
          <th scope="col" className={TH}>
            Sunday
          </th>
          <th scope="col" className={`${TH} hidden md:table-cell`}>
            Weekdays
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-rule">
        {rows.map((row) => (
          <tr key={row.church.id}>
            <th scope="row" className={`${TD} text-left font-normal`}>
              <SiteLink spa href={churchPath(row.church.slug)} className="rubric-link">
                {row.church.name ?? "Unnamed parish"}
              </SiteLink>
              {showCity && row.church.city ? (
                <span className="block text-[0.85rem] text-ink-faint">
                  {row.church.city}
                </span>
              ) : null}
            </th>
            <td className={`${TD} tabular-nums`}>{nbsp(row.vigil) || FAINT_DASH}</td>
            <td className={`${TD} tabular-nums`}>{nbsp(row.sunday) || FAINT_DASH}</td>
            <td
              className={`${TD} hidden text-[0.95rem] text-ink-soft tabular-nums md:table-cell`}
            >
              {row.weekdays || FAINT_DASH}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

/** Confession or Adoration, day by day, earliest first. */
export function ServiceSection({
  id,
  title,
  days,
  showCity = false,
  empty,
}: {
  id: string;
  title: string;
  days: ServiceDay[];
  showCity?: boolean;
  empty: string;
}) {
  return (
    <section aria-labelledby={id} className="mb-14">
      <SectionHeading
        id={id}
        aside={
          days.length > 0
            ? `${new Set(days.flatMap((d) => d.rows.map((r) => r.church.id))).size} churches`
            : undefined
        }
      >
        {title}
      </SectionHeading>
      {days.length === 0 ? (
        <p className="font-serif text-[0.95rem] text-ink-soft">{empty}</p>
      ) : (
        <div className="divide-y divide-rule border-y border-rule">
          {days.map((day) => (
            <div
              key={day.day}
              className="py-4 sm:grid sm:grid-cols-[7.5rem_1fr] sm:gap-x-4"
            >
              <h3 className="smallcaps text-[0.9rem] text-ink-soft">
                {day.label}
                <span className="block font-serif text-[0.8rem] normal-case tracking-normal text-ink-faint">
                  {day.churchCount} {day.churchCount === 1 ? "church" : "churches"}
                </span>
              </h3>
              <ul className="mt-2 space-y-1.5 sm:mt-0">
                {day.rows.map((row) => (
                  <li
                    key={`${row.church.id}-${row.slot.start}-${row.slot.end}`}
                    className="grid grid-cols-[minmax(6.5rem,9.5rem)_1fr] items-baseline gap-x-3 font-serif text-[1rem] leading-snug"
                  >
                    <span className="tabular-nums text-ink">
                      {formatSlot(row.slot)}
                    </span>
                    <span>
                      <SiteLink
                        spa
                        href={churchPath(row.church.slug)}
                        className="rubric-link"
                      >
                        {row.church.name ?? "Unnamed parish"}
                      </SiteLink>
                      {showCity && row.church.city ? (
                        <span className="text-ink-faint">, {row.church.city}</span>
                      ) : null}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

/** A church, as a list row: name, address, weekend times, other services. */
export function ChurchRow({
  item,
  distance,
}: {
  item: ChurchListItem;
  distance?: string;
}) {
  return (
    <li className="py-3.5 md:grid md:grid-cols-[1fr_auto] md:gap-x-8">
      <div>
        <SiteLink
          spa
          href={item.path}
          className="rubric-link font-serif text-[1.1rem] leading-snug"
        >
          {item.name}
        </SiteLink>
        {item.address ? (
          <p className="mt-0.5 font-serif text-[0.9rem] text-ink-soft">
            {item.address}
          </p>
        ) : null}
      </div>
      <div className="mt-1.5 font-serif text-[0.9rem] leading-snug text-ink-soft md:mt-0 md:text-right">
        {distance ? (
          <p className="smallcaps text-[0.85rem] text-rubric">{distance}</p>
        ) : null}
        <p className="tabular-nums text-ink">{item.weekend || "Mass times not listed"}</p>
        {item.extras ? <p className="text-ink-faint">{item.extras}</p> : null}
      </div>
    </li>
  );
}

export function ChurchList({
  items,
  underHeading = false,
}: {
  items: ChurchListItem[];
  /** The list sits right under a ruled heading: skip its own top rule. */
  underHeading?: boolean;
}) {
  return (
    <ul
      className={`divide-y divide-rule border-b border-rule ${underHeading ? "" : "border-t"}`}
    >
      {items.map((item) => (
        <ChurchRow key={item.church.id} item={item} />
      ))}
    </ul>
  );
}

/** "Nearby, outside {city}" and the church page's "Nearby churches". */
export function NearbyList({ items }: { items: NearbyItem[] }) {
  return (
    <ul className="divide-y divide-rule border-y border-rule">
      {items.map((item) => (
        <ChurchRow key={item.church.id} item={item} distance={item.distanceLabel} />
      ))}
    </ul>
  );
}

/** Diocese cards: shared by the diocese index and the state hub. */
export function DioceseCards({ cards }: { cards: DioceseCard[] }) {
  return (
    <ul className="grid gap-5 md:grid-cols-2">
      {cards.map((card) => (
        <li key={card.diocese.key} className="border border-rule-strong">
          <SiteLink
            spa
            href={card.path}
            className="missal-focus block px-5 pt-5 pb-3 transition-colors hover:bg-paper-deep/50"
          >
            <span className="block font-display text-[1.5rem] leading-tight text-ink">
              {card.diocese.shortName}
            </span>
            <span className="smallcaps mt-1 block text-[0.9rem] text-ink-soft">
              {card.churchCount} {card.churchCount === 1 ? "church" : "churches"} in{" "}
              {card.townCount} {card.townCount === 1 ? "town" : "towns"}
            </span>
            {card.diocese.description ? (
              <span className="mt-3 block font-serif text-[0.95rem] leading-relaxed text-ink-soft">
                {card.diocese.description}
              </span>
            ) : null}
          </SiteLink>
          {card.topTowns.length > 0 ? (
            <p className="px-5 pb-4 font-serif text-[0.9rem] text-ink-faint">
              Largest towns:{" "}
              {card.topTowns.map((t, i) => (
                <span key={t.path}>
                  {i > 0 ? ", " : ""}
                  <SiteLink spa href={t.path} className="rubric-link">
                    {t.city}
                  </SiteLink>{" "}
                  ({t.count})
                </span>
              ))}
            </p>
          ) : (
            <div className="pb-2" />
          )}
        </li>
      ))}
    </ul>
  );
}

function formatLongDate(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) return iso;
  return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])).toLocaleDateString(
    "en-US",
    { year: "numeric", month: "long", day: "numeric" },
  );
}

/** Closing note: where the times come from and how fresh the page is. */
export function Freshness({ updated }: { updated: string | null }) {
  return (
    <div className="mt-6">
      <Fleuron solo className="text-brass" />
      <p className="mt-4 text-center font-serif text-[0.9rem] text-ink-faint">
        {updated
          ? `Schedules read from parish bulletins and refreshed ${formatLongDate(updated)}. `
          : "Schedules are read from each parish’s latest weekly bulletin. "}
        Times are extracted with AI and may not always be accurate; please
        confirm with the parish before attending.
      </p>
    </div>
  );
}
