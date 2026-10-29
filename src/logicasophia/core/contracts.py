"""Strict, versioned task contracts. No executable code in the contract."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import PurePosixPath

MAX_STEPS = 8
TOOLS = frozenset({'read_file', 'search_files'})


def valid_path(value: object, allow_root: bool = False) -> str:
    if not isinstance(value, str) or not value or len(value) > 240 or '\\' in value or '\x00' in value:
        raise ValueError('invalid_path')
    if value == '.' and allow_root:
        return '.'
    p = PurePosixPath(value)
    if p.is_absolute() or ':' in value or any(c in ('.', '..', '') for c in value.split('/')):
        raise ValueError('invalid_path')
    return value


@dataclass(frozen=True)
class Step:
    tool: str
    path: str
    query: str | None = None


@dataclass(frozen=True)
class Check:
    kind: str
    path: str
    expected: str


@dataclass(frozen=True)
class Task:
    task_id: str
    goal: str
    allowed_tools: frozenset[str]
    steps: tuple[Step, ...]
    checks: tuple[Check, ...]

    @classmethod
    def parse(cls, payload: object) -> 'Task':
        if not isinstance(payload, dict) or payload.get('schema_version') != 1:
            raise ValueError('invalid_schema')
        task_id, goal = payload.get('task_id'), payload.get('goal')
        if not isinstance(task_id, str) or not (1 <= len(task_id) <= 72) or not all(c.isascii() and (c.isalnum() or c in '-_') for c in task_id):
            raise ValueError('invalid_task_id')
        if not isinstance(goal, str) or not (1 <= len(goal) <= 500):
            raise ValueError('invalid_goal')
        allowed = payload.get('allowed_tools')
        steps = payload.get('steps')
        checks = payload.get('success_checks')
        if not isinstance(allowed, list) or not all(isinstance(x, str) for x in allowed) or len(allowed) != len(set(allowed)):
            raise ValueError('invalid_allowed_tools')
        if not isinstance(steps, list) or not (1 <= len(steps) <= MAX_STEPS):
            raise ValueError('invalid_steps')
        if not isinstance(checks, list) or not (1 <= len(checks) <= MAX_STEPS):
            raise ValueError('invalid_checks')
        parsed_steps = []
        for raw in steps:
            if not isinstance(raw, dict) or not isinstance(raw.get('tool'), str):
                raise ValueError('invalid_step')
            path = valid_path(raw.get('path'), allow_root=raw['tool'] == 'search_files')
            query = raw.get('query')
            if raw['tool'] == 'search_files' and (not isinstance(query, str) or not (1 <= len(query) <= 100)):
                raise ValueError('invalid_query')
            parsed_steps.append(Step(raw['tool'], path, query))
        parsed_checks = []
        for raw in checks:
            if not isinstance(raw, dict) or raw.get('type') != 'file_contains':
                raise ValueError('unsupported_check')
            value = raw.get('text')
            if not isinstance(value, str) or not (1 <= len(value) <= 200):
                raise ValueError('invalid_check_text')
            parsed_checks.append(Check('file_contains', valid_path(raw.get('path')), value))
        return cls(task_id, goal, frozenset(allowed), tuple(parsed_steps), tuple(parsed_checks))
