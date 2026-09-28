const CURRENT_LOCATION_PHRASES = [
  "current location",
  "use current location",
  "use my current location",
  "use your current location",
  "my current location",
  "my location",
  "near me",
  "nearby",
  "locate me",
  "where am i",
];

/** Fewest characters that can signal intent, so "n" or "l" don't trigger it. */
const MIN_INTENT_LENGTH = 3;

/**
 * Whether the "use your current location" suggestion belongs in the dropdown.
 * It's the default on an empty field; once the user types, it stays only if
 * what they've typed is the start of a phrase asking for their location
 * ("cur", "near m", "my loc"), so it doesn't sit above every place result.
 */
export function wantsCurrentLocation(query: string): boolean {
  const normalized = query.trim().toLowerCase().replace(/\s+/g, " ");
  if (normalized.length === 0) return true;
  if (normalized.length < MIN_INTENT_LENGTH) return false;
  return CURRENT_LOCATION_PHRASES.some((phrase) =>
    phrase.startsWith(normalized),
  );
}
