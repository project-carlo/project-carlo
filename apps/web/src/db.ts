import initSqlJs, { type Database } from "sql.js";

let dbPromise: Promise<Database> | null = null;

async function loadSnapshot(): Promise<ArrayBuffer> {
  const response = await fetch("/frontend.snapshot", { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to fetch frontend snapshot: ${response.status}`);
  }

  const compressed = response.body ?? new Blob([await response.arrayBuffer()]).stream();
  const decompressed = compressed.pipeThrough(new DecompressionStream("gzip"));
  return new Response(decompressed).arrayBuffer();
}

function init(): Promise<Database> {
  return Promise.all([initSqlJs({ locateFile: (file: string) => `/${file}` }), loadSnapshot()]).then(
    ([SQL, buf]) => new SQL.Database(new Uint8Array(buf)),
  );
}

export function getDb(): Promise<Database> {
  if (!dbPromise) {
    dbPromise = init().catch((error: unknown) => {
      // Don't hold on to a failed load: callers retry (react-query does so
      // automatically), and a cached rejection would make every retry fail
      // instantly without touching the network again.
      dbPromise = null;
      throw error;
    });
  }
  return dbPromise;
}

