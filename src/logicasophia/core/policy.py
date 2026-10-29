"""Deny-by-default policy; Phase A permits only two read-only tools."""
from __future__ import annotations
from .contracts import Task, Step, TOOLS


def authorize(task: Task, step: Step) -> tuple[bool, str]:
    if step.tool not in TOOLS:
        return False, 'tool_not_implemented_or_denied'
    if step.tool not in task.allowed_tools:
        return False, 'tool_not_allowed_by_task'
    return True, 'read_only_tool_allowed'
