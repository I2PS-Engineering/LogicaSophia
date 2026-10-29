import http.client
import hashlib
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from logicasophia.gui import create_server, STATIC
from logicasophia.backend import BackendError

class FakeBackend:
    def models(self, timeout=2):
        return {'data':[{'id':'test-qwen'}]}
    def request(self, method, path, payload, timeout=180):
        messages=payload['messages']
        if any('TOOL OBSERVATION' in row.get('content','') for row in messages):
            decision={'action':'final','answer':'add(a,b) returns a+b'}
        else:
            decision={'action':'read_file','path':'hello.py'}
        return 200, {'choices':[{'message':{'content':json.dumps(decision)}}]}

class GUIIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        cls.workspace=cls.root/'workspace'
        cls.workspace.mkdir()
        (cls.workspace/'hello.py').write_text('def add(a,b):\n    return a+b\n')
        cls.server=create_server(0,workspace=cls.workspace,results=cls.root/'results')
        cls.server.backend=FakeBackend()
        cls.port=cls.server.server_port
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=3);cls.temp.cleanup()
    def request(self,method,path,body=None,headers=None):
        conn=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        h={'Host':f'127.0.0.1:{self.port}',**(headers or {})}
        conn.request(method,path,body=body,headers=h)
        r=conn.getresponse();raw=r.read();status=r.status;typ=r.getheader('Content-Type')
        conn.close();return status,raw,typ
    def test_index_has_brand_and_csp(self):
        code,raw,typ=self.request('GET','/')
        self.assertEqual(code,200)
        self.assertIn('LogicaSophia',raw.decode())
        self.assertIn(self.server.token,raw.decode())
        self.assertIn('text/html',typ)
    def test_approved_artwork_served(self):
        code,raw,typ=self.request('GET','/assets/identity.jpeg')
        self.assertEqual(code,200)
        self.assertTrue(raw.startswith(b'\xff\xd8\xff'))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39')
        self.assertEqual(raw,(STATIC/'identity.jpeg').read_bytes())
    def test_api_status_models(self):
        code,raw,_=self.request('GET','/api/status')
        data=json.loads(raw)
        self.assertTrue(data['backend_ready'])
        self.assertEqual(data['models'],['test-qwen'])
        self.assertEqual(data['tool_access'],'read-only')
    def test_reject_missing_token(self):
        code,raw,_=self.request('POST','/api/runs','{}',{'Content-Type':'application/json'})
        self.assertEqual(code,403)
    def test_reject_bad_host(self):
        code,_,_=self.request('GET','/api/status',headers={'Host':'evil.example'})
        self.assertEqual(code,403)
    def test_reject_bad_origin(self):
        headers={'Content-Type':'application/json','X-LogicaSophia-Token':self.server.token,'Origin':'https://evil.example'}
        code,_,_=self.request('POST','/api/runs','{}',headers)
        self.assertEqual(code,403)
    def test_reject_oversize(self):
        code,_,_=self.request('POST','/api/runs','x'*8200,{'Content-Type':'application/json','X-LogicaSophia-Token':self.server.token})
        self.assertEqual(code,413)
    def test_real_agent_through_gui_and_evidence(self):
        body=json.dumps({'goal':'Explain hello.py','model':'test-qwen'})
        code,raw,_=self.request('POST','/api/runs',body,{'Content-Type':'application/json','X-LogicaSophia-Token':self.server.token})
        self.assertEqual(code,202,raw)
        run_id=json.loads(raw)['run_id']
        for i in range(80):
            code,raw,_=self.request('GET','/api/runs/'+run_id)
            doc=json.loads(raw)
            if doc['status'] not in ('QUEUED','RUNNING'):break
            time.sleep(0.05)
        self.assertEqual(doc['status'],'ACCEPTED',doc)
        self.assertIn('add(a,b)',doc['result']['answer'])
        self.assertTrue(any(e['type']=='decision' for e in doc['events']))
        self.assertTrue(any(e['type']=='evidence' for e in doc['events']))
        self.assertTrue(any(e['type']=='verification' for e in doc['events']))
        path=Path(doc['result']['directory'])
        self.assertTrue((path/'outcome.json').exists())
        self.assertTrue((path/'trace.jsonl').exists())
        self.assertTrue((path/'events.sqlite3').exists())
    def test_one_task_at_a_time(self):
        from logicasophia.gui import TaskRun
        with self.server.lock:
            self.server.runs['busy']=TaskRun('busy','test',status='RUNNING')
            self.server.active='busy'
        try:
            body=json.dumps({'goal':'Read hello.py'})
            code,_,_=self.request('POST','/api/runs',body,{'Content-Type':'application/json','X-LogicaSophia-Token':self.server.token})
            self.assertEqual(code,409)
        finally:
            with self.server.lock:
                self.server.active=None
                del self.server.runs['busy']

class GUIBoundaryTests(unittest.TestCase):
    def test_reject_remote_bind(self):
        from logicasophia.gui import App,RequestHandler
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                App(('0.0.0.0',0),FakeBackend(),Path(tmp),Path(tmp).parent/'r')
    def test_reject_results_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                create_server(0,workspace=Path(tmp),results=Path(tmp)/'result')

if __name__=='__main__':unittest.main()
