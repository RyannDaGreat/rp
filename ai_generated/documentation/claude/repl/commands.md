# REPL Command System

## Overview
RP's REPL features an extensive command system with 500+ shortcuts that provide instant access to common operations. Commands are processed through a sophisticated shortcut expansion system that turns brief aliases into full functionality.

## Command Processing Architecture

### Location in Code
- **Main command processing**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py` in `pseudo_terminal()` function around line 20,000
- **Shortcut definitions**: `command_shortcuts_string` variable around line 20188
- **Expansion logic**: Command pairs are split and processed into a shortcuts dictionary
- **Key bindings**: `/opt/homebrew/lib/python3.10/site-packages/rp/rp_ptpython/key_bindings.py` for space autocompletions

### Processing Flow
1. User input is checked against `command_shortcuts` dictionary
2. If match found, shortcut is expanded to full command
3. Special commands (CD, VIM, etc.) get dedicated processing
4. Shell commands (starting with `!`) are executed directly
5. Python expressions are evaluated last

## Complete Command Reference

### 1. Error Handling & Debugging

#### Error Investigation
- `M` / `MORE` - Show detailed error traceback
- `MM` / `MMORE` - Extended error information  
- `DM` / `DMORE` - Debug mode error details
- `GM` / `GMORE` - Google search the error
- `HM` / `HMORE` - Help with error
- `AM` / `AMORE` - Advanced error analysis
- `VM` / `VIMORE` - Edit files from error traceback
- `PM` / `PIPMORE` - Auto pip install missing modules
- `IM` / `IMPMORE` - Auto import missing modules
- `UM` / `PREVMORE` - Previous error in history
- `NM` / `NEXTMORE` - Next error in history
- `RIM` / `RMORE` - Comprehensive error report
- `CM` / `RMORE` - Same as RIM

#### Warnings
- `WN` / `WR` / `WARN` - Show warning details

### 2. History Commands

#### Command History
- `HI` / `HIST` - Show command history
- `DH` / `DHI` / `DHIST` - Directory history
- `CH` / `CHI` / `CHIST` - Command history (alternative)
- `GH` / `GHI` / `GHIST` - Git history
- `AH` / `AHI` / `AHIST` - All history
- `VH` / `VHI` / `VHIST` - Vim history
- `QPH` - Query prompt-toolkit history lines (F3)
- `QPHP` - Query prompt-toolkit history paragraphs (F3)  
- `QVH` - Query VHISTORY

### 3. Help & Information

#### Basic Help
- `H` / `HE` / `HELP` - Show help
- `HH` / `HHELP` - Extended help
- `SC` / `SHORTCUTS` - Show shortcuts

### 4. Clipboard Operations

#### Basic Clipboard
- `CO` / `COPY` - Copy ans to clipboard
- `WCO` / `WC` / `WCOPY` - Web copy (to cloud clipboard)
- `LC` / `LCO` / `LCOPY` - Local copy
- `TC` / `TCO` / `TCOPY` - Tmux copy
- `VCO` / `VC` / `VCOPY` - Vim copy
- `FC` / `FCOPY` - File copy

#### Pasting
- `EPA` / `EP` / `EPASTE` - Enhanced paste
- `PA` / `PASTE` - Basic paste
- `WP` / `WPA` / `WPASTE` - Web paste
- `VP` / `VPA` / `VPASTE` - Vim paste
- `LP` / `LPA` / `LPASTE` - Local paste
- `TP` / `TPA` / `TPASTE` - Tmux paste
- `FP` / `FPA` / `FPASTE` - File paste
- `MLP` / `MLPASTE` - Multi-line paste

#### Advanced Clipboard Operations
- `PSP` / `PAS` / `PASH` - Parse clipboard as shell arguments
- `+PA` / `PPA` - Append paste to ans
- `+PAL` / `PPAL` / `PPLA` / `PAL` / `PLA` - Paste with newline

#### Cross-Clipboard Conversions
- `TPWC` / `WCTP` - Tmux paste → web copy
- `TPCO` / `COTP` - Tmux paste → clipboard copy
- `TPLC` / `LCTP` - Tmux paste → local copy  
- `TPVC` / `VCTP` - Tmux paste → vim copy
- `WPTC` / `TCWP` - Web paste → tmux copy
- `WPCO` / `COWP` - Web paste → clipboard copy
- `WPLC` / `LCWP` - Web paste → local copy
- `WPVC` / `VCWP` - Web paste → vim copy
- `PATC` / `TCPA` - Clipboard → tmux copy
- `PAWC` / `WCPA` - Clipboard → web copy
- `PALC` / `LCPA` - Clipboard → local copy
- `PAVC` / `VCPA` - Clipboard → vim copy
- `LPTC` / `TCLP` - Local paste → tmux copy
- `LPWC` / `WCLP` - Local paste → web copy
- `LPCO` / `COLP` - Local paste → clipboard copy
- `LPVC` / `VCLP` - Local paste → vim copy
- `VPTC` / `TCVP` - Vim paste → tmux copy
- `VPWC` / `WCVP` - Vim paste → web copy
- `VPCO` / `COVP` - Vim paste → clipboard copy
- `VPLC` / `LCVP` - Vim paste → local copy

### 5. Directory Navigation

#### Basic Navigation
- `U` / `CDU` - Go up one directory (cd ..)
- `B` / `CDB` - Go back in directory history
- `DA` / `CDA` - CD to ans (if ans is a path)

#### Multi-Level Up Navigation
- `UU` - Up 2 directories (../..)
- `UUU` - Up 3 directories (../../..)
- `UUUU` - Up 4 directories
- (Pattern continues up to `UUUUUUUUUUUUUUUUUUU` - 20 U's)

#### Numbered Up Navigation  
- `1U` - Same as CDU
- `2U` - Up 2 directories
- `3U` - Up 3 directories
- (Pattern continues up to `20U`)

#### Multi-Level Back Navigation
- `BB` / `CDBCDB` - Go back twice in directory history
- `BBB` / `CDBCDBCDB` - Go back 3 times
- (Pattern continues up to 20 B's)

#### Directory History
- `CDC` / `CCL` / `cdhclean` - Clean directory history
- `HC` / `HD` / `CDH` - Browse directory history
- `DG` / `HDG` / `CDH GIT` - CD to git root
- `HDF` / `CDHF` / `CDH FAST` - Fast directory history
- `VCDH` / `CDHV` / `VHD` / `HDV` - Edit directory history file
- `DQ` / `CDHQ FAST` - Quick directory history

#### Special Directory Navigation
- `` ` `` / `D`` ` / `CD`` ` - Go to home directory (~)
- `REPO` - Go to git repo parent directory
- `UG` / `GU` - Go up to git repo parent  
- `CDR` / `RDA` - CD to random directory
- `RF` - Get random file name
- `RD` - Get random directory name
- `RE` - Get random element from ans

### 6. File Operations

#### File Viewing
- `CAT` / `CA` - Display file contents  
- `NCAT` - Display with line numbers
- `CCAT` - Colored cat
- `ACAT` / `AC` / `A` / `AA` / `ACA` / `ACATA` - Auto-select and cat
- `CATA` / `CAA` - Cat with auto-selection
- `NCATA` / `CCATA` / `ACATA` - Variants with line numbers/colors

#### File Management
- `TAKE` / `TA` / `TK` - Make directory and CD into it
- `MKDIR` / `MK` / `MA` - Make directory
- `OPEN` / `OP` - Open with default application
- `OPENH` / `OPH` / `OH` - Open here (current directory)
- `OPENA` / `OPA` / `OA` - Open ans

#### File Information
- `PWD` / `PW` / `PD` / `WD` - Print working directory
- `CPWD` - Copy current directory to clipboard
- `APWD` / `APW` / `AP` / `AW` - Print absolute path
- `GMP` - Get module path of ans
- `GPP` - Get parent path of ans
- `GFN` - Get file name from ans
- `GPN` - Get path name from ans  
- `SFE` - Strip file extension from ans
- `GFE` - Get file extension from ans
- `APA` - Get absolute path of ans
- `RPA` - Get relative path of ans
- `UPA` - Get user path of ans (~)

#### File Manipulation
- `RMA` - Remove/delete ans
- `RNA` - Rename ans (with interactive prompt)
- `CAH` / `CPAH` - Copy ans here (to current directory)
- `CPPH` / `CPH` - Copy clipboard path here
- `HLAH` - Hard link ans here
- `MAH` / `MVAH` - Move ans here
- `MVPH` / `MPH` - Move clipboard path here
- `LNAH` / `LN` - Create symlink to ans here
- `HL` - Create hard link to ans

### 7. Code Execution

#### Python Execution
- `RUN` / `RU` - Run Python script
- `RUNA` / `RA` / `EA` - Run ans as Python script
- `SRUNA` / `SRA` / `SA` / `SR` - Safe run ans
- `SSRUNA` / `SSR` / `SSA` / `SS` - Super safe run ans
- `PYA` - Run ans in separate Python process
- `PUA` / `PDA` - Run ans with pudb debugger

#### Shell Execution  
- `BAA` - Run ans as bash script
- `ZSHA` - Run ans with zsh
- `BA` - Start bash shell
- `S` - Start sh shell  
- `Z` / `ZSH` - Start zsh shell

#### Special Execution Contexts
- `CPR` - Check pip requirements
- `PRP` / `PYM rp` - Run Python module rp
- `SURP` - Run RP with sudo

### 8. Editor Integration

#### Vim Commands
- `V` / `VI` / `VIM` - Open file in vim
- `AV` / `AVA` / `AVIMA` - Auto-select file and open in vim  
- `VA` / `VIMA` - Open ans in vim
- `VHE` / `VIH` / `VIMH` - Open current directory in vim
- `VV` - Direct vim command
- `VCL` - Clear vim info (delete ~/.viminfo)

#### Other Editors
- `EDIT` - Open in external editor
- `SUH` - Open current directory in Sublime Text
- `SUA` - Open ans in Sublime Text  
- `COH` - Open current directory in VS Code
- `COA` - Open ans in VS Code

### 9. System Information & Monitoring

#### System Commands
- `DISK` / `DK` - Show disk usage
- `DISKH` / `DKH` / `KH` - Disk usage (human readable)
- `TREE` / `TR` - Show directory tree
- `TREE ALL` / `TRA` / `treeall` - Show all files in tree
- `TREE DIR` / `TRD` / `treedir` - Show only directories
- `TREE ALL DIR` / `TRAD` / `treealldir` - All files and directories tree

#### GPU Monitoring
- `SMI` - Run nvidia-smi
- `NVI` - Run nvitop  
- `NVT` - Run nvtop
- `GP` - Print GPU summary
- `VGP` - Video GPU monitoring with viddy
- `NGP` - Notebook GPU summary
- `CVD` - Show CUDA_VISIBLE_DEVICES

#### Process Monitoring  
- `MON` / `MONITOR` - System monitor
- `BOP` / `TOP` - Run top
- `bashtop` - Run bashtop alternative

### 10. Profiling & Performance

#### Code Profiling
- `PROF` / `PF` / `PO` - Profile code execution
- `POD` / `PROF DEEP` - Deep profiling
- `POF` / `PROF FLAME` / `FLAME` / `FLA` - Generate flame graph
- `FLAO` / `PROF FLAME OPEN` - Flame graph and open
- `FLAC` / `PROF FLAME COPY` - Flame graph and copy
- `FLAI` / `FLAIC` / `PROF FLAME IMAGE COPY` - Flame graph as image
- `FLAP` / `PROF FLAME PASTE` - Flame graph from paste
- `LO` / `LINEPROF` - Line-by-line profiling
- `TT` / `TICTOC` - Time execution
- `VIMPROF` - Profile vim startup plugins

### 11. File Listing & Search

#### Basic Listing
- `LS` - List files
- `LST` - List files sorted by time
- `LSN` - List files sorted by name length  
- `LSD` - List files sorted by disk size
- `NLS` - Show number of files in directory

#### Advanced Listing
- `LSA` / `ALS` - All files (absolute paths)
- `LSAD` / `ALSD` - All directories
- `LSAF` / `ALSF` - All files only
- `LSAG` - All files globally (absolute paths)
- `LSAFG` - All files globally  
- `LSADG` - All directories globally
- `ALSF` - All files (relative paths)
- `LSM` - Multi-select files with fzf
- `LSAI` - All image files

#### Search Commands
- `FD` - Find files
- `AFD` / `FDA` - Advanced file discovery
- `FDT` / `FDTA` - Find files with text search
- `FDS` / `FD SEL` - Select files with fzf
- `LSS` / `LS SEL` - Select from ls with fzf
- `LSR` / `LS REL` - List relative paths
- `LSZ` / `LS FZF` / `FDZ` - File search with fzf
- `LSQ` / `LS QUE` / `LSF` / `FDQ` - Quick file search
- `RANGER` / `RNG` / `RG` - Open ranger file manager

### 12. Display Commands

#### Image & Video Display
- `DI` - Display image/video (auto-detect from ans)
- `DV` - Display video from ans  
- `DVL` - Display video with loop
- `DCI` - Display image in terminal with colors
- `DISC` - Display image slideshow with colors
- `DISI` - Display image slideshow with imgcat

#### Media Web Operations
- `WCIJ` / `WCIJ1-9` / `WCIJ95` - Web copy image as JPEG (quality levels)
- `WCIP` - Web copy image as PNG
- `WPI` - Web paste image

### 13. Advanced Clipboard - Base64 & Images

#### Base64 Operations
- `64P` - Paste base64 as object (with size info)
- `64C` - Copy object as base64 (with size info)
- `64FC` - Base64 file copy  
- `64FCA` - Base64 file copy ans
- `64FCH` - Base64 file copy here (current directory)
- `64FP` - Base64 file paste
- `64FPA` - Base64 file paste ans

#### Image Clipboard Operations
- `IPA` / `IMPA` / `IMP` - Image object paste (from clipboard)
- `IFP` / `IFPA` - Image file paste
- `IFPAO` / `IFPO` - Image file paste and open
- `ICO` / `IMCO` - Image object copy (display in terminal)
- `IFC` - Image file copy (current selection)
- `IFCA` - Image file copy ans
- `IFCH` - Image file copy here

### 14. Version Control & Git

#### Git Operations
- `GCLP` - Git clone from clipboard
- `GCLPS` - Git clone shallow from clipboard
- `GCLA` - Git clone ans with progress
- `GCLAS` - Git clone ans shallow
- `GURL` - Get git remote URL
- `SURL` - Shorten URL from ans
- `SGC` - Select git commit
- `UNCOMMIT` - Git reset soft HEAD^ (undo last commit)
- `REATTACH_MASTER` - Reattach from reflog to master
- `PULL` / `PUL` / `GPL` - Git pull
- `GITIGNORE` / `GITIGN` / `IGN` / `IGNORE` / `GIG` - Write default .gitignore
- `ZG` - Install and run lazygit

#### Diff Operations
- `DUNKA` - Diff ans with dunk
- `DUNKP` - Diff ans vs clipboard with dunk  
- `PDUNK` - Diff clipboard vs ans with dunk

### 15. Navigation History

#### History Navigation
- `N` / `NN` / `NEXT` - Next in history
- `P` / `PP` / `PREV` - Previous in history

#### Level Management  
- `LVL` / `LV` / `L` / `LEVEL` - Show/manage level

### 16. Package Management

#### Pip Operations
- `PIF` / `PIP freeze` - List installed packages
- `SHOGA` - Shotgun install ans (pip install multiple, aggressive)
- `PIMA` - Pip install multiple ans (conservative)
- `PIRA` - Pip install from requirements file ans
- `PIR` / `PIP install -r requirements.txt` - Install from requirements.txt
- `UP` / `UPDATE` - Update packages
- `UPWA` - Update r.py with confirmation
- `UPYE` / `PIP install rp --upgrade --no-cache` - Upgrade RP package

### 17. File Compression & Archives

#### Archive Operations  
- `UZA` - Unzip ans to folder with progress
- `ZIH` - Make zip file from current directory
- `ZIA` - Make zip file from ans directory

### 18. Data Manipulation & Analysis

#### String Operations
- `strip` / `sp` - Strip whitespace from ans
- `LJ` / `LINE JOIN ANS` - Join lines in ans
- `AJ` / `JA` / `JEA` / `JSON ANS` - Convert ans to/from JSON
- `LJEA` - Line join each element in ans
- `CJ` - Split/join by comma
- `SJ` / `SPAJ` - Split/join by space

#### Data Processing
- `LEA` / `EVLA` - Evaluate each element in ans as expression
- `FN` - Get function names from ans
- `SHA` - Get SHA256 hash of ans with progress

#### Variable Operations
- `VARS` / `VS` - Show all variables
- `VSS` / `VSM` - Select variables with fzf
- `VSR` - Repr all user variables
- `CVSR` / `COVSR` / `CVS` - Copy variable repr to clipboard
- `DR` - Display dir() results in columns

### 19. Code Formatting & Refactoring

#### Code Formatters
- `BLA` - Format Python code with Black
- `FLY` - Refactor with flynt (f-strings)
- `ATC` - Add trailing commas
- `23P` - Convert Python 2 to 3
- `PUP` - Refactor with pyupgrade
- `SIM` - Sort imports with isort
- `CIM` - Clean imports with unimport
- `QIM` - Qualify imports (removestar with qualify)
- `RMS` - Remove star imports (removestar)
- `SW` - Strip trailing whitespace
- `PWS` - Propagate whitespace
- `SPC` - Strip Python comments
- `SDO` - Strip Python docstrings
- `D0L` - Delete empty lines
- `UND` - Unindent code
- `IND` - Indent code
- `RFS` / `RMFS` - Remove f-strings

#### Clipboard Code Formatting
- `CBP` - Format clipboard Python with Black
- `CSP` - Sort clipboard imports with isort

### 20. Network & Web Operations  

#### URL Operations
- `UR` / `UUR` / `UURL` - Unshorten URL from ans
- `GOO` - Open Google search for ans
- `GOOP` - Open Google search for clipboard
- `WGA` - Wget ans and set ans to filename

#### Web Sharing
- `FCA` - Web copy path ans with progress
- `FCH` - Web copy current directory with progress  
- `SG` - Save ans as gist
- `LG` - Load gist from URL prompt
- `LGA` - Load gist from ans URL  
- `OG` - Select and load from old gists
- `OGM` - Select from RP gists
- `RWC` - Web copy RP source code

#### HTTP Server
- `HTTP` / `HTP` - Start HTTP server on current directory
- `HOSTLAB` - Host Jupyter Lab with public access

### 21. File Analysis & Content

#### File Content Analysis
- `WANS` / `WA` - Write ans to file
- `WANS+` / `WAP` - Append ans to file
- `NB` - Extract code from Jupyter notebook
- `NBA` - Extract code from notebook ans
- `NBC` - Clear Jupyter notebook outputs  
- `NBCA` - Clear notebook ans outputs
- `NBCH` - Clear all notebooks in directory
- `NBCHY` - Clear all notebooks (auto-yes)
- `NBCHYF` - Clear all notebooks (fast, parallel)
- `NCA` - Clear notebook ans outputs

#### File Size & Statistics
- `NL` - Show number of lines in ans
- `DUSHA` - Show human readable size of ans files  
- `DUSH` - Show disk usage (du -sh)

### 22. Advanced System Operations

#### Process Management
- `RETK` - Kill current process forcefully
- `INM` - Set __name__ to "__main__"

#### Terminal Operations  
- `RST` / `RS` - Reset terminal
- `CLS` / `CLEAR` - Clear screen
- `PTS` / `ptsave` - Save terminal state
- `ST` / `STIT` / `settitle` - Set terminal title
- `ATS` - Get tmux scrollback

#### Tmux Operations
- `TMD` / `!tmux d` - Tmux detach
- `TMA` / `!tmux a` - Tmux attach  
- `TM` / `TMUX` / `!tmux` - Start tmux
- `TMDA` - Detach all users from all tmux sessions

### 23. Interactive Selection

#### Selection Commands
- `INS` / `ISA` - Input select from ans
- `ISM` / `IMA` / `IMS` - Input select multiple from ans
- `FZM` - Multi-select from ans with fzf

#### Environment & System Selection
- `ISENV` / `ENV` - Select from environment variables  
- `ENP` / `ENVP` - Select from PATH-like env vars with preview
- `WHI` / `WHICH` - Select from which results for all commands
- `GSC` / `SCO` - Select from system commands

### 24. Development Tools

#### AI Code Tools
- `CCA` - Run Claude Code on ans
- `CCH` - Run Claude Code on current directory
- `GEM` - Run Gemini CLI on current directory
- `GEMA` - Run Gemini CLI on ans

#### Module & Import Tools
- `IASM` - Import all submodules of ans verbosely
- `EMA` - Explore PyTorch module ans
- `IPYK` - Add IPython kernel
- `DAPI` - Display all PyPI info

#### Jupyter & Notebooks
- `JL` / `PYM jupyter lab` - Start Jupyter Lab
- `NB` - Extract code from Jupyter notebook

### 25. File System Utilities

#### File Browser & Utilities
- `FB` - Run file browser
- `FMA` / `MDA` - View markdown file ans in terminal

#### Search & Replace  
- `FART` / `AFART` - Find and replace text in current directory
- `FARTA` / `AFARTA` - Find and replace text in paths from ans

#### Cloud Storage
- `RCLAH` - RClone copy ans to current directory (with checksums)
- `RCLAHF` - RClone copy ans to current directory (fast, no checksums)

### 26. Miscellaneous Utilities

#### Text Utilities
- `PAF` - Parse clipboard as file list (for macOS multi-file copy)

#### Display & UI  
- `FON` / `fansion` - Turn on ANSI colors
- `FOF` / `FOFF` / `fansioff` - Turn off ANSI colors

#### PowerPoint  
- `PPT` - Convert PowerPoint file (select with prompt)
- `PPTA` - Convert PowerPoint file ans

#### Configuration
- `RRC` / `RR` / `ryanrprc` - Load Ryan's RP config
- `RTC` / `RT` / `ryantmuxrc` - Load Ryan's tmux config  
- `RVC` / `ryanvimrc` - Load Ryan's vim config
- `RXC` / `RX` / `ryanxonshrc` - Load Ryan's xonsh config
- `RRY` / `RYAN RPRC YES` - Set RP config with confirmation
- `RVY` / `RYAN VIMRC YES` - Set vim config with confirmation
- `RVN` / `RYAN VIMRC NO` - Reject vim config  
- `RRNG` / `RYAN RANGERRC` - Load ranger config
- `RZG` - Load lazygit config

#### Undo/Redo System
- `UNDO` / `REDO` - Undo/redo operations
- `UNDO OFF` / `UOF` - Disable snapshots
- `UNDO ON` / `UON` - Enable snapshots  
- `UNDO ALL` - Show all snapshots

## Implementation Details

### Command Expansion Process
1. Input is checked against shortcuts dictionary built from `command_shortcuts_string`
2. Each line format: `SHORTCUT TARGET_COMMAND`
3. `$r.function_name()` calls are expanded to `__import__('rp').r.function_name()`
4. `$PY` is replaced with current Python executable path
5. Special variables like `ans`, `$string_from_clipboard()` are evaluated

### Special Command Processing
Commands like `CD`, `CDU`, `CDH`, `VIM`, `CAT`, `LS*`, `WANS` get dedicated processing logic in the main pseudo_terminal loop rather than simple expansion.

### Microcompletions Integration  
Space key triggers microcompletions that can expand shortcuts:
- `autocaps` list in key_bindings.py defines commands that auto-capitalize
- `shortcuts` dictionary provides prefix expansions like `u` → `CDU`
- Integration with `kibble_shortcuts` from rprc files for custom shortcuts

### Custom Extensions
- `_add_pterm_prefix_shortcut(shortcut, replacement)` - Add custom prefix shortcuts
- `_add_pterm_command_shortcuts(shortcuts_string)` - Add bulk command shortcuts
- `additional_command_shortcuts` list in r_iterm_comm.py for runtime additions

## Code Locations
- **Main processing**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:pseudo_terminal()` ~line 19500
- **Shortcuts definition**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:command_shortcuts_string` ~line 20188
- **Microcompletions**: `/opt/homebrew/lib/python3.10/site-packages/rp/rp_ptpython/key_bindings.py:handle_character()` ~line 2800
- **Command processing**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py` various elif blocks ~line 21000+