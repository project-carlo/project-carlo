import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useMapHref } from "@/hooks/useMapHref";
import { canonicalForPath } from "@/lib/seo";

export function AboutPage() {
  useDocumentMeta({
    title: "About · Project Carlo",
    description:
      "About Project Carlo — a directory of Catholic parishes with Mass, Confession, and Adoration times parsed from weekly bulletins.",
    canonicalUrl: canonicalForPath("/about"),
  });
  const mapHref = useMapHref();

  return (
    <div className="flex min-h-svh flex-col bg-paper">
      <SiteHeader mapHref={mapHref} showAbout />
      <main className="flex-1 px-4 py-8 sm:py-12">
      <div className="mx-auto flex w-full max-w-[40rem] flex-col gap-8">
        <section className="space-y-3">
          <h1 className="font-display text-[2rem] leading-[1.1] text-ink sm:text-[2.5rem]">
            About
          </h1>
          <p className="font-serif text-base text-ink-soft">
            Placeholder intro paragraph. Replace this copy with a short
            description of what Project Carlo is and who it's for.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="smallcaps text-[1.0625rem] text-ink">What this is</h2>
          <p className="font-serif text-base text-ink-soft">
            Placeholder body. Lorem ipsum dolor sit amet, consectetur adipiscing
            elit. Replace with a paragraph or two explaining the project's
            purpose.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="smallcaps text-[1.0625rem] text-ink">Why we built it</h2>
          <p className="font-serif text-base text-ink-soft">
            Placeholder body. Describe the motivation behind the project — what
            problem it solves and who benefits.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="smallcaps text-[1.0625rem] text-ink">Get in touch</h2>
          <p className="font-serif text-base text-ink-soft">
            Placeholder body. Add contact details, social links, or a feedback
            call-to-action here.
          </p>
        </section>
      </div>
      </main>
      <SiteFooter mapHref={mapHref} showAbout />
    </div>
  );
}
