import { useRef, useState } from "react";
import { formatMinutesMissal } from "../utils";
import {
  minutesFromPointerDelta,
  rangeSelectionStyle,
  shiftTimeRange,
} from "./timeRange";

interface TimeRangeSliderProps {
  min: number;
  max: number;
  step?: number;
  value: [number, number];
  onValueChange: (value: [number, number]) => void;
  /** Compact variant for narrow contexts: smaller digit row, no tick row, tighter gap. */
  compact?: boolean;
}

function getPercent(value: number, min: number, max: number): number {
  if (max <= min) return 0;
  return ((value - min) / (max - min)) * 100;
}

const TIME_TICKS = [
  { pct: 25, label: "6 a.m.", offsetRem: 0.25 },
  { pct: 50, label: "noon", offsetRem: 0 },
  { pct: 75, label: "6 p.m.", offsetRem: -0.25 },
];

interface RangeDrag {
  pointerId: number;
  originX: number;
  start: number;
  end: number;
  last: [number, number];
}

export function TimeRangeSlider({
  min,
  max,
  step = 1,
  value,
  onValueChange,
  compact = false,
}: TimeRangeSliderProps) {
  const [start, end] = value;
  const startPercent = getPercent(start, min, max);
  const endPercent = getPercent(end, min, max);
  const formatValue = (minutes: number) =>
    formatMinutesMissal(Math.min(minutes, max - 1));

  const trackRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<RangeDrag | null>(null);
  const onValueChangeRef = useRef(onValueChange);
  onValueChangeRef.current = onValueChange;
  const [dragging, setDragging] = useState(false);

  const span = end - start;
  const canDragRange = span > 0 && span < max - min;
  const { left: rangeLeft, width: rangeWidth } = rangeSelectionStyle(
    startPercent,
    endPercent,
  );

  const applyPointerDelta = (clientX: number) => {
    const drag = dragRef.current;
    const track = trackRef.current;
    if (!drag || !track) return;
    const deltaMinutes = minutesFromPointerDelta(
      clientX - drag.originX,
      track.getBoundingClientRect().width,
      min,
      max,
    );
    const next = shiftTimeRange(
      drag.start,
      drag.end,
      deltaMinutes,
      min,
      max,
      step,
    );
    if (next[0] === drag.last[0] && next[1] === drag.last[1]) return;
    drag.last = next;
    onValueChangeRef.current(next);
  };

  const endDrag = (pointerId: number) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== pointerId) return;
    dragRef.current = null;
    setDragging(false);
  };

  return (
    <div className={compact ? "space-y-3" : "space-y-5"}>
      <div
        className={`grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-baseline gap-4 font-serif text-ink ${
          compact ? "text-[15px]" : "text-base"
        }`}
      >
        <span className="justify-self-start tabular-nums">{formatValue(start)}</span>
        <span className="font-serif text-[0.9375rem] italic text-ink-faint">
          through
        </span>
        <span className="justify-self-end tabular-nums">{formatValue(end)}</span>
      </div>

      <div ref={trackRef} className="relative h-6 px-1">
        <div className="pointer-events-none absolute top-1/2 left-1 right-1 h-[2px] -translate-y-1/2 bg-rule-strong" />
        {TIME_TICKS.map(({ pct, offsetRem }) => (
          <div
            key={pct}
            className="pointer-events-none absolute top-1/2 h-3 w-px -translate-x-1/2 -translate-y-1/2 bg-rule-strong"
            style={{ left: `calc(${pct}% + ${offsetRem}rem)` }}
          />
        ))}
        <div
          data-testid="time-range-selection"
          aria-hidden={!canDragRange}
          aria-label={
            canDragRange
              ? `Move time range, ${formatValue(start)} through ${formatValue(end)}`
              : undefined
          }
          className={`absolute top-0 h-6 select-none touch-none ${
            canDragRange
              ? dragging
                ? "cursor-grabbing"
                : "cursor-grab"
              : "pointer-events-none"
          }`}
          style={{ left: rangeLeft, width: rangeWidth }}
          onPointerDown={(event) => {
            if (!canDragRange || event.button !== 0) return;
            event.preventDefault();
            event.currentTarget.setPointerCapture(event.pointerId);
            dragRef.current = {
              pointerId: event.pointerId,
              originX: event.clientX,
              start,
              end,
              last: [start, end],
            };
            setDragging(true);
          }}
          onPointerMove={(event) => {
            if (dragRef.current?.pointerId !== event.pointerId) return;
            applyPointerDelta(event.clientX);
          }}
          onPointerUp={(event) => endDrag(event.pointerId)}
          onPointerCancel={(event) => endDrag(event.pointerId)}
          onLostPointerCapture={(event) => endDrag(event.pointerId)}
        >
          <div className="pointer-events-none absolute top-1/2 right-0 left-0 h-[3px] -translate-y-1/2 bg-rubric" />
        </div>
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={start}
          aria-label="Earliest start"
          className="time-range-slider missal-focus absolute inset-0 h-6 w-full"
          onChange={(event) => {
            const nextStart = Math.min(Number(event.target.value), end);
            onValueChange([nextStart, end]);
          }}
        />
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={end}
          aria-label="Latest start"
          className="time-range-slider missal-focus absolute inset-0 h-6 w-full"
          onChange={(event) => {
            const nextEnd = Math.max(Number(event.target.value), start);
            onValueChange([start, nextEnd]);
          }}
        />
      </div>

      {compact ? null : (
        <div className="relative h-5 px-1 font-serif text-[0.8125rem] tabular-nums text-ink-soft">
          {TIME_TICKS.map(({ pct, label, offsetRem }) => (
            <span
              key={pct}
              className="absolute top-0 -translate-x-1/2"
              style={{ left: `calc(${pct}% + ${offsetRem}rem)` }}
            >
              {label}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
