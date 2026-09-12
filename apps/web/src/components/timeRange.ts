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
