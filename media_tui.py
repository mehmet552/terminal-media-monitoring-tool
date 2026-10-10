import subprocess
import time
import sys
import select
import tty
import termios
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

def get_mpris_info():
    try:
        status = subprocess.check_output(["playerctl", "status"], text=True, stderr=subprocess.DEVNULL).strip()
        title = subprocess.check_output(["playerctl", "metadata", "title"], text=True, stderr=subprocess.DEVNULL).strip()
        artist = subprocess.check_output(["playerctl", "metadata", "artist"], text=True, stderr=subprocess.DEVNULL).strip()
        player = subprocess.check_output(["playerctl", "metadata", "--format", "{{playerName}}"], text=True, stderr=subprocess.DEVNULL).strip()
        
        progress_bar = ""
        try:
            pos = float(subprocess.check_output(["playerctl", "position"], text=True, stderr=subprocess.DEVNULL).strip())
            length = float(subprocess.check_output(["playerctl", "metadata", "mpris:length"], text=True, stderr=subprocess.DEVNULL).strip()) / 1_000_000
            
            if length > 0:
                percent = min(1.0, pos / length)
                bar_length = 20
                filled = int(bar_length * percent)
                bar = "█" * filled + "░" * (bar_length - filled)
                pos_min, pos_sec = divmod(int(pos), 60)
                len_min, len_sec = divmod(int(length), 60)
                progress_bar = f"\n[{bar}] {pos_min:02d}:{pos_sec:02d} / {len_min:02d}:{len_sec:02d}"
        except Exception:
            progress_bar = ""

        return {
            "status": "▶ Playing" if status == "Playing" else "⏸ Paused",
            "title": title or "Unknown Title",
            "artist": artist or "Unknown Artist",
            "player": player.capitalize(),
            "progress": progress_bar
        }
    except Exception:
        return None

def make_layout(data):
    if not data:
        text = Text("\n  󰎈 No active media player found...\n  (Start playing media in Spotify, VLC, or browser)\n", style="bold yellow")
        return Panel(text, title="[bold red]Media Controller[/bold red]", border_style="red")

    content = Text()
    content.append("Source: ", style="dim")
    content.append(f"{data['player']}\n\n", style="bold cyan")
    content.append("🎵 Title:  ", style="bold white")
    content.append(f"{data['title']}\n", style="bold green")
    content.append("👤 Artist: ", style="bold white")
    content.append(f"{data['artist']}\n\n", style="bold magenta")
    content.append(f"Status: {data['status']}", style="bold bright_blue" if "▶" in data['status'] else "bold orange3")
    
    if data['progress']:
        content.append(f"\n{data['progress']}", style="bright_black")

    controls = "\n\n[Shortcuts: SPACE (Play/Pause) | N (Next) | P (Previous) | Q (Quit)]"
    content.append(controls, style="bold yellow")

    return Panel(
        content,
        title="[bold magenta]󰎈 Media Player TUI[/bold magenta]",
        subtitle="[dim]Linux MPRIS TUI[/dim]",
        border_style="bright_blue",
        expand=False
    )

def is_key_pressed():
    return select.select([sys.stdin], [], [], 0.1)[0] != []

if __name__ == "__main__":
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
                    if key == ' ':
                        subprocess.run(["playerctl", "play-pause"], stderr=subprocess.DEVNULL)
                    elif key.lower() == 'n':
                        subprocess.run(["playerctl", "next"], stderr=subprocess.DEVNULL)
                    elif key.lower() == 'p':
                        subprocess.run(["playerctl", "previous"], stderr=subprocess.DEVNULL)
                    elif key.lower() == 'q':
                        break
                time.sleep(0.1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("\nMedia interface closed.")
