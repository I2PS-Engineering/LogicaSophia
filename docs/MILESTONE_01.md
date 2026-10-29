# Milestone 1 — Standalone Linux hardware qualification

**Project:** LogicaSophia  |  **Scope:** local Linux machine only  |  **Status:** Tool ready for operator execution

## Execute

~~~bash
git clone https://github.com/I2PS-Engineering/LogicaSophia.git
cd LogicaSophia
python3 scripts/qualify_linux.py
~~~

If the repository already exists locally:

~~~bash
cd LogicaSophia && git pull && python3 scripts/qualify_linux.py
~~~

Requires Python 3.10+. No pip packages, root permissions, model weights or inference runtime. The script reads Linux procfs/sysfs, and optionally queries existing lsblk / nvidia-smi installations. It writes a single JSON file in your current directory.

## Output

- Filename: logicasophia_hardware.json
- CPU: model, architecture, observed physical topology, logical processors, relevant instruction flags and sampled frequency when supported.
- RAM: total, sampled available RAM, swap, huge pages; RAM type and speed remain null unless reliable data is available in a later milestone.
- GPU: Linux sysfs devices, PCI vendor/device IDs, and optional NVIDIA name/VRAM/driver data. The two lists can describe the same device; do not add their counts.
- Storage: capacity/free on the root filesystem and block-device type, size, rotational status and transport when available.
- Network: anonymized link index, link state and reported link speed, where readable.
- Assessment: no inference performance or model compatibility claims before benchmarking.

## Privacy and operating constraints

Read-only hardware queries, with no root/sudo, system changes or background services. The only written artifact is the requested JSON report. No remote requests or uploads. Hostname, username, IP/MAC address, interface names and serial numbers are not stored. Review the JSON before sharing it.

## Verification and acceptance

~~~bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m json.tool logicasophia_hardware.json >/dev/null
~~~

Local engineering test: eight qualification tests passed in a Linux test environment. This is not a measurement of your machine; your own hardware report is still needed.

**Milestone 1 is complete when:** the script runs on a target Linux machine, produces valid JSON, and its CPU/RAM/GPU observations are reviewed. The software delivery alone is not a completed field qualification.
