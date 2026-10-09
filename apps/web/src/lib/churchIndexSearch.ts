/**
 * The all-churches index's search box. It works on the page's markup
 * (ChurchIndexContent) rather than through React, so the prerendered page
 * runs it as a tiny script of its own (src/islands/churchIndex.ts) and the
 * app runs the same code over the same markup. The box is rendered `hidden`
 * and this reveals it, so without JavaScript the page is just the full list.
 *
 * A church matches when every word typed appears in its name or its city's
 * name, ignoring case, accents and punctuation; "St." also matches "saint"
 * (and the reverse), "Mt." "mount". A city stays listed while any of its
 * churches match, and a diocese while any of its cities do. The diocese's
 * name isn't searched: "Buffalo" means the city, not the whole diocese.
 */

const ALIASES: Record<string, string> = {
  st: "saint",
  saint: "st",
  mt: "mount",
  mount: "mt",
};

/** Lowercase, accent- and punctuation-free words, space-separated. */
export function foldSearchText(text: string): string {
  return text
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/['’]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

/** What a query's words are looked for in: the folded text plus aliases. */
export function searchHaystack(text: string): string {
  return foldSearchText(text)
    .split(" ")
    .map((word) => (ALIASES[word] ? `${word} ${ALIASES[word]}` : word))
    .join(" ");
}

/**
 * Wires up the search box inside `root`. Returns a function that unhooks it,
 * leaving the list as it is.
 */
export function attachChurchIndexSearch(root: Document | HTMLElement = document): () => void {
  const input = root.querySelector<HTMLInputElement>("#church-search");
  const status = root.querySelector<HTMLElement>("#church-search-status");
  const empty = root.querySelector<HTMLElement>("#church-search-empty");
  const form = root.querySelector<HTMLFormElement>("#church-search-form");
  if (!form || !input || !status || !empty) return () => {};

  const sections = Array.from(root.querySelectorAll<HTMLElement>("[data-city-group]")).map(
    (section) => {
      const city = searchHaystack(
        section.querySelector("[data-city-heading]")?.textContent ?? "",
      );
      const items = Array.from(section.querySelectorAll("li")).map((item) => ({
        item,
        text: `${searchHaystack(item.textContent ?? "")} ${city}`,
      }));
      return { section, items };
    },
  );
  const total = sections.reduce((n, s) => n + s.items.length, 0);
  const dioceses = Array.from(root.querySelectorAll<HTMLElement>("[data-diocese-group]")).map(
    (diocese) => ({
      diocese,
      cities: Array.from(diocese.querySelectorAll<HTMLElement>("[data-city-group]")),
    }),
  );

  const apply = () => {
    const words = foldSearchText(input.value).split(" ").filter(Boolean);
    let shown = 0;
    for (const { section, items } of sections) {
      let shownHere = 0;
      for (const { item, text } of items) {
        const match = words.every((word) => text.includes(word));
        item.hidden = !match;
        if (match) shownHere++;
      }
      section.hidden = shownHere === 0;
      shown += shownHere;
    }
    for (const { diocese, cities } of dioceses) {
      diocese.hidden = cities.every((city) => city.hidden);
    }
    status.textContent =
      words.length === 0 || shown === 0 ? "" : `Showing ${shown} of ${total} churches.`;
    empty.hidden = words.length === 0 || shown > 0;
    if (!empty.hidden) {
      empty.textContent =
        `No churches or cities match “${input.value.trim()}”. ` +
        "Try fewer words, or just the town.";
    }
  };
  const onKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape" && input.value) {
      input.value = "";
      apply();
    }
  };
  // Filtering is live; Enter shouldn't reload the page.
  const onSubmit = (event: Event) => event.preventDefault();

  input.addEventListener("input", apply);
  input.addEventListener("keydown", onKeyDown);
  form.addEventListener("submit", onSubmit);
  form.hidden = false;
  // A value the browser restored on back/forward navigation still applies.
  apply();

  return () => {
    input.removeEventListener("input", apply);
    input.removeEventListener("keydown", onKeyDown);
    form.removeEventListener("submit", onSubmit);
  };
}
