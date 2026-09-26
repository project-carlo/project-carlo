const SHORTCUTS: [string, string][] = [
  ["n", "New row (keeps church, type, kind; page = page in view)"],
  ["m / c / a", "Mass / Confession / Adoration"],
  ["w / d / f", "Weekly / dated / first of the month. d places a weekly row on that weekday of the bulletin's week. f keeps that weekday (or the weekday of a date), marks the first week, and clears the note"],
  ["x", "Toggle cancelled"],
  ["Enter", "Edit the selected row (first empty field)"],
  ["↑ ↓  or  j k", "Select previous / next row"],
  ["Ctrl+D", "Duplicate row"],
  ["Delete", "Delete row"],
  ["Ctrl+Z / Ctrl+Shift+Z", "Undo / redo"],
  ["Ctrl+Enter", "Mark done and open the next bulletin"],
  ["?", "Show or hide this help"],
];

const GEMINI: [string, string][] = [
  ["Enter / y", "Accept, then go to the next candidate and its page"],
  ["d", "Accept a weekly row as that weekday of the bulletin's week"],
  ["f", "Accept as the first of that weekday each month, and clear the note"],
  ["e", "Edit this Gemini row"],
  ["Delete / n", "Dismiss (or restore) it"],
  ["↑ ↓  or  j k", "Move between Gemini rows and show that page"],
];

const ENTRY: [string, string][] = [
  ["Times", "530p · 5:30 · 17:30 · noon (bare 1–6 means PM)"],
  ["Days", "Sun · Mon-Fri · Sat & Sun · weekdays: several days make one row each"],
  ["Dates", "10/5 · Oct 5 · 2026-10-05; several (10/2; 10/9) make one row each"],
  ["Season", "Sep-May · Jun 4 - Sep 10 · empty = all year"],
];

function Table({ rows }: { rows: [string, string][] }) {
  return (
    <table className="w-full text-sm">
      <tbody>
        {rows.map(([k, v]) => (
          <tr key={k}>
            <td className="py-0.5 pr-4 align-top whitespace-nowrap">
              <kbd>{k}</kbd>
            </td>
            <td className="py-0.5 text-slate-700">{v}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function HelpOverlay({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={onClose}>
      <div className="max-h-[90vh] w-[36rem] space-y-3 overflow-y-auto rounded-lg bg-white p-5 shadow-xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center">
          <h2 className="text-lg font-semibold">Keyboard shortcuts</h2>
          <button className="btn ml-auto" onClick={onClose}>
            Close
          </button>
        </div>
        <p className="text-xs text-slate-500">Row shortcuts apply to the selected row when you are not typing in a field. Esc leaves a field.</p>
        <Table rows={SHORTCUTS} />
        <h3 className="font-semibold">Gemini panel</h3>
        <Table rows={GEMINI} />
        <h3 className="font-semibold">Loose entry</h3>
        <Table rows={ENTRY} />
      </div>
    </div>
  );
}
