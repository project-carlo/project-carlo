import { useQuery } from "@tanstack/react-query";
import { fetchSnapshot } from "../api";
import {
  buildBrowseEntries,
  createPlaceIndex,
  type PlaceIndex,
} from "../lib/browse";

/** Every church with its weekly schedule, built once from the snapshot. */
async function loadPlaceIndex(): Promise<PlaceIndex> {
  const snapshot = await fetchSnapshot();
  return createPlaceIndex(
    buildBrowseEntries(snapshot.churches, (id) => snapshot.eventsOf(id)),
  );
}

/**
 * The browse pages' data (and the church page's "nearby churches"), read from
 * the same snapshot the map uses. Cached for the life of the page: the
 * snapshot never changes underneath a session.
 */
export function usePlaceIndex() {
  return useQuery({
    queryKey: ["place-index"],
    queryFn: loadPlaceIndex,
    staleTime: Infinity,
  });
}
