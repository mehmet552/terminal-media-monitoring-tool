# Terminal Media Monitoring Tool

A lightweight, terminal-based media control panel built with Python, `rich`, and `playerctl`. It works on Linux desktop environments with MPRIS support (Spotify, VLC, YouTube Music, Firefox, Chrome, and other compatible players).



<img width="745" height="297" alt="Screenshot From 2026-10-10 15-08-09" src="https://github.com/user-attachments/assets/f5660887-2f87-4fda-b65b-8bf2f8c126dd" />

## Features

- Real-time status display for the current track title, artist, and media source.
- Playback progress bar with elapsed and total time.
- Keyboard controls for playback directly in the terminal.
- Low resource usage with a minimal terminal footprint.

## Install and run (Ubuntu / Fedora)

For a quick, single-command installation on a clean system, run:

```bash
curl -sSL https://raw.githubusercontent.com/mehmet552/terminal-media-monitoring-tool/main/install.sh | bash
```

*(Alternatively, to download and inspect first: `curl -sSL https://raw.githubusercontent.com/mehmet552/terminal-media-monitoring-tool/main/install.sh -o /tmp/install.sh && less /tmp/install.sh && bash /tmp/install.sh`)*

This is a one-time setup; after installation, run `media_tui` from any terminal. The installer downloads the app from GitHub, installs only the required missing system packages (`playerctl`, Python, Git, and virtual-environment support) using `apt` on Ubuntu or `dnf` on Fedora, creates an isolated Python environment under `~/.local/share/media-tui`, and installs the `media_tui` command in `/usr/local/bin`. It runs as your regular user and asks for `sudo` only when the package manager or `/usr/local/bin` requires it.

`curl` must be available to fetch the installer; if it is missing, install it first with `sudo apt install curl` (Ubuntu) or `sudo dnf install curl` (Fedora). These are the distributions currently supported by the automatic installer.

The installer does not run the app as root or set up a background service. It does change the package-manager state if dependencies are missing and creates one command link in `/usr/local/bin`. The GitHub `main` branch can change; inspect the script before running it and only run software from a source you trust. HTTPS protects the download in transit but is not a code signature.

To register a locally cloned copy without waiting for a GitHub release, enter the directory containing `media_tui` and run this once:

```bash
sudo ln -s "$PWD/media_tui" /usr/local/bin/media_tui
```

This link requires sudo because `/usr/local/bin` is system-managed. It does not change your PATH or shell startup files. Do not use `ln -sf` here: that could replace an existing command link.

Open a new terminal after installation, then start the player with:

```bash
media_tui
```

`/usr/local/bin` is on the standard PATH on Ubuntu and Fedora, so the command remains available in new terminals and after a reboot without shell-specific configuration.

Run the command in an interactive terminal while media is playing in an MPRIS-compatible player. The app checks status, metadata, and (when available) position about once per second. Each `playerctl` command has a two-second timeout; a timeout is reported instead of leaving the app waiting indefinitely. The app does not run a background service or autostart at boot.

## Performance

- Track metadata, playback status, duration, and position are fetched together in one `playerctl` call per polling cycle.
- The app polls about once per second; each `playerctl` call has a two-second timeout.
- Rich's automatic redraw timer is disabled; the screen is redrawn only when a new polling cycle completes.
- The app avoids a permanently running background process. Exact CPU/RAM usage has not been benchmarked and depends on the desktop, media player, and terminal.

## Keyboard Controls

| Key | Action |
| --- | --- |
| SPACE | Play / Pause |
| N | Next Track |
| P | Previous Track |
| Q | Quit TUI |

## Notes

- If no active MPRIS player is detected, the app shows a "No active media player found" message.
- The app and its Python dependency (`rich`) are installed in your home directory's virtual environment; system prerequisites are managed by the distribution package manager.

## Uninstall

To completely remove the tool and all its downloaded files with a single command, run:

```bash
curl -sSL https://raw.githubusercontent.com/mehmet552/terminal-media-monitoring-tool/main/uninstall.sh | bash
```

This removes the command links, the local virtual environment, and the cloned repository. It intentionally leaves system packages such as `playerctl`, Git, and Python installed because other applications may need them.

## Technical references

- [Playerctl](https://github.com/altdesktop/playerctl) documents MPRIS control and formatted metadata output.
- [Rich Live Display](https://rich.readthedocs.io/en/stable/live.html) documents manual refresh and disabling automatic redraws.
