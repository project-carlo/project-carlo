/**
 * The four browse pages as pure presentational components over the models in
 * src/lib/browse.ts. The client routes (BrowseRoutes.tsx) and the prerenderer
 * (src/prerender/StaticBrowsePage.tsx) render these same components.
 */
import { ExternalLinkIcon } from "@/components/icons";
import { SiteLink } from "@/components/SiteLink";
import {
  groupTownsByLetter,
  serviceByDay,
  weekendRows,
  type CityModel,
  type DioceseIndexModel,
  type DioceseModel,
  type PlaceSection,
  type StateModel,
} from "@/lib/browse";
import {
  BrowseShell,
  ChurchList,
  DioceseCards,
  Freshness,
  HighlightGrid,
  JumpLinks,
  NearbyList,
  PageHeader,
  SectionHeading,
  ServiceSection,
  WeekendTable,
  type JumpLink,
} from "./parts";

export interface BrowseViewProps {
  /** ISO date the schedules were last refreshed, when known. */
  updated: string | null;
  mapHref?: string;
  showAbout?: boolean;
}

/** The Mass / Confession / Adoration sections every place page carries. */
function ServiceSections({
  section,
  showCity,
  place,
}: {
  section: PlaceSection;
  showCity: boolean;
  place: string;
}) {
  const confession = serviceByDay(section.entries, "confession");
  const adoration = serviceByDay(section.entries, "adoration");
  return (
    <>
      <section aria-labelledby="mass" className="mb-14">
        <SectionHeading id="mass" aside="Saturday vigil and Sunday Masses">
          This weekend
        </SectionHeading>
        <WeekendTable rows={weekendRows(section.entries)} showCity={showCity} />
      </section>
      <ServiceSection
        id="confession"
        title="Confession"
        days={confession}
        showCity={showCity}
        empty={`No Confession times are listed for ${place} yet.`}
      />
      <ServiceSection
        id="adoration"
        title="Adoration"
        days={adoration}
        showCity={showCity}
        empty={`No Adoration times are listed for ${place} yet.`}
      />
    </>
  );
}

const SERVICE_JUMPS: JumpLink[] = [
  { href: "#mass", label: "Mass" },
  { href: "#confession", label: "Confession" },
  { href: "#adoration", label: "Adoration" },
];

// ------------------------------------------------------------ city page

export function CityView({
  model,
  updated,
  mapHref,
  showAbout,
}: BrowseViewProps & { model: CityModel }) {
  return (
    <BrowseShell mapHref={mapHref} showAbout={showAbout}>
      <PageHeader
        crumbs={model.crumbs}
        title={
          <>
            Mass &amp; Confession Times in {model.city}, {model.state}
          </>
        }
        lede={model.intro}
      />
      <JumpLinks
        links={[
          ...SERVICE_JUMPS,
          { href: "#churches", label: "Churches" },
          ...(model.nearby.length > 0 ? [{ href: "#nearby", label: "Nearby" }] : []),
        ]}
      />
      <HighlightGrid highlights={model.highlights} />
      <ServiceSections section={model} showCity={false} place={model.city} />

      <section aria-labelledby="churches" className="mb-14">
        <SectionHeading
          id="churches"
          aside={`${model.stats.churchCount} Catholic churches in ${model.city}`}
        >
          Churches in {model.city}
        </SectionHeading>
        <ChurchList items={model.churches} />
      </section>

      {model.nearby.length > 0 ? (
        <section aria-labelledby="nearby" className="mb-14">
          <SectionHeading
            id="nearby"
            aside="Within about 10 miles of the city centre"
          >
            Nearby, outside {model.city}
          </SectionHeading>
          <NearbyList items={model.nearby} />
        </section>
      ) : null}

      <p className="text-center font-serif text-[0.95rem] text-ink-soft">
        More in{" "}
        <SiteLink spa href={model.crumbs[1].path} className="rubric-link">
          {model.stateName}
        </SiteLink>
        .
      </p>
      <Freshness updated={updated} />
    </BrowseShell>
  );
}

// --------------------------------------------------------- diocese page

export function DioceseView({
  model,
  updated,
  mapHref,
  showAbout,
}: BrowseViewProps & { model: DioceseModel }) {
  const { diocese } = model;
  return (
    <BrowseShell mapHref={mapHref} showAbout={showAbout}>
      <PageHeader
        crumbs={model.crumbs}
        title={diocese.shortName}
        lede={
          <>
            {diocese.description ? <>{diocese.description} </> : null}
            {model.intro}
          </>
        }
      >
        {diocese.website ? (
          <p className="mt-5">
            <a
              href={diocese.website}
              target="_blank"
              rel="noopener noreferrer"
              className="rubric-link inline-flex items-center gap-2 font-serif text-[0.9375rem]"
            >
              <ExternalLinkIcon className="size-3.5" />
              Visit the diocesan website
            </a>
          </p>
        ) : null}
      </PageHeader>
      <JumpLinks links={[{ href: "#towns", label: "Towns" }, ...SERVICE_JUMPS]} />
      <HighlightGrid highlights={model.highlights} />

      <section aria-labelledby="towns" className="mb-14">
        <SectionHeading
          id="towns"
          aside={`${model.stats.churchCount} churches in ${model.stats.townCount} towns`}
        >
          Churches by town
        </SectionHeading>
        <div className="space-y-8">
          {model.towns.map((town) => (
            <div key={town.slug}>
              <h3 className="mb-1 flex items-baseline gap-3 border-b border-rule-strong pb-2">
                {town.cityPagePath ? (
                  <SiteLink
                    spa
                    href={town.cityPagePath}
                    className="rubric-link smallcaps text-[1rem]"
                  >
                    {town.city}
                  </SiteLink>
                ) : (
                  <span className="smallcaps text-[1rem] text-ink">{town.city}</span>
                )}
                <span className="font-serif text-[0.85rem] text-ink-faint">
                  {town.items.length}{" "}
                  {town.items.length === 1 ? "church" : "churches"}
                  {town.cityPagePath ? " · all times" : ""}
                </span>
              </h3>
              <ChurchList items={town.items} underHeading />
            </div>
          ))}
        </div>
      </section>

      <ServiceSections section={model} showCity place={diocese.shortName} />
      <Freshness updated={updated} />
    </BrowseShell>
  );
}

// ------------------------------------------------------- diocese index

export function DioceseIndexView({
  model,
  updated,
  mapHref,
  showAbout,
}: BrowseViewProps & { model: DioceseIndexModel }) {
  return (
    <BrowseShell mapHref={mapHref} showAbout={showAbout}>
      <PageHeader
        crumbs={model.crumbs}
        title="Dioceses"
        lede={`${model.churchCount} Catholic churches across ${model.cards.length} dioceses in New York State. Choose a diocese to see its churches by town, with this weekend’s Mass times and Confession and Adoration schedules.`}
      />
      <DioceseCards cards={model.cards} />
      <p className="mt-10 text-center font-serif text-[0.95rem] text-ink-soft">
        Or browse{" "}
        <SiteLink spa href="/mass-times/ny/" className="rubric-link">
          every town in New York
        </SiteLink>{" "}
        or the{" "}
        <SiteLink href="/churches/" className="rubric-link">
          A–Z list of churches
        </SiteLink>
        .
      </p>
      <Freshness updated={updated} />
    </BrowseShell>
  );
}

// ------------------------------------------------------------ state hub

export function StateView({
  model,
  updated,
  mapHref,
  showAbout,
}: BrowseViewProps & { model: StateModel }) {
  const letters = groupTownsByLetter(model.towns);
  return (
    <BrowseShell mapHref={mapHref} showAbout={showAbout}>
      <PageHeader
        crumbs={model.crumbs}
        title={<>Mass Times in {model.stateName}</>}
        lede={model.intro}
      />
      <JumpLinks
        links={[
          { href: "#dioceses", label: "Dioceses" },
          { href: "#cities", label: "Cities" },
          { href: "#towns", label: "All towns A–Z" },
        ]}
      />
      <HighlightGrid highlights={model.highlights} />

      <section aria-labelledby="dioceses" className="mb-14">
        <SectionHeading id="dioceses" aside="Browse by diocese">
          Dioceses
        </SectionHeading>
        <DioceseCards cards={model.dioceseCards} />
      </section>

      <section aria-labelledby="cities" className="mb-14">
        <SectionHeading
          id="cities"
          aside={`${model.cityPages.length} cities with several churches`}
        >
          Cities
        </SectionHeading>
        <ul className="grid grid-cols-1 gap-x-8 sm:grid-cols-2 md:grid-cols-3">
          {model.cityPages.map((c) => (
            <li
              key={c.path}
              className="flex items-baseline justify-between gap-3 border-b border-rule py-2"
            >
              <SiteLink spa href={c.path} className="rubric-link font-serif text-[1.05rem]">
                {c.city}
              </SiteLink>
              <span className="font-serif text-[0.85rem] text-ink-faint tabular-nums">
                {c.count}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section aria-labelledby="towns" className="mb-14">
        <SectionHeading
          id="towns"
          aside={`${model.towns.length} towns, A–Z`}
        >
          All towns
        </SectionHeading>
        <nav aria-label="Jump to letter" className="mb-6">
          <ul className="flex flex-wrap gap-x-3 gap-y-1">
            {letters.map((l) => (
              <li key={l.letter}>
                <a
                  href={`#letter-${l.letter}`}
                  className="rubric-link smallcaps text-[1rem]"
                >
                  {l.letter}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <div className="space-y-6">
          {letters.map((l) => (
            <div key={l.letter}>
              <h3
                id={`letter-${l.letter}`}
                className="mb-2 scroll-mt-20 border-b border-rule-strong pb-1 font-display text-[1.25rem] leading-none text-ink"
              >
                {l.letter}
              </h3>
              <ul className="gap-x-8 sm:columns-2 md:columns-3">
                {l.towns.map((t) => (
                  <li key={t.slug} className="break-inside-avoid py-1 font-serif text-[1rem] leading-snug">
                    <SiteLink spa href={t.path} className="rubric-link">
                      {t.city}
                    </SiteLink>
                    {t.churchName ? (
                      <span className="block text-[0.85rem] italic text-ink-faint">
                        {t.churchName}
                      </span>
                    ) : (
                      <span className="ml-1.5 text-[0.85rem] text-ink-faint">
                        ({t.count} churches)
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
      <Freshness updated={updated} />
    </BrowseShell>
  );
}
