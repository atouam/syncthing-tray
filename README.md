# Syncthing Tray

Windows tray app for Syncthing.

It starts Syncthing in the background, gives you a tray icon with an `Open Web UI` action, and shuts Syncthing down when you quit the tray app.

## Setup

`syncthing.exe` must be available on `PATH`.

Build the Windows executable with `uv` directly from the git repository:

```powershell
uv run --with git+https://github.com/atouam/syncthing-tray build-exe
```

The generated file is written to your current folder as `syncthing-tray.exe`.
