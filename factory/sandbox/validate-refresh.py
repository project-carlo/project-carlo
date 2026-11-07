"""Measure and check production workspace refresh against an isolated Run snapshot.

uv run python factory/sandbox/validate-refresh.py /path/to/completed/run
Source checkout is read only: git archive plus SQLite read-only online backup.
Only the temporary copies are changed. Does not start a dispatcher or containers.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import tempfile
import time
from pathlib import Path

from pdf_extract.factory import workspace


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    os.umask(0o077)
    output = Path(tempfile.mkdtemp(prefix='carlo-pr184-refresh-'))
    print(f'Private artifacts: {output}', flush=True)
    trusted = output / 'trusted'
    trusted.mkdir()
    report = {'source': str(source), 'source_commit': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip(),
        'cache_caveat': 'Empty-destination timings; OS page caches were not flushed.',
        'timings': []}
    # No untracked files or credentials copied from the source Run.
    with tempfile.TemporaryFile() as archive:
        subprocess.run(['git', 'archive', 'HEAD'], cwd=source, stdout=archive, check=True)
        archive.seek(0)
        subprocess.run(['tar', '-x', '-C', str(trusted)], stdin=archive, check=True)
    databases = []
    for database in (source / 'data').glob('*.db'):
        dest = trusted / 'data' / database.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        reader = sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)
        writer = sqlite3.connect(dest)
        try:
            reader.backup(writer)
        finally:
            reader.close()
            writer.close()
        databases.append(dest.relative_to(trusted).as_posix())
    report['databases'] = databases
    files = [p for p in trusted.rglob('*') if p.is_file() and not p.is_symlink()]
    report['source_files'] = len(files)
    report['source_bytes'] = sum(p.stat().st_size for p in files)

    def refresh(kind: str, work: Path):
        started = time.perf_counter()
        snapshot = workspace.refresh(trusted, work)
        elapsed = time.perf_counter() - started
        report['timings'].append({'kind': kind, 'seconds': elapsed,
                                  'snapshot_entries': len(snapshot)})
        print(f'{kind}: {elapsed:.3f}s ({len(snapshot)} snapshot entries)', flush=True)

    # Three independent empty destinations; not three OS-cold cache runs.
    for index in range(3):
        refresh('empty-destination', output / f'work-{index}')
    work = output / 'work-0'
    for _ in range(5):
        refresh('unchanged', work)

    cached = work / '.cache' / 'validation-keep.txt'
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text('worker-private cache')
    database = work / databases[0] if databases else None
    if database:
        with sqlite3.connect(database) as db:
            db.execute('CREATE TABLE validation_private_marker (value TEXT)')
            db.execute('INSERT INTO validation_private_marker VALUES (?)', ('keep',))

    relative = 'src/pdf_extract/factory/workers.py'
    original = (trusted / relative).read_bytes()
    before = (trusted / relative).stat()
    before_bytes = (work / relative).read_bytes()
    (work / relative).write_text('out-of-scope worker edit\n')
    rogue = work / 'src' / 'validation-rogue.py'
    rogue.write_text('untrusted extra file\n')
    stray = work / 'validation-out-of-scope.txt'
    stray.write_text('untrusted extra file\n')
    refresh('after-worker-edits', work)
    assert (work / relative).read_bytes() == original == before_bytes
    assert not rogue.exists() and not stray.exists()
    assert cached.read_text() == 'worker-private cache'
    if database:
        with sqlite3.connect(database) as db:
            assert db.execute('SELECT value FROM validation_private_marker').fetchone() == ('keep',)
        with sqlite3.connect(trusted / databases[0]) as db:
            assert not db.execute("SELECT 1 FROM sqlite_master WHERE name='validation_private_marker'").fetchone()
    assert (trusted / relative).stat().st_mtime_ns == before.st_mtime_ns

    # A trusted source update must reach the worker without resetting its private state.
    (trusted / relative).write_bytes(original + b'\n# validation-only trusted update\n')
    refresh('after-trusted-update', work)
    assert (work / relative).read_bytes() == (trusted / relative).read_bytes()
    assert cached.read_text() == 'worker-private cache'
    report['checks'] = {'out_of_scope_edit_reset': True, 'out_of_scope_additions_removed': True,
                        'private_cache_preserved': True, 'private_database_preserved': bool(database),
                        'trusted_update_copied': True, 'source_run_modified': False}
    report['passed'] = True
    (output / 'report.json').write_text(json.dumps(report, indent=2))
    print(f'Report: {output / "report.json"}', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
