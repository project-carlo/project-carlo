"""Isolated, authenticated pre-merge checks; never starts a dispatcher.

Run from the PR checkout: uv run python factory/sandbox/validate-live.py
Reads only account names/config/token paths from the live local.yaml. Tokens stay in
process environments, never argv or reports. Results and sessions stay in a private
temporary directory printed at startup. Production cleanup() is deliberately unused.
"""

from __future__ import annotations

import dataclasses
import json
import os
import secrets
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import yaml

from pdf_extract.factory import sandbox, workers, workspace
from pdf_extract.factory.config import Account
from pdf_extract.factory.stages import StageSpec

ROOT = Path(__file__).resolve().parents[2]


def account_usage(account: Account) -> dict:
    """Read-only correlation with the existing login; never refresh its credentials."""
    oauth = json.loads((account.config_dir / '.credentials.json').read_text())['claudeAiOauth']
    request = urllib.request.Request('https://api.anthropic.com/api/oauth/usage', headers={
        'Authorization': f'Bearer {oauth["accessToken"]}',
        'anthropic-beta': 'oauth-2025-04-20', 'User-Agent': 'project-carlo-factory'})
    with urllib.request.urlopen(request, timeout=30) as response:
        usage = json.load(response)
    return {'plan': oauth.get('subscriptionType'),
            'windows': {k: usage[k] for k in ('five_hour', 'seven_day')}}


def windows_match(events: list[dict], usage: dict) -> bool:
    """The API rounds worker event resets to seconds; allow a second of rounding."""
    windows = next((e['raw']['unifiedWindows'] for e in events
                    if e.get('raw', {}).get('unifiedWindows')), {})
    return all(key in windows and abs(windows[key]['resetsAt'] -
               datetime.fromisoformat(usage['windows'][key]['resets_at']).timestamp()) < 1
               for key in ('five_hour', 'seven_day'))

BROWSER_PROBE = r'''
import json, subprocess, urllib.request, urllib.error
from pathlib import Path
from pdf_extract.browser import launch_stealth_browser

sites = ['https://queenofpeacehawley.com/', 'https://stlouischurch.org/']
baselines = []
for url in sites:
    try:
        response = urllib.request.urlopen(url, timeout=30)
    except urllib.error.HTTPError as error:
        response = error
    except Exception as error:
        baselines.append({'url': url, 'error': str(error)})
        continue
    baselines.append({'url': url, 'status': response.status,
                      'server': response.headers.get('server'),
                      'cf_ray': response.headers.get('cf-ray')})
Path('scratch/http-baseline.json').write_text(json.dumps(baselines, indent=2))
with launch_stealth_browser(channel='chrome') as page:
    page.goto('chrome://version')
    assert '--no-sandbox' not in page.locator('#command_line').inner_text()
    page.goto('chrome://sandbox')
    status = page.locator('body').inner_text()
    assert 'You are adequately sandboxed.' in status, status
    Path('scratch/chrome-sandbox.txt').write_text(status)
cmd = ['uv', 'run', 'python', '.claude/skills/parish-site-access/scripts/visit.py',
       *sites, '--text', '--chars', '500', '--links', '--match', 'ecatholic|bulletin',
       '--screenshot', 'scratch/parish.png', '--html', 'scratch/parish.html',
       '--retries', '4']
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
Path('scratch/visit.json').write_text(result.stdout)
Path('scratch/visit.stderr').write_text(result.stderr)
assert result.returncode == 0, result.stderr
visits = json.loads(result.stdout)
assert all(r['status'] == 200 and r['verdict'] == 'ok' and r['publications']
           for r in visits['results']), visits
assert all(b.get('server') == 'cloudflare' and b['status'] == 403 for b in baselines), baselines
print(json.dumps({'baseline': baselines, 'visit': visits,
                  'chrome_sandbox': status}), flush=True)
'''


def main() -> int:
    os.umask(0o077)
    output = Path(tempfile.mkdtemp(prefix='carlo-pr184-validation-'))
    print(f'Private artifacts: {output}', flush=True)
    suffix = str(os.getpid())
    sandbox.NETWORK = f'carlo-validation-workers-{suffix}'
    sandbox.PROXY = f'carlo-validation-egress-{suffix}'
    sandbox.PROXY_URL = f'http://{sandbox.PROXY}:{sandbox.PROXY_PORT}'
    # Distinct from production labels: even its startup cleanup cannot remove these.
    sandbox.LABEL = f'carlo.validation={suffix}'
    backend = sandbox.PodmanBackend(ROOT, 'HEAD', sandbox_dir=output / 'sandbox',
                                    sessions_dir=output / 'sessions')
    report = {'started_at': datetime.now(UTC).isoformat(),
              'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                                cwd=ROOT, text=True).strip(),
              'accounts': []}

    def save():
        (output / 'report.json').write_text(json.dumps(report, indent=2, default=str))

    # Only tracked tools/manifests, no repository metadata, live data or credentials.
    trusted = output / 'trusted'
    trusted.mkdir()
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    for rel in tracked:
        if rel and rel.split('/')[0] in workspace.READ_ONLY:
            target = trusted / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, target)
    (trusted / 'scratch').mkdir()
    local = yaml.safe_load((Path.home() / 'carlo-factory/data/factory/local.yaml').read_text())
    accounts = [Account(a['name'], Path(a['config_dir']).expanduser(),
                        worker_token_file=Path(a['worker_token_file']).expanduser())
                for a in local['accounts']]
    names = []
    try:
        report['image'] = backend.ready()
        save()
        for index, account in enumerate(accounts):
            nonce = secrets.token_hex(16)
            events, steps = [], []
            run = f'validation-{suffix}-{index}'
            spec = StageSpec('map', 'agent', model='claude-sonnet-5-5', effort='high',
                             tools=['Bash'], writes=['scratch/**'], max_turns=6,
                             max_minutes=3)
            request = workers.WorkerRequest(
                job_id=int(suffix) * 100 + index * 10, run_id=run, job_name='auth',
                stage='map', spec=spec, worktree=trusted, account=account,
                prompt=f'Remember this nonce in this conversation: {nonce}. '
                       'Use Bash to run mkdir -p scratch and write the word AUTH_OK '
                       f'to scratch/auth-{index}.txt. Then reply exactly READY. '
                       'Do not read environment variables or credentials. Do not '
                       'write the nonce to any file.',
                system_append='This is a small sandbox authentication/resume test.',
                values={}, on_step=lambda *s: steps.append(s),
                on_rate_limit=events.append)
            names.append(f'carlo-job-{request.job_id}')
            print(f'{account.name}: authenticated SDK attempt', flush=True)
            result = workers.SdkWorker(backend).run(request)
            entry = {'account': account.name, 'first': dataclasses.asdict(result),
                     'first_rate_limits': list(events), 'first_steps': list(steps),
                     'file_written': (trusted / f'scratch/auth-{index}.txt').exists(),
                     'first_container_removed': backend.call('container', 'exists',
                                                            names[-1]).returncode != 0}
            report['accounts'].append(entry)
            save()
            try:
                entry['account_usage'] = account_usage(account)
                entry['account_windows_match'] = windows_match(events, entry['account_usage'])
            except Exception as error:
                entry['account_usage_error'] = str(error)
            save()
            print(f'{account.name}: {result.outcome}; usage={result.usage is not None}; '
                  f'rate_events={len(events)}', flush=True)
            if result.outcome != workers.OK or not result.session_id:
                continue
            events.clear()
            steps.clear()
            resume = dataclasses.replace(request, job_id=request.job_id + 1,
                                         job_name='resume', session_id=result.session_id,
                                         spec=dataclasses.replace(spec, tools=[]),
                                         prompt='What nonce did I ask you to remember? '
                                                'Reply with that nonce only. Use no tools.')
            names.append(f'carlo-job-{resume.job_id}')
            print(f'{account.name}: resume in fresh container', flush=True)
            resumed = workers.SdkWorker(backend).run(resume)
            replies = [s[2] or '' for s in steps if s[0] in ('text', 'result')]
            entry.update(resume=dataclasses.asdict(resumed), resume_rate_limits=list(events),
                         resume_steps=list(steps), nonce_recalled=any(nonce in s for s in replies),
                         same_session=resumed.session_id == result.session_id,
                         transcript_exists=bool(resumed.transcript and resumed.transcript.is_file()),
                         resumed_container_removed=backend.call('container', 'exists',
                                                                 names[-1]).returncode != 0)
            save()
            print(f'{account.name}: resume={resumed.outcome}; '
                  f'nonce_recalled={entry["nonce_recalled"]}', flush=True)
        print('Headed parish-site browser probe', flush=True)
        work = output / 'browser'
        workspace.refresh(trusted, work)
        (work / 'probe.py').write_text(BROWSER_PROBE)
        name = f'carlo-validation-browser-{suffix}'
        names.append(name)
        box = sandbox.Box(name, report['image'], work,
                          mounts=[sandbox.Mount(p, p, ro) for p, ro in workspace.mounts(work)],
                          env=sandbox.container_env(work) | {'CARLO_NO_DOTENV': '1'},
                          command=['xvfb-run', '-a', 'python', 'probe.py'])
        browser = subprocess.run(sandbox.run_argv(backend.podman, box), capture_output=True,
                                 text=True, timeout=420)
        (output / 'browser.stdout').write_text(browser.stdout)
        (output / 'browser.stderr').write_text(browser.stderr)
        report['browser'] = {'exit_code': browser.returncode}
        if browser.returncode == 0:
            report['browser']['result'] = json.loads(browser.stdout)
        save()
        print(f'Browser exit: {browser.returncode}; report: {output / "report.json"}', flush=True)
        passed = bool(report['accounts']) and all(a.get('nonce_recalled') and a.get('same_session') and
                     a.get('account_windows_match') and
                     a.get('file_written') and a.get('transcript_exists') and
                     a['resume']['outcome'] == workers.OK for a in report['accounts'])
        return 0 if passed and browser.returncode == 0 else 1
    finally:
        for name in [*names, sandbox.PROXY]:
            backend.call('rm', '-f', name)
        backend.call('network', 'rm', sandbox.NETWORK)
        report['finished_at'] = datetime.now(UTC).isoformat()
        save()


if __name__ == '__main__':
    raise SystemExit(main())
