import shutil
import subprocess
import logging
from pathlib import Path

from core.config_manager import load_settings

logger = logging.getLogger(__name__)

TOOL_CATALOG = {
    "1": {
        "name": "Ngspice",
        "description": "Circuit simulation engine"
    },
    "2": {
        "name": "KiCad",
        "description": "Electronic design automation suite"
    }
}


def get_configured_path(tool_key):
    try:
        settings = load_settings()
        return settings.get("tool_paths", {}).get(tool_key)
    except Exception as error:
        logger.error("Configuration error: %s", error)
        return None


def find_executable(tool_key):
    configured = get_configured_path(tool_key)

    if configured:
        path = Path(configured)
        if path.is_file():
            return path

    if tool_key == "1":
        found = shutil.which("ngspice")
        if found:
            return Path(found)

        candidates = [
            Path(r"C:\Program Files\ngspice\bin\ngspice.exe"),
            Path(r"C:\Program Files (x86)\ngspice\bin\ngspice.exe")
        ]

    elif tool_key == "2":
        found = shutil.which("kicad-cli")
        if found:
            return Path(found)

        candidates = [
            Path(r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"),
            Path(r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"),
            Path(r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe")
        ]

    else:
        return None

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    return None


def read_version(executable):
    if executable is None:
        return "Unknown"

    for option in ["version", "--version", "-v"]:
        try:
            result = subprocess.run(
                [str(executable), option],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = (result.stdout + "\n" + result.stderr).strip()

            if output:
                return output.splitlines()[0][:150]

        except (OSError, subprocess.TimeoutExpired):
            continue

    return "Unknown"


def detect_tools():
    results = {}

    for key, details in TOOL_CATALOG.items():
        executable = find_executable(key)

        results[key] = {
            "name": details["name"],
            "installed": executable is not None,
            "version": read_version(executable),
            "path": str(executable) if executable else "Not detected"
        }

    logger.info("Tool detection completed")
    return results
