import argparse
from pathlib import Path

import PyInstaller.__main__

APP_NAME = "syncthing-tray"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Syncthing tray executable with PyInstaller.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where the final executable should be written. Defaults to the current working directory.",
    )
    return parser.parse_args()


def build_executable(package_dir: Path, output_dir: Path) -> int:
    build_dir = output_dir / ".pyinstaller-build"
    spec_dir = build_dir / "spec"
    work_dir = build_dir / "work"
    icon_file = package_dir / "syncthing.ico"
    main_script = package_dir / "main.py"

    output_dir.mkdir(parents=True, exist_ok=True)

    pyinstaller_args = [
        "--noconfirm",
        "--onefile",
        "--noconsole",
        "--name",
        APP_NAME,
        "--distpath",
        str(output_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(spec_dir),
        "--add-data",
        f"{icon_file};.",
        "--icon",
        str(icon_file),
        str(main_script),
    ]

    try:
        PyInstaller.__main__.run(pyinstaller_args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        return 1

    return 0


def main() -> int:
    package_dir = Path(__file__).resolve().parent
    args = parse_args()
    output_dir = Path(args.output_dir).resolve()
    return build_executable(package_dir, output_dir)
