"""One command to test LogicaSophia's evidence-governed Phase A controller."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from logicasophia.core.controller import execute
from logicasophia.core.ledger import replay


def main() -> int:
    parser = argparse.ArgumentParser(description='LogicaSophia deterministic execution demo')
    parser.add_argument('--task', type=Path, default=ROOT / 'fixtures/inspect_python.json')
    parser.add_argument('--workspace', type=Path, default=ROOT / 'fixtures/project_fixture')
    parser.add_argument('--results', type=Path, default=ROOT / 'results')
    args = parser.parse_args()
    contract = json.loads(args.task.read_text(encoding='utf-8'))
    outcome = execute(contract, args.workspace, args.results)
    print(json.dumps({'result': outcome['status'], 'reason': outcome['reason'],
                      'folder': outcome['directory'], 'replay': replay(Path(outcome['directory']))}, indent=2))
    return 0 if outcome['status'] == 'ACCEPTED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
