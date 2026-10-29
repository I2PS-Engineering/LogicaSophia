import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "qualify_linux.py"
spec = importlib.util.spec_from_file_location("qualify_linux", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class QualificationTests(unittest.TestCase):
    def test_meminfo(self):
        d = module.meminfo_values("MemTotal: 1024 kB\nHugePages_Total: 2\nInvalid: blah")
        self.assertEqual(d["MemTotal"], 1048576)
        self.assertEqual(d["HugePages_Total"], 2)
        self.assertNotIn("Invalid", d)

    def test_cpuinfo(self):
        cpu = module.cpuinfo_values("processor : 0\nmodel name : Test CPU\nphysical id : 0\ncore id : 0\nflags : avx2 fma aes\n\nprocessor : 1\nmodel name : Test CPU\nphysical id : 0\ncore id : 0\nflags : avx2 fma\n")
        self.assertEqual(cpu["physical_cores_observed"], 1)
        self.assertEqual(cpu["logical_processors_reported"], 2)
        self.assertIn("avx2", cpu["relevant_instruction_flags"])

    def test_gpu_rows(self):
        g = module.nvidia_rows('"GeForce GTX 1080 Ti", 11264, 535.104.05\n')
        self.assertEqual(g[0]["vram_total_bytes"], 11264 * 1024 * 1024)

    def test_gpu_bad_number(self):
        self.assertIsNone(module.nvidia_rows('"Test", N/A, 1.0')[0]["vram_total_bytes"])

    def test_gpu_missing_sysfs(self):
        with tempfile.TemporaryDirectory() as p, patch.object(module, "run_checked", return_value=(None,"command_unavailable")):
            g = module.detect_gpus(pathlib.Path(p))
            self.assertEqual(g["devices"], [])
            self.assertEqual(g["nvidia_query_status"], "command_unavailable")

    def test_missing_memory(self):
        with tempfile.TemporaryDirectory() as p:
            self.assertIsNone(module.read_int(pathlib.Path(p)/"absent"))

    def test_link_speed_unknown(self):
        with tempfile.TemporaryDirectory() as p:
            root=pathlib.Path(p)/"class"/"net"/"eth0"
            root.mkdir(parents=True)
            (root/"speed").write_text("-1")
            (root/"operstate").write_text("down")
            links=module.network_links(pathlib.Path(p))
            self.assertIsNone(links[0]["speed_mbps_reported"])
            self.assertEqual(links[0]["link_id"], "link_1")
            self.assertNotIn("interface", links[0])

    def test_collect_linux_report(self):
        if module.platform.system() != "Linux":
            self.skipTest("Linux only")
        report=module.collect()
        self.assertEqual(report["project"],"LogicaSophia")
        self.assertEqual(report["assessment"]["actual_inference"],"not_tested")
        self.assertIn("ram_type", report["memory"])
        self.assertEqual(report["privacy"].split(";")[0],"local_only")

if __name__ == "__main__":
    unittest.main()
