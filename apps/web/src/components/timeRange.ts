/** Matches `.time-range-slider` thumb size in app.css. */
export const RANGE_THUMB_WIDTH_REM = 1;

function calcPercentPlusRem(percent: number, rem: number): string {
  const roundedRem = Number(rem.toFixed(4));
  if (roundedRem === 0) return `${percent}%`;
  const sign = roundedRem < 0 ? "-" : "+";
  return `calc(${percent}% ${sign} ${Math.abs(roundedRem)}rem)`;
}

/**
 * CSS position for the highlighted range between two native range thumbs.
 *
 * Native thumbs travel across `(trackWidth - thumbWidth)`, so a value of 100%
 * sits half a thumb inside the right edge — not at 100% of the track. The fill
 * is therefore placed from the start-thumb center to the end-thumb center so it
 * never paints past either circle.
 */
export function rangeSelectionStyle(
  startPercent: number,
  endPercent: number,
  thumbWidthRem = RANGE_THUMB_WIDTH_REM,
): { left: string; width: string } {
  const spanPercent = Math.max(endPercent - startPercent, 0);
  const startShiftRem =
    thumbWidthRem / 2 - (startPercent / 100) * thumbWidthRem;
  const spanShiftRem = (spanPercent / 100) * thumbWidthRem;
  return {
    left: calcPercentPlusRem(startPercent, startShiftRem),
    width: calcPercentPlusRem(spanPercent, -spanShiftRem),
  };
}

/** Convert a horizontal pointer delta on the track into minutes. */
export function minutesFromPointerDelta(
  deltaX: number,
  trackWidthPx: number,
  min: number,
  max: number,
): number {
  if (trackWidthPx <= 0 || max <= min) return 0;
  return (deltaX / trackWidthPx) * (max - min);
}

/**
 * Translate a [start, end] window by `delta` minutes, keeping its width
 * and clamping so it stays inside [min, max]. `delta` is snapped to `step`
 * so a drag lands on the same grid as the thumbs.
 */
export function shiftTimeRange(
  start: number,
  end: number,
  delta: number,
  min: number,
  max: number,
  step: number,
): [number, number] {
  const span = end - start;
  if (span < 0 || max <= min) return [start, end];
  if (span > max - min) return [min, max];

  const snappedDelta = step > 0 ? Math.round(delta / step) * step : delta;
  const minStart = min;
  const maxStart = max - span;
  const nextStart = Math.min(Math.max(start + snappedDelta, minStart), maxStart);
  return [nextStart, nextStart + span];
}
