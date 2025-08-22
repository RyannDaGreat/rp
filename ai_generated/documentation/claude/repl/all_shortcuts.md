# Complete RP Command Shortcuts Reference

## Overview
RP has **555+ command shortcuts** organized into categories. These shortcuts are case-insensitive and work when no variable with that name exists.

## How Shortcuts Work

1. **Activation**: Type the shortcut in uppercase (e.g., `CD`, `PWD`)
2. **Case Flexibility**: Can type lowercase if no variable exists (e.g., `pwd` → `PWD`)
3. **Transformation**: RP shows what command it transforms to
4. **Special Syntax**: 
   - `$` prefix gets replaced with `rp.` imports
   - `!` prefix runs shell commands
   - `#` comments describe functionality

## Major Categories

### 1. Directory Navigation (50+ shortcuts)

#### Core Navigation
- `CD` - Change directory with path completion
- `CDU` / `U` - Go up one directory  
- `CDB` / `B` - Go back in directory history
- `CDH` - Interactive directory history browser
- `CDHF` - Fast directory history
- `PWD` - Print working directory
- `CPWD` - Copy PWD to clipboard

#### Advanced CD Commands
- `CDG` - CD to git root
- `CDGG` - CD to great git root (top-level)
- `CDA` - CD to location of ans
- `CDT` - CD to temp directory
- `CDR` - CD to RP directory
- `CDPY` - CD to Python site-packages
- `CDD` - CD to Desktop
- `CDDOWN` / `CDDL` - CD to Downloads
- `CDHOME` - CD to home directory

#### History Management
- `CDC` / `CDHCLEAN` - Clean CD history
- `CDH GIT` - Find git repos in history
- `TAKE` - Make directory and CD into it

### 2. File Operations (80+ shortcuts)

#### Basic File Commands
- `LS` / `L` - List files
- `LSS` - Interactive file selector
- `LSA` - List all files (including hidden)
- `LSL` - List files with details
- `TREE` - Display file tree
- `OPEN` / `O` - Open file/folder

#### File Management
- `RM` / `DEL` - Remove file
- `RMA` - Remove ans
- `CP` / `COPY` - Copy files
- `MV` / `MOVE` - Move files
- `TOUCH` - Create empty file
- `MKDIR` - Make directory

#### File Content
- `CAT` - Display file contents
- `HEAD` / `TAIL` - Show file beginning/end
- `GREP` - Search in files
- `FIND` / `FD` - Find files
- `FZF` - Fuzzy file finder

### 3. History & Search (40+ shortcuts)

#### Command History
- `HISTORY` / `HIST` - Show command history
- `AHISTORY` / `AHIST` - All history (including failures)
- `GHISTORY` / `GHIST` - Green history (successful single-line)
- `DHISTORY` / `DHIST` - Function definition history
- `CHISTORY` / `CHIST` - Copy history to clipboard

#### History Queries
- `QVH` - Query visual history (interactive)
- `QPH` - Query prompt-toolkit history
- `QPHP` - Query history paragraphs

### 4. Image & Media (100+ shortcuts)

#### Image Display
- `I` / `IMG` - Display image (ans)
- `IA` - Display ans as image
- `II` - Interactive image viewer
- `IIA` - Display all images in ans
- `IIS` - Select and display images
- `ITERM` - Display in iTerm2

#### Image Operations
- `IMGA` - Apply operation to image
- `IMGS` - Save image
- `IMGR` - Resize image
- `IMGB` - Blur image
- `IMGF` - Flip image
- `IMGG` - Convert to grayscale

#### Video Operations
- `VID` / `V` - Play video
- `VIDA` - Play ans as video
- `VIDS` - Save video
- `GIF` - Create/play GIF
- `GIFA` - Convert ans to GIF

#### Audio Operations
- `AUDIO` / `A` - Play audio
- `RECORD` - Record audio
- `TTS` - Text to speech

### 5. Clipboard Operations (30+ shortcuts)

#### Basic Clipboard
- `COPY` / `C` - Copy to clipboard
- `PASTE` / `P` - Paste from clipboard
- `EPASTE` - Execute pasted code

#### Advanced Clipboard
- `WCOPY` - Web copy (internet clipboard)
- `WPASTE` - Web paste
- `LCOPY` - Local file copy
- `LPASTE` - Local file paste
- `TCOPY` - tmux copy
- `TPASTE` - tmux paste
- `VCOPY` - Vim copy
- `VPASTE` - Vim paste

### 6. Git Operations (20+ shortcuts)

- `GIT` - Git status
- `GITS` / `GS` - Git status
- `GITD` / `GD` - Git diff
- `GITA` / `GA` - Git add
- `GITC` / `GC` - Git commit
- `GITP` / `GP` - Git push
- `GITPL` / `GPL` - Git pull
- `GITL` / `GL` - Git log
- `GITB` / `GB` - Git branch
- `UNCOMMIT` - Undo last commit
- `GITIGNORE` / `GIG` - Create .gitignore

### 7. Python & Development (60+ shortcuts)

#### Python Execution
- `RUN` - Run Python file
- `EXEC` / `E` - Execute code
- `EPASTE` - Execute clipboard
- `PY` - Python interpreter
- `IPY` / `IPYTHON` - IPython shell
- `JUPYTER` / `J` - Jupyter notebook

#### Module Management
- `IMPORT` - Import module
- `RELOAD` - Reload modules
- `PIP` - pip command
- `PIPINSTALL` / `PIPI` - pip install
- `PIPLIST` / `PIPL` - pip list

#### Debugging
- `DEBUG` / `D` - Enter debugger
- `TRACE` - Trace execution
- `PROF` - Toggle profiler
- `LINEPROF` - Line profiler
- `MORE` - Show last error
- `MMORE` - Detailed error
- `DMORE` - Debug last error

### 8. Display & Visualization (50+ shortcuts)

#### Data Display
- `SHOW` / `S` - Show ans
- `PRINT` / `PR` - Print value
- `PP` - Pretty print
- `TABLE` / `T` - Display as table
- `DF` - Display DataFrame
- `PLOT` - Create plot
- `PLOTLY` - Interactive plot

#### Terminal Display
- `CLEAR` / `CLS` - Clear screen
- `FANSI` - Colored output
- `BANNER` - Display banner
- `COLORS` - Show color palette

### 9. System & Process (30+ shortcuts)

- `PS` - Process list
- `TOP` - System monitor
- `HTOP` - Interactive process viewer
- `KILL` - Kill process
- `MONITOR` - System monitoring
- `GPU` - GPU status
- `DISK` - Disk usage
- `MEM` - Memory usage

### 10. Network & Web (20+ shortcuts)

- `CURL` - HTTP request
- `WGET` - Download file
- `HTTP` - Start HTTP server
- `SSH` - SSH connection
- `PING` - Ping host
- `IP` - Show IP address
- `GURL` - Get git remote URL
- `SURL` - Shorten URL

### 11. Terminal & Shell (30+ shortcuts)

- `SHELL` / `SH` - Shell prompt
- `BASH` - Bash shell
- `ZSH` - Zsh shell
- `TMUX` / `TM` - tmux session
- `SCREEN` - GNU Screen
- `EXIT` / `QUIT` - Exit RP

### 12. Text Editing (40+ shortcuts)

- `VIM` / `VI` - Edit in Vim
- `NANO` - Edit in Nano
- `MICRO` - Edit in Micro
- `EDIT` - External editor
- `SED` - Stream editor
- `AWK` - Text processing
- `FART` - Find and replace text

### 13. Special RP Commands (50+ shortcuts)

#### Session Control
- `RETURN` / `RET` - Exit and return ans
- `SUSPEND` / `SUS` - Suspend session
- `FORK` - Fork process
- `LEVEL` - Show environment info

#### RP Settings
- `PT ON/OFF` - Prompt toolkit toggle
- `MOD ON/OFF` - Modifier toggle
- `FANSI ON/OFF` - Color toggle
- `TICTOC ON/OFF` - Timing toggle
- `GC ON/OFF` - Garbage collection
- `UNDO ON/OFF` - Snapshot history

#### Answer Management
- `ANS` - Show answer
- `PREV` - Previous answer
- `NEXT` - Next answer (redo)
- `UNDO` - Undo to snapshot
- `REDO` - Redo snapshot

### 14. Quick Aliases (Single Letters)

- `B` - Go back (CDB)
- `C` - Copy
- `D` - Debug
- `E` - Execute
- `G` - Git
- `H` - Help
- `I` - Image
- `J` - Jupyter
- `L` - List files
- `M` - More (error)
- `N` - Next
- `O` - Open
- `P` - Paste/Previous
- `Q` - Query
- `R` - Run
- `S` - Show
- `T` - Table
- `U` - Up directory
- `V` - Video/Vim
- `W` - Write
- `X` - Execute
- `Y` - Yes
- `Z` - Fuzzy finder

## Special Input Transformations

### Slash to Question Mark
When variable doesn't exist:
- `/v` → `?v` (vim ans)
- `/s` → `?s` (show string)
- `/p` → `?p` (print)
- `/e` → `?e` (execute)

### Lowercase to Uppercase
When no variable exists:
- `pwd` → `PWD`
- `cd` → `CD`
- `ls` → `LS`

### Operators
- `+ 5` → `ans + 5`
- `.shape` → `ans.shape`
- `[0]` → `ans[0]`

## Command Modifiers

### Execution Modifiers
- `!command` - Run shell command
- `$function` - Run RP function
- `#comment` - Add comment

### Path Modifiers
- `~` - Home directory
- `.` - Current directory
- `..` - Parent directory
- `-` - Previous directory

## Customization

### Adding Custom Shortcuts
Shortcuts can be extended via `r_iterm_comm.additional_command_shortcuts`

### Settings Location
- `~/.rp/` - RP configuration directory
- `RPRC` file for initialization

## Tips

1. **Tab Completion**: Most commands support tab completion
2. **Case Insensitive**: Commands work in any case
3. **Partial Matching**: Many commands have shorter aliases
4. **Chaining**: Commands can be chained with `;`
5. **History**: All commands are saved in history

## Total Count: 555+ Shortcuts

This represents one of the most comprehensive REPL command systems ever created, with shortcuts for virtually every common operation.