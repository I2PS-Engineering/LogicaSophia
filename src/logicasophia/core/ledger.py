"""SQLite event archive + JSONL hash-chained audit trail, and offline replay."""
from __future__ import annotations
import hashlib
import json
import sqlite3
from pathlib import Path
from .state_machine import transition


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


class Ledger:
    def __init__(self, directory: Path, task_id: str, trace_id: str):
        directory.mkdir(parents=True, exist_ok=False)
        self.directory = directory
        self.trace = (directory / 'trace.jsonl').open('w', encoding='utf-8')
        self.db = sqlite3.connect(directory / 'events.sqlite3')
        self.db.execute('CREATE TABLE events (seq INTEGER PRIMARY KEY, state TEXT NOT NULL, kind TEXT NOT NULL, digest TEXT NOT NULL, payload_json TEXT NOT NULL)')
        self.task_id, self.trace_id = task_id, trace_id
        self.prev, self.seq = '0' * 64, 0

    def append(self, state: str, kind: str, payload: dict) -> None:
        self.seq += 1
        row = {'seq': self.seq, 'task_id': self.task_id, 'trace_id': self.trace_id,
               'state': state, 'kind': kind, 'payload': payload, 'previous_hash': self.prev}
        row['hash'] = hashlib.sha256(canonical(row)).hexdigest()
        encoded = canonical(row).decode('utf-8')
        self.trace.write(encoded + '\n')
        self.trace.flush()
        self.db.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?)',
                        (self.seq, state, kind, row['hash'], json.dumps(payload, sort_keys=True)))
        self.db.commit()
        self.prev = row['hash']

    def close(self):
        self.trace.close()
        self.db.close()


def replay(directory: Path) -> dict:
    rows = [json.loads(line) for line in (directory / 'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    if not rows:
        raise ValueError('empty_trace')
    previous, state, task_id, trace_id = '0' * 64, None, rows[0]['task_id'], rows[0]['trace_id']
    for seq, row in enumerate(rows, 1):
        digest = row.get('hash')
        data = {k: v for k, v in row.items() if k != 'hash'}
        if (row.get('seq') != seq or row.get('previous_hash') != previous
                or row.get('task_id') != task_id or row.get('trace_id') != trace_id
                or hashlib.sha256(canonical(data)).hexdigest() != digest):
            raise ValueError('trace_integrity_failure')
        if row['kind'] == 'transition':
            if state is None:
                if row['state'] != 'RECEIVED':
                    raise ValueError('invalid_initial_state')
            else:
                transition(state, row['state'])
            state = row['state']
        elif row['state'] != state:
            raise ValueError('event_state_mismatch')
        previous = digest
    if state not in ('ACCEPTED', 'FAILED', 'UNCERTAIN'):
        raise ValueError('nonterminal_trace')
    outcome = json.loads((directory / 'outcome.json').read_text(encoding='utf-8'))
    if outcome.get('status') != state or outcome.get('trace_hash') != previous or outcome.get('trace_id') != trace_id:
        raise ValueError('outcome_integrity_failure')
    return {'task_id': task_id, 'trace_id': trace_id, 'status': state, 'events': len(rows), 'trace_hash': previous}
