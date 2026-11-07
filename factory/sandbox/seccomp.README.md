# Worker seccomp profile

`seccomp.json` is derived from `/usr/share/containers/seccomp.json` in Ubuntu's
`golang-github-containers-common` package `0.66.0+ds2-3`, used by Podman 5.7.0.
The unmodified file has SHA-256
`886ae167646b7e5db381ecf7c31e6de720a8e8da15cf3202fe1f67f424af2b75`.
Upstream: https://github.com/containers/common (the profile is generated from
`pkg/seccomp/default_linux.go`). Copyright 2013-2018 Docker, Inc.;
2018 containers/common authors. Apache-2.0; see `seccomp.LICENSE`.

Modification: remove the capability-dependent `chroot` rules and allow that syscall
unconditionally. All other rules are unchanged. Chromium's namespace sandbox needs
`chroot` after entering its own user namespace; the capability-dependent filter was
compiled while the container had no capabilities, so it otherwise refuses that call.
The kernel still checks capabilities: a worker without `CAP_SYS_CHROOT` cannot chroot
in its original namespace. The exception lets Chromium chroot within its nested
namespace, where it has the needed capability.

No capability is added to the container. `--cap-drop=ALL`, no-new-privileges, private
namespaces and the read-only root remain. The smoke test verifies Chromium and Chrome
report PID/network namespace sandboxing and seccomp-BPF, and have no `--no-sandbox`.
The profile is read from the dispatcher's installed code, never a worker's files.
