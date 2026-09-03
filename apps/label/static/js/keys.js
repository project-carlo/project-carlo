/** Keyboard dispatch.
 *
 *  The whole point of the app is that a labeler never has to reach for the
 *  mouse, so every action has a key and typing into a field always wins.
 */

const TYPING_TAGS = new Set(["INPUT", "TEXTAREA", "SELECT"]);

function isTyping(target) {
  return TYPING_TAGS.has(target?.tagName) || target?.isContentEditable;
}

/** Wire a `{ key: handler }` map to the document.
 *
 *  Keys are matched case-sensitively, so `s` (save progress) and `S` (skip) are
 *  distinct. Digits are dispatched through the special `digit` handler.
 */
export function bindKeys(bindings) {
  document.addEventListener("keydown", (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;

    if (isTyping(event.target)) {
      // Escape is the way back out of a text field to the keyboard-driven flow.
      if (event.key === "Escape") event.target.blur();
      return;
    }

    if (/^[1-9]$/.test(event.key) && bindings.digit) {
      event.preventDefault();
      bindings.digit(Number(event.key));
      return;
    }

    const handler = bindings[event.key];
    if (handler) {
      event.preventDefault();
      handler();
    }
  });
}
