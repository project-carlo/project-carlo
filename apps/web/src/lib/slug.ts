/**
 * URL slug for a city name: "Niagara Falls" -> "niagara-falls",
 * "St. Johnsville" -> "st-johnsville", "Cañon" -> "canon". Shared by
 * scripts/generate-places.ts, so it must stay free of app imports.
 */
export function citySlug(city: string): string {
  return city
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/['’]/g, "")
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
