import platform
import shutil
import sys
from core.tool_detector import detect_tools
from core.logger import get_logger

logger = get_logger()

def run_dependency_check():
    print("\n--- Dependency and environment check ---")
    checks = [
        ("Python 3.10+", sys.version_info >= (3, 10),
         f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
        ("Supported operating system", platform.system().lower() in ("windows", "linux"),
         platform.platform()),
    ]
    system = platform.system().lower()
    if system == "windows":
        checks.append(("Windows Package Manager (winget)", bool(shutil.which("winget")),
                       shutil.which("winget") or "Not found"))
    elif system == "linux":
        checks.append(("APT package manager", bool(shutil.which("apt-get")),
                       shutil.which("apt-get") or "Not found"))

    for key, tool in detect_tools().items():
        checks.append((f"{tool['name']} availability", tool["installed"],
                       tool["version"] or "Not detected"))

    failed = 0
    for name, ok, detail in checks:
        status = "PASS" if ok else "CHECK"
        print(f"[{status}] {name}: {detail}")
        if not ok:
            failed += 1
    print(f"\nSummary: {len(checks) - failed}/{len(checks)} checks passed.")
    print("CHECK means the item needs attention; it does not always mean the application cannot run.")
    logger.info("Dependency check completed: %s/%s passed", len(checks)-failed, len(checks))
