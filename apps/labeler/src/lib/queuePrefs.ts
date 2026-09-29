const UNLABELED_PARISHES_KEY = "labeler:unlabeled-parishes";
const UNLABELED_PARISH_CURSOR_KEY = "labeler:unlabeled-parish-cursor";

const SLUG = /^[a-z0-9-]+$/;
const HASH = /^[0-9a-f]{64}$/;

export function unlabeledParishesOn(): boolean {
  return localStorage.getItem(UNLABELED_PARISHES_KEY) === "1";
}

export function setUnlabeledParishesOn(on: boolean): void {
  localStorage.setItem(UNLABELED_PARISHES_KEY, on ? "1" : "0");
}

/** The bulletin Next last opened while cycling parishes that have no label yet. */
export function unlabeledParishCursor(): { parish: string; hash: string } | undefined {
  const raw = localStorage.getItem(UNLABELED_PARISH_CURSOR_KEY);
  if (!raw) return undefined;
  const slash = raw.indexOf("/");
  if (slash <= 0) return undefined;
  const parish = raw.slice(0, slash);
  const hash = raw.slice(slash + 1);
  return SLUG.test(parish) && HASH.test(hash) ? { parish, hash } : undefined;
}

export function rememberUnlabeledParishCursor(parish: string, hash: string): void {
  localStorage.setItem(UNLABELED_PARISH_CURSOR_KEY, `${parish}/${hash}`);
}
