# Project Carlo mobile app

The iOS and Android app, built with Expo (SDK 58) and Expo Router. It is at
phase 1 of [docs/mobile-port-plan.md](../../docs/mobile-port-plan.md): a shell
that decodes the shared snapshot fixture through `@carlo/core` and lists the
churches. The website stays in `apps/web`.

## Commands

From the repository root:

```bash
pnpm dev:mobile      # Expo dev server
pnpm check:mobile    # tsc
pnpm lint:mobile     # expo lint
pnpm bundle:mobile   # Metro bundles for iOS and Android, into apps/mobile/dist
```

Add native packages with `pnpm exec expo install <package>` from this directory,
not `pnpm add`: it picks the version that matches the Expo SDK. Run
`pnpm --filter mobile doctor` after changing dependencies.

## Running it on a device

`ios/` and `android/` are generated (Continuous Native Generation) and not
committed; configure native behavior in `app.json`.

- **Expo Go** runs the current shell. It stops working once the app adds a
  native module Expo Go doesn't bundle; after that, use a development build
  (`eas build --profile development`, set up in a later change).
- **WSL:** a phone or the Windows Android emulator can't reach Metro under
  WSL2's default NAT networking. Use `pnpm dev:mobile --tunnel`, or turn on
  mirrored networking in `.wslconfig`.
- **iOS:** the simulator needs a Mac. A development build on a physical iPhone
  needs an Apple Developer account.

The bundle and package ID `com.projectcarlo.app` is a placeholder until the
store accounts exist.
