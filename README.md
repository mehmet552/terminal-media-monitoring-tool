# Terminal Media Monitoring Tool

A lightweight, terminal-based media control panel built with Python, `rich`, and `playerctl`. Works across Linux desktop environments with MPRIS support (Spotify, VLC, YouTube Music, Firefox, Chrome, and other compatible players).

## Features

- Real-time status display for the current track title, artist, and media source.
- Playback progress bar with elapsed and total time.
- Keyboard controls for controlling media directly inside the terminal.
- Low resource usage with a minimal terminal footprint.

## Prerequisites

Install `playerctl` and the Python dependencies on your Linux distribution:

```bash
# Fedora
sudo dnf install playerctl python3-pip

# Debian / Ubuntu
sudo apt install playerctl python3-pip

# Arch
sudo pacman -S playerctl python-pip
```

## Installation

```bash
git clone https://github.com/mehmet552/terminal-media-monitoring-tool.git
cd terminal-media-monitoring-tool/terminal-media-monitoring-tool
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
