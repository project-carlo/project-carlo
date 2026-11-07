# Project Carlo mobile app

The iOS and Android app, built with Expo (SDK 58) and Expo Router. It is at
phase 1 of [docs/mobile-port-plan.md](../../docs/mobile-port-plan.md): a shell
that decodes the shared snapshot fixture through `@carlo/core` and lists the
churches. The website stays in `apps/web`.

## Commands

From the repository root:

```bash
pnpm dev:mobile      # Expo dev server for the development build (add --go for Expo Go)
pnpm check:mobile    # tsc
pnpm lint:mobile     # expo lint
pnpm bundle:mobile   # Metro bundles for iOS and Android, into apps/mobile/dist

pnpm build:android   # build the Android development build and install it on the device
pnpm device:mobile   # start Metro on a free port and open the development build on the device
pnpm e2e:mobile -e METRO_URL=http://127.0.0.1:8081   # run the Maestro flows in .maestro/
```

Add native packages with `pnpm exec expo install <package>` from this directory,
not `pnpm add`: it picks the version that matches the Expo SDK. Run
`pnpm --filter mobile run doctor` after changing dependencies.

## Running it on a device

`ios/` and `android/` are generated (Continuous Native Generation) and not
committed; configure native behavior in `app.json`.

The app is a development build (`expo-dev-client`): a native app that loads its
JavaScript from Metro. Rebuild it with `pnpm build:android` only after adding a
native package or changing native config in `app.json`; JavaScript changes reload
through Metro. Expo Go (`pnpm dev:mobile --go`) still runs the current shell, but
stops working once the app adds a native module Expo Go doesn't bundle.

### Android emulator in WSL

The emulator, Gradle, Metro and Maestro all run inside WSL, with no Windows
networking involved. Keep the repository on the Linux filesystem, not under
`/mnt/c`, so Metro's file watching works.

One-time setup (the root steps need sudo; the rest installs under your home):

1. **KVM and audio library.** `sudo usermod -aG kvm $USER` and
   `sudo apt install -y libpulse0` (the emulator links against it even with
   `-no-audio`). The group applies to new logins: run `wsl --shutdown` from
   Windows, or `sudo chmod o+rw /dev/kvm` to use KVM until the next restart.
   `emulator -accel-check` should report KVM as usable.
2. **JDK 17.** Unpack an [Eclipse Temurin](https://adoptium.net/) 17 tarball to
   `~/.local/jdk/` and link `~/.local/jdk/17` to it.
3. **Android SDK.** Unpack the
   [command-line tools](https://developer.android.com/studio#command-line-tools-only)
   to `~/Android/Sdk/cmdline-tools/latest`, then:

   ```bash
   yes | sdkmanager --licenses
   sdkmanager "platform-tools" "emulator" "system-images;android-36;google_apis;x86_64"
   echo no | avdmanager create avd -n carlo-api36 -k "system-images;android-36;google_apis;x86_64" -d pixel_7
   sed -i -e 's/^hw.ramSize=.*/hw.ramSize=4096M/' \
     -e 's/^hw.lcd.width=.*/hw.lcd.width=720/' -e 's/^hw.lcd.height=.*/hw.lcd.height=1600/' \
     -e 's/^hw.lcd.density=.*/hw.lcd.density=320/' ~/.android/avd/carlo-api36.avd/config.ini
   ```

   The `sed` gives the emulator 4 GB of RAM and a 720×1600 screen. With the
   default 2 GB, Android 16 swaps constantly and System UI stops responding.
   The emulator renders in software (SwiftShader) by default, so the CPU draws
   every frame and the smaller screen saves work. Together they took a cold boot to 43s, the Maestro flow from 13–18s to
   9s, and the idle emulator from 41% to 27% of a core. After the first boot,
   turn off animations, which also speeds up flows:

   ```bash
   for s in window_animation_scale transition_animation_scale animator_duration_scale; do
     adb shell settings put global $s 0
   done
   ```

   Gradle installs the SDK platform, build tools and NDK it needs on the first
   build.

   **GPU rendering** is possible but not faster yet. WSL exposes the Windows GPU
   through Mesa's d3d12 driver, which the emulator only uses when forced:

   ```bash
   GALLIUM_DRIVER=d3d12 MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA \
     emulator -avd carlo-api36 -no-window -no-audio -no-boot-anim -gpu host &
   ```

   Without the variables, `-gpu host` gets Mesa's llvmpipe, which is also
   software. With them, `adb shell dumpsys SurfaceFlinger | grep GLES` names the
   GPU. On the church list, a GTX 1650 was slightly slower than SwiftShader
   (Maestro flow 11–12s against 9–10s), probably because copying frames back
   from the GPU costs more than drawing a simple screen. Measure again once the
   app has a map. T3 Code boots the emulator with `-gpu auto` (software), but it attaches
   to one that is already running.
4. **Maestro.** Unpack `maestro.zip` from the
   [Maestro CLI releases](https://github.com/mobile-dev-inc/maestro/releases) to
   `~/.maestro/`.
5. **Memory.** WSL gets half the host's RAM by default. The emulator (about
   5 GB), Metro, Gradle and its Kotlin daemon together need most of 16 GB, and when WSL runs
   short the emulator stalls and its watchdog kills it. On a 32 GB host, raise
   the limit in `%UserProfile%\.wslconfig` and run `wsl --shutdown`:

   ```ini
   [wsl2]
   memory=24GB
   swap=8GB
   ```

6. **Environment,** in `~/.profile` (`~/.bashrc` returns early for the
   non-interactive shells agents use):

   ```bash
   export JAVA_HOME="$HOME/.local/jdk/17"
   export ANDROID_HOME="$HOME/Android/Sdk"
   export MAESTRO_CLI_NO_ANALYTICS=1
   PATH="$HOME/.maestro/maestro/bin:$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
   ```

7. **T3 Code's Device panel** (optional). To watch and drive the emulator from
   T3 Code, turn on device support in T3 Code and put an `ffmpeg` built with
   the libx264 encoder on `PATH`, since the panel streams the screen as H.264.
   Without it, opening the emulator fails with "Android emulator video needs
   working ffmpeg with the libx264 encoder". Ubuntu's `ffmpeg` package works;
   without sudo, unpack a static GPL build such as
   [BtbN's](https://github.com/BtbN/FFmpeg-Builds/releases) to
   `~/.local/opt/ffmpeg` and link `bin/ffmpeg` into `~/.local/bin`.
   `ffmpeg -hide_banner -encoders | grep libx264` should list it.

Day to day:

```bash
emulator -avd carlo-api36 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect &
adb wait-for-device
pnpm build:android     # first time, and after native changes
pnpm device:mobile     # leave running; prints its Metro port
pnpm e2e:mobile -e METRO_URL=http://127.0.0.1:<port>
```

`pnpm build:android` runs Gradle at low CPU priority and stops the Gradle and
Kotlin daemons when it finishes (they hold about 4 GB while idle), so a running
emulator survives the build. To watch the emulator, open it in T3 Code's Device
panel (step 7), or drop `-no-window` for a window (needs WSLg). `pnpm device:mobile`
picks a free Metro port per worktree, so several worktrees can share one
emulator, though only one of them drives the app at a time. With several devices
attached, set `ANDROID_SERIAL`. The first Gradle build takes several minutes;
later builds are incremental, but each worktree has its own `android/` and
builds from scratch.

### Physical devices and iOS

- **Android phone or the Windows emulator:** these can't reach Metro under
  WSL2's default NAT networking. Use `pnpm dev:mobile --tunnel`, or turn on
  mirrored networking in `.wslconfig`.
- **iOS:** the simulator needs a Mac. A development build on a physical iPhone
  needs an Apple Developer account.

The bundle and package ID `com.projectcarlo.app` is a placeholder until the
store accounts exist.
