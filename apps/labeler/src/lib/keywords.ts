/** Words that mark schedule lines in a bulletin, highlighted in the PDF's text layer. */
export const KEYWORD_RE =
  /\b(masses|mass|confessions?|reconciliation|adoration|holy\s+hour|cancel(?:l?ed|lations?|s)?)\b/gi;

export interface Segment {
  text: string;
  keyword: "schedule" | "cancel" | null;
}

export function splitKeywords(text: string): Segment[] {
  const out: Segment[] = [];
  let last = 0;
  for (const m of text.matchAll(KEYWORD_RE)) {
    const at = m.index ?? 0;
    if (at > last) out.push({ text: text.slice(last, at), keyword: null });
    out.push({ text: m[0], keyword: /^cancel/i.test(m[0]) ? "cancel" : "schedule" });
    last = at + m[0].length;
  }
  if (last < text.length) out.push({ text: text.slice(last), keyword: null });
  return out;
}

/** Wrap keywords inside a rendered text layer's spans in <mark> elements. */
export function markKeywords(container: HTMLElement): void {
  for (const span of container.querySelectorAll("span")) {
    if (span.childElementCount > 0 || !span.textContent) continue;
    const segments = splitKeywords(span.textContent);
    if (!segments.some((s) => s.keyword)) continue;
    span.textContent = "";
    for (const s of segments) {
      if (!s.keyword) {
        span.append(s.text);
        continue;
      }
      const mark = document.createElement("mark");
      mark.className = s.keyword === "cancel" ? "kw kw-cancel" : "kw";
      mark.textContent = s.text;
      span.append(mark);
    }
  }
}
