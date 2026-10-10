#  Terminal Media Monitoring Tool

A lightweight, terminal-based media control panel built with Python, `rich`, and `playerctl`. Works seamlessly across Linux desktop environments with MPRIS support (Spotify, VLC, YouTube Music, Firefox, Chrome, etc.).

##  Features

- **Real-time Status:** Displays current track title, artist name, and media source.
- **Progress Bar:** Interactive duration/playback progress indicator.
- **Keyboard Controls:** Manage playback directly inside the terminal.
- **Low Resource Usage:** Minimal CPU and RAM footprint.

##  Prerequisites

Ensure you have `playerctl` installed on your Linux distribution:

**Fedora:**
```bash
sudo dnf install playerctl python3-pip

sudo apt install playerctl python3-pip

sudo pacman -S playerctl python-pip

git clone [https://github.com/mehmet552/terminal-media-monitoring-tool.git](https://github.com/mehmet552/terminal-media-monitoring-tool.git)
cd terminal-media-monitoring-tool

pip install -r requirements.txt

python3 media_tui.py

Key,Action
SPACE,Play / Pause
N,Next Track
P,Previous Track
Q,Quit TUI
