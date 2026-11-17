
import platform
import shutil
import subprocess

from core.tool_detector import TOOL_CATALOG
from core.logger import get_logger

logger = get_logger()

# Verified package-manager identifiers
WINDOWS_PACKAGE_IDS = {
    "2": "KiCad.KiCad"
}

LINUX_PACKAGE_IDS = {
    "1": "ngspice",
    "2": "kicad"
}


def check_updates():
    system = platform.system().lower()

    if system == "windows":
        manager = "winget"
        package_ids = WINDOWS_PACKAGE_IDS
    elif system == "linux":
        manager = "apt-get"
        package_ids = LINUX_PACKAGE_IDS
    else:
        print("Updates are not configured for this operating system.")
        return {}

    if not shutil.which(manager):
        print("Supported package manager not found.")
        return {}

    results = {}

    for key, item in TOOL_CATALOG.items():

        package_id = package_ids.get(key)

        if not package_id:
            results[key] = {
                "name": item["name"],
                "available": False,
                "message": "No verified package ID configured for this tool."
            }
            continue

        if system == "windows":
            command = [
                "winget", "upgrade",
                "--id", package_id,
                "--exact"
            ]
        else:
            command = ["apt-cache", "policy", package_id]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )

            output = (result.stdout + result.stderr).strip()

            if system == "windows":
                no_update_messages = [
                    "No applicable upgrade found",
                    "No available upgrade found",
                    "No installed package found"
                ]

                no_update = any(
                    message.lower() in output.lower()
                    for message in no_update_messages
                )

                available = result.returncode == 0 and not no_update

                message = (
                    "Possible update available. Review the output."
                    if available
                    else "No upgrade reported."
                )

            else:
                installed = "(not installed)"
                candidate = "unknown"

                for line in output.splitlines():
                    if line.strip().startswith("Installed:"):
                        installed = line.split(":", 1)[1].strip()

                    if line.strip().startswith("Candidate:"):
                        candidate = line.split(":", 1)[1].strip()

                available = (
                    installed != "(not installed)"
                    and candidate != installed
                    and candidate != "(none)"
                    and candidate != "unknown"
                )

                message = (
                    f"Installed: {installed} | Candidate: {candidate}"
                )

            results[key] = {
                "name": item["name"],
                "available": available,
                "message": message
            }

            logger.info(
                "Checked updates for %s: %s",
                item["name"],
                message
            )

        except (OSError, subprocess.SubprocessError) as exc:
            results[key] = {
                "name": item["name"],
                "available": False,
                "message": str(exc)
            }

            logger.error(
                "Update check failed for %s: %s",
                item["name"],
                exc
            )

    return results


def update_tool(key):

    if key not in TOOL_CATALOG:
        print("Invalid tool selection.")
        return

    item = TOOL_CATALOG[key]
    system = platform.system().lower()

    if system == "windows":
        package_id = WINDOWS_PACKAGE_IDS.get(key)

        if not package_id:
            print("No verified Windows package ID configured for this tool.")
            return

        command = [
            "winget", "upgrade",
            "--id", package_id,
            "--exact",
            "--accept-package-agreements",
            "--accept-source-agreements"
        ]

    elif system == "linux":
        package_id = LINUX_PACKAGE_IDS.get(key)

        if not package_id:
            print("No Linux package ID configured for this tool.")
            return

        command = [
            "sudo", "apt-get",
            "install", "--only-upgrade",
            "-y", package_id
        ]

    else:
        print("Updates are not configured for this operating system.")
        return

    if not shutil.which("winget" if system == "windows" else "apt-get"):
        print("Required package manager not found.")
        return

    print("Running update for:", item["name"])
    print("Command:", " ".join(command))

    try:
        result = subprocess.run(command)

        logger.info(
            "Update command for %s returned %s",
            item["name"],
            result.returncode
        )

        if result.returncode == 0:
            print("Update command completed successfully.")
        else:
            print(
                f"Update command failed with exit code "
                f"{result.returncode}."
            )

    except (OSError, subprocess.SubprocessError) as exc:
        logger.error(
            "Update failed for %s: %s",
            item["name"],
            exc
        )
        print("Could not run update:", exc)
