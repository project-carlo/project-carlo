/**
 * The church map's marker shapes, shared by the map's own markers
 * (ChurchMap) and the city and church pages' still preview (CityMapPreview),
 * which draws the same markers on the same pixels before the live map takes
 * over.
 */

/** The church pin's outline (a 34×42 viewBox, tip at 17,40). */
const CHURCH_PIN_OUTLINE =
  "M17 2C9.27 2 3 8.27 3 16c0 3.7 1.73 7.3 4 10.5C9.5 30 13.5 34.4 15.8 38.6a1.35 1.35 0 0 0 2.4 0C20.5 34.4 24.5 30 27 26.5 29.27 23.3 31 19.7 31 16 31 8.27 24.73 2 17 2Z";

/** The church pin, as SVG markup for a `0 0 34 42` viewBox with `fill="none"`. */
export const CHURCH_PIN_BODY = `<path d="${CHURCH_PIN_OUTLINE}" fill="var(--paper)" stroke="var(--brass)" stroke-width="1.3" />
<circle cx="17" cy="16" r="9.5" fill="none" stroke="var(--rule-strong)" stroke-width="0.8" />
<g stroke="var(--rubric)" stroke-width="2" stroke-linecap="round"><path d="M17 9.5 V 21.5" /><path d="M12.5 13.5 H 21.5" /></g>`;

/**
 * The pin of the church a church page is about: the same shape in rubric,
 * with a paper cross, so it reads apart from its neighbours.
 */
export const CURRENT_CHURCH_PIN_BODY = `<path d="${CHURCH_PIN_OUTLINE}" fill="var(--rubric)" stroke="var(--paper)" stroke-width="1.3" />
<circle cx="17" cy="16" r="9.5" fill="none" stroke="var(--paper)" stroke-opacity="0.45" stroke-width="0.8" />
<g stroke="var(--paper)" stroke-width="2" stroke-linecap="round"><path d="M17 9.5 V 21.5" /><path d="M12.5 13.5 H 21.5" /></g>`;

export const CHURCH_PIN_SIZE: [number, number] = [34, 42];
/** The pin's tip, which sits on the church. */
export const CHURCH_PIN_ANCHOR: [number, number] = [17, 40];

/** From a church pin's tip (its anchor) up to the middle of its round head. */
const PIN_HEAD_RISE = 24;

/** Roundel diameter by cluster size: a lone church's is the size of a pin's
 *  head, a small group's about a pin wide, and a city-sized one reads as
 *  bigger without swallowing its neighbours. */
export function clusterDiameter(count: number): number {
  if (count === 1) return 28;
  if (count < 10) return 32;
  if (count < 50) return 38;
  if (count < 100) return 44;
  return 50;
}

/**
 * A roundel's anchor: centred where a pin's head would be, not on the point
 * itself (where a pin puts its tip), so a roundel splits into pins at the
 * same height.
 */
export function clusterAnchor(size: number): [number, number] {
  return [size / 2, size / 2 + PIN_HEAD_RISE];
}

/** Lifts roundels over pins, so a count is never hidden behind a neighbour's pin. */
export const CLUSTER_Z_INDEX_OFFSET = 500;

/** Lifts a church page's own pin over everything else on its map. */
export const CURRENT_CHURCH_Z_INDEX_OFFSET = 1000;
