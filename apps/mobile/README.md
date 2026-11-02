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
   ```

   Gradle installs the SDK platform, build tools and NDK it needs on the first
   build.
4. **Maestro.** Unpack `maestro.zip` from the
   [Maestro CLI releases](https://github.com/mobile-dev-inc/maestro/releases) to
   `~/.maestro/`.
5. **Memory.** WSL gets half the host's RAM by default. The emulator, Metro,
   Gradle and its Kotlin daemon together need most of 16 GB, and when WSL runs
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
emulator survives the build. Drop `-no-window` to watch the emulator in a window
(needs WSLg). `pnpm device:mobile`
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
