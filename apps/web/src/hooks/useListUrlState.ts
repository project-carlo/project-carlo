import { useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { parseListSort, type ListSort } from "../lib/churchList";

export type MobileView = "map" | "list";

/**
 * The results list's two URL params: `view=list` (phones only — desktop always
 * shows the list beside the map) and `sort=soonest`. Both are omitted at their
 * defaults. Switching view pushes a history entry so Back leaves the list the
 * way it does on any other screen; sort just replaces.
 */
export function useListUrlState() {
  const [searchParams, setSearchParams] = useSearchParams();
  const view: MobileView = searchParams.get("view") === "list" ? "list" : "map";
  const sort = parseListSort(searchParams.get("sort"));

  const setView = useCallback(
    (next: MobileView) => {
      setSearchParams((prev) => {
        const params = new URLSearchParams(prev);
        if (next === "list") params.set("view", "list");
        else params.delete("view");
        return params;
      });
    },
    [setSearchParams],
  );

  const setSort = useCallback(
    (next: ListSort) => {
      setSearchParams(
        (prev) => {
          const params = new URLSearchParams(prev);
          if (next === "nearest") params.delete("sort");
          else params.set("sort", next);
          return params;
        },
        { replace: true },
      );
    },
    [setSearchParams],
  );

  return { view, sort, setView, setSort };
}
