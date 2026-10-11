import type { SeedQueueRow } from "../types";

export const SEED_STATUS_STYLE: Record<SeedQueueRow["status"], string> = {
  needs_review: "bg-amber-100 text-amber-900",
  ready: "bg-sky-100 text-sky-800",
  drafting: "bg-slate-100 text-slate-600",
  blocked: "bg-zinc-200 text-zinc-700",
  approved: "bg-emerald-100 text-emerald-800",
  invalid: "bg-red-100 text-red-800",
};

export const SEED_STATUS_LABEL: Record<SeedQueueRow["status"], string> = {
  needs_review: "Needs review",
  ready: "Ready to approve",
  drafting: "Drafting",
  blocked: "Blocked",
  approved: "Approved",
  invalid: "Unreadable",
};
