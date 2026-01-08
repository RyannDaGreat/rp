#!/usr/bin/env python3
"""
Textual-based panel for managing ClaudeSH tmux processes.
Displays active processes with CPU/memory graphs, allows kill/goto actions.
"""

import subprocess
from collections import deque
from dataclasses import dataclass, field

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Button, Static, Header, Footer

SESSION = "ClaudeSh"
ARCHIVE_WINDOW = "ARCHIVE"
PANEL_WINDOW = "PANEL"
CPU_HISTORY_LEN = 20


def run_cmd(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
    except subprocess.CalledProcessError:
        return ""


def get_tmux_windows() -> list[tuple[str, str]]:
    """Return list of (window_name, window_id) for ClaudeSH session."""
    out = run_cmd(["tmux", "list-windows", "-t", SESSION, "-F", "#{window_name} #{window_id}"])
    if not out:
        return []
    result = []
    for line in out.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            result.append((parts[0], parts[1]))
    return result


def extract_pid_from_name(name: str) -> int | None:
    """Extract trailing digits from window name as PID."""
    digits = ""
    for c in reversed(name):
        if c.isdigit():
            digits = c + digits
        else:
            break
    return int(digits) if digits else None


def get_process_stats(pid: int) -> tuple[str, float, float, str]:
    """Return (command, cpu_percent, memory_mb, elapsed) for a process."""
    # Get stats separately to avoid parsing issues with command containing spaces
    pid_str = str(pid)
    command = run_cmd(["ps", "-o", "command=", "-p", pid_str])
    stats = run_cmd(["ps", "-o", "%cpu=,rss=,etime=", "-p", pid_str])
    if not stats:
        return command, 0.0, 0.0, ""
    parts = stats.split()
    if len(parts) >= 3:
        try:
            cpu = float(parts[0])
            mem_mb = float(parts[1]) / 1024
            elapsed = parts[2].strip()
            return command, cpu, mem_mb, elapsed
        except ValueError:
            pass
    return command, 0.0, 0.0, ""


def kill_process(pid: int):
    """Kill a process by PID."""
    subprocess.run(["kill", "-9", str(pid)], check=False)


def goto_window(window_id: str):
    """Switch to a tmux window."""
    run_cmd(["tmux", "select-window", "-t", window_id])


def get_spawner_pane(window_id: str) -> str | None:
    """Get the spawner pane ID stored in the tmux window option."""
    return run_cmd(["tmux", "show-option", "-t", window_id, "-qv", "@spawner_pane"]) or None


def get_pane_path(pane_id: str) -> str:
    """Convert pane ID to session:window.pane format."""
    out = run_cmd(["tmux", "display", "-t", pane_id, "-p", "#{session_name}:#{window_name}.#{pane_index}"])
    return out or pane_id


def goto_pane(pane_id: str):
    """Switch to a tmux pane (potentially in a different session)."""
    run_cmd(["tmux", "switch-client", "-t", pane_id])


@dataclass
class ProcessInfo:
    pid: int
    window_id: str
    emoji: str
    command: str = ""
    elapsed: str = ""
    cpu_history: deque = field(default_factory=lambda: deque(maxlen=CPU_HISTORY_LEN))
    cpu_pct: float = 0.0
    memory_mb: float = 0.0
    spawner_pane: str | None = None
    spawner_path: str = ""


class CpuGraph(Static):
    """Mini sparkline graph for CPU usage with percentage."""

    def __init__(self, proc: ProcessInfo, **kwargs):
        super().__init__(**kwargs)
        self.proc = proc

    def render(self) -> str:
        blocks = "▁▂▃▄▅▆▇█"
        if not self.proc.cpu_history:
            graph = "▁" * CPU_HISTORY_LEN
        else:
            max_val = max(self.proc.cpu_history) or 100
            graph = "".join(
                blocks[min(int(v / max_val * 7), 7)] for v in self.proc.cpu_history
            ).ljust(CPU_HISTORY_LEN, "▁")
        return f"{graph} {self.proc.cpu_pct:5.1f}%"


class MemoryBar(Static):
    """Memory usage bar."""

    def __init__(self, proc: ProcessInfo, **kwargs):
        super().__init__(**kwargs)
        self.proc = proc

    def render(self) -> str:
        filled = min(int(self.proc.memory_mb / 1024 * 10), 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"[{bar}] {self.proc.memory_mb:.0f}MB"


class ProcessRow(Static):
    """A row displaying one process with controls."""

    DEFAULT_CSS = """
    ProcessRow {
        height: auto;
        padding: 1;
        border: solid $primary;
        margin-bottom: 1;
    }
    ProcessRow:focus {
        border: double $accent;
        background: $surface-lighten-1;
    }
    ProcessRow .row-header { height: 3; width: 100%; }
    ProcessRow .pid-label { width: 20; }
    ProcessRow .elapsed { width: 15; color: $accent; }
    ProcessRow .command-display { height: 1; padding-left: 2; color: $text-muted; }
    ProcessRow .stats-row { height: 1; width: 100%; margin-top: 1; }
    ProcessRow .cpu-label { width: 5; color: $success; }
    ProcessRow .cpu-graph { width: 28; color: $success; }
    ProcessRow .mem-label { width: 5; color: $warning; }
    ProcessRow .mem-bar { width: 25; color: $warning; }
    ProcessRow Button { min-width: 10; height: 3; }
    ProcessRow .kill-btn { margin-left: 2; }
    ProcessRow .goto-btn { margin-left: 1; }
    ProcessRow .spawner-btn { margin-left: 1; }
    """

    can_focus = True

    def __init__(self, proc: ProcessInfo, **kwargs):
        super().__init__(**kwargs)
        self.proc = proc

    def compose(self) -> ComposeResult:
        with Horizontal(classes="row-header"):
            yield Static(f"{self.proc.emoji} PID {self.proc.pid}", classes="pid-label")
            yield Static(f"⏱ {self.proc.elapsed}", classes="elapsed", id=f"elapsed-{self.proc.pid}")
            yield Button("✕ Kill", id=f"kill-{self.proc.pid}", classes="kill-btn", variant="error")
            yield Button("→ Go", id=f"goto-{self.proc.pid}", classes="goto-btn", variant="primary")
            if self.proc.spawner_pane:
                yield Button(f"⬅ {self.proc.spawner_path}", id=f"spawner-{self.proc.pid}", classes="spawner-btn", variant="success")

        yield Static(f"  {self.proc.command[:150] or '(no command)'}", classes="command-display")

        with Horizontal(classes="stats-row"):
            yield Static("CPU:", classes="cpu-label")
            yield CpuGraph(self.proc, classes="cpu-graph", id=f"cpu-{self.proc.pid}")
            yield Static(" MEM:", classes="mem-label")
            yield MemoryBar(self.proc, classes="mem-bar", id=f"mem-{self.proc.pid}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if btn_id.startswith("kill-"):
            kill_process(self.proc.pid)
            self.app.refresh_processes()
        elif btn_id.startswith("goto-"):
            goto_window(self.proc.window_id)
        elif btn_id.startswith("spawner-") and self.proc.spawner_pane:
            goto_pane(self.proc.spawner_pane)


class ClaudePanel(App):
    """Main panel application for ClaudeSH process management."""

    TITLE = "ClaudeSH Panel"
    CSS = """
    Screen { background: $surface; }
    #container { height: 100%; }
    #no-processes { text-align: center; padding: 5; color: $text-muted; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("j", "next", "Next", show=False),
        Binding("k", "prev", "Prev", show=False),
        Binding("down", "next", "Next"),
        Binding("up", "prev", "Prev"),
        Binding("x", "kill_focused", "Kill"),
        Binding("g", "goto_focused", "Go To"),
        Binding("enter", "goto_focused", "Go To", show=False),
        Binding("s", "spawner_focused", "Spawner"),
    ]

    def __init__(self):
        super().__init__()
        self.processes: dict[int, ProcessInfo] = {}
        self._ui_built = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(id="container")
        yield Footer()

    def on_mount(self) -> None:
        self.call_after_refresh(self.refresh_processes)
        self.set_interval(1.0, self.update_stats)
        self.set_interval(2.0, self.refresh_processes)

    def refresh_processes(self) -> None:
        """Refresh the list of processes from tmux."""
        try:
            windows = get_tmux_windows()
            current_pids = set(self.processes.keys())
            new_pids = set()

            for name, wid in windows:
                if name in (ARCHIVE_WINDOW, PANEL_WINDOW):
                    continue
                pid = extract_pid_from_name(name)
                if pid is None:
                    continue
                new_pids.add(pid)

                if pid not in self.processes:
                    emoji = name[0] if name else "?"
                    cmd, cpu, mem, elapsed = get_process_stats(pid)
                    spawner = get_spawner_pane(wid)
                    spawner_path = get_pane_path(spawner) if spawner else ""
                    self.processes[pid] = ProcessInfo(
                        pid=pid, window_id=wid, emoji=emoji,
                        command=cmd, elapsed=elapsed, cpu_pct=cpu, memory_mb=mem,
                        spawner_pane=spawner, spawner_path=spawner_path,
                    )

            for pid in current_pids - new_pids:
                del self.processes[pid]

            if new_pids != current_pids or not self._ui_built:
                self._ui_built = True
                self.rebuild_ui()
        except Exception:
            pass

    def rebuild_ui(self) -> None:
        """Rebuild the process list UI."""
        try:
            container = self.query_one("#container", ScrollableContainer)
            container.remove_children()

            if not self.processes:
                container.mount(Static("No active processes", id="no-processes"))
            else:
                for pid in sorted(self.processes.keys()):
                    container.mount(ProcessRow(self.processes[pid], id=f"row-{pid}"))
                rows = self.query("ProcessRow")
                if rows:
                    rows.first().focus()
        except Exception:
            pass

    def update_stats(self) -> None:
        """Update CPU/memory/elapsed stats for all processes."""
        try:
            for pid, proc in list(self.processes.items()):
                _, cpu, mem, elapsed = get_process_stats(pid)
                proc.cpu_history.append(cpu)
                proc.cpu_pct = cpu
                proc.memory_mb = mem
                proc.elapsed = elapsed

                try:
                    self.query_one(f"#cpu-{pid}").refresh()
                    self.query_one(f"#mem-{pid}").refresh()
                    self.query_one(f"#elapsed-{pid}", Static).update(f"⏱ {elapsed}")
                except Exception:
                    pass
        except Exception:
            pass

    def action_refresh(self) -> None:
        self.refresh_processes()

    def action_next(self) -> None:
        self.screen.focus_next("ProcessRow")

    def action_prev(self) -> None:
        self.screen.focus_previous("ProcessRow")

    def action_kill_focused(self) -> None:
        if isinstance(self.focused, ProcessRow):
            kill_process(self.focused.proc.pid)
            self.refresh_processes()

    def action_goto_focused(self) -> None:
        if isinstance(self.focused, ProcessRow):
            goto_window(self.focused.proc.window_id)

    def action_spawner_focused(self) -> None:
        if isinstance(self.focused, ProcessRow) and self.focused.proc.spawner_pane:
            goto_pane(self.focused.proc.spawner_pane)


def main():
    ClaudePanel().run()


if __name__ == "__main__":
    main()
