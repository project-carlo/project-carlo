import type { ChurchBase, ChurchDetail } from "../types";
import { num, str } from "./sqlRow";

/**
 * The church SELECT list and its row mapper, shared by the SPA (api.ts) and
 * the prerenderer (prerender/queries.ts) so the two cannot end up reading a
 * different set of columns out of the same snapshot.
 */
export const CHURCH_COLUMNS =
  "id, parish_id, slug, name, address_line1, address_line2, city, state, postal_code, latitude, longitude";

/** `CHURCH_COLUMNS` plus the two parish links only the church page shows. */
export const CHURCH_DETAIL_COLUMNS = `${CHURCH_COLUMNS}, homepage_url, bulletin_url`;

export function mapChurchRow(row: Record<string, unknown>): ChurchBase {
  return {
    id: row["id"] as number,
    parish_id: row["parish_id"] as number,
    slug: row["slug"] as string,
    name: str(row["name"]),
    address_line1: str(row["address_line1"]),
    address_line2: str(row["address_line2"]),
    city: str(row["city"]),
    state: str(row["state"]),
    postal_code: str(row["postal_code"]),
    latitude: num(row["latitude"]),
    longitude: num(row["longitude"]),
  };
}

export function mapChurchDetailRow(row: Record<string, unknown>): ChurchDetail {
  return {
    ...mapChurchRow(row),
    homepage_url: str(row["homepage_url"]),
    bulletin_url: str(row["bulletin_url"]),
  };
}
