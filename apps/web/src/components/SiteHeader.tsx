import { Link } from "react-router-dom";
import { ArrowLeftIcon } from "@/components/icons";
import { Masthead } from "@/components/Masthead";
import { useHomeHref } from "@/hooks/useHomeHref";

/** The sticky strip atop the church and city pages: "Back to map" and the wordmark. */
export function SiteHeader() {
  const homeHref = useHomeHref();
  return (
    <header className="sticky top-0 z-40 border-b border-rule-strong bg-paper/95 backdrop-blur supports-[backdrop-filter]:bg-paper/85">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 pt-[calc(0.85rem+var(--safe-area-inset-top))] pb-3">
        <Link to={homeHref} className="rubric-link font-serif text-[0.9375rem]">
          <ArrowLeftIcon className="size-3.5" />
          Back to map
        </Link>
        <Masthead compact />
      </div>
    </header>
  );
}
