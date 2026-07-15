# Syncthing Tray

Windows tray app for Syncthing.

It starts Syncthing in the background, gives you a tray icon with an `Open Web UI` action, and shuts Syncthing down when you quit the tray app.

## Install

Requires `syncthing.exe` on `PATH`.

Download `syncthing-tray.exe` from the [latest release](https://github.com/atouam/syncthing-tray/releases/latest).

## Run on startup

Put `syncthing-tray.exe` in the Windows Startup folder:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

## Build from source

```powershell
uv run build-exe
```

The generated file is written to your current folder as `syncthing-tray.exe`.
