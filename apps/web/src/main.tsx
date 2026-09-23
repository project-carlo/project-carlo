import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import { onLocalDayChange } from "./lib/dayRollover";
import { router } from "./router";
import "leaflet/dist/leaflet.css";
import "./app.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: 2,
    },
  },
});

// The map and church-page queries list events by their next occurrence, which
// is relative to the local date. A tab can stay open (or be resumed) past
// midnight, and nothing about the query key changes then, so mark them stale
// when the day does: the visible ones refetch at once, the rest on next use.
onLocalDayChange(() => {
  void queryClient.invalidateQueries({ queryKey: ["churches"] });
  void queryClient.invalidateQueries({ queryKey: ["church-events"] });
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
);
