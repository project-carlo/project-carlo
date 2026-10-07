import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import { createAppRouter } from "./router";
import { createQueryClient } from "./lib/queryClient";
import { reloadOnStaleChunk } from "./lib/staleDeploy";
import "leaflet/dist/leaflet.css";
import "./app.css";

const queryClient = createQueryClient();
const router = createAppRouter(queryClient);

// A chunk that fails on the way to another page reloads into that page.
reloadOnStaleChunk(() => {
  const next = router.state.navigation.location;
  return next ? router.createHref(next) : undefined;
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
);
