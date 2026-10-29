"""Independent evidence verification, not model self-certification."""
from __future__ import annotations
import hashlib
from pathlib import Path
from .contracts import Task
from .filesystem import ObservationError, read_scoped


def verify(task: Task, observations: list[dict], workspace: Path) -> tuple[str, list[dict]]:
    evidence = {o['path']: o['sha256'] for o in observations if o['tool'] == 'read_file'}
    results = []
    for check in task.checks:
        if check.path not in evidence:
            results.append({'path': check.path, 'result': 'missing_observation'})
            return 'UNCERTAIN', results
        try:
            raw = read_scoped(workspace, check.path)
        except ObservationError:
            results.append({'path': check.path, 'result': 'unavailable_at_verification'})
            return 'UNCERTAIN', results
        digest = hashlib.sha256(raw).hexdigest()
        if digest != evidence[check.path]:
            results.append({'path': check.path, 'result': 'changed_after_observation'})
            return 'UNCERTAIN', results
        passed = check.expected in raw.decode('utf-8')
        results.append({'path': check.path, 'result': 'pass' if passed else 'mismatch', 'sha256': digest})
        if not passed:
            return 'FAILED', results
    return 'ACCEPTED', results
