#!/usr/bin/env python3

"""
Advanced Cellebrite UFED Troubleshooting Framework
Author: Emanuela Signor
Focus: forensic environment validation & diagnostics
Platform: Kali Linux / Debian-based systems
"""

import os
import subprocess
import shutil
import json
import platform
from datetime import datetime

REPORT = {
    "timestamp": str(datetime.now()),
    "system": {},
    "checks": {}
}


def run(cmd):
    try:
        output = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT
        )
        return output.decode(errors="ignore")
    except subprocess.CalledProcessError as e:
        return e.output.decode(errors="ignore")


def record(section, result):
    REPORT["checks"][section] = result


def check_system_info():
    info = {
        "os": platform.platform(),
        "kernel": run("uname -r").strip(),
        "python": platform.python_version()
    }
    REPORT["system"] = info
    print("\n[+] System Info:", info)


def check_java():
    print("\n[+] Checking Java...")
    output = run("java -version")

    status = "OK" if "version" in output else "FAIL"
    record("java", {"status": status, "output": output})

    print(output)


def check_usb():
    print("\n[+] USB Devices...")
    output = run("lsusb")

    record("usb_devices", output)
    print(output)


def check_adb():
    print("\n[+] Android Debug Bridge (ADB)...")

    adb_version = run("adb version")
    adb_devices = run("adb devices")

    record("adb", {
        "version": adb_version,
        "devices": adb_devices
    })

    print(adb_version)
    print(adb_devices)


def check_ios_libs():
    print("\n[+] iOS forensic libraries...")

    tools = [
        "idevice_id",
        "ideviceinfo",
        "iproxy"
    ]

    results = {}

    for tool in tools:
        results[tool] = run(f"which {tool}")

    record("ios_tools", results)

    for k, v in results.items():
        print(k, ":", v.strip())


def check_disk():
    total, used, free = shutil.disk_usage("/")

    disk_data = {
        "total_gb": total // (2**30),
        "used_gb": used // (2**30),
        "free_gb": free // (2**30)
    }

    record("disk", disk_data)

    print("\n[+] Disk:", disk_data)


def check_permissions():
    groups = run("groups")
    record("permissions", groups)

    print("\n[+] Groups:", groups)


def check_kernel_modules():
    print("\n[+] Kernel modules...")

    modules = run("lsmod | grep usb")
    record("kernel_modules", modules)

    print(modules)


def check_running_processes():
    processes = run("ps aux | grep -i cellebrite | grep -v grep")

    record("processes", processes)

    print("\n[+] Processes:\n", processes)


def locate_logs():
    print("\n[+] Searching logs...")

    paths = [
        "/var/log",
        os.path.expanduser("~"),
        "/opt"
    ]

    found = []

    for path in paths:
        results = run(f"find {path} -iname '*cellebrite*' 2>/dev/null")
        if results.strip():
            found.append(results)

    record("logs", found)

    for f in found:
        print(f)


def performance_test():
    print("\n[+] Disk speed test...")

    test_cmd = "dd if=/dev/zero of=test_speed.tmp bs=1M count=100 conv=fdatasync 2>&1"
    result = run(test_cmd)

    run("rm -f test_speed.tmp")

    record("disk_performance", result)

    print(result)


def generate_report():
    filename = f"cellebrite_diagnostic_{int(datetime.now().timestamp())}.json"

    with open(filename, "w") as f:
        json.dump(REPORT, f, indent=4)

    print("\n[+] Report saved:", filename)


def main():
    print("=" * 60)
    print("Cellebrite Advanced Troubleshooter")
    print("Created by Emanuela Signor")
    print("=" * 60)

    check_system_info()
    check_java()
    check_usb()
    check_adb()
    check_ios_libs()
    check_disk()
    check_permissions()
    check_kernel_modules()
    check_running_processes()
    locate_logs()
    performance_test()

    generate_report()

    print("\n[✓] Diagnostic complete")


if __name__ == "__main__":
    main()
