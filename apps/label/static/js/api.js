/** Thin fetch wrapper over the labeling server's JSON API. */

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const text = await response.text();
  const payload = text ? JSON.parse(text) : null;
  if (!response.ok) {
    throw new Error(payload?.error || `${response.status} ${response.statusText}`);
  }
  return payload;
}

const query = (params) => {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== "") search.set(key, value);
  }
  const encoded = search.toString();
  return encoded ? `?${encoded}` : "";
};

export const api = {
  config: () => request("/api/config"),
  queue: (params) => request(`/api/queue${query(params)}`),
  task: (url, params) => request(`/api/task${query({ url, ...params })}`),
  saveLabel: (label) =>
    request("/api/label", { method: "POST", body: JSON.stringify(label) }),
  clearLabel: (url) => request(`/api/label${query({ url })}`, { method: "DELETE" }),
  reload: () => request("/api/reload", { method: "POST" }),
  pdfUrl: (url) => `/api/pdf${query({ url })}`,
};
