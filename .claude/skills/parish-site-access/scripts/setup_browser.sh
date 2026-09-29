#!/bin/bash
# Makes a Claude Code cloud sandbox able to open parish websites the way the
# pipeline does (src/pdf_extract/browser.py). Idempotent; ~1 minute the first
# time, instant after.
#
#  1. Google Chrome. The venv's Playwright wants a newer bundled Chromium than
#     the image ships (and `playwright install` is blocked), and real Chrome
#     gets past Cloudflare more often anyway -- detect.py already asks for it.
#     dl.google.com is reachable, so install the .deb.
#  2. The agent proxy's CA in Chrome's NSS store. The proxy re-terminates TLS
#     and the store starts empty, so every page fails with
#     ERR_CERT_AUTHORITY_INVALID until the CA is trusted.
#
# xvfb-run is already in the image; the pipeline runs headed and headless
# Chrome is blocked by Cloudflare almost every time.
set -euo pipefail

if ! command -v google-chrome >/dev/null 2>&1; then
  deb="$(mktemp --suffix=.deb)"
  curl -fsSL -o "$deb" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "$deb" >/dev/null
  rm -f "$deb"
fi

if ! command -v certutil >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libnss3-tools >/dev/null
fi

proxy_ca=/root/.ccr/agent-proxy-ca.crt
nssdb="sql:$HOME/.pki/nssdb"
if [ -f "$proxy_ca" ]; then
  mkdir -p "$HOME/.pki/nssdb"
  if [ ! -f "$HOME/.pki/nssdb/cert9.db" ]; then
    certutil -d "$nssdb" -N --empty-password
  fi
  # Drop the single name this script used to import under: a cert already stored
  # under it keeps that name and would not be re-imported under its own.
  while certutil -d "$nssdb" -D -n ccr-agent-proxy >/dev/null 2>&1; do :; done
  # The file can hold more than one CA. Re-import each under its own name every
  # time, so a saved nssdb never keeps an older proxy CA under one of them.
  certs="$(mktemp -d)"
  awk -v dir="$certs" '/BEGIN CERTIFICATE/ {n++} n {print > (dir "/" n ".pem")}' "$proxy_ca"
  for pem in "$certs"/*.pem; do
    name="ccr-agent-proxy-$(basename "$pem" .pem)"
    while certutil -d "$nssdb" -D -n "$name" >/dev/null 2>&1; do :; done
    certutil -d "$nssdb" -A -t "C,," -n "$name" -i "$pem"
  done
  rm -rf "$certs"
fi

echo "ready: $(google-chrome --version); proxy CA trusted: $(certutil -d "$nssdb" -L -n ccr-agent-proxy-1 >/dev/null 2>&1 && echo yes || echo no)"
