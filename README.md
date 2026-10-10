# Terminal Media Monitoring Tool

A lightweight, terminal-based media control panel built with Python, `rich`, and `playerctl`. It works on Linux desktop environments with MPRIS support (Spotify, VLC, YouTube Music, Firefox, Chrome, and other compatible players).

## Features

- Real-time status display for the current track title, artist, and media source.
- Playback progress bar with elapsed and total time.
- Keyboard controls for playback directly in the terminal.
- Low resource usage with a minimal terminal footprint.

## Install and run (Ubuntu / Fedora)

Open a terminal and run this one command:

```bash
curl -fsSL https://raw.githubusercontent.com/mehmet552/terminal-media-monitoring-tool/main/install.sh | bash
```

The installer downloads the app from GitHub, installs missing system packages (`playerctl`, Python and Git) using `apt` on Ubuntu or `dnf` on Fedora, creates an isolated Python environment under `~/.local/share/media-tui`, and adds the `media_tui` command under `~/.local/bin`. System package installation may ask for your password through `sudo`.

`curl` must be available to fetch the installer; if it is missing, install it first with `sudo apt install curl` (Ubuntu) or `sudo dnf install curl` (Fedora). These are the distributions currently supported by the automatic installer.

Open a new terminal after installation, then start the player with:

```bash
media_tui
```

If the current terminal says `media_tui: command not found`, use `export PATH="$HOME/.local/bin:$PATH"` in that terminal. The installer adds the PATH entry to your shell startup file for future terminals.

Run the command in an interactive terminal while media is playing in an MPRIS-compatible player. The app polls playback about once per second and does not run a background service.

## Performance

- Track metadata is fetched together in one `playerctl` call instead of separate calls for title, artist, player, and duration.
- Playback status and position still require separate `playerctl` calls; the app checks them at most once per polling cycle (about once per second).
- Rich's automatic redraw timer is disabled; the screen is redrawn only when a new polling cycle completes.
- This keeps the implementation simple and avoids a permanently running background process. Exact CPU/RAM usage depends on the desktop, media player, and terminal.

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
- To uninstall, remove `~/.local/bin/media_tui` and `~/.local/share/media-tui`. `playerctl` and any system packages installed by the installer can be removed with your distribution's package manager.

## Technical references

- [Playerctl](https://github.com/altdesktop/playerctl) documents MPRIS control and formatted metadata output.
- [Rich Live Display](https://rich.readthedocs.io/en/stable/live.html) documents manual refresh and disabling automatic redraws.
