#!/usr/bin/env python3
"""LogicaSophia M1: read-only Linux hardware qualification; stdlib only.

The report stays on this machine until the operator chooses to share it.
No credentials, hostnames, usernames, MAC/IP addresses, or serial numbers are collected.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPORT_VERSION = "1.0"


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace").strip()
    except (OSError, UnicodeError):
        return None


def read_int(path: Path) -> int | None:
    value = read_text(path)
    if value is None:
        return None
    try:
        result = int(value)
        return result if result >= 0 else None
    except ValueError:
        return None


def meminfo_values(text: str) -> dict[str, int]:
    values = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parts = value.strip().split()
        if not parts:
            continue
        try:
            number = int(parts[0])
        except ValueError:
            continue
        unit = parts[1] if len(parts) > 1 else None
        if unit == "kB":
            number *= 1024
        elif unit is not None:
            continue
        values[key] = number
    return values


def cpuinfo_values(text: str) -> dict:
    processors = [part for part in text.split("\n\n") if part.strip()]
    first = {}
    unique_cores = set()
    sockets = set()
    for part in processors:
        fields = {}
        for line in part.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip().lower()] = value.strip()
        if not first:
            first = fields
        if "physical id" in fields:
            sockets.add(fields["physical id"])
            if "core id" in fields:
                unique_cores.add((fields["physical id"], fields["core id"]))
    flags = first.get("flags", first.get("features", "")).split()
    relevant = [x for x in ("sse4_1", "sse4_2", "avx", "avx2", "avx512f", "fma", "aes", "neon", "asimd", "sve") if x in flags]
    return {
        "model": first.get("model name") or first.get("hardware") or first.get("processor"),
        "logical_processors_reported": len(processors) or None,
        "physical_sockets_observed": len(sockets) or None,
        "physical_cores_observed": len(unique_cores) or None,
        "relevant_instruction_flags": relevant,
    }


def run_checked(command: list[str], timeout: int = 5) -> tuple[str | None, str | None]:
    if not shutil.which(command[0]):
        return None, "command_unavailable"
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None, "command_failed_or_timed_out"
    if result.returncode != 0:
        return None, "command_returned_error"
    return result.stdout, None


def nvidia_rows(output: str) -> list[dict]:
    result = []
    for values in csv.reader(io.StringIO(output)):
        if len(values) < 3:
            continue
        name, mem, driver = [part.strip() for part in values[:3]]
        try:
            mib = int(mem)
        except ValueError:
            mib = None
        result.append({"name": name or None, "vram_total_bytes": mib * 1024 * 1024 if mib is not None else None,
                       "driver_version": driver or None, "source": "nvidia-smi"})
    return result


def detect_gpus(sysfs: Path = Path("/sys")) -> dict:
    cards = []
    for card in sorted((sysfs / "class" / "drm").glob("card[0-9]*")):
        if not card.name[4:].isdigit():
            continue
        device = card / "device"
        vendor = read_text(device / "vendor")
        if vendor is None:
            continue
        cards.append({
            "device": card.name,
            "pci_vendor_id": vendor,
            "pci_device_id": read_text(device / "device"),
            "vram_total_bytes": read_int(device / "mem_info_vram_total"),
            "source": "linux_sysfs",
        })
    raw, error = run_checked(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"])
    return {"devices": cards, "nvidia_details": nvidia_rows(raw) if raw is not None else [],
            "nvidia_query_status": "ok" if raw is not None else error,
            "note": "PCI/sysfs cards and nvidia-smi entries may describe the same physical GPU; do not add their counts."}


def network_links(sysfs: Path = Path("/sys")) -> list[dict]:
    result = []
    for link in sorted((sysfs / "class" / "net").glob("*")):
        if link.name == "lo" or not link.is_dir():
            continue
        speed = read_int(link / "speed")
        # Interface names can embed a MAC address (e.g. enx001122334455).
        # Assign anonymous, per-report link IDs instead of collecting raw names.
        kind = "wireless" if (link / "wireless").exists() else "unknown"
        result.append({"link_id": f"link_{len(result) + 1}", "kind": kind,
                       "state": read_text(link / "operstate"),
                       "speed_mbps_reported": speed if speed and speed > 0 else None})
    return result


def collect() -> dict:
    if platform.system() != "Linux":
        raise RuntimeError("This qualification script is for Linux only")
    mem = meminfo_values(read_text(Path("/proc/meminfo")) or "")
    cpu = cpuinfo_values(read_text(Path("/proc/cpuinfo")) or "")
    cpu["logical_processors_os"] = os.cpu_count()
    cpu["logical_processors_available_to_process"] = (
        len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    )
    cpu["frequency_mhz_current_sample"] = (
        (read_int(Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")) or 0) / 1000 or None
    )
    disk = shutil.disk_usage("/")
    lsblk, lsblk_error = run_checked(["lsblk", "-J", "-b", "-o", "NAME,TYPE,SIZE,ROTA,TRAN,MOUNTPOINT"], timeout=5)
    devices = None
    if lsblk:
        try:
            devices = json.loads(lsblk).get("blockdevices")
        except (ValueError, AttributeError):
            lsblk_error = "invalid_lsblk_json"
    return {
        "project": "LogicaSophia",
        "milestone": "M1_LINUX_HARDWARE_QUALIFICATION",
        "report_version": REPORT_VERSION,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "privacy": "local_only; excludes hostname, username, network addresses, hardware serials",
        "os": {"system": platform.system(), "release": platform.release(), "architecture": platform.machine()},
        "cpu": cpu,
        "memory": {
            "total_bytes": mem.get("MemTotal"),
            "available_bytes_sample": mem.get("MemAvailable"),
            "swap_total_bytes": mem.get("SwapTotal"),
            "huge_pages_total": mem.get("HugePages_Total"),
            "huge_pages_free": mem.get("HugePages_Free"),
            "huge_page_size_bytes": mem.get("Hugepagesize"),
            "ram_type": None,
            "ram_speed_mt_s": None,
            "note": "RAM DDR type and speed are not inferred without reliable firmware/SMBIOS data.",
        },
        "gpu": detect_gpus(),
        "storage": {"root_total_bytes": disk.total, "root_free_bytes_sample": disk.free,
                    "block_devices": devices, "block_devices_query_status": "ok" if devices is not None else lsblk_error},
        "network": {"interfaces": network_links(), "note": "No IP addresses or MACs collected."},
        "assessment": {
            "hardware_report_complete": True,
            "model_fit": "not_assessed_until_model_and_quantization_are_selected",
            "throughput": "not_measured",
            "actual_inference": "not_tested",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="LogicaSophia Linux hardware qualification (read-only)")
    parser.add_argument("--output", default="logicasophia_hardware.json", help="Local report destination (default: logicasophia_hardware.json)")
    args = parser.parse_args()
    try:
        report = collect()
        data = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        output = Path(args.output).expanduser()
        # Write only to the explicitly selected path (or default working directory).
        output.write_text(data, encoding="utf-8")
    except (RuntimeError, OSError) as exc:
        print(f"Qualification failed: {exc}", file=sys.stderr)
        return 1
    print("LogicaSophia M1 — Linux hardware qualification complete")
    print(f"Report: {output.resolve()}")
    print(f"CPU: {report['cpu']['model'] or 'unknown'}")
    mem_total = report['memory']['total_bytes']
    print(f"RAM: {mem_total / (1024 ** 3):.1f} GiB" if mem_total is not None else "RAM: unknown")
    print(f"GPU sysfs devices: {len(report['gpu']['devices'])}; NVIDIA reports: {len(report['gpu']['nvidia_details'])}")
    print("No model inference was attempted; no data was uploaded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
