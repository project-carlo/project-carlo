import { Link } from "react-router-dom";
import { MapIcon } from "@/components/icons";
import { ALL_CHURCHES, MAP_LINK } from "@/copy";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useHomeHref } from "@/hooks/useHomeHref";
import { CHURCH_INDEX_PATH } from "@/lib/seo";

interface NotFoundPageProps {
  title?: string;
  message?: string;
}

export function NotFoundPage({
  title = "Page not found",
  message = "That link may be out of date.",
}: NotFoundPageProps) {
  useDocumentMeta({ title: `${title} · Project Carlo`, noindex: true });
  const homeHref = useHomeHref();

  return (
    <main className="flex min-h-svh flex-col items-center justify-center gap-4 bg-paper px-4 py-8 text-center">
      <h1 className="font-display text-[1.5rem] leading-[1.1] text-ink">
        {title}
      </h1>
      <p className="max-w-md font-serif text-base text-ink-soft">{message}</p>
      {/* Two ways on: the map, or the list (a plain link: /churches/ is a
          prerendered page the SPA has no route for). */}
      <div className="flex items-baseline gap-5">
        <Link to={homeHref} className="rubric-link font-serif text-[0.9375rem]">
          <MapIcon className="size-3.5" />
          {MAP_LINK}
        </Link>
        <a
          href={CHURCH_INDEX_PATH}
          className="rubric-link font-serif text-[0.9375rem]"
        >
          {ALL_CHURCHES}
        </a>
      </div>
    </main>
  );
}
