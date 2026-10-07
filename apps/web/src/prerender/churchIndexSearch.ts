/**
 * The all-churches index's search box, as an inline script: the page is
 * static HTML with no React, so this is plain browser JavaScript. The box is
 * rendered `hidden` and this script reveals it, so without JavaScript the page
 * is just the full list.
 *
 * A church matches when every word typed appears in its name or its city's
 * name, ignoring case, accents and punctuation; "St." also matches "saint"
 * (and the reverse), "Mt." "mount". A city stays listed while any of its
 * churches match.
 */
export const CHURCH_INDEX_SEARCH_SCRIPT = `(() => {
  const input = document.getElementById("church-search");
  const status = document.getElementById("church-search-status");
  const empty = document.getElementById("church-search-empty");
  const form = document.getElementById("church-search-form");
  if (!form || !input || !status || !empty) return;

  const fold = (text) =>
    text
      .normalize("NFKD")
      .replace(/[\\u0300-\\u036f]/g, "")
      .toLowerCase()
      .replace(/['\\u2019]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  const ALIASES = { st: "saint", saint: "st", mt: "mount", mount: "mt" };
  const haystack = (text) =>
    fold(text)
      .split(" ")
      .map((word) => (ALIASES[word] ? word + " " + ALIASES[word] : word))
      .join(" ");

  const sections = Array.from(document.querySelectorAll("[data-city-group]")).map(
    (section) => {
      const city = haystack(section.querySelector("h2").textContent);
      const items = Array.from(section.querySelectorAll("li")).map((item) => ({
        item,
        text: haystack(item.textContent) + " " + city,
      }));
      return { section, items };
    },
  );
  const total = sections.reduce((n, s) => n + s.items.length, 0);

  const apply = () => {
    const words = fold(input.value).split(" ").filter(Boolean);
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
    status.textContent =
      words.length === 0 || shown === 0
        ? ""
        : "Showing " + shown + " of " + total + " churches.";
    empty.hidden = words.length === 0 || shown > 0;
    if (!empty.hidden) {
      empty.textContent =
        "No churches or cities match \u201c" + input.value.trim() + "\u201d. " +
        "Try fewer words, or just the town.";
    }
  };

  input.addEventListener("input", apply);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && input.value) {
      input.value = "";
      apply();
    }
  });
  // Filtering is live; Enter shouldn't reload the page.
  form.addEventListener("submit", (event) => event.preventDefault());
  form.hidden = false;
  // A value the browser restored on back/forward navigation still applies.
  apply();
})();`;
