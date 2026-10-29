"""Integration smoke test: local mocked model server + REAL agent tool loop."""
from __future__ import annotations
import json
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from logicasophia.agent import run_agent
from logicasophia.backend import LocalBackend
from logicasophia.core.ledger import replay


class ModelStub(BaseHTTPRequestHandler):
    turns = 0

    def log_message(self, *args):
        pass

    def send(self, doc):
        raw = json.dumps(doc).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == '/v1/models':
            self.send({'data': [{'id': 'mock-local-model'}]})
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
        messages = body['messages']
        inspected = any('TOOL OBSERVATION' in m.get('content', '') for m in messages)
        action = ({'action': 'final', 'answer': 'The file defines a greeting function.'} if inspected
                  else {'action': 'read_file', 'path': 'hello.py'})
        self.send({'choices': [{'message': {'role': 'assistant', 'content': json.dumps(action)}}]})


def main():
    with tempfile.TemporaryDirectory() as scratch:
        workspace = Path(scratch) / 'workspace'
        workspace.mkdir()
        (workspace / 'hello.py').write_text('def hello():\n    return "hello"\n')
        with ThreadingHTTPServer(('127.0.0.1', 0), ModelStub) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                outcome = run_agent('Summarize hello.py', workspace, Path(scratch) / 'results',
                                    LocalBackend('127.0.0.1', server.server_port))
                assert outcome['status'] == 'ACCEPTED', outcome
                assert replay(Path(outcome['directory']))['status'] == 'ACCEPTED'
                print(json.dumps({'status': outcome['status'], 'answer': outcome['answer'],
                                  'trace_replay': 'passed', 'model': outcome['model']}, indent=2))
            finally:
                server.shutdown()
                thread.join()


if __name__ == '__main__':
    main()
