import type { BulletinDetail, BulletinSummary, Config, Label, Progress, SeedApprovalResult, SeedDetail, SeedFile, SeedQueueRow } from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init);
  const text = await response.text();
  let body: unknown = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    throw new Error(`${response.status} ${response.statusText}: the labeler API is not answering (is \`pnpm label\` running?)`);
  }
  if (!response.ok) {
    const message = (body as { error?: string } | null)?.error ?? response.statusText;
    throw new Error(message);
  }
  return body as T;
}

export function pdfUrl(parish: string, hash: string): string {
  return `/api/bulletins/${parish}/${hash}/pdf`;
}

export const api = {
  config: () => request<Config>("/api/config"),
  bulletins: () => request<{ bulletins: BulletinSummary[]; progress: Progress }>("/api/bulletins"),
  next: (
    after?: { parish: string; hash: string },
    parish?: string,
    options?: { unlabeledParishes?: boolean },
  ) => {
    const params = new URLSearchParams();
    if (after) params.set("after", `${after.parish}/${after.hash}`);
    if (parish) params.set("parish", parish);
    if (options?.unlabeledParishes) params.set("unlabeled_parishes", "1");
    return request<{ bulletin: BulletinSummary | null; progress: Progress }>(`/api/next?${params}`);
  },
  detail: (parish: string, hash: string) =>
    request<BulletinDetail>(`/api/bulletins/${parish}/${hash}`),
  save: (label: Label, { keepalive = false } = {}) =>
    request<{ label: Label }>(`/api/labels/${label.parish_slug}/${label.content_hash}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(label),
      keepalive,
    }),
  seeds: () => request<{ seeds: SeedQueueRow[] }>("/api/seeds"),
  approveReadySeeds: (reviewer: string) =>
    request<SeedApprovalResult>("/api/seeds/approve-ready", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reviewer }),
    }),
  seed: (parish: string) => request<SeedDetail>(`/api/seeds/${parish}`),
  saveSeed: (seed: SeedFile) =>
    request<SeedDetail>(`/api/seeds/${seed.parish_slug}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(seed),
    }),
};
