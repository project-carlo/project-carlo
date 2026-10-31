"""Smoke-test the full worker image without credentials or the live factory.

    uv run python factory/sandbox/smoke-worker.py [--image carlo-worker:<hash>]

Uses the production container settings with an isolated network, proxy, workspace and
session directory. Does not submit a Claude prompt or read account tokens.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from pdf_extract.factory import sandbox, workspace

ROOT = Path(__file__).resolve().parents[2]

PROBE = r'''
import json
import os
import subprocess
from pathlib import Path


def command(*args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, (args, result.stdout, result.stderr)
    print(json.dumps({'command': list(args), 'ok': True,
                      'first_line': result.stdout.splitlines()[:1]}), flush=True)


for args in [('python', '--version'), ('node', '--version'), ('pnpm', '--version'),
             ('claude', '--version'), ('uv', '--version'), ('gs', '--version'),
             ('pdftoppm', '-v'), ('pnpm', 'diocese', '--help'), ('pnpm', 'seed', '--help')]:
    command(*args)

import boto3, google.genai, openai, PIL, playwright.sync_api, pydantic, pypdf, pypdfium2, yaml
from pdf_extract.browser import launch_stealth_browser

assert os.geteuid() == 1000
assert not Path('node_modules').exists()
assert not Path('.git').exists()
for name in ('CLAUDE_CODE_OAUTH_TOKEN', 'OPENAI_API_KEY', 'GEMINI_API_KEY', 'GH_TOKEN',
             'R2_ACCESS_KEY_ID', 'SSH_AUTH_SOCK'):
    assert not os.environ.get(name), name
for parent in (Path('/tmp'), Path.home(), Path.home() / '.claude',
               Path.home() / '.claude/projects', Path('scratch')):
    parent.mkdir(exist_ok=True)
    path = parent / 'smoke-write'
    path.write_text('ok')
    assert path.read_text() == 'ok'
for parent in (Path('/usr'), Path('/opt/venv'), Path('src'), Path('.claude')):
    try:
        (parent / 'smoke-write').write_text('must not be writable')
    except OSError:
        pass
    else:
        raise AssertionError(f'{parent} is writable')
try:
    os.chroot('/')
except PermissionError:
    pass
else:
    raise AssertionError('chroot must require a nested user namespace')
print(json.dumps({'dependencies': 'ok', 'writable_paths': 'ok',
                  'read_only_tools': 'ok', 'outer_chroot': 'denied'}), flush=True)

for channel in (None, 'chrome'):
    with launch_stealth_browser(channel=channel) as page:
        page.goto('https://example.com/', wait_until='domcontentloaded', timeout=30000)
        assert page.title() == 'Example Domain', page.title()
        page.screenshot(path=f'scratch/{channel or "chromium"}.png')
        page.goto('chrome://version')
        assert '--no-sandbox' not in page.locator('#command_line').inner_text()
        page.goto('chrome://sandbox')
        status = page.locator('body').inner_text()
        for expected in ('PID namespaces\tYes', 'Network namespaces\tYes',
                         'Seccomp-BPF sandbox\tYes', 'You are adequately sandboxed.'):
            assert expected in status, status
        print(json.dumps({'browser': channel or 'chromium', 'headed': True,
                          'https': 'ok', 'sandbox': status}), flush=True)

pdf = pypdf.PdfWriter()
pdf.add_blank_page(width=144, height=144)
with open('scratch/probe.pdf', 'wb') as stream:
    pdf.write(stream)
command('uv', 'run', 'python', '.claude/skills/parish-site-access/scripts/render.py',
        'scratch/probe.pdf', 'scratch/rendered', '--pages', '1')
assert Path('scratch/rendered-p1.jpg').stat().st_size > 0

'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', help='An already-built full worker image')
    args = parser.parse_args()
    suffix = str(os.getpid())
    sandbox.NETWORK = f'carlo-smoke-workers-{suffix}'
    sandbox.PROXY = f'carlo-smoke-egress-{suffix}'
    sandbox.PROXY_URL = f'http://{sandbox.PROXY}:{sandbox.PROXY_PORT}'
    name = f'carlo-smoke-worker-{suffix}'
    backend = sandbox.PodmanBackend(ROOT, 'HEAD')
    try:
        image = args.image or backend.image()
        backend.network()
        backend.proxy()
        with tempfile.TemporaryDirectory(prefix='carlo-worker-smoke-') as directory:
            work = Path(directory) / 'work'
            sessions = Path(directory) / 'sessions'
            work.mkdir()
            sessions.mkdir()
            # Only tracked tools and manifests: no .env, credentials, git metadata or live data.
            tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
            for rel in tracked:
                if not rel or rel.split('/')[0] not in workspace.READ_ONLY:
                    continue
                source, target = ROOT / rel, work / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            (work / 'probe.py').write_text(PROBE)
            env = sandbox.container_env(work) | {'CARLO_NO_DOTENV': '1'}
            mounts = [sandbox.Mount(p, p, ro) for p, ro in workspace.mounts(work)]
            mounts.append(sandbox.Mount(sessions, sandbox.WORKER_PROJECTS))
            box = sandbox.Box(name=name, image=image, workdir=work, mounts=mounts, env=env,
                              command=['xvfb-run', '-a', 'python', 'probe.py'])
            result = subprocess.run(sandbox.run_argv(backend.podman, box), timeout=240)
            if result.returncode == 0:
                assert (work / "scratch/rendered-p1.jpg").stat().st_uid == os.getuid()
                print(f"Full worker smoke test passed: {image}", flush=True)
            return result.returncode
    finally:
        for container in (name, sandbox.PROXY):
            subprocess.run(['podman', 'rm', '-f', container], capture_output=True)
        subprocess.run(['podman', 'network', 'rm', sandbox.NETWORK], capture_output=True)


if __name__ == '__main__':
    raise SystemExit(main())
