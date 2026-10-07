import type { Ref } from "react";
import { ExpandIcon } from "@/components/icons";
import { CITY_MAP_CHIP_CLASS } from "@/lib/cityMap";

const POSITION_CLASS = "absolute top-3 right-3 z-[950]";

/**
 * The city map's Expand button, top right. The still preview draws it too,
 * as an inert copy on the same pixels, so the live one replaces it unseen.
 */
export function CityMapExpandChip({
  onClick,
  buttonRef,
  className = "",
}: {
  /** Leave out for the still preview's copy. */
  onClick?: () => void;
  buttonRef?: Ref<HTMLButtonElement>;
  className?: string;
}) {
  const content = (
    <>
      <ExpandIcon className="size-3.5" />
      Expand map
    </>
  );
  if (!onClick) {
    return (
      <span
        aria-hidden="true"
        className={`${CITY_MAP_CHIP_CLASS} ${POSITION_CLASS} pointer-events-none ${className}`}
      >
        {content}
      </span>
    );
  }
  return (
    <button
      ref={buttonRef}
      type="button"
      onClick={onClick}
      className={`${CITY_MAP_CHIP_CLASS} ${POSITION_CLASS} ${className}`}
    >
      {content}
    </button>
  );
}
