import json
import tempfile
import unittest
from pathlib import Path
from logicasophia.core.contracts import Task
from logicasophia.core.controller import execute
from logicasophia.core.filesystem import ObservationError, read_scoped, search_observation
from logicasophia.core.ledger import replay
from logicasophia.core.state_machine import transition


def contract(**kw):
    d = {'schema_version': 1, 'task_id': 'test-001', 'goal': 'Verify text',
         'allowed_tools': ['read_file'], 'steps': [{'tool': 'read_file', 'path': 'file.txt'}],
         'success_checks': [{'type': 'file_contains', 'path': 'file.txt', 'text': 'hello'}]}
    d.update(kw)
    return d

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        self.work = self.root / 'work'
        self.work.mkdir()
        (self.work / 'file.txt').write_text('hello world\n')
        self.results = self.root / 'results'

    def tearDown(self):
        self.dir.cleanup()

    def test_success_and_replay(self):
        result = execute(contract(), self.work, self.results)
        self.assertEqual(result['status'], 'ACCEPTED')
        self.assertEqual(replay(Path(result['directory']))['status'], 'ACCEPTED')
        self.assertEqual(len(result['observations']), 1)

    def test_verifier_detects_false_claim(self):
        obj = contract(success_checks=[{'type':'file_contains', 'path':'file.txt','text':'not there'}])
        result = execute(obj, self.work, self.results)
        self.assertEqual(result['status'], 'FAILED')
        self.assertEqual(replay(Path(result['directory']))['status'], 'FAILED')

    def test_missing_observation_unknown(self):
        (self.work / 'other.txt').write_text('hello')
        obj = contract(success_checks=[{'type':'file_contains', 'path':'other.txt', 'text':'hello'}])
        result = execute(obj, self.work, self.results)
        self.assertEqual(result['status'], 'UNCERTAIN')

    def test_changed_after_observation_uncertain(self):
        def change():
            (self.work / 'file.txt').write_text('hello, but changed')
        result = execute(contract(), self.work, self.results, before_verify=change)
        self.assertEqual(result['status'], 'UNCERTAIN')
        self.assertEqual(result['checks'][0]['result'], 'changed_after_observation')

    def test_explicit_denial_before_execution(self):
        obj = contract(steps=[{'tool':'apply_patch','path':'file.txt'}], allowed_tools=['apply_patch'])
        result = execute(obj, self.work, self.results)
        self.assertEqual(result['status'], 'FAILED')
        self.assertEqual(result['reason'], 'policy_denied')
        self.assertEqual((self.work / 'file.txt').read_text(), 'hello world\n')
        self.assertEqual(result['observations'], [])

    def test_deny_tool_not_in_task_permissions(self):
        result = execute(contract(allowed_tools=[]), self.work, self.results)
        self.assertEqual(result['status'], 'FAILED')
        self.assertEqual(result['reason'], 'policy_denied')

    def test_no_path_escape(self):
        for path in ('../outside', '/etc/passwd', 'sub/../file.txt', 'C:/Windows', '.hidden/../hello'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                Task.parse(contract(steps=[{'tool':'read_file','path':path}]))
        self.assertFalse(self.results.exists())

    def test_refuse_symlinks(self):
        (self.work/'link.txt').symlink_to(self.work/'file.txt')
        with self.assertRaises(ObservationError):
            read_scoped(self.work, 'link.txt')
        (self.work/'linked').symlink_to(self.work, target_is_directory=True)
        with self.assertRaises(ObservationError):
            read_scoped(self.work, 'linked/file.txt')

    def test_nested_symlink_directory_search_rejected(self):
        (self.work/'sub').symlink_to(self.root, target_is_directory=True)
        from logicasophia.core.filesystem import search_observation
        with self.assertRaises(ObservationError):
            search_observation(self.work, 'sub', 'hello')

    def test_refuse_large_file(self):
        (self.work/'huge.txt').write_text('A' * 70000)
        with self.assertRaises(ObservationError):
            read_scoped(self.work, 'huge.txt')

    def test_search_no_shell(self):
        result = search_observation(self.work, '.', 'hello')
        self.assertEqual([m['path'] for m in result['matches']], ['file.txt'])
        self.assertFalse(result['truncated'])

    def test_search_policy(self):
        obj = contract(allowed_tools=['search_files','read_file'], steps=[{'tool':'search_files','path':'.','query':'hello'}, {'tool':'read_file','path':'file.txt'}])
        result = execute(obj, self.work, self.results)
        self.assertEqual(result['status'], 'ACCEPTED')

    def test_nonexistent_file_not_accepted(self):
        result = execute(contract(steps=[{'tool':'read_file','path':'missing.txt'}]), self.work, self.results)
        self.assertEqual(result['status'], 'UNCERTAIN')

    def test_max_steps(self):
        with self.assertRaises(ValueError):
            Task.parse(contract(steps=[{'tool':'read_file','path':'file.txt'}]*9))

    def test_trace_tampering_detected(self):
        result=execute(contract(), self.work, self.results)
        p=Path(result['directory'])/'trace.jsonl'
        p.write_text(p.read_text().replace('observation','not_observation',1))
        with self.assertRaises(ValueError):
            replay(Path(result['directory']))

    def test_illegal_transition(self):
        with self.assertRaises(ValueError):
            transition('ACCEPTED','EXECUTING')

    def test_report_outside_workspace(self):
        with self.assertRaises(ValueError):
            execute(contract(), self.work, self.work/'results')

if __name__ == '__main__': unittest.main()
