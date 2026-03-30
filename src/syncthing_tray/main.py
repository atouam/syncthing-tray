import ctypes
import shutil
import subprocess
import sys
import webbrowser
from contextlib import contextmanager
from functools import partial
from pathlib import Path

from PIL import Image
from pystray import Icon, Menu, MenuItem

ERROR_ALREADY_EXISTS = 183
MUTEX_NAME = "Local\\syncthing-tray"

SUBPROCESS_KWARGS: dict[str, object] = {
    "stdout": subprocess.DEVNULL,
    "stderr": subprocess.DEVNULL,
}

if sys.platform == "win32":
    SUBPROCESS_KWARGS["creationflags"] = subprocess.CREATE_NO_WINDOW


@contextmanager
def single_instance():
    if sys.platform != "win32":
        yield True
        return

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)

    if not mutex:
        raise ctypes.WinError(ctypes.get_last_error())

    already_running = ctypes.get_last_error() == ERROR_ALREADY_EXISTS

    try:
        yield not already_running
    finally:
        kernel32.CloseHandle(mutex)


def icon_path():
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "syncthing.ico"
    return Path(__file__).resolve().with_name("syncthing.ico")


def syncthing_exe_path():
    return shutil.which("syncthing")


def shutdown_syncthing(exe_path) -> None:
    subprocess.run(
        [exe_path, "cli", "operations", "shutdown"],
        **SUBPROCESS_KWARGS,
    )


def quit_tray(exe_path: str, icon, item) -> None:
    shutdown_syncthing(exe_path)
    icon.stop()


def open_web_ui(icon, item) -> None:
    webbrowser.open("http://127.0.0.1:8384")


def create_tray(exe_path: str) -> None:
    menu = Menu(
        MenuItem("Open Web UI", open_web_ui, default=True),
        MenuItem("Quit", partial(quit_tray, exe_path)),
    )
    Icon("SyncthingTray", Image.open(icon_path()), "Syncthing", menu).run()


def main() -> int:
    with single_instance() as is_primary_instance:
        if not is_primary_instance:
            print("syncthing-tray is already running.")
            return 0

        exe_path = syncthing_exe_path()

        if exe_path:
            subprocess.Popen(
                [exe_path, "--no-browser"],
                **SUBPROCESS_KWARGS,
            )

        else:
            print("syncthing.exe was not found in PATH.")
            return 1

        create_tray(exe_path)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
