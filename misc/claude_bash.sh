#!/bin/bash

# Wrapper that mirrors bash output to a tmux pane for visibility
# TO USE THIS FILE: Set $SHELL = <this script file path> - then use ClaudeCode.
#     ClaudeCode will use $SHELL to run bash commands by default, which means it will now use this
#     This file is a plug-and-play replacement for bash - and lets you monitor and log processes as they run
# It's useful for if Claude launches long jobs you want to keep track of
# The process that needs to be killed will be shown in the window name of each process
# When a process is done, you can find it in the ARCHIVE pane - scroll up and down to view previous outputs

IS_MACOS=$([[ "$(uname)" == "Darwin" ]] && echo 1)
SESSION="ClaudeSh"
ARCHIVE_WINDOW="ARCHIVE"
ARCHIVE_DIR="/tmp/claude_bash_archive"
EMOJIS="🔴🟠🟡🟢🔵🟣🟤⚫⚪🩶🩷🩵❤️🧡💛💚💙💜🖤🤍🤎💗💖💝💘🍎🍊🍋🍏🫐🍇🍓🍒🍑🥭🍍🥝🌶️🥕🌽🥦🍆🫑🔥🌊🌿🌸🌺🌻🌼🌷💐🌈☀️⭐🌙💫✨⚡💎🔮🎈🎀🧊❄️🎯🎨🎭🎪🎠🎡🎢🏀🏈⚽🎾🎱🧩🪁🛸🚀💊🧬🦠🔬🧪🎵🎶🔔💡🔦🏮🪔🎃👾🤖👽🦋🐝🐞🌵🍄🌴🥀🪷🪻"
BASH_BIN="/bin/bash"

mkdir -p "$ARCHIVE_DIR"
export PATH="$(dirname "$BASH_BIN"):$PATH"

pid_emoji() { echo "${EMOJIS:$(($1 % ${#EMOJIS})):1}"; }

# Use RP_PID if set (parent rp process), else fall back to PPID
PID=${RP_PID:-$PPID}


EMOJI=$(pid_emoji $PID)
WINDOW_NAME="${EMOJI}$$"
ARCHIVE_NAME="${EMOJI}${PID}->$$"

# --- Archive viewer with background cleaner ---
archive_viewer() {
    trap 'true' INT
    # Cleaner: archive and kill windows whose PID (trailing digits in name) is dead
    while true; do
        sleep 1
        tmux list-windows -t "$SESSION" -F "#{window_name} #{window_id}" 2>/dev/null | while read -r name id; do
            pid="${name##*[^0-9]}"
            [[ -z "$pid" ]] || kill -0 "$pid" 2>/dev/null && continue
            arch=$(tmux show-option -t "$id" -qv @archive_name)
            tmux capture-pane -e -t "$id" -p -S - > "$ARCHIVE_DIR/$(date +%Y-%m-%d_%H:%M:%S)__${arch}.log" 2>/dev/null
            tmux kill-window -t "$id" 2>/dev/null
        done
    done &
    # FZF browser
    RELOAD="ls -1 $ARCHIVE_DIR/*.log 2>/dev/null | sort -r"
    while true; do
        selected=$(fzf --no-sort --preview 'cat {}' \
            --bind "start:reload:$RELOAD" \
            --bind "focus:reload:$RELOAD" \
            --bind "space:reload:$RELOAD")
        [[ -n "$selected" ]] && less -R --mouse --wheel-lines=5 "$selected"
    done
}

# --- Tmux setup ---
ARCHIVE_CMD="SESSION=$SESSION; ARCHIVE_DIR=$ARCHIVE_DIR; $(declare -f archive_viewer); archive_viewer"

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux new-session -d -s "$SESSION" -n "$ARCHIVE_WINDOW" "$ARCHIVE_CMD"
elif ! tmux list-windows -t "$SESSION" -F "#{window_name}" | grep -q "^${ARCHIVE_WINDOW}$"; then
    # Respawn ARCHIVE at index 0
    tmux move-window -t "$SESSION" -r
    for i in $(tmux list-windows -t "$SESSION" -F "#{window_index}" | sort -rn); do
        # Move all other windows 1 index up to make room
        tmux move-window -s "$SESSION:$i" -t "$SESSION:$((i+1))"
    done
    tmux new-window -d -t "$SESSION:0" -n "$ARCHIVE_WINDOW" "$ARCHIVE_CMD"
fi

PANE=$(tmux new-window -d -t "$SESSION" -n "$WINDOW_NAME" -P -F "#{pane_id}" "cat")
tmux set-option -t "$PANE" @archive_name "$ARCHIVE_NAME"
TTY=$(tmux display -p -t "$PANE" "#{pane_tty}")

# --- Run command, mirror to tmux ---
if [ -t 0 ]; then
    if [ "$IS_MACOS" ]; then
        script -q "$TTY" "$BASH_BIN" "$@"
    else
        script -qefc "$(printf '%q ' "$BASH_BIN" "$@")" /dev/stdout | tee "$TTY"
    fi
else
    "$BASH_BIN" "$@" 2>&1 | tee "$TTY"
fi
