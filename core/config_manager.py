import json
from pathlib import Path
from core.logger import get_logger

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "config" / "settings.json"
logger = get_logger()

DEFAULTS = {"tool_paths": {}, "preferences": {"package_manager": "auto"}}

def load_settings():
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        save_settings(DEFAULTS)
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        data.setdefault("tool_paths", {})
        data.setdefault("preferences", {"package_manager": "auto"})
        return data
    except (json.JSONDecodeError, OSError):
        print("Warning: settings file could not be read. Using defaults.")
        return DEFAULTS.copy()

def save_settings(settings):
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(settings, indent=4), encoding="utf-8")
    logger.info("Saved configuration")

def set_tool_path(key, path):
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        print("File not found. Please enter the full path to the executable.")
        return
    settings = load_settings()
    settings["tool_paths"][key] = str(candidate.resolve())
    save_settings(settings)
    print("Tool path saved. The manager will use this path during detection.")

def show_settings():
    print("\n--- Current settings ---")
    print(json.dumps(load_settings(), indent=4))
