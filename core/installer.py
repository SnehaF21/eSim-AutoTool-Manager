import platform
import shutil
import subprocess

from core.tool_detector import TOOL_CATALOG, detect_tools
from core.logger import get_logger

logger = get_logger()

# Package IDs used by the installer
WINDOWS_PACKAGE_IDS = {
    "2": "KiCad.KiCad"
}

LINUX_PACKAGE_IDS = {
    "1": "ngspice",
    "2": "kicad"
}


def _run(command):
    print("\nRunning:", " ".join(command))

    try:
        result = subprocess.run(command, text=True)

        logger.info(
            "Command completed with return code %s: %s",
            result.returncode,
            command
        )

        if result.returncode == 0:
            print("Command completed successfully.")
            return True

        print(f"Command failed with exit code {result.returncode}.")
        return False

    except (OSError, subprocess.SubprocessError) as exc:
        logger.error("Could not run command %s: %s", command, exc)
        print("Could not run package manager:", exc)
        return False


def install_tool(key):

    if key not in TOOL_CATALOG:
        print("Invalid tool selection.")
        return

    item = TOOL_CATALOG[key]
    system = platform.system().lower()

    print(f"\nSelected: {item['name']}")

    # Check whether the tool is already installed
    detected = detect_tools()
    tool_status = detected.get(key, {})

    if tool_status.get("installed", False):
        print(f"{item['name']} is already installed.")
        print("Installation skipped to avoid reinstalling it.")
        return

    # Windows installation
    if system == "windows":

        if not shutil.which("winget"):
            print("winget was not found.")
            print("Install or enable App Installer from Microsoft Store.")
            return

        package_id = WINDOWS_PACKAGE_IDS.get(key)

        if not package_id:
            print("No verified Windows package ID configured for this tool.")
            print("Automatic installation is unavailable.")
            return

        print("Package manager: Windows Package Manager")
        print("Package ID:", package_id)

        confirm = input("Type YES to install: ").strip()

        if confirm == "YES":
            command = [
                "winget",
                "install",
                "--id", package_id,
                "--exact",
                "--accept-package-agreements",
                "--accept-source-agreements"
            ]

            _run(command)

        else:
            print("Installation cancelled.")

    # Linux installation
    elif system == "linux":

        if not shutil.which("apt-get"):
            print("This prototype supports apt-based Linux distributions.")
            return

        package_id = LINUX_PACKAGE_IDS.get(key)

        if not package_id:
            print("No Linux package ID configured for this tool.")
            return

        print("Package manager: APT")
        print("Package ID:", package_id)

        confirm = input("Type YES to install: ").strip()

        if confirm == "YES":

            updated = _run(["sudo", "apt-get", "update"])

            if not updated:
                print("Package list update failed. Installation stopped.")
                return

            command = [
                "sudo",
                "apt-get",
                "install",
                "-y",
                package_id
            ]

            _run(command)

        else:
            print("Installation cancelled.")

    else:
        print("Automatic installation is not configured for this operating system.")
