import select
import subprocess
import sys
import termios
import time
import tty

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


def run_playerctl(*args):
    return subprocess.check_output(["playerctl", *args], text=True, stderr=subprocess.DEVNULL).strip()


def format_progress(position, length):
    if length <= 0:
        return ""

    percent = min(max(position / length, 0.0), 1.0)
    bar_length = 20
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    pos_min, pos_sec = divmod(int(position), 60)
    len_min, len_sec = divmod(int(length), 60)
    return f"\n[{bar}] {pos_min:02d}:{pos_sec:02d} / {len_min:02d}:{len_sec:02d}"


def get_mpris_info():
    try:
        status = run_playerctl("status")
        title = run_playerctl("metadata", "title") or "Unknown Title"
        artist = run_playerctl("metadata", "artist") or "Unknown Artist"
        player = run_playerctl("metadata", "--format", "{{playerName}}") or "Unknown Player"
    except Exception:
        return None

    progress = ""
    try:
        position = float(run_playerctl("position"))
        length_ms = float(run_playerctl("metadata", "mpris:length"))
        length = length_ms / 1_000_000 if length_ms > 0 else 0
        progress = format_progress(position, length)
    except Exception:
        progress = ""

    return {
        "status": "▶ Playing" if status == "Playing" else "⏸ Paused",
        "title": title,
        "artist": artist,
        "player": player.capitalize(),
        "progress": progress,
    }


def make_layout(data):
    if not data:
        text = Text("\n  No active media player found...\n  Start playing media in Spotify, VLC, Firefox, or Chrome.\n", style="bold yellow")
        return Panel(text, title="[bold red]Media Controller[/bold red]", border_style="red")

    content = Text()
    content.append("Source: ", style="dim")
    content.append(f"{data['player']}\n\n", style="bold cyan")
    content.append("🎵 Title:  ", style="bold white")
    content.append(f"{data['title']}\n", style="bold green")
    content.append("👤 Artist: ", style="bold white")
    content.append(f"{data['artist']}\n\n", style="bold magenta")
    content.append(f"Status: {data['status']}", style="bold bright_blue" if "▶" in data["status"] else "bold orange3")

    if data["progress"]:
        content.append(data["progress"], style="bright_black")

    controls = "\n\n[Shortcuts: SPACE (Play/Pause) | N (Next) | P (Previous) | Q (Quit)]"
    content.append(controls, style="bold yellow")

    return Panel(
        content,
        title="[bold magenta]Media Player TUI[/bold magenta]",
        subtitle="[dim]Linux MPRIS TUI[/dim]",
        border_style="bright_blue",
        expand=False,
    )


def is_key_pressed():
    return select.select([sys.stdin], [], [], 0.1)[0] != []


def handle_key(key):
    if key == " ":
        subprocess.run(["playerctl", "play-pause"], stderr=subprocess.DEVNULL)
    elif key.lower() == "n":
        subprocess.run(["playerctl", "next"], stderr=subprocess.DEVNULL)
    elif key.lower() == "p":
        subprocess.run(["playerctl", "previous"], stderr=subprocess.DEVNULL)
    elif key.lower() == "q":
        return False
    return True


def main():
    console = Console()
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())
        with Live(make_layout(get_mpris_info()), refresh_per_second=4, console=console) as live:
            while True:
                data = get_mpris_info()
                live.update(make_layout(data))

                if is_key_pressed():
                    key = sys.stdin.read(1)
                    if not handle_key(key):
                        break

                time.sleep(0.1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("\nMedia interface closed.")


if __name__ == "__main__":
    main()

