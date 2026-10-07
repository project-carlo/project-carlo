import { useEffect, type ReactNode } from "react";
import { useRouteError } from "react-router-dom";
import { RefreshCwIcon } from "@/components/icons";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { isReloadingForNewVersion } from "@/lib/staleDeploy";

interface RouteErrorProps {
  /** Shown while the page reloads for a new deploy. */
  fallback: ReactNode;
}

/**
 * What a route shows when it throws, in place of React Router's developer
 * screen ("Unexpected Application Error!"). A page left over from an earlier
 * deploy is already reloading (see lib/staleDeploy.ts), so it keeps showing
 * the loading state until the new version arrives.
 */
export function RouteError({ fallback }: RouteErrorProps) {
  return isReloadingForNewVersion() ? fallback : <RouteErrorScreen />;
}

function RouteErrorScreen() {
  const error = useRouteError();
  useDocumentMeta({ title: "Something went wrong · Project Carlo", noindex: true });
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="flex min-h-svh flex-col items-center justify-center gap-4 bg-paper px-4 py-8 text-center">
      <h1 className="font-display text-[1.5rem] leading-[1.1] text-ink">
        Something went wrong
      </h1>
      <p className="max-w-md font-serif text-base text-ink-soft">
        This page didn't load properly. Reloading usually fixes it.
      </p>
      <button
        type="button"
        onClick={() => window.location.reload()}
        className="rubric-link inline-flex items-center gap-1.5 font-serif text-[0.9375rem]"
      >
        <RefreshCwIcon className="size-3" />
        Reload
      </button>
    </main>
  );
}
