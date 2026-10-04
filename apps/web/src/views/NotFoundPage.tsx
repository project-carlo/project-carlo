import { Link } from "react-router-dom";
import { ArrowLeftIcon } from "@/components/icons";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useMapHref } from "@/hooks/useMapHref";
import { isAboutPageEnabled } from "@/lib/featureFlags";

interface NotFoundPageProps {
  title?: string;
  message?: string;
}

export function NotFoundPage({
  title = "Page not found",
  message = "We couldn't find what you were looking for.",
}: NotFoundPageProps) {
  useDocumentMeta({ title: `${title} · Project Carlo`, noindex: true });
  const mapHref = useMapHref();
  const showAbout = isAboutPageEnabled();

  return (
    <div className="flex min-h-svh flex-col bg-paper">
      <SiteHeader mapHref={mapHref} showAbout={showAbout} />
      <main className="flex flex-1 flex-col items-center justify-center gap-4 px-4 py-12 text-center">
        <h1 className="font-display text-[1.5rem] leading-[1.1] text-ink">
          {title}
        </h1>
        <p className="max-w-md font-serif text-base text-ink-soft">{message}</p>
        <Link to={mapHref} className="rubric-link font-serif text-[0.9375rem]">
          <ArrowLeftIcon className="size-3" />
          Back to map
        </Link>
      </main>
      <SiteFooter mapHref={mapHref} showAbout={showAbout} />
    </div>
  );
}
