"""Explicit transition graph; terminal states cannot change."""
TRANSITIONS = {
    'RECEIVED': {'VALIDATED', 'FAILED'},
    'VALIDATED': {'PLANNED', 'FAILED'},
    'PLANNED': {'POLICY_CHECKED', 'FAILED'},
    'POLICY_CHECKED': {'EXECUTING', 'FAILED'},
    'EXECUTING': {'OBSERVING', 'FAILED', 'UNCERTAIN'},
    'OBSERVING': {'VERIFYING', 'FAILED', 'UNCERTAIN'},
    'VERIFYING': {'ACCEPTED', 'FAILED', 'UNCERTAIN'},
    'ACCEPTED': set(), 'FAILED': set(), 'UNCERTAIN': set(),
}


def transition(current: str, target: str) -> str:
    if target not in TRANSITIONS.get(current, set()):
        raise ValueError(f'illegal_transition:{current}->{target}')
    return target
