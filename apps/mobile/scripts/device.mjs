#!/usr/bin/env node
// Start Metro for this worktree and open the installed development build on an
// Android device or emulator.
//
//   pnpm device:mobile [--port <n>] [--no-open]
//
// Each worktree gets its own free Metro port (8081 upward), so parallel
// worktrees can share one emulator. `adb reverse` lets the device reach Metro
// on localhost, and a development-client deep link opens the build at this
// worktree's Metro. Set ANDROID_SERIAL when more than one device is attached.
// Metro keeps running in the foreground; stop it with Ctrl-C.

import { execFileSync, spawn } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { createServer } from "node:net";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const appDir = join(dirname(fileURLToPath(import.meta.url)), "..");
const { expo } = JSON.parse(readFileSync(join(appDir, "app.json"), "utf8"));
const packageName = expo.android.package;
const devClientScheme = `exp+${expo.slug}`;

const { values: args } = parseArgs({
  options: {
    port: { type: "string" },
    "no-open": { type: "boolean", default: false },
  },
});

// Set once Metro starts, so a later failure doesn't leave it running.
let metro = null;

function fail(message) {
  console.error(`device: ${message}`);
  metro?.kill("SIGTERM");
  process.exit(1);
}

function adbPath() {
  const sdk = process.env.ANDROID_HOME ?? process.env.ANDROID_SDK_ROOT;
  const fromSdk = sdk && join(sdk, "platform-tools", "adb");
  return fromSdk && existsSync(fromSdk) ? fromSdk : "adb";
}

const adbBinary = adbPath();

function adb(...adbArgs) {
  return execFileSync(adbBinary, adbArgs, { encoding: "utf8" }).trim();
}

function pickDevice() {
  let output;
  try {
    output = adb("devices");
  } catch {
    fail("adb not found. Set ANDROID_HOME or put platform-tools on PATH.");
  }
  const ready = output
    .split("\n")
    .slice(1)
    .map((line) => line.trim().split(/\s+/))
    .filter(([, state]) => state === "device")
    .map(([serial]) => serial);
  const wanted = process.env.ANDROID_SERIAL;
  if (wanted) {
    if (!ready.includes(wanted)) fail(`ANDROID_SERIAL=${wanted} is not attached and ready.`);
    return wanted;
  }
  if (ready.length === 0) fail("no Android device or emulator is attached and booted.");
  if (ready.length > 1) fail(`several devices attached (${ready.join(", ")}); set ANDROID_SERIAL.`);
  return ready[0];
}

function portIsFree(port) {
  return new Promise((resolve) => {
    const server = createServer()
      .once("error", () => resolve(false))
      .once("listening", () => server.close(() => resolve(true)))
      .listen(port);
  });
}

async function pickPort() {
  if (args.port) {
    const port = Number(args.port);
    if (!(await portIsFree(port))) fail(`port ${port} is in use.`);
    return port;
  }
  for (let port = 8081; port < 8181; port++) {
    if (await portIsFree(port)) return port;
  }
  fail("no free port between 8081 and 8180.");
}

async function waitForMetro(port, metro) {
  const deadline = Date.now() + 120_000;
  while (Date.now() < deadline) {
    if (metro.exitCode !== null) fail("Metro exited before it was ready.");
    try {
      const response = await fetch(`http://127.0.0.1:${port}/status`);
      if ((await response.text()).includes("packager-status:running")) return;
    } catch {
      // Not listening yet.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  fail(`Metro did not answer on port ${port} within two minutes.`);
}

const serial = pickDevice();
process.env.ANDROID_SERIAL = serial;

function isInstalled() {
  try {
    return adb("shell", "pm", "path", packageName) !== "";
  } catch {
    return false; // pm exits non-zero for a missing package.
  }
}

if (!isInstalled()) {
  fail(`${packageName} is not installed on ${serial}. Build it with \`pnpm build:android\`.`);
}

const port = await pickPort();
const metroUrl = `http://127.0.0.1:${port}`;

metro = spawn("pnpm", ["exec", "expo", "start", "--dev-client", "--port", String(port)], {
  cwd: appDir,
  stdio: "inherit",
});

let cleanedUp = false;
function cleanUp() {
  if (cleanedUp) return;
  cleanedUp = true;
  try {
    adb("reverse", "--remove", `tcp:${port}`);
  } catch {
    // The device may already be gone.
  }
}

for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
  process.on(signal, () => {
    cleanUp();
    metro.kill(signal);
  });
}
metro.on("exit", (code) => {
  cleanUp();
  process.exit(code ?? 0);
});

await waitForMetro(port, metro);

// disableAutoLaunch skips the development client's onboarding and its menu at launch.
const devClientUrl =
  `${devClientScheme}://expo-development-client/` +
  `?url=${encodeURIComponent(metroUrl)}&disableAutoLaunch=1`;
try {
  adb("reverse", `tcp:${port}`, `tcp:${port}`);
  if (!args["no-open"]) {
    adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", `'${devClientUrl}'`, packageName);
  }
} catch (error) {
  cleanUp();
  fail(`adb failed: ${error.stderr?.trim() || error.message}`);
}

console.log(`
device: Metro is serving this worktree on port ${port} for ${serial}.
device: ${args["no-open"] ? "Open" : "Opened"} the development build with ${devClientUrl}
device: Run the Maestro flows with \`pnpm e2e:mobile -e METRO_URL=${metroUrl}\`.
`);
