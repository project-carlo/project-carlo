---
name: mobile-device
description: Run the Expo app in apps/mobile on the local Android emulator and check a change on a device. Covers starting the headless emulator, building and installing the development build, starting this worktree's Metro, running the Maestro flows, taking screenshots and reading the app's logs. Use when asked to run, test, screenshot or debug the mobile app, or to confirm a mobile change works on a device rather than only in tsc and lint.
---

# Running the mobile app on the Android emulator

Everything runs inside WSL: the emulator (headless, KVM), Gradle, Metro and Maestro.
The one-time setup is in [apps/mobile/README.md](../../../apps/mobile/README.md#android-emulator-in-wsl);
if `adb`, `emulator` or `maestro` is missing, point the owner there rather than
installing system packages yourself. Run commands from the repository root of your
worktree.

## In T3 Code: use the Device panel

If you have T3 Code's device tools (`device_list`, `device_open`), use them so the
owner can watch the emulator in the Device panel:

- `device_open` with the `carlo-api36` AVD boots it if needed (skip step 1) and
  returns an `agent-device` command bound to it. If it fails with "needs working
  ffmpeg with the libx264 encoder", point the owner to step 7 of the README setup.
- Build, Metro and Maestro work as below (steps 2 to 4). For your own launches,
  taps, scrolls and screenshots, use `agent-device` and `device_screenshot`
  rather than `adb shell am start`, `adb shell input` or `adb exec-out screencap`.
  To open the app at your Metro, run `pnpm device:mobile --no-open`, then
  `<agent-device> open com.projectcarlo.app --relaunch --metro-port <port>`. On a
  busy emulator it can fail with "remained foreground after close"; run it again.
- Check the screen through its accessibility tree: `<agent-device> snapshot -i`
  lists `testID`s such as `church-list`, and `<agent-device> wait 'id=church-count'`
  waits for one.
- After a cold boot Android often shows "System UI isn't responding".
  `agent-device` won't tap that dialog's buttons; `<agent-device> alert dismiss`
  closes it.

## 1. Make sure an emulator is running

```bash
adb devices
```

An `emulator-5554  device` line means one is booted; reuse it, since other worktrees
may be using it too. Otherwise start one in the background and wait for boot:

```bash
emulator -list-avds        # carlo-api36
emulator -avd carlo-api36 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect -no-snapshot-save > /tmp/carlo-emulator.log 2>&1 &
adb wait-for-device shell 'while [ "$(getprop sys.boot_completed)" != 1 ]; do sleep 1; done'
```

A cold boot takes a minute or two. If `emulator -accel-check` says KVM isn't usable,
stop and tell the owner (see the README's KVM step). An emulator costs about 3 GB of
memory; don't start a second one when one is already running.

If the emulator disappears from `adb devices`, check `/tmp/carlo-emulator.log` for
`detected a hanging thread`: WSL ran short of memory or CPU and the emulator's
watchdog killed it. Look for what's using memory (`ps -eo rss,args --sort=-rss | head`),
such as leftover Gradle daemons (`./apps/mobile/android/gradlew -p apps/mobile/android --stop`),
then boot it again.

## 2. Install the development build if needed

```bash
adb shell pm path com.projectcarlo.app
```

No output means it isn't installed. Build and install it with `pnpm build:android`
(several minutes the first time in a worktree, since `android/` is generated per
worktree). Rebuild only when the change adds a native package or changes native
config in `apps/mobile/app.json`; JavaScript changes don't need a rebuild. A build
from another worktree works as long as the native dependencies match.

## 3. Start Metro and open the app

Run in the background and leave it running:

```bash
pnpm device:mobile
```

It picks a free port from 8081 upward, runs `adb reverse`, opens the development
build at that Metro (skipping the development client's onboarding and menu), and prints the port and the `METRO_URL` for Maestro. Read its
output for bundling errors. Edits to JavaScript reach the app through Fast Refresh.
Stop it when you're done; it removes its `adb reverse` on exit.

Only one worktree drives the app at a time: opening it from your Metro takes it over
from whoever had it.

## 4. Check the change

**Maestro flows** live in `apps/mobile/.maestro/` (top-level files are flows;
`subflows/` holds shared steps such as `launch.yaml`):

```bash
pnpm e2e:mobile -e METRO_URL=http://127.0.0.1:<port>
pnpm e2e:mobile -e METRO_URL=http://127.0.0.1:<port> .maestro/explore-list.yaml   # one flow
```

Screenshots, logs and failure artifacts go to `apps/mobile/.maestro/output/`
(ignored by git). Select elements by `id:` (a `testID`) rather than by text where
possible, and give every new interactive element a `testID` and an accessibility
label. Add or extend a flow for user-visible behavior you change.

**Screenshot** of the current screen (in T3 Code, `device_screenshot` instead),
then read the PNG to look at it:

```bash
adb exec-out screencap -p > /tmp/carlo-screen.png
```

**App logs** (console output and JavaScript errors):

```bash
adb logcat -d -s ReactNativeJS:V ReactNative:V AndroidRuntime:E | tail -50
```

A red error screen in a screenshot means a JavaScript error; the Metro output and
`ReactNativeJS` logs give the stack.

## Troubleshooting

- **`device: ... is not installed`**: run `pnpm build:android`.
- **App shows "Unable to load script" or the dev launcher**: Metro isn't reachable.
  Check `pnpm device:mobile` is still running and `adb reverse --list` shows its port.
- **Gradle fails on a missing SDK component**: `yes | sdkmanager --licenses`, then
  rebuild; Gradle installs platforms, build tools and the NDK itself.
- **Emulator is `offline` or unresponsive**: `adb kill-server && adb start-server`;
  if that doesn't help, `adb emu kill` and boot it again.
- **iOS**: there is no local iOS loop (no Mac). iOS simulator runs in CI are planned
  in docs/mobile-port-plan.md but not set up yet.
