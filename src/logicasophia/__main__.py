"""Standalone LogicaSophia CLI: inventory, localhost gateway, autonomous agent."""
from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

from .backend import LocalBackend
from .inventory import collect_inventory
from .service import serve


def main() -> None:
    parser = argparse.ArgumentParser(prog='logicasophia', description='LogicaSophia local AI engineering system')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('inventory', help='Print read-only Linux inventory as JSON')
    server = commands.add_parser('serve', help='Start the localhost HTTP gateway')
    server.add_argument('--port', type=int, default=8765)
    server.add_argument('--backend-url', help='LOCAL OpenAI-compatible inference server')
    agent = commands.add_parser('agent', help='Run autonomous, evidence-governed workspace analysis')
    agent.add_argument('--goal', required=True, help='What LogicaSophia should analyze')
    agent.add_argument('--workspace', type=Path, default=Path('.'))
    agent.add_argument('--results', type=Path, default=Path.home() / '.local/share/logicasophia/results')
    agent.add_argument('--backend-url', default='http://127.0.0.1:8090')
    agent.add_argument('--model', help='Optional exact model ID; default uses the first available local model')
    agent.add_argument('--max-steps', type=int, default=6)
    agent.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    if platform.system() != 'Linux' and args.command != 'inventory':
        parser.error('LogicaSophia currently supports Linux hosts')
    if args.command == 'inventory':
        print(json.dumps(collect_inventory(), indent=2, ensure_ascii=False))
    elif args.command == 'serve':
        try:
            backend = LocalBackend.from_url(args.backend_url) if args.backend_url else None
        except ValueError as exc:
            parser.error(str(exc))
        serve(port=args.port, backend=backend)
    else:
        from .agent import run_agent
        try:
            backend = LocalBackend.from_url(args.backend_url)
            outcome = run_agent(args.goal, args.workspace, args.results, backend,
                                model=args.model, max_steps=args.max_steps, timeout=args.timeout)
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        print('\nLogicaSophia: ' + outcome['status'])
        print('Model: ' + str(outcome['model']))
        if outcome['answer']:
            print('\n' + outcome['answer'])
        if outcome['reason']:
            print('Reason: ' + outcome['reason'])
        print('\nAudit: ' + outcome['directory'])
        print('Verification covers source integrity, not factual correctness of the AI answer.')
        if outcome['status'] != 'ACCEPTED':
            raise SystemExit(2)


if __name__ == '__main__':
    main()
