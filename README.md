# Terminal Media Monitoring Tool

A lightweight, terminal-based media control panel built with Python, `rich`, and `playerctl`. It works on Linux desktop environments with MPRIS support (Spotify, VLC, YouTube Music, Firefox, Chrome, and other compatible players).

## Features

- Real-time status display for the current track title, artist, and media source.
- Playback progress bar with elapsed and total time.
- Keyboard controls for playback directly in the terminal.
- Low resource usage with a minimal terminal footprint.

## Prerequisites

Install the required system package:

```bash
# Fedora
sudo dnf install playerctl python3-pip

# Debian / Ubuntu
sudo apt install playerctl python3-pip

# Arch
sudo pacman -S playerctl python-pip
```

## Run the project

This repository contains the project inside a nested folder named `terminal-media-monitoring-tool`.

From the repository root:

```bash
cd /home/mehmet/projoler/terminal-media-monitoring-tool
cd terminal-media-monitoring-tool
python3 -m pip install -r requirements.txt
python3 media_tui.py
```

If you are already inside the project folder, use:

```bash
cd terminal-media-monitoring-tool
python3 -m pip install -r requirements.txt
python3 media_tui.py
```

## Keyboard Controls

| Key | Action |
| --- | --- |
| SPACE | Play / Pause |
| N | Next Track |
| P | Previous Track |
| Q | Quit TUI |

## Notes

- The app expects `playerctl` to be installed and a media player to be running.
- If no active MPRIS player is detected, the app shows a "No active media player found" message.
