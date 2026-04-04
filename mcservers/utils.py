from datetime import datetime
from pathlib import Path
import sys

def get_minecraft_path():
    home = Path.home()

    if sys.platform == "win32":
        return home / "AppData" / "Roaming" / ".minecraft"

    elif sys.platform == "linux":
        return home / ".minecraft"

    elif sys.platform == "darwin":
        return home / "Library" / "Application Support" / "minecraft"

    else:
        raise OSError(f"Unsupported platform: {sys.platform}")

def get_servers_path():
    return get_minecraft_path() / "servers.dat"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M")

def get_export_path():
    timestamp = get_timestamp()
    return Path.cwd() / f"servers_{timestamp}.txt"