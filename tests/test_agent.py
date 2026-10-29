import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from logicasophia.agent import parse_decision, run_agent, safe_manifest
from logicasophia.backend import BackendError
from logicasophia.core.ledger import replay


class FakeBackend:
    def __init__(self, actions, on_completion=None):
        self.actions = list(actions)
        self.calls = []
        self.on_completion = on_completion

    def models(self, timeout=10):
        return {'data': [{'id': 'mock-brain'}]}

    def request(self, method, path, payload, timeout=180):
        self.calls.append((method, path, payload))
        if self.on_completion:
            self.on_completion(len(self.calls))
        return 200, {'choices': [{'message': {'content': json.dumps(self.actions.pop(0))}}]}


class ModelAgentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.workspace = self.root / 'workspace'
        self.workspace.mkdir()
        (self.workspace / 'hello.py').write_text('def hello():\n    return "hello"\n')
        self.results = self.root / 'results'

    def run_actions(self, actions, **kwargs):
        backend = FakeBackend(actions, on_completion=kwargs.pop('on_completion', None))
        outcome = run_agent('Explain hello.py', self.workspace, self.results,
                            backend, **kwargs)
        return outcome, backend

    def test_autonomous_read_and_final_verifies(self):
        outcome, backend = self.run_actions([
            {'action':'read_file','path':'hello.py'},
            {'action':'final','answer':'Defines hello() which returns hello.'},
        ])
        self.assertEqual(outcome['status'], 'ACCEPTED')
        self.assertEqual(outcome['model'], 'mock-brain')
        self.assertEqual(outcome['model_calls'], 2)
        self.assertEqual(replay(Path(outcome['directory']))['status'], 'ACCEPTED')
        self.assertEqual(outcome['verification_scope'], 'source_integrity_only_not_semantic_correctness')
        self.assertEqual(backend.calls[1][2]['messages'][-1]['role'], 'user')

    def test_unobserved_final_is_uncertain(self):
        outcome, _ = self.run_actions([{'action':'final','answer':'unsupported'}])
        self.assertEqual(outcome['status'], 'UNCERTAIN')

    def test_unknown_tool_denied_by_parser(self):
        with self.assertRaises(ValueError):
            parse_decision('{"action":"shell","command":"rm -rf /"}')

    def test_traversal_denied(self):
        with self.assertRaises(ValueError):
            parse_decision('{"action":"read_file","path":"../../etc/passwd"}')

    def test_malformed_model_json_fails_closed(self):
        class Invalid(FakeBackend):
            def request(self,*a,**kw):
                return 200, {'choices':[{'message':{'content':'not json'}}]}
        out=run_agent('Explain',self.workspace,self.results,Invalid([]))
        self.assertEqual(out['status'],'FAILED')
        self.assertEqual(replay(Path(out['directory']))['status'],'FAILED')

    def test_no_backend_model_reports_failure(self):
        class NoModel(FakeBackend):
            def models(self,timeout=10):
                raise BackendError('offline')
        out=run_agent('Explain',self.workspace,self.results,NoModel([]))
        self.assertEqual(out['status'],'FAILED')
        self.assertEqual(out['reason'],'offline')
        self.assertEqual(replay(Path(out['directory']))['status'],'FAILED')

    def test_evidence_mutation_uncertain(self):
        def change(call_number):
            if call_number==2:
                (self.workspace / 'hello.py').write_text('modified')
        out,_=self.run_actions([{'action':'read_file','path':'hello.py'},
            {'action':'final','answer':'It defines hello'}],on_completion=change)
        self.assertEqual(out['status'],'UNCERTAIN')
        self.assertEqual(out['reason'],'file_evidence_changed')

    def test_symlink_not_observed(self):
        (self.workspace / 'bad.txt').symlink_to('/etc/passwd')
        out,_=self.run_actions([{'action':'read_file','path':'bad.txt'},
            {'action':'final','answer':'No evidence'}])
        self.assertEqual(out['status'],'UNCERTAIN')
        self.assertEqual(out['evidence'],[])

    def test_manifest_omits_hidden_and_symlink(self):
        (self.workspace/'.secret').write_text('secret')
        (self.workspace/'link').symlink_to('/etc/passwd')
        self.assertEqual(safe_manifest(self.workspace), ['hello.py'])

    def test_results_within_workspace_refused(self):
        with self.assertRaises(ValueError):
            run_agent('Explain', self.workspace, self.workspace/'results', FakeBackend([]))

    def test_limits_rejected(self):
        with self.assertRaises(ValueError):
            run_agent('x', self.workspace, self.results, FakeBackend([]), max_steps=99)

    def test_search_then_read(self):
        actions=[{'action':'search_files','path':'.','query':'def hello'},
                 {'action':'read_file','path':'hello.py'},
                 {'action':'final','answer':'Found definition.'}]
        out,_=self.run_actions(actions)
        self.assertEqual(out['status'],'ACCEPTED')
        self.assertEqual(len(out['evidence']),2)


if __name__ == '__main__':
    unittest.main()
