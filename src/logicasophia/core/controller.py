"""Deterministic Phase-A controller. No model, shell or external agent runtime."""
from __future__ import annotations
import json
import uuid
from pathlib import Path
from .contracts import Task
from .filesystem import ObservationError, read_observation, search_observation
from .ledger import Ledger
from .policy import authorize
from .state_machine import transition
from .verifier import verify


def execute(contract: dict, workspace: Path, results: Path, before_verify=None) -> dict:
    task = Task.parse(contract)  # invalid input fails before any results are written
    workspace = workspace.expanduser().resolve(strict=True)
    results = results.expanduser().resolve()
    if not workspace.is_dir() or results == workspace or results.is_relative_to(workspace):
        raise ValueError('unsafe_workspace_or_results')
    trace_id = uuid.uuid4().hex
    directory = results / trace_id
    ledger = Ledger(directory, task.task_id, trace_id)
    state = None
    observations = []
    checks = []
    reason = None

    def step(next_state: str):
        nonlocal state
        if state is not None:
            transition(state, next_state)
        elif next_state != 'RECEIVED':
            raise ValueError('invalid_initial_state')
        state = next_state
        ledger.append(state, 'transition', {})

    try:
        step('RECEIVED')
        step('VALIDATED')
        step('PLANNED')
        for planned in task.steps:
            step('POLICY_CHECKED') if state == 'PLANNED' else None
            permitted, decision = authorize(task, planned)
            ledger.append(state, 'policy', {'tool': planned.tool, 'path': planned.path, 'allowed': permitted, 'reason': decision})
            if not permitted:
                reason = 'policy_denied'
                step('FAILED')
                break
        else:
            step('EXECUTING')
            for planned in task.steps:
                try:
                    if planned.tool == 'read_file':
                        observation = read_observation(workspace, planned.path)
                    else:
                        observation = search_observation(workspace, planned.path, planned.query)
                    observations.append(observation)
                    ledger.append(state, 'observation', observation)
                except ObservationError as exc:
                    reason = exc.code
                    ledger.append(state, 'execution_error', {'code': reason, 'exit_code': 1})
                    step('UNCERTAIN')
                    break
            else:
                step('OBSERVING')
                if before_verify:
                    before_verify()
                step('VERIFYING')
                status, checks = verify(task, observations, workspace)
                ledger.append(state, 'verification', {'status': status, 'checks': checks})
                if status != 'ACCEPTED':
                    reason = 'verification_failed' if status == 'FAILED' else 'missing_or_changed_evidence'
                step(status)
    except Exception:
        # Unexpected exceptions must never result in an acceptance claim.
        # There may be an incomplete trace; operator must investigate it.
        raise
    finally:
        outcome = {'task_id': task.task_id, 'trace_id': trace_id, 'status': state,
                   'reason': reason, 'checks': checks, 'observations': observations,
                   'trace_hash': ledger.prev}
        (directory / 'outcome.json').write_text(json.dumps(outcome, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        ledger.close()
    return {'directory': str(directory), **outcome}
