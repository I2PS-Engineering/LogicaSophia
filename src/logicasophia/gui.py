"""LogicaSophia local-first task GUI. No external web server or dependencies.

The UI is only accessible from 127.0.0.1, never from the LAN. Task execution
uses the existing evidence-governed agent, with an explicit workspace scope.
"""
from __future__ import annotations

import json
import secrets
import threading
import uuid
import webbrowser
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .agent import run_agent
from .backend import BackendError, LocalBackend

STATIC = Path(__file__).with_name('web')
MAX_POST = 8192
MAX_RUNS = 20


@dataclass
class TaskRun:
    run_id: str
    goal: str
    status: str = 'QUEUED'
    events: list[dict] = field(default_factory=list)
    result: dict | None = None
    error: str | None = None

    def public(self) -> dict:
        return {'run_id': self.run_id, 'goal': self.goal, 'status': self.status,
                'events': self.events[-100:], 'result': self.result,
                'error': self.error}


class App(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address: tuple[str,int], backend: LocalBackend,
                 workspace: Path, results: Path):
        if address[0] != '127.0.0.1':
            raise ValueError('GUI must bind only to 127.0.0.1')
        self.backend = backend
        self.workspace = workspace.expanduser().resolve(strict=True)
        if not self.workspace.is_dir():
            raise ValueError('GUI workspace must be a directory')
        self.results = results.expanduser().resolve()
        if self.results == self.workspace or self.results.is_relative_to(self.workspace):
            raise ValueError('Results must be outside workspace')
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.RLock()
        self.runs: dict[str,TaskRun] = {}
        self.active: str | None = None
        super().__init__(address, RequestHandler)

    def enqueue(self, goal: str, model: str | None) -> TaskRun:
        if not isinstance(goal, str) or not (1 <= len(goal.strip()) <= 1500):
            raise ValueError('goal must have 1 to 1500 characters')
        if model is not None and (not isinstance(model, str) or len(model) > 256):
            raise ValueError('invalid model')
        with self.lock:
            if self.active and self.runs[self.active].status in ('QUEUED','RUNNING'):
                raise RuntimeError('one task at a time on this Linux host')
            record = TaskRun(uuid.uuid4().hex, goal.strip())
            self.runs[record.run_id] = record
            self.active = record.run_id
            for key in list(self.runs)[:-MAX_RUNS]:
                del self.runs[key]
        threading.Thread(target=self._execute, args=(record, model), daemon=True).start()
        return record

    def _execute(self, record: TaskRun, model: str | None) -> None:
        with self.lock:
            record.status = 'RUNNING'
            record.events.append({'type':'state','state':'RUNNING'})
        def on_event(event: dict) -> None:
            with self.lock:
                record.events.append(event)
                if len(record.events) > 100:
                    del record.events[:len(record.events)-100]
        try:
            result = run_agent(record.goal, self.workspace, self.results,
                               self.backend, model=model, event_sink=on_event)
            with self.lock:
                record.result = result
                record.status = result['status']
        except Exception as exc:
            with self.lock:
                record.status = 'FAILED'
                record.error = type(exc).__name__ + ': ' + str(exc)[:300]
        finally:
            with self.lock:
                record.events.append({'type':'state','state':record.status})


class RequestHandler(BaseHTTPRequestHandler):
    server: App
    def log_message(self, fmt, *args):
        pass

    def _reply(self, status: int, data: bytes, kind: str, *, cache: str = 'no-store') -> None:
        self.send_response(status)
        self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control',cache)
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',
            "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status: int, value: object) -> None:
        self._reply(status,json.dumps(value,ensure_ascii=False).encode('utf-8'), 'application/json; charset=utf-8')

    def _allowed_host(self) -> bool:
        # The server binds loopback; also reject attacker-controlled Host headers.
        host = self.headers.get('Host','')
        port = self.server.server_port
        return host in (f'127.0.0.1:{port}', f'localhost:{port}')

    def do_GET(self):
        if not self._allowed_host():
            return self._json(403, {'error':'unrecognized_host'})
        route = urlsplit(self.path).path
        if route == '/':
            template=(STATIC/'index.html').read_text(encoding='utf-8')
            # Token is ASCII URL-safe. Never store it outside the local HTML page.
            content=template.replace('__LOCAL_TASK_TOKEN__',self.server.token)
            return self._reply(200,content.encode('utf-8'),'text/html; charset=utf-8')
        if route in ('/assets/identity.jpeg','/assets/app.css','/assets/app.js'):
            file = STATIC / route.split('/')[-1]
            kind = {'jpeg':'image/jpeg','css':'text/css; charset=utf-8','js':'text/javascript; charset=utf-8'}[file.suffix[1:]]
            return self._reply(200,file.read_bytes(),kind,cache='public, max-age=300')
        if route == '/api/status':
            try:
                names = [r.get('id') for r in self.server.backend.models(timeout=2).get('data',[])
                         if isinstance(r,dict) and isinstance(r.get('id'),str)]
                available = bool(names)
                err = None
            except (BackendError,ValueError,TypeError) as exc:
                names,available,err = [],False,str(exc)
            return self._json(200, {'project':'LogicaSophia','gui_version':'0.4.0',
                'backend_ready':available,'models':names,'backend_error':err,
                'workspace':str(self.server.workspace),'tool_access':'read-only',
                'verification':'source_integrity_not_semantic_truth'})
        if route == '/api/runs':
            with self.server.lock:
                values=[{'run_id':r.run_id,'goal':r.goal,'status':r.status} for r in self.server.runs.values()]
            return self._json(200, {'runs':list(reversed(values))})
        if route.startswith('/api/runs/'):
            ident=route[len('/api/runs/'):]
            with self.server.lock:
                result = self.server.runs.get(ident)
                doc = result.public() if result else None
            return self._json(200,doc) if doc else self._json(404,{'error':'run_not_found'})
        return self._json(404, {'error':'not_found'})

    def do_POST(self):
        if not self._allowed_host():
            return self._json(403, {'error':'unrecognized_host'})
        origin=self.headers.get('Origin')
        port=self.server.server_port
        if origin and origin not in (f'http://127.0.0.1:{port}',f'http://localhost:{port}'):
            return self._json(403,{'error':'origin_denied'})
        if self.headers.get('X-LogicaSophia-Token') != self.server.token:
            return self._json(403, {'error':'invalid_local_token'})
        if self.path != '/api/runs':
            return self._json(404,{'error':'not_found'})
        if self.headers.get('Content-Type','').split(';')[0].strip().lower() != 'application/json':
            return self._json(415,{'error':'expected_json'})
        try:
            length=int(self.headers.get('Content-Length','0'))
        except ValueError:
            return self._json(400,{'error':'invalid_content_length'})
        if not 1 <= length <= MAX_POST:
            return self._json(413,{'error':'request_size_limit'})
        try:
            data=json.loads(self.rfile.read(length))
        except (ValueError,UnicodeError):
            return self._json(400, {'error':'invalid_json'})
        if not isinstance(data,dict) or set(data) - {'goal','model'}:
            return self._json(400,{'error':'invalid_fields'})
        try:
            record=self.server.enqueue(data.get('goal'),data.get('model'))
        except ValueError as exc:
            return self._json(400, {'error':str(exc)})
        except RuntimeError as exc:
            return self._json(409, {'error':str(exc)})
        return self._json(202, {'run_id':record.run_id,'status':record.status})


def create_server(port: int = 8766, *, backend_url: str = 'http://127.0.0.1:8090',
                  workspace: Path, results: Path) -> App:
    return App(('127.0.0.1',port), LocalBackend.from_url(backend_url),workspace,results)


def launch_gui(port: int, backend_url: str, workspace: Path, results: Path,
               *, open_browser: bool = True) -> None:
    with create_server(port, backend_url=backend_url, workspace=workspace,results=results) as app:
        url=f'http://127.0.0.1:{app.server_port}'
        print(f'LogicaSophia GUI: {url}\nWorkspace: {app.workspace}\nCtrl+C to close.')
        if open_browser:
            # A web-browser launch is optional; headless Linux hosts can use the URL.
            threading.Thread(target=webbrowser.open,args=(url,),daemon=True).start()
        try:
            app.serve_forever(poll_interval=0.2)
        except KeyboardInterrupt:
            pass
