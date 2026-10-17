import {
  createContext,
  useContext,
  useEffect,
  useImperativeHandle,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import type { ReactNode, Ref } from "react";
import { createPortal } from "react-dom";
import L from "leaflet";
import type {
  DivIcon,
  Icon,
  LatLngExpression,
  LatLngTuple,
  Layer,
  LeafletEventHandlerFnMap,
  Map as LeafletMap,
  MapOptions,
  Marker as LeafletMarker,
  PolylineOptions,
  TileLayerOptions,
} from "leaflet";
import { LeafletMapContext, useMap } from "@/lib/leafletMap";

/*
 * The few Leaflet layers the map needs, as React components, in place of
 * react-leaflet: its Hippocratic License adds restrictions on use that the
 * AGPL, this project's license, doesn't allow passing on. Each creates
 * its Leaflet object once, on its first render, and adds it to the map (or
 * binds it to its marker) in an effect, taking it off again in the effect's
 * cleanup, so React's StrictMode, which runs a new component's effects twice,
 * leaves one copy on the map. A prop the component doesn't list as updatable
 * is read only as the object is created.
 */

/** The marker a `Popup` inside a `Marker` is bound to. */
const PopupSourceContext = createContext<LeafletMarker | null>(null);

/**
 * Adds `layer` to the map while mounted, with `eventHandlers` bound to it.
 * The handlers are bound again whenever the object changes, so memoize it.
 */
function useLayer(layer: Layer, eventHandlers?: LeafletEventHandlerFnMap) {
  const map = useMap();
  useEffect(() => {
    if (!eventHandlers) return;
    layer.on(eventHandlers);
    return () => {
      layer.off(eventHandlers);
    };
  }, [layer, eventHandlers]);
  useEffect(() => {
    map.addLayer(layer);
    return () => {
      map.removeLayer(layer);
    };
  }, [map, layer]);
}

interface MapContainerProps extends Omit<MapOptions, "center" | "zoom"> {
  center: LatLngExpression;
  zoom: number;
  /** Called with the map once it has its first view, before any layer or
   *  listener is added to it. */
  whenReady?: (map: LeafletMap) => void;
  className?: string;
  /** Layers and behaviors, rendered once the map exists so they can `useMap`. */
  children?: ReactNode;
  /** Gets the map once it exists, and null before then and after it's gone. */
  ref?: Ref<LeafletMap | null>;
}

/**
 * A Leaflet map on a div of its own. Everything but the children is read
 * once, as the map is created: from then on the view is the visitor's to
 * move, and a class React set again would wipe the ones Leaflet adds to
 * the same element.
 */
export function MapContainer({
  center,
  zoom,
  whenReady,
  className,
  children,
  ref,
  ...options
}: MapContainerProps) {
  const [initial] = useState(() => ({
    center,
    zoom,
    whenReady,
    className,
    options,
  }));
  const containerRef = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<LeafletMap | null>(null);
  useImperativeHandle<LeafletMap | null, LeafletMap | null>(
    ref,
    () => map,
    [map],
  );

  // A layout effect, so the map exists in the same commit as its div, before
  // the browser paints the empty box.
  useLayoutEffect(() => {
    const instance = L.map(containerRef.current!, initial.options);
    instance.setView(initial.center, initial.zoom);
    initial.whenReady?.(instance);
    setMap(instance);
    return () => {
      instance.remove();
    };
  }, [initial]);

  return (
    <div ref={containerRef} className={initial.className}>
      {map ? (
        <LeafletMapContext.Provider value={map}>
          {children}
        </LeafletMapContext.Provider>
      ) : null}
    </div>
  );
}

/** A tile layer, with its URL and options read once. */
export function TileLayer({
  url,
  ...options
}: TileLayerOptions & { url: string }) {
  const [layer] = useState(() => L.tileLayer(url, options));
  useLayer(layer);
  return null;
}

/**
 * A polygon. Its options are read once, as it's created, which is the only
 * way to give it a `className`: Leaflet's setStyle ignores that one.
 */
export function Polygon({
  positions,
  ...options
}: PolylineOptions & { positions: LatLngExpression[] }) {
  const [polygon] = useState(() => L.polygon(positions, options));
  const appliedRef = useRef(positions);
  useEffect(() => {
    if (positions === appliedRef.current) return;
    appliedRef.current = positions;
    polygon.setLatLngs(positions);
  }, [polygon, positions]);
  useLayer(polygon);
  return null;
}

interface MarkerProps {
  position: LatLngTuple;
  icon: Icon | DivIcon;
  zIndexOffset?: number;
  /** Read once, as the marker is created. */
  title?: string;
  /** Bound again whenever the object changes, so memoize it. */
  eventHandlers?: LeafletEventHandlerFnMap;
  /** A `Popup`, bound to this marker. */
  children?: ReactNode;
  ref?: Ref<LeafletMarker | null>;
}

/**
 * A marker. Its position, icon and z-index offset follow their props, but
 * are passed on only when they change, and the position by value, not by
 * array: each of Leaflet's setters redraws the pin (setIcon rebuilds its
 * DOM), and a fresh array literal on every render would otherwise move it
 * to where it already is.
 */
export function Marker({
  position,
  icon,
  zIndexOffset = 0,
  title,
  eventHandlers,
  children,
  ref,
}: MarkerProps) {
  const [lat, lng] = position;
  const [marker] = useState(() =>
    L.marker([lat, lng], { icon, zIndexOffset, title }),
  );
  useImperativeHandle(ref, () => marker, [marker]);

  const appliedRef = useRef({ lat, lng, icon, zIndexOffset });
  useEffect(() => {
    const applied = appliedRef.current;
    if (lat !== applied.lat || lng !== applied.lng) {
      marker.setLatLng([lat, lng]);
    }
    if (icon !== applied.icon) marker.setIcon(icon);
    if (zIndexOffset !== applied.zIndexOffset) {
      marker.setZIndexOffset(zIndexOffset);
    }
    appliedRef.current = { lat, lng, icon, zIndexOffset };
  }, [marker, lat, lng, icon, zIndexOffset]);
  useLayer(marker, eventHandlers);

  return children == null ? null : (
    <PopupSourceContext.Provider value={marker}>
      {children}
    </PopupSourceContext.Provider>
  );
}

/**
 * The popup of the `Marker` it's rendered in, with its children rendered
 * into Leaflet's popup through a portal.
 *
 * Leaflet builds the popup's DOM only as it first opens, so the children
 * render only from then on. They stay mounted while it's closed: Leaflet
 * fades a closing popup out with its content still in it, and reuses the
 * same DOM the next time it opens.
 */
export function Popup({
  minWidth,
  maxWidth,
  children,
}: {
  minWidth: number;
  maxWidth: number;
  children?: ReactNode;
}) {
  const map = useMap();
  const source = useContext(PopupSourceContext);
  if (!source) throw new Error("A Popup must be rendered inside a Marker");
  const [popup] = useState(() => L.popup({ minWidth, maxWidth }, source));
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handlers: LeafletEventHandlerFnMap = {
      popupopen: (event) => {
        if (event.popup === popup) setOpen(true);
      },
      popupclose: (event) => {
        if (event.popup === popup) setOpen(false);
      },
    };
    map.on(handlers);
    source.bindPopup(popup);
    return () => {
      map.off(handlers);
      source.unbindPopup();
      map.removeLayer(popup);
    };
  }, [map, source, popup]);

  // A popup can change widths while it's open (the city map's opening or
  // closing over it switches its card); they're set before the effect below
  // lays it out again, so the new card isn't laid out to the old widths.
  useEffect(() => {
    popup.options.minWidth = minWidth;
    popup.options.maxWidth = maxWidth;
  }, [popup, minWidth, maxWidth]);

  // Leaflet sizes the popup, and pans the map to fit it, as it opens, before
  // React has rendered anything into it, and never notices the content
  // change after that. So it's laid out again once the content is in, and
  // after every render that may have changed it.
  useEffect(() => {
    if (open) popup.update();
  }, [popup, open, children]);

  const contentNode = popup
    .getElement()
    ?.querySelector<HTMLElement>(".leaflet-popup-content");
  return contentNode ? createPortal(children, contentNode) : null;
}
