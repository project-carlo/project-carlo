import { Link } from "react-router-dom";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { Fleuron } from "@/components/Fleuron";
import { SiteHeader } from "@/components/SiteHeader";
import { dioceseCoverage, diocesePath, type Diocese } from "@/lib/dioceses";
import { CHURCH_INDEX_PATH } from "@/lib/seo";
import { ALL_CHURCHES, DIOCESES, SOURCE_PHRASE } from "@/copy";

/** What the list of dioceses shows of each. */
export type DioceseIndexEntry = Pick<Diocese, "slug" | "label" | "churches" | "cities">;

/**
 * The list of dioceses: those the site covers in full, each linking its
 * page. Prerendered (StaticDioceseIndexPage) and in the app
 * (DioceseIndexPage) alike.
 */
export function DioceseIndexContent({ dioceses }: { dioceses: DioceseIndexEntry[] }) {
  return (
    <>
      <main className="min-h-svh bg-paper">
        <SiteHeader />

        <div className="mx-auto w-full max-w-3xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
          <section className="mx-auto max-w-2xl text-center">
            <Breadcrumbs
              className="mb-6"
              crumbs={[{ label: ALL_CHURCHES, to: CHURCH_INDEX_PATH }, { label: DIOCESES }]}
            />
            <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
              {DIOCESES}
            </h1>
            <p className="mt-4 font-serif text-[1rem] text-ink-soft">
              Catholic churches by diocese, with Mass, Confession, and Adoration
              times {SOURCE_PHRASE}. Project Carlo is independent and not
              affiliated with any diocese.
            </p>
          </section>

          <ul className="mt-10 divide-y divide-rule border-y border-rule">
            {dioceses.map((diocese) => (
              <li key={diocese.slug} className="py-5 text-center">
                <h2 className="font-display text-[1.75rem] leading-tight font-normal text-ink">
                  <Link to={diocesePath(diocese.slug)} className="hover:text-rubric-deep">
                    {diocese.label}
                  </Link>
                </h2>
                <p className="mt-1 font-serif text-[0.95rem] text-ink-soft">
                  {dioceseCoverage(diocese)}
                </p>
              </li>
            ))}
          </ul>

          <div className="mx-auto mt-16 max-w-2xl">
            <Fleuron solo className="text-brass" />
          </div>
        </div>
      </main>
      <footer className="bg-paper pb-[calc(3rem+var(--safe-area-inset-bottom))] text-center">
        <Link to={CHURCH_INDEX_PATH} className="rubric-link font-serif text-[0.9375rem]">
          {ALL_CHURCHES}
        </Link>
      </footer>
    </>
  );
}
