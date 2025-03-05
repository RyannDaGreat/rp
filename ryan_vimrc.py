"   - vim should boot super duper fast
"   - vim should run super duper fast
"   - should have many convenience shortcuts
"       - ALL the important ones should be listed under SHORTCUTS, so we can swap out one plugin for another if we want to
"   - the SHORTCUTS section is basically a specification
"   - It's ok to have duplicate shortcuts, as long as they're for things you use very often and the shortcuts are on different parts of the keyboard.
"       - Though redundant, duplicate shortcuts can make editing faster by letting you move your hands less on they keybord - opting for the closest shortcut to your fingers at a given time. Often I've found this is useful in practice, especially for exiting vim etc.

"SHORTCUTS
" ; is :
" gcc comments out lines
" K shows documentation for variable (python)
" \g goes to definition (python)
" \r renames a variable under cursor (python)
" \u finds all usages of variable under cursor (Python)
" F3 Toggles relative number
" F4 toggles the minimap
" F5 toggles NERDTree " F6 toggles indent guidelines " F7 toggles line wrapping
" F8 toggles a global vim session (saves the layout like tabs and splits etc)
" F8F8 just saves the current vim session globally, instead of loading
" \ff triggers a search for text inside files, like sublime's ctrl+shift+f
" \[space], while in Quickfix, previews a result
" gs  is an interactive alternative to g< and g>. When in interactive argument swap mode try moving arguments with hjkl, g, G, r, s
" \ctrl+p will fuzzy-search most recent files
" tq        closes the current tab
" td or ts  duplicates (aka splits) the current tab
" tq        is an alias for :quit
" <esc>q    is also an alias for :quit
" ctrl+h, ctrl+j, ctrl+k, ctrl+l: This will drag the current line, character or selection's text up, down, left or right
" gc toggles comments. gcc toggles comment on line. gc4k toggles comments four lines up. gc in visual mode toggles comments in selection. Etc
" fh cycles between different syntax color schemes
" ctrl+wz  toggles the zoom of a window, like in tmux
" alt+w  is equivalent to control+w (alt+w is esc followed by w). This is useful when using vim in a web browser (where control+w would close the tab)

"Multicursor Plugin Stuff " ctrl+down, ctrl+up adds a second cursor above or below
    " shift+right, shift+left selects one character to the right or the left
    " control+leftclick places a new cursor where you clicked (multi-cursor plugin)
    " \\\ will place a multicursor where your vim cursor is (move vim cursors with arrow keys, move multicursors with hjkl)
    " While there are multiple cursors:
    "     M           turns on multiline mode (by default, multiple cursor selection regions are limited to one line per cursor. This allows multi-line selections per cursor)
    "     \\a         inserts spaces to 'align' all cursors to the same position. Similar to \ac followed by \al in rp's microcompletions
    "     \\n and \\N inserts a number on every cursor, so you can write 1,2,3,4,5 etc very fast. The only difference between \n and \N is the side of the cursor the numbers are placed.
    "     tab         toggles multi-cursor's visal mode. toggles whether you're selecting text or just moving cursors
    "     [  and  ]   moves the terminal's cursor to the next or previous multicurors. Useful when your multi-cursors are beyond your current view, and you want to see all of them.

" Use the middle mouse button to make box selections

"Vim motions specific to python:
"  * Allows for viM (select entire def) etc
"  * https://github.com/jeetsukumaran/vim-pythonsense
"     vaf selects a python function
"     vif selects a python function's body
"     vac selects a python class
"     vic selects a python class's body
"     ]m  moves to the next python function
"     [m  moves to the previous python function
"  * python.vim:
"     ]k  moves up   to the previous line with the same indent
"     ]j  moves down to the next     line with the same indent
"  * https://github.com/michaeljsmith/vim-indent-object
"     vii selects the inner body of the current code block (vim in indent)
"     vai selects the entire code block


"Vanilla Tips/Tricks/Shortcuts I like to remember:
" :tab split      Duplicates a tab
" \c   when added to the end of a search query in vim, makes the query case-insensitive
" o    when in visual mode, this will swap which side of the selection your cursor is on
" gv   reselects your last visual-mode selection. Useful for repeating > and < from visual mode
" ^x^f when in insert mode, will autocomplete file paths (^x is for selecting a type of autocompletion, ^f is for files)
" ^v   starts visual block mode. Then, use I to insert text.
" :only   closes all other windows in the current tab

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Allow backspace to delete over everything in insert mode, solving the issue where
" backspace only deletes characters typed in the current insert mode session on macOS
set backspace=indent,eol,start


set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim' " This is the program that downloads all of our plugins...

Plugin 'tpope/vim-obsession' " Automatically saves vim sessions, such as the pane and tab layouts etc before closing vim so you can restore your layouts
nnoremap <F8>     :source ~/.Session.vim<CR>:Obsession ~/.Session.vim<CR>
nnoremap <F8><F8> :Obsession ~/.Session.vim<CR>

nnoremap td :tab split<cr>
nnoremap tn :tabnew<cr>
nnoremap ts :tab split<cr>
nnoremap tc :tab close<cr>
nnoremap \co gg"+yG<c-o>zz
nnoremap <esc>w <c-w>

Plugin 'machakann/vim-swap' "Allows us to swap the arguments of functions and definitions with g< and g> and gs. See https://github.com/machakann/vim-swap

" Failed attempt to get control+up and control+down to work in tmux
" noremap <esc>[1;5A <c-up>
" noremap <esc>[1;5B <c-down>

""Open jupyter notebooks in vim. Needs 'pip install jupytext'
"Plugin 'goerz/jupytext.vim'

"This is an alternative plugin for editing .ipynb files...
" Note: pip install notedown
" Plugin 'szymonmaszke/vimpyter'

" What does this do? Does it work? TODO find out
Plugin 'gmarik/sudo-gui.vim'


" In visual mode, allow < and > to indent multiple times without having to manually reselect the text
vnoremap < <gv
vnoremap > >gv

"Below is a lighter-weight alternative to csv.vim, that activates when opening a file that has .csv or .tsv syntax, but not the .csv or .tsv file extension
" NOTE: While csv.vim is installed, rainbow_csv will be invisible.
Plugin 'mechatroner/rainbow_csv' " Syntax highlighting for .csv and .tsv files. When displaying .tsv or .csv files, highlight each column in a different color

"https://github.com/mg979/vim-visual-multi
let g:VM_mouse_mappings = 1
Plugin 'mg979/vim-visual-multi' "Multiple cursors
"    - select words with Ctrl-N (like Ctrl-d in Sublime Text/VS Code)
"    - create cursors vertically with Ctrl-Down/Ctrl-Up
"    - select one character at a time with Shift-Arrows

""ctrl+p will search for files
Plugin 'kien/ctrlp.vim'
let g:ctrlp_show_hidden = 1

"Fuzzy search recent files - lol its freaking useless, it doesnt sort based on match
"nnoremap <leader><C-p> :CtrlPMRU<CR>



" Better javascript syntax highlighting
Plugin 'pangloss/vim-javascript'


"fzf requires an external program to be installed
"Plugin 'junegunn/fzf.vim' "To quickly search for files..
""ctrl+p will search for files
"" nnoremap <C-p> :<C-u>FZF<CR>
"" Mapping selecting mappings
"nmap <leader><tab> <plug>(fzf-maps-n)
"xmap <leader><tab> <plug>(fzf-maps-x)
"omap <leader><tab> <plug>(fzf-maps-o)
"" Insert mode completion
"imap <c-x><c-k> <plug>(fzf-complete-word)
"imap <c-x><c-f> <plug>(fzf-complete-path)
"imap <c-x><c-l> <plug>(fzf-complete-line)

" let g:indentLine_color_gui = '#000000'
" let g:indentLine_setColors = 0

" I COULDN'T GET THIS TO WORK. I HAVE A NEW SOLUTION ON THE BOTTOM.
" Plugin 'gsiano/vmux-clipboard' " Allows us to synchronize yanks between separate VIM processes (useful in TMUX for example)
" let mapleader = ","
" map <silent> <leader>y :WriteToVmuxClipboard<cr>
" map <silent> <leader>p :ReadFromVmuxClipboard<cr>
" map <silent> y :WriteToVmuxClipboard<cr>
" map <silent> p :ReadFromVmuxClipboard<cr>

Plugin 'ronakg/quickr-preview.vim' " When in a Quickfix window (aka the search result preview window, like you'd see if using \u or \ff), let us use \[space] to preview a result in multiple lines

"Plugin 'severin-lemaignan/vim-minimap' " Adds a minimap to vim. Can be seen by pressing 'F4'
" Plugin 'wfxr/code-minimap'
" Plugin 'wfxr/minimap.vim'

"My own version of wfxr/minimap.vim - only needs RP to run
Plugin 'RyannDaGreat/minimap.vim'
:hi minimapRange ctermbg=black
:hi minimapCursor ctermbg=blue ctermfg=cyan



" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo



Plugin 'nathanaelkane/vim-indent-guides'

" Plugin 'christoomey/vim-system-copy' "This doesn't seem to work...


Plugin 'scrooloose/nerdtree' "File explorer. Get it by pressing F5
Plugin 'jistr/vim-nerdtree-tabs' "Make NERDTree persist across different tabs

" Plugin 'tpope/vim-commentary' "Allows commenting out code with 'gcc' etc
Plugin 'tomtom/tcomment_vim' " JS in HTML isn't commented right with tpope's. This is hopefully more powerful. https://github.com/tpope/vim-commentary/issues/60
"Shortcut to comment out functions in python without commenting whitespace below them...
nmap gcd vifokgc

Plugin 'mhinz/vim-startify' "Shows the startup menu
" Plugin 'dkprice/vim-easygrep' "Currently disabled until I figure out a good way to use it
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub

" Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.

" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" https://github.com/mgedmin/taghelper.vim
Plugin 'mgedmin/taghelper.vim'
" set statusline=%<%f\ %h%m%r\ %1*%{taghelper#curtag()}%*%=%-14.(%l,%c%V%)\ %P
"
" set statusline=%<%f\ %h%m%r\ %{taghelper#curtag()}%*%=%-14.(%l,%c%V%)\ %P
" Only file NAME, not path:
" set statusline=%<%t\ %h%m%r\ %{taghelper#curtag()}%*%=%-14.(%l,%c%V%)\ %P
" Attempt to center the taghelper
set statusline=%<%t\ %h%m%r%=\ %{taghelper#curtag()}\ %=%-14.(%l,%c%V%)\ %P



"Shows the number of lines we're selecting in visual mode on the bottom right of the screen
"If we're selecting from a single row, shows the num charactes
"If we're selecting multiple lines, shows the number of lines
:set showcmd

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
"
"
"
"
"

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

set undofile "Persistent undo
set mouse=a
set nu
set paste
set cursorline

"Highlight all search results
set hlsearch

" noremap : ;
noremap ; :

" map [1;5A <C-Up>
" map [1;5B <C-Down>
" map [1;2D <S-Left>
" map [1;2C <S-Right>
" cmap [1;2D <S-Left>
" cmap [1;2C <S-Right>

set smartindent
set tabstop=4
set shiftwidth=4
set expandtab

" Better search highlight color: blue
    "hi Search ctermfg=NONE  ctermbg=blue
    hi Search ctermfg=white  ctermbg=blue

" Some styling; the vertical separators are ugly as hecklestein
    nmap <C-C> cp
" NOTE: To see all available colors, use :help cterm-colors
    set fillchars+=vert:\|
    set fillchars+=vert:▎
"set fillchars+=vert:\
" set fillchars+=vert:⁞
    hi VertSplit ctermbg=black ctermfg=darkgray
    hi VertSplit ctermbg=darkcyan ctermfg=black
    hi LineNr ctermfg=darkcyan
    hi LineNr ctermfg=gray
    hi LineNr ctermfg=darkgray
    hi LineNr ctermbg=black
    hi CursorLineNR cterm=bold ctermfg=lightcyan

" function ToggleWrap()
"  if (&wrap == 1)
"    set nowrap
"  else
"    set wrap
"  endif
" endfunction
" map <F7> :call ToggleWrap()<CR>
" map! <F9> ^[:call ToggleWrap()<CR>


"let us toggle paste mode with the shortcut key:
    " set pastetoggle=<F2>
    set list "Initially, we're not in list mode, so we <F3
    nmap <F9> : set list! <CR> : hi ryan_tabs ctermfg=DarkGray <CR> : match ryan_tabs /\t/ <CR>
" Let us see tabs and spaces when we're NOT in paste mode...
    " The | at the end is so if this vimrc is formatted with stripping whitespace off all strings we still have spaces at the end of them. | in vim is like ; in python, making multiline commands in one line
    let &showbreak='↪ '
    let &listchars='tab:▸ '
    
    "Initial highlighting for the ▸ and · displayed over whitespace
    hi clear SpecialKey
    hi SpecialKey ctermfg=darkgray
    hi ryan_tabs ctermfg=darkgray
    :match ryan_tabs /\t/



" Function to toggle space visualization in listchars
" https://chat.openai.com/share/f125f059-9cf1-4f42-a076-bbc69d4ba988
function! ToggleSpaceVisualization()
    if &list && match(&listchars, 'space:·') >= 0
        "Delete 'space:·' from listchars
        :let &listchars = substitute(&listchars, ',space:·', '', '')
        " Basically does this - :let &listchars = 'tab:▸ '
    else
        "Add 'space:·' to listchars
        " Basically does this - :let &listchars = 'space:·,tab:▸ '
        :let l:other_listchars = substitute(&listchars, 'space:[^,]*', '', '')
        :let &listchars = l:other_listchars . (l:other_listchars[-1:] == ',' ? '' : ',') . 'space:·'
    endif
endfunction


" Toggle relative line number
    nmap <F3> : set invrelativenumber <CR>

" Toggle NERDTree
    nmap <F5> : NERDTreeTabsToggle <CR>
    " nmap <F5> : NERDTreeToggle <CR>


"Tons of vim color schemes
Plugin 'dracula/vim'
Plugin 'franbach/miramare'
Plugin 'ghifarit53/tokyonight-vim'
"Plugin 'sickill/vim-monokai'
"Plugin 'noah/vim256-color' " 256-color schemes for vim
Plugin 'RyannDaGreat/vim-wombat256mod'
Plugin 'kyoz/purify' ", { 'rtp': 'vim' }
"Plugin 'NLKNguyen/papercolor-theme'
Plugin 'boschni/vim-sublime256'

function! Fansi()
    " Color schemes are disabled because it lags over SSH. Probably because it uses more bandwidth for 256 colors?
    "      See https://github.com/noah/vim256-color/tree/master/colors
    "     Use: Type ':color t\' and you'll see a list of themes to choose from
    "      NOTE: The default color theme is set torwards the bottom of the .vimrc file, in a function that's run after loading vim
    
    " set termguicolors "For RLAB. I'm basically always using truecolor terminals nowadays...
    
    " highlight Normal ctermfg=grey ctermbg=240
    
    set t_Co=256 "Enable 256 colors in vim
    
    if !exists("g:colors_name")
        
        colorscheme wombat256mod
    elseif g:colors_name=='wombat256mod'
        
        colorscheme        dracula
    elseif g:colors_name=='dracula'
        
        " colorscheme        distinguished
    " elseif g:colors_name=='distinguished'
    
    "     colorscheme        hybrid
    " elseif g:colors_name=='hybrid'
    
    "     colorscheme        jellybeans
    " elseif g:colors_name=='jellybeans'
    
    "     colorscheme        darcula
    " elseif g:colors_name=='Darcula'
        
        colorscheme        miramare
    elseif g:colors_name=='miramare'
        
        colorscheme        sublime256
    elseif g:colors_name=='sublime256'
    
    "Sublime256 is a better version of this
    "     colorscheme        monokai
    " elseif g:colors_name=='monokai'
        
        colorscheme        tokyonight
    elseif g:colors_name=='tokyonight'
    
    "Kinda ugly lol
    "     colorscheme        PaperColor
    " elseif g:colors_name=='PaperColor'
    
    "     colorscheme        flattown
    " elseif g:colors_name=='flattown'
    
    "     colorscheme        apprentice
    " elseif g:colors_name=='apprentice'
    
    "     colorscheme        badwolf
    " elseif g:colors_name=='badwolf'
    
    "     colorscheme        molokai
    " elseif g:colors_name=='molokai'
    
    "     colorscheme        vilight
    " elseif g:colors_name=='vilight'
    
    "     colorscheme        babymate256
    " elseif g:colors_name=='babymate256'
    
    "     colorscheme        codeschool
    " elseif g:colors_name=='codeschool'
        
        colorscheme        wombat256mod_grb
    elseif g:colors_name=='wombat256mod_grb'
        
        colorscheme        wombat256mod_rbg
    elseif g:colors_name=='wombat256mod_rbg'
        
        colorscheme        wombat256mod_brg
    elseif g:colors_name=='wombat256mod_brg'
        
        colorscheme        wombat256mod_bgr
    elseif g:colors_name=='wombat256mod_bgr'
        
        colorscheme        wombat256mod_gbr
    elseif g:colors_name=='wombat256mod_gbr'
    
    "    colorscheme        default
    "elseif g:colors_name=='default'
        
        colorscheme        wombat256mod
    else
        colorscheme        wombat256mod
    
    endif
    
    
    call RyanHighlightDefaults()
    
    "Display the color
    echo g:colors_name


endfunction

function RyanHighlightDefaults()
    " call SetDefaultTabbarTheme()
    :hi TabLineFill ctermfg=255 ctermbg=238 cterm=NONE guifg=#eeeeee guibg=#444444
    :hi XTFill      ctermbg=233 cterm=bold guibg=#121212
    :hi XTFill      ctermbg=235
    
    "SET BACKGROUND BRIGHTNESS:
    " highlight Normal ctermbg=233
    :highlight Normal ctermbg=234 guibg=#1c1c1c
    
    :highlight Identifier     ctermfg=170 guifg=#d75fd7
    " highlight Structure     ctermfg=221  "Like map, set, but not print
    
    "Highlighting for the ▸ and · displayed over whitespace
    :hi clear SpecialKey
    :hi SpecialKey ctermfg=darkgray
    :hi SpecialKey ctermfg=237
    
    "highlight ryan_tabs   ctermfg=236 ctermbg=234
    "highlight ryan_spaces ctermfg=236 ctermbg=234
    :highlight ryan_tabs   ctermfg=238 guifg=#262626 ctermbg=none
    :highlight ryan_spaces ctermfg=235 guifg=#262626 ctermbg=none
    
    "UPDATE GITGUTTER COLORS: https://github.com/airblade/vim-gitgutter/issues/614
    :highlight DiffAdd guifg=#000000 guibg=#f5deb3 ctermfg=16 ctermbg=223
    :highlight DiffChange guifg=#000000 guibg=#87cefa ctermfg=16 ctermbg=117
    :highlight DiffDelete guifg=#000000 guibg=#8a8a8a ctermfg=16 ctermbg=245
    let g:gitgutter_override_sign_column_highlight = 0
    :highlight GitGutterAdd          guifg=#009900 ctermfg=2   cterm=bold ctermbg=232 guibg=#080808
    :highlight GitGutterChange       guifg=#bbbb00 ctermfg=3   cterm=bold ctermbg=232 guibg=#080808
    :highlight GitGutterDelete       guifg=#ff2222 ctermfg=9   cterm=bold ctermbg=232 guibg=#080808
    :highlight GitGutterChangeDelete guifg=#ff8000 ctermfg=208 cterm=bold ctermbg=232 guibg=#080808
    :highlight GutterMarks           guifg=#F07fff ctermfg=2 cterm=bold ctermbg=232 guibg=#080808
    :highlight PudbBreakpointSign    ctermfg=red cterm=bold ctermbg=232 guibg=#080808
    
    " call RyanGitGutterHighlights()
    :highlight ALEErrorSign ctermfg=199 cterm=bold ctermbg=232 guifg=#ff0087 guibg=#080808
    
    :highlight clear SignColumn
    :highlight SignColumn ctermbg=232 guibg=#080808
    :highlight LineNr     ctermbg=232 ctermfg=240 guibg=#080808 guifg=#585858
    " :highlight CursorLineNr ctermbg = 240
    :highlight cursorline ctermbg=236 guibg=#303030
    :highlight FoldColumn ctermbg=232 ctermfg=103 guibg=#080808 guifg=#8787af
    :highlight Folded     ctermbg=232 ctermfg=103 guibg=#080808 guifg=#8787af
    " highlight FoldColumn             ctermfg=60
    " highlight Folded                 ctermfg=60
    
    :highlight StatusLine term=bold,reverse ctermfg=230 ctermbg=238 gui=italic guifg=#ffffd7 guibg=#444444
    :highlight StatusLineNC   term=reverse ctermfg=241 ctermbg=238 guifg=#626262 guibg=#444444
    :highlight StatusLineNC   ctermbg=236 ctermfg=239 guibg=#303030 guifg=#4e4e4e cterm=underline
    
    :hi VertSplit ctermbg=232  ctermfg=238  cterm=none guibg=#080808 guifg=#444444
    
    "For ↪
    :hi clear NonText
    :hi NonText ctermfg=240
    
    :hi minimapRange ctermbg=237
    :hi minimapCursor ctermbg=61 ctermfg=228
    
    " highlight Called ctermfg=228 guifg=#FF00FF
    " " syntax match Called "\w*("
    " syntax match Called "\w\+\ze("
    
    :highlight SignColumn ctermbg=232 guibg=#080808
    
    "For 'blueyed/vim-diminactive'
    :hi ColorColumn ctermbg=233 guibg=#121212
    let g:diminactive_use_colorcolumn = 1
    let g:diminactive_use_syntax = 1
    let g:diminactive_filetype_blacklist = ['startify']
    let g:diminactive_buftype_blacklist = ['nofile', 'nowrite', 'acwrite', 'quickfix', 'help']
    let g:diminactive_buftype_blacklist = []
    let g:diminactive_filetype_blacklist = []
    
    :silent! DimInactive
    :silent! DimInactiveSyntaxOff
    
    "Below the text, at the ~ ~ ~ ~'s
    :hi EndOfBuffer ctermbg=0
    :hi EndOfBuffer ctermbg=16 ctermfg=236
    
    
    "MY MANUAL REGEX'S
    :highlight Parenthesis ctermfg=176 guifg=#FF00FF
    :syntax match Parenthesis "[()]"
    
    :highlight Brackets ctermfg=176 guifg=#FF00FF
    :syntax match Brackets "[\[\]{}()]"

    :syntax match Statement "[-=+*/&@<>\|~%^]"

    "FORMAT OPTIONS:
    " cterm=bold
    " cterm=underline
    " cterm=italic
    " cterm=reverse
    " cterm=none

    "Call this function to see what higlight group the cursor is on so you can highlight it manually
    "Good for debugging: https://stackoverflow.com/questions/9464844/how-to-get-group-name-of-highlighting-under-cursor-in-vim
    function! SynGroup()
        let l:s = synID(line('.'), col('.'), 1)
        echo synIDattr(l:s, 'name') . ' -> ' . synIDattr(synIDtrans(l:s), 'name')
    endfun

    " Indentline ▏characters are in the Conceal group
    :hi clear Conceal
    :hi Conceal ctermfg=237

    :hi DiffAdd ctermfg=111 ctermbg=236 cterm=reverse
    :hi DiffChange ctermfg=188 ctermbg=236 cterm=reverse
    :hi DiffDelete ctermfg=222 ctermbg=236 cterm=reverse
    :hi DiffText ctermfg=145 ctermbg=236 cterm=reverse

endfunction

" fh = Fansi Highlight
nnoremap fh :call<space>Fansi()<cr>:colorscheme<cr>


" Instead of having to type :q! have vim ask us 'Would you like to save? Yes or no'
set confirm

" Python JEDI plugin commands (from their git page)
" Look at the below to learn how to effectively use the JEDI plugin!
" \g goes to definition
" \r is to rename a variable
" \n shows all usages of a given variable
" control+space triggers intelligent autocompletion
" K shows documentation for a python function/class/module. Just like regular vim.
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>u"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>rn"

" This is can be laggy and can pop up unexpectedly. Fuck it - I don't need them. Just use rp.
let g:jedi#completions_enabled = 0

"I'm not sure what the next 3 do, so for now I'll comment them out...
" let g:jedi#goto_stubs_command = "<leader>s"
" let g:jedi#goto_command = "<leader>d"
" let g:jedi#goto_definitions_command = ""

" Save us from some lag and don't automatically show python function signatures; leave that for when we're using rp
let g:jedi#show_call_signatures = 0

" Disable swap files. This might be controversial, but I think .swp files might be more of a pain in the butt than they're worth...vim just never crashes...
" set noswapfile

"Enable autocompletion menu while typing vim commands (after pressing :)
"To do this, press 'tab'. For example, try :w[tab] and :write will be an option
set wildmenu

" Plugin 'chrisbra/csv.vim' " Provides an excel-like column editor for .csv files
" Plugin 'klen/python-mode' " An impressively full-featured plugin that makes vim much more like a python ide. But it's a bit too bulky for my tastes...

" This plugin allows us to visually drag text selections up and down in visual mode
" https://github.com/matze/vim-move
Plugin 'matze/vim-move'
let g:move_key_modifier = 'C'

" Let the middle mouse button do box selections, like in sublime
" Fun fact: By default, you can do box selections with quadruple-clicks...
" Source: https://stackoverflow.com/questions/33731468/how-to-assign-visual-block-selection-to-mouses-middle-button-in-vim
noremap <MiddleMouse> <4-LeftMouse>
noremap <MiddleDrag> <LeftDrag>

" Increase vim's command history size. By default it only stores the 15 most recent commands.
" https://vi.stackexchange.com/questions/2920/how-to-further-increase-cmdline-history-size
set viminfo=!,'10000,<50,s10,h,:10000


" https://github.com/mduan/python.vim
" This is complementary to vim-pythonsense
" Adds shortcuts for jumping between python blocks etc
" Plugin 'mduan/python.vim'
Plugin 'RyannDaGreat/python.vim' "I removed all ] shortcuts from it as they interfere with my own shortcuts



" Graveyard of failed attempts at fuzzy autocompletion
"      Plugin 'ycm-core/YouCompleteMe'
"      Plugin 'maralla/completor.vim'
"      https://github.com/junegunn/fzf.vim
"      Plugin 'junegunn/fzf', { 'do': { -> fzf#install() } }
"      Plugin 'junegunn/fzf.vim'
"      " https://vim.fandom.com/wiki/Fuzzy_insert_mode_completion_(using_FZF)
"      function! PInsert2(item)
"          let @z=a:item
"          norm "zp
"          call feedkeys('a')
"      endfunction
"      function! CompleteInf()
"          echo "CLBO"
"          let nl=[]
"          let l=complete_info()
"          for k in l['items']
"          call add(nl, k['word']. ' : ' .k['info'] . ' '. k['menu'] )
"          endfor
"          call fzf#vim#complete(fzf#wrap({ 'source': nl,'reducer': { lines -> split(lines[0], '\zs :')[0] },'sink':function('PInsert2')}))
"      endfunction
"      imap <c-e> <CMD>:call CompleteInf()<CR>

"MY FUNCTIONS:
    function! ExtractVariable() range
        "Written by Ryan Burgert, May 3 2024.
        "This is for extracting a variable from the visual selection in python
        "It doesn't need rope or any fancy library - its very simple!
        "Written with aid of Claude Opus (and a LOT of manual intervention lol)
        
        " Get the new variable name from the user
        let var_name = input("Enter the new variable name: ")
        
        " Save the current register contents
        let saved_reg = getreg('"')
        let saved_regtype = getregtype('"')
        
        " Yank the selected text
        normal! gvy
        
        " Delete the selected text and replace it with the variable name
        execute "normal! gv\"_c" . var_name
        
        " Create a mark at the current position
        normal! m9
        
        " Get the current indentation
        
        " Insert line above while preserving indentation
        " This is correct regardless of whether O preserves idents or not
        let indent = matchstr(getline('.'), '^\s*')
        normal! O
        normal! d0
        execute "normal! i" . indent . var_name . " = "
        
        " Paste the yanked text at the end of the line
        normal! p
        
        " Move back to the mark then delete it
        normal! `9
        delmark 9
        
        " Put cursor after variable name
        normal! $F=la
        
        " Restore the original register contents
        call setreg('"', saved_reg, saved_regtype)
    endfunction
    
    
    function! PropagateWhitespace()
        " Ryan May 3 2024
        " Great for when using indent guides!
        " Modifies whole buffer right now
        " https://chat.openai.com/share/f125f059-9cf1-4f42-a076-bbc69d4ba988
        
        " Get the current position
        let l:save_pos = getpos(".")
        
        " Start from the bottom of the file or current visual selection
        let l:start_line = line("v")
        let l:end_line = line(".")
        if l:start_line == l:end_line
            let l:start_line = 1
            let l:end_line = line("$")
        endif
        
        " Variable to keep the last non-empty line's indentation
        let l:last_indent = ''
        
        " Iterate over each line from bottom to top
        for l:num in range(l:end_line, l:start_line, -1)
            let l:line = getline(l:num)
            if l:line =~ '^\s*$'
                " Line is empty, replace its whitespace
                call setline(l:num, l:last_indent)
            else
                " Line is not empty, update the last non-empty line's indentation
                let l:last_indent = matchstr(l:line, '^\s*')
            endif
        endfor
        
        " Restore the cursor position
        call setpos('.', l:save_pos)
    endfunction
    
    function! StripWhitespace()
        " Ryan May 3 2024
        " Modifies whole buffer right now
        " https://vi.stackexchange.com/questions/454/whats-the-simplest-way-to-strip-trailing-whitespace-from-all-lines-in-a-file
        
        let l:save = winsaveview()
        keeppatterns %s/\s\+$//e
        call winrestview(l:save)
    endfunction



" Zoom / Restore window.
" FROM https://stackoverflow.com/questions/13194428/is-better-way-to-zoom-windows-in-vim-than-zoomwin
function! s:ZoomToggle() abort
    if exists('t:zoomed') && t:zoomed
        execute t:zoom_winrestcmd
        let t:zoomed = 0
    else
        let t:zoom_winrestcmd = winrestcmd()
        resize
        vertical resize
        let t:zoomed = 1
    endif
endfunction
command! ZoomToggle call s:ZoomToggle()
nnoremap <silent> <C-W>z  :ZoomToggle<CR>
nnoremap <silent> <esc>wz :ZoomToggle<CR>

syntax on

set shortmess-=S "Show the count of the search like item 5/10 etc https://stackoverflow.com/questions/4668623/show-count-of-matches-in-vim

Plugin 'simeji/winresizer' "Use control+e to resize windows

" KEY MAPPINGS:
    "Vimdiff mappings: d> and d<
        
        "Get or put diff hunks with d< and d>
        autocmd VimEnter * if &diff | execute 'nnoremap <silent> d> :if winnr() == 1 <Bar> diffput <Bar> else <Bar> diffget <Bar> endif<CR>' | endif
        autocmd VimEnter * if &diff | execute 'nnoremap <silent> d< :if winnr() == 1 <Bar> diffget <Bar> else <Bar> diffput <Bar> endif<CR>' | endif

    " Shifting lines   https://chat.openai.com/share/05160497-c34c-426f-b9f6-8cf10aec09f5
        " Normal Mode: Move current line down with Ctrl-j
        nnoremap <C-j> :m .+1<CR>==
        " Normal Mode: Move current line up with Ctrl-k
        nnoremap <C-k> :m .-2<CR>==
        " Visual Mode: Move selected lines down with Ctrl-j
        vnoremap <C-j> :m '>+1<CR>gv=gv
        " Visual Mode: Move selected lines up with Ctrl-k
        vnoremap <C-k> :m '<-2<CR>gv=gv
    
    "Shifting Tabs
        " Use gr to go to the previous tab
        nnoremap gr :tabprevious<CR>
        
        " Use gt to go to the next tab
        nnoremap gt :tabnext<CR>
        
        " Move current tab one position to the left, with wrap-around
        nnoremap gR :if tabpagenr() == 1<CR>:tabmove $<CR>:else<CR>:tabmove -1<CR>:endif<CR><CR>
        
        " Move current tab one position to the right, with wrap-around
        nnoremap gT :if tabpagenr() == tabpagenr('$')<CR>:tabmove 0<CR>:else<CR>:tabmove +1<CR>:endif<CR><CR>
    
    "Buffer switching [b and ]b
        " Use ]b to go to the next buffer
        nnoremap ]b :bnext<CR>
        
        " Use [b to go to the previous buffer
        nnoremap [b :bprevious<CR>
    
    "Minimap toggle and Statusbar toggle and tab bar toggle
        
        " Toggle the tab bar between always displaying and displaying only when there are multiple tabs using F4+t
        nnoremap <F4>t :if &showtabline == 2<CR>:set showtabline=1<CR>:else<CR>:set showtabline=2<CR>:endif<CR><CR>
        nnoremap <leader>jt :if &showtabline == 2<CR>:set showtabline=1<CR>:else<CR>:set showtabline=2<CR>:endif<CR><CR>
        
        " Toggle the status bar between always displaying and displaying only when there are multiple windows using F4+s
        nnoremap <F4>s :if &laststatus == 2<CR>:set laststatus=1<CR>:else<CR>:set laststatus=2<CR>:endif<CR><CR>
        nnoremap <leader>js :if &laststatus == 2<CR>:set laststatus=1<CR>:else<CR>:set laststatus=2<CR>:endif<CR><CR>
        
        " Toggle Minimap
        " Silent in case we trigger it inside the minimap. Don't care about that error.
        nmap       <F4> :silent! MinimapToggle <CR>
        nmap <leader>jm :silent! MinimapToggle <CR>
        
        " Toggle Gitgutter
        nmap <F4>g : GitGutterToggle <CR>
        nmap <leader>jg : GitGutterToggle <CR>

        " Gitgutter Commit Selection
        nnoremap <leader>jG :call<space>GitGutterSelectDiffBase()<CR>
        
        "Doesn't work - idk why
        " " NerdTree
        
        " nnoremap <F4>b : NERDTreeTabsToggle <CR>
        " nnoremap <leader>jb : NERDTreeTabsToggle <CR>
        
        "Linting Toggle
        map <leader>jl :ALEToggle<return>
        
        " Lines Toggle
        map <leader>jn :windo set nu!<return>


    "Disable Q, which is annoying. Why not reload?
        nnoremap Q :e<cr>

"Added Nov1 2023
    "GIT STUFF:
        "NERDTREE:
            " A plugin that lets us see which files are modified in NERDTree
            Plugin 'Xuyuanp/nerdtree-git-plugin'
            let g:NERDTreeGitStatusIndicatorMapCustom = {
                            \ 'Modified'  :'✹',
                            \ 'Staged'    :'✚',
                            \ 'Untracked' :'✭',
                            \ 'Renamed'   :'➜',
                            \ 'Unmerged'  :'═',
                            \ 'Deleted'   :'✖',
                            \ 'Dirty'     :'✗',
                            \ 'Ignored'   :'☒',
                            \ 'Clean'     :'✔︎',
                            \ 'Unknown'   :'?',
                            \ }
        "GIT GUTTER: \jg, zg, [h, ]h, \hu, \hp
            set updatetime=100 " This is the recommended update interval from airblade/gitgutter's github page. By default, it's 4 seconds.
            nmap ]h <Plug>(GitGutterNextHunk)
            nmap [h <Plug>(GitGutterPrevHunk)
            omap ih <Plug>(GitGutterTextObjectInnerPending)
            omap ah <Plug>(GitGutterTextObjectOuterPending)
            xmap ih <Plug>(GitGutterTextObjectInnerVisual)
            xmap ah <Plug>(GitGutterTextObjectOuterVisual)
            nmap <leader>hu <Plug>(GitGutterUndoHunk)
            nmap <leader>hp <Plug>(GitGutterPreviewHunk)
            " Git Gutter"
            set updatetime=250
            let g:gitgutter_max_signs = 500
            let g:gitgutter_map_keys = 0 " No mapping
            let g:gitgutter_override_sign_column_highlight = 0 " Colors
            let g:gitgutter_sign_allow_clobber = 0 " Let other plugins take priority over gutter
            let g:gitgutter_sign_priority = -10
            function RyanGitGutterHighlights()
                highlight GitGutterDelete guifg=#ff2222 ctermfg=1
                highlight GitGutterAdd    guifg=#009900 ctermfg=2
                highlight GitGutterChange guifg=#bbbb00 ctermfg=3
                highlight GitGutterChangeDelete ctermfg=4
            endfunction
            
            " Initial theme: make background black to match gutter
            highlight SignColumn            ctermbg=black
            highlight GitGutterDelete       ctermbg=black
            highlight GitGutterAdd          ctermbg=black
            highlight GitGutterChange       ctermbg=black
            highlight GitGutterChangeDelete ctermbg=black
            
            call RyanGitGutterHighlights()
            Plugin 'airblade/vim-gitgutter'
            silent! call gitgutter#disable() " Disable it by default

            "Folding with zg
            function! EnableGitGutterAndFold() abort
                GitGutterBufferEnable
                call timer_start(250, {-> execute('GitGutterFold')})
            endfunction
            nnoremap zg :call EnableGitGutterAndFold()<cr>
        
        "GITIGNORE SYTAX HIGHLIGHTING:
            Plugin 'gisphm/vim-gitignore' " Highlight .gitignore files
        
        "GIT BLAME: \gb    \gB --> p
            " Small shortcut to print blame info for current line
            Plugin 'zivyangll/git-blame.vim'
            nnoremap <Leader>gb :<C-u>call gitblame#echo()<CR>
            
            Plugin 'tpope/vim-fugitive'
            nnoremap <Leader>gB :Git blame<CR>
            " In this mode, press 'p' to preview (don't use <CR>)
    "PYTHON STUFF:
        "IMPORT SORT: ^i
            "DISABLED Because it slowed down startup (only a tiny bit - like .04 seconds)
            " if has('python3')
            "     Plugin 'fisadev/vim-isort' " You need pip install isort for this to work. Activate with control+i in visual mode, or the :ISort command
            " endif
        "MACCHIATO: ⌥l
            Plugin 'smbl64/vim-black-macchiato' "Autformat specific sections of python code using   pip install black-macchiato
            " autocmd FileType python xmap <buffer> <Esc>l <plug>(BlackMacchiatoSelection)
            autocmd FileType python nmap <buffer> <Esc>l <plug>(BlackMacchiatoCurrentLine)
            autocmd FileType python vnoremap <buffer> <Esc>l :BlackMacchiato<cr>
        "RPY FILES:
            autocmd BufRead,BufNewFile *.rpy          set filetype=python "Treat .rpy files as python files
            autocmd BufRead,BufNewFile *.rprc          set filetype=python "Treat .rprc files as python files
            autocmd BufRead,BufNewFile *ryan_vimrc.py set filetype=vim    "Treat ryan_vimrc.py as a vimrc
        "OUTLINER: \jo
            " Add an outliner for python so we can quickly jump between functions and classes
            " Works for several languages: python, latex, html, and more
            
            " Plugin 'vim-voom/VOoM' 
            Plugin 'RyannDaGreat/VOoM' " Don't spam vim errors when invalid syntax, put the error in the outliner instead

            let g:voom_syntax = 'python'
            function! VoomWithSyntax()
                "A list of all Voom-supported languages, and their filetype-to-voom-command translations
                "If we can't find it, just default to python syntax and probably show an error lol
                let syntax_map = {
                      \ 'python' : 'python',
                      \ 'tex': 'latex',
                      \ 'html' : 'html',
                      \ 'markdown' : 'markdown',
                      \ 'asciidoc' : 'asciidoc',
                      \ 'cwiki' : 'cwiki',
                      \ 'dokuwiki' : 'dokuwiki',
                      \ 'fmr' : 'fmr',
                      \ 'fmr1' : 'fmr1',
                      \ 'fmr2' : 'fmr2',
                      \ 'fmr3' : 'fmr3',
                      \ 'hashes' : 'hashes',
                      \ 'inverseAtx' : 'inverseAtx',
                      \ 'latexDtx' : 'latexDtx',
                      \ 'org' : 'org',
                      \ 'pandoc' : 'pandoc',
                      \ 'paragraphBlank' : 'paragraphBlank',
                      \ 'paragraphIndent' : 'paragraphIndent',
                      \ 'paragraphNoIndent' : 'paragraphNoIndent',
                      \ 'rest' : 'rest',
                      \ 'taskpaper' : 'taskpaper',
                      \ 'thevimoutliner' : 'thevimoutliner',
                      \ 'txt2tags' : 'txt2tags',
                      \ 'viki' : 'viki',
                      \ 'vimoutliner' : 'vimoutliner',
                      \ 'vimwiki' : 'vimwiki',
                      \ 'wiki' : 'wiki',
                  \ }

                  let g:voom_syntax = get(syntax_map, &filetype, 'python')
                  execute 'Voom ' . g:voom_syntax 
              set nonu

            endfunction

            nnoremap <leader>jo :call VoomWithSyntax()<cr>

        "JEDI: \g, K, \u, ^[space], \r
            if has('python3') "On Macs, this doesn't work. Don't spam errors.
                Plugin 'davidhalter/jedi-vim' " This adds python-specific refactoring abilities
            endif
        "LINTING: \jl, ]l, [l
            "ALE:
                "Python linting! Toggle with \jl
                "NOTE: To be useful, I need to dig into this and disable stupid errors...
                Plugin 'dense-analysis/ale'
                let g:ale_enabled=0 "Disable ale by default
                let g:ale_linters={'python':['pyflakes']} " I coudn't care less about the other linters...flake8 has pep8 in it, so screw it...just use pyflakes which is a subset of flake8
                autocmd VimEnter * nnoremap ]l :ALENextWrap<cr>
                autocmd VimEnter * nnoremap [l :ALEPreviousWrap<cr>
                " ]l and [l stand for next lint and prev lint
                let g:ale_set_highlights = 0 "Ale's in-text highlights are really bad; they're always at the beginning or end of a line and don't indicate anything important that the gutter doesn't
                " highlight clear ALEErrorSign
                " hi  ALEErrorSign ctermfg=Red
                " let g:ale_python_pyflakes_executable = 'pyflakes3' "https://vi.stackexchange.com/questions/20508/switch-pyflakes-linter-from-python2-to-python3-in-ale
                
                "One of the next two commands did the trick, where it used to put text next to the errors on the screen (which was confusing as its the same color as my code comments):
                let g:LanguageClient_useVirtualText = 0
                let g:ale_virtualtext_cursor=0
            "FLAKE8:
                " "This one isn't as good yet...might delete from my vimrc...I've had more luck with ALE: despite it's horrible defaults, it's actually pretty nice once configured
                " Plugin 'nvie/vim-flake8' "Let us analyze our python code...
                " "NOTE: To be useful, I need to dig into this and disable stupid errors...
                " autocmd FileType python nmap <buffer> <esc><F3> :call flake8#Flake8()<CR>
                " " Errors to ignore: https://stackoverflow.com/questions/59241007/flake8-disable-all-formatting-rules
                " let g:syntastic_python_flake8_args='--ignore=E101,E111,E112,E113,E114,E115,E116,E121,E122,E123,E124,E125,E126,E127,E128,E129,E131,E133,E201,E202,E203,E211,E221,E222,E223,E224,E225,E226,E227,E228,E231,E241,E242,E251,E261,E262,E265,E266,E271,E272,E273,E274,E301,E302,E303,E304,E401,E402,E501,E502,E701,E702,E703,E704,E711,E712,E713,E714,E721,E731,E901,E902,W191,W291,W292,W293,W391,W503,W601,W602,W603,W604' "This doesn't actually seem to help...
        "ROPE REFACTORING:  (commands)
            " Disabled until I figure out a way to easily install this everywhere
            " when installed, it's great! But idk how to make the installation bulletproof yet
            " if has('python3') "On Macs, this doesn't work. Don't spam errors.
            "     Plugin 'python-rope/ropevim'
            " endif
            
            "CALL THESE WITH YOUR CURSOR OVER THE APPROPRIATE PLACE:
            " :RopeExtractMethod
            " :RopeExtractVariable
            " :RopeInline
            " :RopeRename
            " :RopeChangeSignature
            "There are many others too, :Rope*
            " :RopeMethodObject  (makes a function into a __call__able class
        "MY REFACTORING: \ev
            " Extracts the visual selection to a variable
            vnoremap <leader>ev :call ExtractVariable()<CR>
    
    "EDITING:
        "SEE SPACES: \jW
            "Will show spaces as ·
            nnoremap \jW :call ToggleSpaceVisualization()<CR>
        
        "STRIP AND PROPOGATE WHITESPACE:
            command! StripWhitespace call StripWhitespace()
            command! PropagateWhitespace call PropagateWhitespace()

        "Right now it doesn't seem to work...
        ""AUTORELOAD:  :set autoread     :set noautoread
        "    Plugin 'chrisbra/vim-autoread'
        "    :set noautoread

        "AUTOREAD:
        " https://superuser.com/questions/181377/auto-reloading-a-file-in-vim-as-soon-as-it-changes-on-disk
        set autoread                                                                                                                                                                                    
        au CursorHold * checktime  
        
        "VIM SURROUND:
            " Add parenthesis or quotes around stuff
            " NORMAL:  ys<movement><bracket>
            " VISUAL:  S<bracket>
            " Example: ysiw(
            " Example: S(
            Plugin 'tpope/vim-surround'

            " Multiline strings with d and D  (d for docstring)
            " https://github.com/tpope/vim-surround/issues/213
            let b:surround_{char2nr('d')} = "'''\r'''"
            let b:surround_{char2nr('D')} = "\"\"\"\r\"\"\""
        
        "LINE WRAP: f7 \jw
            function ToggleWrap()
            if (&wrap == 1)
                if (&linebreak == 1)
                    set nolinebreak
                else
                    set nowrap
                    set breakindent! "The second time we go around, toggle whether we wrap at the far left, or at the paragraphs
                endif
             else
                set wrap
               set linebreak
             endif
            endfunction
            map <F7>       :call ToggleWrap()<CR>
            map <leader>jw :call ToggleWrap()<CR>

        " INDENTATION: \<tab><tab>   \<tab><space> \<tab>2  \<tab>4  \<tab>8
            " Disabled because it doesn't work very well - it made my vimrc use tabs, and rp have 2-spaces-indent.
            " Plugin 'tpope/vim-sleuth' "Auto-detects what indentation the file uses
            
            nnoremap <leader><tab><tab> :set noexpandtab<cr>
            nnoremap <leader><tab><space> :set expandtab<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>1 :set expandtab<cr>:set tabstop=1<cr>:set shiftwidth=1<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>2 :set expandtab<cr>:set tabstop=2<cr>:set shiftwidth=2<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>3 :set expandtab<cr>:set tabstop=3<cr>:set shiftwidth=3<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>4 :set expandtab<cr>:set tabstop=4<cr>:set shiftwidth=4<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>5 :set expandtab<cr>:set tabstop=5<cr>:set shiftwidth=5<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>6 :set expandtab<cr>:set tabstop=6<cr>:set shiftwidth=6<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>7 :set expandtab<cr>:set tabstop=7<cr>:set shiftwidth=7<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>8 :set expandtab<cr>:set tabstop=8<cr>:set shiftwidth=8<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            nnoremap <leader><tab>9 :set expandtab<cr>:set tabstop=9<cr>:set shiftwidth=9<cr>:set autoindent<cr>:set textwidth=0<cr>:set wrapmargin=0<cr>
            
            " Set default indentation by filetype
            filetype plugin indent on
            autocmd FileType python setlocal shiftwidth=4 tabstop=4 expandtab nopaste
            autocmd FileType vim    setlocal shiftwidth=4 tabstop=4 expandtab nopaste

            " " Make backspace more powerful in python. Perhaps add other languages too in the future. Backspace through indents.
            " " Disabled simply out of preference.
            " autocmd FileType python setlocal backspace=indent,eol,start

            " I want >> to indent comments that begin at the beginning of a line. After setting this, I can. Multiline strings are indented either way.
            autocmd FileType python setlocal nosmartindent

            "Make shift-tab unindent in insert mode
            inoremap <s-tab> <Esc><<gi

        " SYNTAX HIGHLIGHTING: fh \sss \ssv \ssp \ss...
           
            " " Warning: Disabled because it was slow and didn't offer enough new functionality to justify slow scrolling!
            " " PYTHON SYNTAX PLUGIN:
            "    " A bit more nuance for python syntax highlighting
            "    let g:python_version_2=0                          "Python 2 mode
            "    let b:python_version_2=0                          "Python 2 mode (buffer local)
            "    let g:python_highlight_builtins=1                 "Highlight builtin objects, types, and functions
            "    let g:python_highlight_builtin_objs=1             "Highlight builtin objects only
            "    let g:python_highlight_builtin_types=1            "Highlight builtin types only
            "    let g:python_highlight_builtin_funcs=1            "Highlight builtin functions only
            "    let g:python_highlight_builtin_funcs_kwarg=1      "Highlight builtin functions when used as kwarg
            "    let g:python_highlight_exceptions=1               "Highlight standard exceptions
            "    let g:python_highlight_string_formatting=1        "Highlight % string formatting
            "    let g:python_highlight_string_format=1            "Highlight syntax of str.format syntax
            "    let g:python_highlight_string_templates=1         "Highlight syntax of string.Template
            "    let g:python_highlight_indent_errors=1            "Highlight indentation errors
            "    let g:python_highlight_space_errors=0             "Highlight trailing spaces
            "    let g:python_highlight_doctests=1                 "Highlight doc-tests
            "    let g:python_highlight_func_calls=0               "Highlight functions calls
            "    let g:python_highlight_class_vars=1               "Highlight class variables self, cls, and mcs
            "    let g:python_highlight_operators=1                "Highlight all operators
            "    let g:python_highlight_all=1                      "Enable all highlight options above, except for previously set.
            "    let g:python_highlight_file_headers_as_comments=0 "Highlight shebang and coding headers as comments
            "    Plugin 'vim-python/python-syntax'
            
            " DOCKERFILE SYNTAX HIGHLIGHTING:
                Plugin 'ekalinin/Dockerfile.vim'
            
            " LANGUAGE SWITCHING:
                " fh - changes color theme. Already accounted for elsewhere
                nnoremap <leader>sss :set filetype=
                nnoremap <leader>ssv :set filetype=vim<cr>
                nnoremap <leader>ssj :set filetype=javascript<cr>
                nnoremap <leader>ssp :set filetype=python<cr>
                nnoremap <leader>ssc :set filetype=cpp<cr>
                nnoremap <leader>ssm :set filetype=markdown<cr>
                nnoremap <leader>ssl :set filetype=tex<cr>
                nnoremap <leader>ssh :set filetype=html<cr>
                nnoremap <leader>ssz :set filetype=zsh<cr>
                nnoremap <leader>ssb :set filetype=bash<cr>

        " INDENT LINES: f6 \ji
            "Disable by default...
            let g:indentLine_enabled = 0
            let g:indentLine_char_list = ['|', '¦', '┆', '┊']
            let g:indentLine_char_list = ['▏']
            
            "NEAR-IMPOSSIBLE TO SOLVE BUG: This interacts with
            "blueyed/vim-diminactive poorly when unfocused.
            "You can get around this by :hi conceal ctermfg=none
            "But this makes it white. You can then do :hi normal ctermfg=red
            "But that affects some text in the file...
            "By default it uses the Conceal group, but the background colors
            "aren't handled properly by blueyed/vim-diminactive so I used this
            "group instead
            "let g:indentLine_defaultGroup = 'SpecialKey'
            " Don't have them overwrite my Conceal syntax higlighting group
            " because we're not going to use it...
            " let g:indentLine_setColors = 0
            
            "Adds indent guide lines
            Plugin 'Yggdroot/indentLine'
            
            "Note: Indentline does not play nicely with DimInactive, so I disabled it
            "nmap <F6>       :windo IndentLinesToggle <CR>:silent! DimInactiveToggle<cr>
            "nmap <leader>ji :windo IndentLinesToggle <CR>:silent! DimInactiveToggle<cr>
            
            " Define a global variable to keep track of the toggle state
            let g:ToggleState = 0
            
            function! ToggleIndentDim()
              " Check the current state of the toggle
              if g:ToggleState == 0
                " If it's 0, enable indent lines and dim inactive
                :windo IndentLinesEnable
                :DimInactiveOff
                " Update the toggle state to 1
                :let g:ToggleState = 1
              else
                " If it's 1, disable indent lines and dim inactive
                :windo IndentLinesDisable
                :DimInactiveOn
                " Update the toggle state to 0
                :let g:ToggleState = 0
              endif
            endfunction
            
            " Map the toggle function to a key combination
            nmap <leader>ji :call ToggleIndentDim()<CR>
            nmap <f6> :call ToggleIndentDim()<CR>
        
        "EDITOR AESTHETICS:
            "DIM INACTIVE WINDOWS:
                " It works fine, but meh lol - its cool but I can live without it if it gets slow
                let g:diminactive_enable_focus = 1
                Plugin 'blueyed/vim-diminactive'
                "Setting ColorColumn ctermbg=none effectively disables it until we trigger fh and style changes
                :hi ColorColumn ctermbg=none
        
        "YANK REGISTERS: "
            "Peekaboo will show you the contents of the registers on the sidebar when you hit " or @ in normal mode or <CTRL-R> in insert mode. The sidebar is automatically closed on subsequent key strokes.
            "You can toggle fullscreen mode by pressing spacebar.
            Plugin 'junegunn/vim-peekaboo'

        "UNDO TREE: \ju
            " Displays an entire tree for undo/redo's
            Plugin 'mbbill/undotree'
            nnoremap <leader>ju :UndotreeToggle<CR>

        "VISUAL SELECTION:
            "SELECTION HISTORY:  [v ]v
                "Currently a bit annoying - it tracks too much history
                "I raised an issue on github for it
                let g:visual_history_create_mappings = 0
                vmap <silent> [v <Plug>(SelectPrevious)
                vmap <silent> ]v <Plug>(SelectNext)
                nmap <silent> [v <Plug>(SelectPrevious)
                nmap <silent> ]v <Plug>(SelectNext)
                Plugin 'Matt-A-Bennett/vim-visual-history'
    
    "NAVIGATION:
        "SEARCHING: * / \ff \fr
            " TIP:  add \c at the end of a search to make it case-insensitive.   /ryan\c   matches   Ryan
            " TIP:  gn  is a motion to select the current search result!    So,  cgnHello replaces the next search result with Hello
            
            " Allows us to search for text with * from visual mode
            Plugin 'bronson/vim-visual-star-search' " How was this not already a thing?

            "This is responsible for automatically jumping to /search results as you type them! 
            "It's cool but I find it kinda irritating
            " set incsearch

            "Eh doesn't work so great anymore idk
            " Plugin 'eugen0329/vim-esearch' " The vim-easysearch plugin. This plugin adds the ability to search for text in files with the \ff command

            "Find and replace
            " :Farr    -->  Just find text
            " :Far     -->  Find and replace text
            "
            "     In search box:
            "         <c-c>  exits without searching
            "         <tab>  completes with previous searches
            "
            "     In search results box:
            "         s      does the replacement
            "         u      undoes the replacement
            "
            "         q      exits searching mode
            "         <cr>   goes to that code
            "
            "         F      toggles all lines for replacement
            "         t      toggles whether to replace that line
            "         i x    on/off line for replacement respectively
            "
            "         Folds-per-file:
            "             zc zo
            "
            nnoremap <leader>ff :Farf<cr>
            nnoremap <leader>fr :Farr<cr>
            vnoremap <leader>ff :Farf<cr>
            vnoremap <leader>fr :Farr<cr>
            let g:far#enable_undo=1
            let g:far#limit=10000   "Default = 1000
            let g:far#prompt_mapping = {
                        \ 'quit'           : { 'key' : '<c-c>', 'prompt' : '^C'  },
                        \ 'regex'          : { 'key' : '<c-x>', 'prompt' : '^X'  },
                        \ 'case_sensitive' : { 'key' : '<c-a>', 'prompt' : '^A'  },
                        \ 'word'           : { 'key' : '<c-w>', 'prompt' : "^W"  },
                        \ 'substitute'     : { 'key' : '<c-f>', 'prompt' : '^F'  },
                        \ }
            Plugin 'brooth/far.vim'

        "WINDOW PANE JUMPING: -
            " When you press -, letters appear on each pane - and you press the letter of the one you want to jump to
            " These letters are not always visible in default color scheme - try 'fh' !
            Plugin 't9md/vim-choosewin'
            nmap  -  <Plug>(choosewin)
            let g:choosewin_overlay_enable = 1  " if you want to use overlay feature

        "TAB KEY:
            nnoremap <Tab> <C-w>w
            nnoremap <S-Tab> <C-w>W

        "EXITING INSERT MODE:
            "Don't trigger autoformatting
            inoremap <esc>l <c-c>ll
            
            "We already go to the left when exiting insert
            inoremap <esc>h <c-c>

        "MOTIONS: af if ac ic ]m [m g:
            " Allows for shortcuts that let you select in functions, classes, etc
            " https://github.com/jeetsukumaran/vim-pythonsense
            "
            " g:  shows you classname --> funcname --> funcname  of where you are 
            Plugin 'jeetsukumaran/vim-pythonsense'
            
            " Allows us to select entire python blocks, with vai (visualselect all indent) etc and vii (visual select in indent)
            Plugin 'michaeljsmith/vim-indent-object'
            
            "Vim motions specific to python:
            "  * Allows for viM (select entire def) etc
            "  * https://github.com/jeetsukumaran/vim-pythonsense
            "     vaf selects a python function
            "     vif selects a python function's body
            "     vac selects a python class
            "     vic selects a python class's body
            "     vad selects a python docstring
            "     vid selects a python docstring's contents
            "     ]m  [m   moves to function signatures
            "     ]M  [M   moves to function endings
            "  * https://github.com/michaeljsmith/vim-indent-object
            "     vii selects the inner body of the current code block (vim in indent)
            "     vai selects the entire code block
        "FILE HISTORY: \p
            let MRU_Max_Menu_Entries=10000 "They said it would get slow if this is a large number. Let's find out...
            Plugin 'yegappan/mru' "Let us have more than vim's default 10 recent files
            nnoremap <leader>p :MruRefresh<cr>:enew<cr>:MRU<cr>
            " autocmd BufEnter * silent! MruRefresh " Always get rid of files that no longer exist from the MRU. Clean up the temp files that no longer exist...
        
        "MARKS:   m.   m-   ]`   [`   m/     m<space>     m<bs>
            "This plugin places marks in the gutter, maing them easy to use
            "Potential Key Mappings:
            "       mx           Toggle mark 'x' and display it in the leftmost column
            "       dmx          Remove mark 'x' where x is a-zA-Z
            "
            "       m,           Place the next available mark
            "       m.           If no mark on line, place the next available mark. Otherwise, remove (first) existing mark.
            "       m-           Delete all marks from the current line
            "       m<Space>     Delete all marks from the current buffer
            "       ]`           Jump to next mark
            "       [`           Jump to prev mark
            "       ]'           Jump to start of next line containing a mark
            "       ['           Jump to start of prev line containing a mark
            "       `]           Jump by alphabetical order to next mark
            "       `[           Jump by alphabetical order to prev mark
            "       ']           Jump by alphabetical order to start of next line having a mark
            "       '[           Jump by alphabetical order to start of prev line having a mark
            "       m/           Open location list and display marks from current buffer
            "
            "       m[0-9]       Toggle the corresponding marker !@#$%^&*()
            "       m<S-[0-9]>   Remove all markers of the same type
            "       ]-           Jump to next line having a marker of the same type
            "       [-           Jump to prev line having a marker of the same type
            "       ]=           Jump to next line having a marker of any type
            "       [=           Jump to prev line having a marker of any type
            "       m?           Open location list and display markers from current buffer
            "       m<BS>        Remove all markers
            let g:SignatureMap = {
              \ 'ToggleMarkAtLine'   :  "m.",
              \ 'PurgeMarksAtLine'   :  "m-",
              \ 'GotoNextSpotByPos'  :  "]`",
              \ 'GotoPrevSpotByPos'  :  "[`",
              \ 'ListBufferMarks'    :  "m/",
              \ 'PurgeMarks'         :  "m<Space>",
              \ 'PurgeMarkers'       :  "m<BS>",
              \ }
            " let g:SignatureMarkTextHLDynamic = 1
            let g:SignaturePrioritizeMarks = 1
            let g:SignatureMarkTextHL = 'GutterMarks'
            :highlight GutterMarks  ctermfg=6 cterm=bold ctermbg=black
            Plugin 'kshenoy/vim-signature'
            " Plugin 'RyannDaGreat/vim-signature' "This takes a non-trivial time to start (not bad, but not super fast either). I don't really use marks - this plugin's purpose is to preview where marks are in the gutter.
        
        "NERDTREE VISUAL MODE:
            Plugin 'PhilRunninger/nerdtree-visual-selection' " Lets us use visual selection mode in NERDTree, then do operations such as 'T' for loading tab on all files in that selection
        
        "QUICKFIX: q
            " Map 'q' to quit the quickfix window when it is focused
            autocmd FileType qf nnoremap <buffer> q :close<CR>
        
        "HORIZONAL SCROLLING: <shift>ScrollWheel
            nnoremap <S-ScrollWheelUp> <ScrollWheelLeft>
            nnoremap <S-2-ScrollWheelUp> <2-ScrollWheelLeft>
            nnoremap <S-3-ScrollWheelUp> <3-ScrollWheelLeft>
            nnoremap <S-4-ScrollWheelUp> <4-ScrollWheelLeft>
            nnoremap <S-ScrollWheelDown> <ScrollWheelRight>
            nnoremap <S-2-ScrollWheelDown> <2-ScrollWheelRight>
            nnoremap <S-3-ScrollWheelDown> <3-ScrollWheelRight>
            nnoremap <S-4-ScrollWheelDown> <4-ScrollWheelRight>

    "PERSISTENCE:
        "Contains code for persistence when closing and opening vim
        
        "PERSISTENT CURSOR POSITION:
            """""""" The next section: Remeber the cursor position next time we open the same file
            " FROM: https://vim.fandom.com/wiki/Restore_cursor_to_file_position_in_previous_editing_session
            "               Tell vim to remember certain things when we exit
            "                '10  :  marks will be remembered for up to 10 previously edited files
            "                "100 :  will save up to 100 lines for each register
            "                :20  :  up to 20 lines of command-line history will be remembered
            "                %    :  saves and restores the buffer list
            "                n... :  where to save the viminfo files
            set viminfo='10,\"100,:20,%,n~/.viminfo
            function! ResCur()
                " color atom-dark-256
              if line("'\"") <= line("$")
                normal! g`"
                return 1
              endif
            endfunction
            augroup resCur
              autocmd!
              autocmd BufWinEnter * call ResCur()
            augroup END
    
        "PERSISTENT FOLDS EXPANDTAB ETC:
            "Make sure folds stay when opening a file again
            "I think this also restores cursor position? It might make the previous restore cursor position code here redundant
            
            "Some things it saves on a per-file basis:
            "   filetype
            "   cursor position
            "   folds

            "Originally I tried this script, and it mostly worked, but didn't always save the view properly
            "This, for example, resulted in RP loading with tab spacing etc
            "https://www.vim.org/scripts/script.php?script_id=4021
            "Plugin 'vim-scripts/restore_view.vim'

            "NOTE: You can see options saved by this in files in ~/.vim/view
            "It saves....basically everything lol hundreds of variables...
            "...it actually messed up DimInactiveView...but you can limit them with set viewoptions...
            "The subset that will be chosen by viewoptions is best found by autocompleting :set viewoptions=<tab>
            "Disable "slash" - idk what it is but it messes up diminactive
            "Disable "unix" - not important because I don't use windows+unix with the same vim lol
            "See what the viewoptions do here: https://vimdoc.sourceforge.net/htmldoc/options.html
            set viewoptions=cursor,folds,slash,unix
            set viewoptions=cursor,folds
            augroup AutoView
                autocmd!
                " Autosave & Load Views.
                autocmd BufWritePre,BufWinLeave ?* mkview 
                autocmd BufWinEnter ?* loadview
            augroup END
        
        "SESSIONS: \ss \sl \sg
            "\ss saves session in local dir and user dir (aka ~)
            "\sl loads session from local dir
            "\sg loags sessoin from user dir (aka ~)
            
            "Save Session (saves to both global and local)
            nnoremap <Leader>ss :mks! .session.vim<CR>:mks! ~/.session.vim<CR>
            
            ""Local Session Load
            "<nnoremap> <leader>sl :source .session.vim
            
            " Global variable for session file name
            let g:session_file_name = '.session.vim'
            
            " Function: LoadSession
            " Description: This function searches for a session file (defined by g:session_file_name)
            " starting from the current directory and moving up the directory tree until it reaches the root.
            " It loads the first session file found. If no such file is found in any
            " of the parent directories up to the root, it notifies the user.
            " https://chat.openai.com/share/67bb94f3-e10c-422e-86b2-55133b7ffb7d
            function! LoadSession()
                let current_dir = getcwd()
                let found_session = 0
                " Loop through parent directories to find the session file
                while current_dir != "/"
                    " Check if the session file is readable in the current directory
                    if filereadable(current_dir . '/' . g:session_file_name)
                        " Source the session file and notify the user
                        execute 'source ' . current_dir . '/' . g:session_file_name
                        echo "Loaded session from " . current_dir . '/' . g:session_file_name
                        let found_session = 1
                        break
                    endif
                    " Move to the parent directory
                    let current_dir = fnamemodify(current_dir, ':h')
                endwhile
                " Notify the user if no session file was found
                if found_session == 0
                    echo "No " . g:session_file_name . " file found in any parent directory."
                endif
            endfunction
            
            nnoremap <Leader>sl :call LoadSession()<CR>
            nnoremap <Leader>sg :call source ~/.session.vim<CR>

        "FOLDER SESSIONS: \tQQ
            "INCOMPLETE - I didn't finish making this yet
            "HALF BAKED IDEA: Sessions auto-saved when we've opened a folder and
            "closing vim via \tQQ to close all windows - which will save all session info to the folder it was orginally opened in
            "Upon opening that folder, the session will be reloaded. To do this nicely we gotta delete nerdtree windows and minimaps and vooms upon exiting
            function! CloseNonEditableWindows()
                "When saving sessions, we need to avoid glitchyness with NerdTree and
                "minimaps etc
                " Save the current window number
                let current_window = winnr()

                " Traverse all windows
                windo if &buftype == 'nofile' || &buftype == 'quickfix' || &buftype == 'help' | silent! hide | endif

                " Restore the focus to the original window
                execute current_window . 'wincmd w'
            endfunction

    "FOLDS: \jf \jF ]f [f zR zM zo zc zd zf zj zk
        "SHORTCUTS:
        " \jf  toggle fold gutter
        " zf   create new fold
        " zR   open all folds
        " zM   close all folds
        " zo   open fold
        " zc   close fold
        " zd   delete fold
        " zE   delete all folds
        " zi   temporarily toggle all folds
        " zj or ]f   jump to next fold
        " zk or [f   jump to prev fold
        
        "Don't let some other folding method stop us from deleting folds
        nnoremap zE :set foldmethod=manual<cr>zE
        nnoremap zd :set foldmethod=manual<cr>zd

        "STYLING:
            "FOLD COLUMN STYLE:
                " Set custom fold characters and vertical line
                silent! set fillchars=foldopen:▽,foldclose:△,foldsep:┇
                silent! set fillchars=foldopen:▽,foldclose:△,fold:\ ,foldsep:┆
                silent! set fillchars=foldopen:▽,foldclose:△,fold:\ ,foldsep:┆
                " set fillchars=foldopen:▽,foldclose:△,foldsep:┃
                " set fillchars=foldopen:▽,foldclose:△
                " set fillchars=foldopen:▿,foldclose:▵,foldsep:│
            
            "FOLD TEXT STYLE:
                function! NeatFoldText()
                  "https://dhruvasagar.dev/2013/03/28/vim-better-foldtext/
                  let line = ' ' . substitute(getline(v:foldstart), '^\s*"\?\s*|\s*"\?\s*{' . '{\d*\s*', '', 'g') . ' '
                  let lines_count = v:foldend - v:foldstart + 1
                  let lines_count_text = '| ' . printf("%10s", lines_count . ' lines') . ' |'
                  let foldchar = matchstr(&fillchars, 'fold:\zs.')
                  let foldtextstart = strpart('›››››' . repeat(foldchar, v:foldlevel*2) . line, 0, (winwidth(0)*2)/3)
                  let foldtextend = lines_count_text . repeat(foldchar, 3)
                  let foldtextlength = strlen(substitute(foldtextstart . foldtextend, '.', 'x', 'g')) + &foldcolumn
                  let remaining_width = winwidth(0) - foldtextlength - strlen('‹‹‹‹‹')+5
                  let padding = repeat(foldchar, remaining_width)
                  return foldtextstart . padding . foldtextend . '‹‹‹‹‹'
                endfunction
                
                " Apply custom fold text setting after Vim has finished loading everything
                autocmd VimEnter * setlocal foldtext=NeatFoldText()
        
        "FOLD COLUMN:  \jf [f ]f
            " Disable foldcolumn by default
            set foldcolumn=0
            
            " Set the background color of the foldcolumn to black
            highlight FoldColumn guibg=black ctermbg=black
            
            
            " Map ]f to jump to the next fold
            nnoremap ]f zj
            
            " Map [f to jump to the previous fold
            nnoremap [f zk
            
            
            " \jf \jF : Useful when there are nested folds or we want to keep foldcolumn invisible
            function! IncreaseFoldColumn()
                let g:auto_origami_foldcolumn += 1
                echo "Foldcolumn set to " . g:auto_origami_foldcolumn
            endfunction
            function! DecreaseFoldColumn()
                if g:auto_origami_foldcolumn > 0
                    let g:auto_origami_foldcolumn -= 1
                endif
                echo "Foldcolumn set to " . g:auto_origami_foldcolumn
            endfunction
            nnoremap <leader>jF :call IncreaseFoldColumn()<CR>
            nnoremap <leader>jf :call DecreaseFoldColumn()<CR>
            
            " OLDER - before vim-auto-origami
            " Map <leader>jf to toggle foldcolumn
            " nnoremap <leader>jf :if &foldcolumn == '0' \| set foldcolumn=2 \| else \| set foldcolumn=0 \| endif<CR>
        
        "AUTO FOLD COLUMN:
            "Removes the need for \jf
            "Automatically displays the fold column when we have folds
            Plugin 'benknoble/vim-auto-origami'
            "Width of fold column: (
            let g:auto_origami_foldcolumn = 2
            augroup autofoldcolumn
              au!
              " Apply AutoOrigamiFoldColumn only if the current buffer's filename does not contain 'VOOM'
              au CursorHold,BufWinEnter,WinEnter * if expand('%:t') !~ 'VOOM' | exec 'AutoOrigamiFoldColumn' | endif
            augroup END
        
        
        
        "FOLD BY SYNTAX: \zs
        "    This works. But, manual folding is better.
        "    "We need this plugin to fold python syntax
        "    " Plugin 'vim-scripts/Python-Syntax-Folding'
        "    Plugin 'tmhedberg/SimpylFold'
        "    set foldmethod=manual
        "
        "    " Create all folds by syntax *once*
        "    function! CreateStaticSyntaxFolds()
        "        " Temporarily set fold method to syntax to generate folds
        "        setlocal foldmethod=syntax
        "        " Close all folds
        "        normal! zM
        "        " Open all folds in the current view to ensure they are created
        "        normal! zR
        "        " Switch to manual fold method to keep the folds
        "        setlocal foldmethod=manual
        "    endfunction
        "
        "    " Create a command zs that calls the function
        "    nnoremap zs :call CreateStaticSyntaxFolds()<cr>
    
    
    "BUFFERS AND TABS: \bb \bt \bq \bf \xtn
        "BUFFERS:
            "CLOSING BUFFERS: \bq
                " Great for closing all unused buffers
                Plugin 'Asheq/close-buffers.vim'
                nnoremap <silent> <leader>bq :Bdelete menu<CR>
            "BUFFERGATOR: \bb or \bt (then ^n ^p tt d)     gB gb
                " ^n ^p  preview next/prev buffers
                " tt or ^t opens buffer in new tab
                " d   to close buffer
                " gb gB   goes to next/prev buffers
                let g:buffergator_suppress_keymaps = 1
                Plugin 'jeetsukumaran/vim-buffergator' " Using \b, will let you switch buffers. Use control+n and control+p to cycle through with previews.
                nnoremap <leader>bb :BuffergatorOpen<cr>
                nnoremap <leader>bt :BuffergatorTabsOpen<cr>
                nnoremap gb :BuffergatorMruCyclePrev<cr>
                nnoremap gB :BuffergatorMruCycleNext<cr>
            "NERDTREE FIND BUFFER: \bf
                nnoremap <leader>bf :NERDTreeFind<cr>
        "TABLINE: \xtn
            " Plugin 'mg979/vim-xtabline' "Make the tabline prettier with separators etc. Supports renaming tabs, searching through tabs, saving bookmarks, custom themes and more. \x? will show you the help menu.
            Plugin 'RyannDaGreat/vim-xtabline' "I modified it because I don't like it adding annoying keyboard shortcuts I can't get rid of, like backspace in normal mode
            
            "FIX THE DEFAULT TAB HIGHLIGHTING: (this plugin makes it really hard to see the highlighted tab in the default color scheme)
            function! SetDefaultTabbarTheme()
                silent! call xtabline#hi#generate('custom_theme', CustomTheme())
                :hi TabLine     ctermfg=255 ctermbg=238 cterm=NONE "an  inactive tab
                :hi TabLineSel  ctermfg=17  ctermbg=190 cterm=NONE "the selected tab
                :hi TabLineFill ctermfg=255 ctermbg=238 cterm=NONE "the unused   portion of the tab line (not enough tabs)
                :hi XTFill      ctermbg=233 cterm=bold "the background of the tab bar
                :hi XTSelect    ctermbg=blue ctermfg=black
                :hi XTSelectMod ctermbg=blue ctermfg=yellow cterm=bold
                :hi XTNum cterm=bold
                :hi XTNumSel cterm=bold ctermbg=blue ctermfg=black
                
                :hi Folded ctermbg=black cterm=italic
                :hi StatusLine ctermfg=white "selected status line
                :hi StatusLineNC ctermfg=blue  "unselected status line
                let g:xtabline_settings.indicators = {
                            \ 'modified': '[+]',
                            \ 'pinned': '[📌]',
                            \}

                let g:xtabline_settings.icons = {
                            \'pin': '📌',
                            \'star': '★',
                            \'book': '📖',
                            \'lock': '🔒',
                            \'hammer': '🔨',
                            \'tick': '✔',
                            \'cross': '✖',
                            \'warning': '⚠',
                            \'menu': '☰',
                            \'apple': '🍎',
                            \'linux': '🐧',
                            \'windows': '⌘',
                            \'git': '',
                            \'palette': '🎨',
                            \'lens': '🔍',
                            \'flag': '🏁',
                            \'flag2': '🍋',
                            \'ico': '🦄',
                            \'train': '🚂',
                            \'gear': '⚙️',
                            \'fire': '🔥',
                            \'snowflake': '❄️',
                            \'huggingface': '🤗',
                            \'robot': '🤖',
                            \'videogame': '👾',
                            \'clock': '🕓',
                            \}
            endfunction


            
            " This is the solution suggested to me by the author: https://github.com/mg979/vim-xtabline/issues/34
            " To use it, run :XTabTheme custom_theme
            function CustomTheme()
            return {
            \"XTSelect":      [ 'black', 'blue',   'NONE',   'NONE',   1 ],
            \"XTSelectMod":   [ 'black', 'blue',   'NONE',   'NONE',   1 ],
            \"XTVisible":     [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \"XTVisibleMod":  [ 'blue', 'black',   'NONE',   'NONE',   1 ],
            \"XTHidden":      [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \"XTHiddenMod":   [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \"XTExtra":       [ 'blue', 'black',   'NONE',   'NONE',   1 ],
            \"XTExtraMod":    [ 'blue', 'black',   'NONE',   'NONE',   1 ],
            \"XTSpecial":     [ 'blue', 'black',   'NONE',   'NONE',   1 ],
            \"XTNumSel":      [ 'black', 'blue',   'NONE',   'NONE',   0 ],
            \"XTNum":         [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \"XTCorner":      [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \"XTFill":        [ 'blue', 'black',   'NONE',   'NONE',   0 ],
            \}
            endfunction
            au VimEnter * silent! call xtabline#hi#generate('custom_theme', CustomTheme())
            
            
            "This is how to run a function AFTER all plugins have been loaded:
            au VimEnter * call SetDefaultTabbarTheme()
    
    
    
    " EXPERIMENTAL:
        
        " PUDB: \jpp \jpl \jpc \jpe
            " \jpp toggles breakpoints
            " \jpl lists all breakpoints
            " \jpc clears all breakpoints
            " \jpe enables seeing breakpoints without toggling anything (equivalent to \jpl twice at first)
            " TODO: ]p and [p jump to next/prev breakpoints
            " TODO: \jpq opens quickfix with all breakpoints instead of just \jpl
            
            "NOTE: It will *silently* fail on python files with invalid syntax. This is by my design.
            
            " Slow startup time right now, and not connected to current RP environ. Gotta fix these before its usable.
            " Plugin 'mvanderkamp/vim-pudb-and-jam'
            
            " My version: Fixed these things
            Plugin 'RyannDaGreat/vim-pudb-and-jam'

            nnoremap <leader>jpp :silent! PudbEnable<cr>:silent! PudbToggle<cr>
            nnoremap <leader>jpe :PudbEnable<cr>
            nnoremap <leader>jpc :PudbClearAll<cr>
            nnoremap <leader>jpd :PudbDisable<cr>
            nnoremap <leader>jpl :PudbList<cr>
            nnoremap <leader>jpt :PudbToggleEnabled<cr>

            hi PudbBreakpointSign ctermfg=red
            hi PudbBreakpointSign ctermbg=black

        "VERDICT: This is cool but it randomly doesn't show up on some files, so because its inconsistent I won't use it.
        "Adds a scrollbar in the statusbar
        "Plugin 'gcavallanti/vim-noscrollbar'
        "set statusline+=\ %{noscrollbar#statusline(15,'■','◫',['◧'],['◨'])}%{'\ '}
        
        "DO NOT USE LIGHTLINE. It works, but other plugins have allergic reactions to it - I can't remove it once installed!
        "And a bunch of chaotic shit happens, like some plugin sets :nowrap when lightline is installed
        " Plugin 'itchyny/lightline.vim'
        
        
        " augroup GlobalSpecialCharHighlight
        "     autocmd!
        "     " Apply custom highlight settings every time a file is opened or a buffer is entered
        "     autocmd VimEnter,BufWinEnter * highlight SpecialChar ctermfg=219 guifg=#FF00FF
        "     autocmd VimEnter,BufWinEnter * syntax match SpecialChar "[().=]"
        " augroup END
        " " Plugin 'NLKNguyen/papercolor-theme'
        
        ""WHICHKEY - Try pressing \<space>l then wait for a second - a menu should appear. This is experimental and I'll use it to make my config easier to use!
        "    Plugin 'liuchengxu/vim-which-key'
        "
        "    " Define prefix dictionary
        "    let g:which_key_map =  {}
        "
        "    let g:mapleader = "\<Space>"
        "    let g:maplocalleader = ','
        "    nnoremap <silent> <leader>      :<c-u>WhichKey '<Space>'<CR>
        "    nnoremap <silent> <localleader> :<c-u>WhichKey  ','<CR>
        "
        "    nnoremap <leader>1 :1wincmd w<CR>
        "    let g:which_key_map.1 = 'which_key_ignore'
        "
        "    nnoremap <leader>_a :echom '_a'<CR>
        "    nnoremap <leader>_b :echom '_b'<CR>
        "    let g:which_key_map['_'] = { 'name': 'which_key_ignore' }
        "
        "    nnoremap <silent> <leader> :<c-u>WhichKey '<Space>'<CR>
        "    vnoremap <silent> <leader> :<c-u>WhichKeyVisual '<Space>'<CR>
        "
        "    call which_key#register('<Space>', "g:which_key_map")
        "
        "    call which_key#register('<Space>', "g:which_key_map", 'n')
        "    call which_key#register('<Space>', "g:which_key_map_visual", 'v')
        "
        "    " Second level dictionaries:
        "    " 'name' is a special field. It will define the name of the group, e.g., leader-f is the "+file" group.
        "    " Unnamed groups will show a default empty string.
        "
        "    " =======================================================
        "    " Create menus based on existing mappings
        "    " =======================================================
        "    " You can pass a descriptive text to an existing mapping.
        "
        "    let g:which_key_map.f = { 'name' : '+file' }
        "
        "    nnoremap <silent> <leader>fs :update<CR>
        "    let g:which_key_map.f.s = 'save-file'
        "
        "    nnoremap <silent> <leader>fd :e $MYVIMRC<CR>
        "    let g:which_key_map.f.d = 'open-vimrc'
        "
        "    nnoremap <silent> <leader>oq  :copen<CR>
        "    nnoremap <silent> <leader>ol  :lopen<CR>
        "    let g:which_key_map.o = {
        "          \ 'name' : '+open',
        "          \ 'q' : 'open-quickfix'    ,
        "          \ 'l' : 'open-locationlist',
        "          \ }
        "
        "    " =======================================================
        "    " Create menus not based on existing mappings:
        "    " =======================================================
        "    " Provide commands(ex-command, <Plug>/<C-W>/<C-d> mapping, etc.)
        "    " and descriptions for the existing mappings.
        "    "
        "    " Note:
        "    " Some complicated ex-cmd may not work as expected since they'll be
        "    " feed into `feedkeys()`, in which case you have to define a decicated
        "    " Command or function wrapper to make it work with vim-which-key.
        "    " Ref issue #126, #133 etc.
        "    let g:which_key_map.b = {
        "          \ 'name' : '+buffer' ,
        "          \ '1' : ['b1'        , 'buffer 1']        ,
        "          \ '2' : ['b2'        , 'buffer 2']        ,
        "          \ 'd' : ['bd'        , 'delete-buffer']   ,
        "          \ 'f' : ['bfirst'    , 'first-buffer']    ,
        "          \ 'h' : ['Startify'  , 'home-buffer']     ,
        "          \ 'l' : ['blast'     , 'last-buffer']     ,
        "          \ 'n' : ['bnext'     , 'next-buffer']     ,
        "          \ 'p' : ['bprevious' , 'previous-buffer'] ,
        "          \ '?' : ['Buffers'   , 'fzf-buffer']      ,
        "          \ }
        "
        "    let g:which_key_map.l = {
        "          \ 'name' : '+lsp',
        "          \ 'f' : ['spacevim#lang#util#Format()'          , 'formatting']       ,
        "          \ 'r' : ['spacevim#lang#util#FindReferences()'  , 'references']       ,
        "          \ 'R' : ['spacevim#lang#util#Rename()'          , 'rename']           ,
        "          \ 's' : ['spacevim#lang#util#DocumentSymbol()'  , 'document-symbol']  ,
        "          \ 'S' : ['spacevim#lang#util#WorkspaceSymbol()' , 'workspace-symbol'] ,
        "          \ 'g' : {
        "            \ 'name': '+goto',
        "            \ 'd' : ['spacevim#lang#util#Definition()'     , 'definition']      ,
        "            \ 't' : ['spacevim#lang#util#TypeDefinition()' , 'type-definition'] ,
        "            \ 'i' : ['spacevim#lang#util#Implementation()' , 'implementation']  ,
        "            \ },
        "            \ }
    
    
    
    "CLIPBOARDS:
    
        "EDIT MODES: F2
            "An alternative to 'set paste' and 'set nopaste' that preserves indent etc
            " Define global variables to store settings
            let g:original_tabstop = 0
            let g:original_shiftwidth = 0
            let g:original_softtabstop = 0
            let g:original_expandtab = 0
            let g:is_paste = 0
            
            function! SaveSettings()
                let g:original_tabstop = &tabstop
                let g:original_shiftwidth = &shiftwidth
                let g:original_softtabstop = &softtabstop
                let g:original_expandtab = &expandtab
            endfunction
            
            function! RestoreSettings()
                let &tabstop = g:original_tabstop
                let &shiftwidth = g:original_shiftwidth
                let &softtabstop = g:original_softtabstop
                let &expandtab = g:original_expandtab
            endfunction

            function! TogglePaste()
                if g:is_paste
                    :NoPaste
                    echo "NoPaste"
                    let g:is_paste=0
                else
                    :Paste
                    echo "Paste"
                    let g:is_paste=1
                endif
            endfunction
            
            " Define Paste command
            command Paste call SaveSettings() | set paste
            
            " Define NoPaste command
            command NoPaste set nopaste | call RestoreSettings()

            nnoremap <F2> :call TogglePaste()<cr>
            inoremap <F2> <C-O>:call TogglePaste()<cr>
        
        " TMUX COPY/PASTE: \tco \tpa
            " In visual mode or normal mode, use \ty to copy to tmux clipboard
            " In normal mode this results in copying a single line
            " In normal mode, use \tp to paste from tmux
            vnoremap <leader>tco y<cr>:call system("tmux load-buffer -", @0)<cr>gv
            nnoremap <leader>tco :.y<cr>:call system("tmux load-buffer -", @0)<cr>
            
            nnoremap <leader>tpa :let @0 = system("tmux save-buffer -")<cr>"0p<cr>g;
        
         " BRACKETED PASTE (use in normal mode)
            " When you paste in visual mode, it overwrites selection (like a regular text editor)
            " (and by paste, I mean from command+v - actual paste)

            " Plugin 'ConradIrwin/vim-bracketed-paste'
            " The above plugin extracted below and modified
            " It should work in insert mode I think, but it doesn't
            " It does work in normal mode though!
            " NOTE This needs to be fixed, it never actually toggles paste mode properly...it never leaves it...
            " And it never brings us out of insert mode either. When we paste from normal mode I expect to go back to normal mode...
            " Tried getting claude and gpt4 to fix it but it didnt work yet...

            let &t_ti .= "\<Esc>[?2004h"
            let &t_te = "\e[?2004l" . &t_te
            function! XTermPasteBegin(ret)
                set pastetoggle=<f29>
                set paste
                return a:ret
            endfunction
            execute "set <f28>=\<Esc>[200~"
            execute "set <f29>=\<Esc>[201~"
            nnoremap <expr> <f28> XTermPasteBegin("i")
            inoremap <expr> <f28> XTermPasteBegin("")
            vnoremap <expr> <f28> XTermPasteBegin("c")

            " Disable bracketed paste in command mode
            cmap <f28> <nop>
            cmap <f29> <nop>

        "OSC52 Copy: \co <c-c>
            " \co          copies whole buffer to clipboard
            " \co or <c-c> in visual copies the selection

            "Copies text to system clipboard via OSC52 - supported by some terminals (Alacritty, and Tmux when configured right)
            Plugin 'ojroques/vim-oscyank', {'branch': 'main'}
            nnoremap <leader>co ggyG:call OSCYankRegister('"')<cr>``
            vnoremap <leader>co :OSCYankVisual<cr>gv
            vnoremap      <c-c> :OSCYankVisual<cr><c-c>

            "Copy a single line in normal mode with <c-c>
            " nnoremap        <c-c> yy:call OSCYankRegister('"')<cr>
            
            "Ever since adding OSC52 via <c-c> I found myself reaching for <c-z> to undo things, probably out of rp muscle memory lol
            nnoremap <c-z> u
            inoremap <c-z> <c-o>u
            " inoremap <c-r> <c-o><c-r>

        " RP CLIPBOARDS: \wco \wpa \lco \lpa \rco \rpa \rrms \rsim \rbla
            " Helper function to check RP_SYS_EXECUTABLE and execute the command
            " Same rules as \tco \tpa (visual mode or normal for copy, normal for paste)
            
            
            function! ExecuteRP(command)
                "Save cursor line and num lines in buffer into some local variables
                let g:rp_save = winsaveview()
                let g:rp_old_num_lines = line('$')
                let g:rp_old_cursor_line = line('.')
                
                if empty($RP_SYS_EXECUTABLE) || !executable($RP_SYS_EXECUTABLE)
                    echohl ErrorMsg
                    echo "ExecuteRP: Error: Please run Vim as a child of rp - $RP_SYS_EXECUTABLE environment var not set"
                    echohl None
                    call input("Press Enter to continue...") "TODO: Handle this error in a more elegant way; right now it still tries pressing <cr>gv
                    return
                endif
                let cmd = $RP_SYS_EXECUTABLE . ' -m rp exec ' . shellescape(a:command, 1)
                let output = system(cmd, @0)
                if v:shell_error == 0
                    let @0 = output
                else
                    echohl ErrorMsg
                    echo "ExecuteRP: Error: Runtime error. Perhaps this is why? Please run Vim as a child of rp - $RP_SYS_EXECUTABLE environment var not set"
                    echohl None
                    call input("Press Enter to continue...") "TODO: Handle this error in a more elegant way; right now it still tries pressing <cr>gv
                endi
                call winrestview(g:rp_save)
                
                "Calculate new cursor line as difference of lines + old line
                " let g:rp_new_num_lines = line('$')
                " let g:rp_new_cursor_line = g:rp_new_num_lines - g:rp_old_num_lines + g:rp_old_cursor_line
            endfunction
            
            function! PostExecuteRP()
                "Restore cursor position etc after a ExecuteRP command
                " :call cursor(g:rp_new_cursor_line, col('.'))
                :call cursor(g:rp_old_cursor_line, col('.'))
                :call winrestview(g:rp_save)
            endfunction
            
            vnoremap <leader>rco :%y<cr>:call ExecuteRP('string_to_clipboard(sys.stdin.read())')<cr>gv
            nnoremap <leader>rco :call ExecuteRP('string_to_clipboard(sys.stdin.read())')<cr>
            
            vnoremap <leader>wco y<cr>:call ExecuteRP('web_copy(sys.stdin.read())')<cr>gv
            nnoremap <leader>wco :%y<cr>:call ExecuteRP('web_copy(sys.stdin.read())')<cr>
            
            vnoremap <leader>lco y<cr>:call ExecuteRP('local_copy(sys.stdin.read())')<cr>gv
            nnoremap <leader>lco :%y<cr>:call ExecuteRP('local_copy(sys.stdin.read())')<cr>
            
            nnoremap <leader>wpa :call ExecuteRP('print(web_paste())')<cr>"0p<cr>g;
            nnoremap <leader>lpa :call ExecuteRP('print(local_paste())')<cr>"0p<cr>g;
            nnoremap <leader>rpa :call ExecuteRP('print(clipboard_to_string())')<cr>"0p<cr>g;
            
            nnoremap <leader>rrms :%y<cr>:call ExecuteRP('print(r._removestar(sys.stdin.read(),max_line_length=1000000,quiet=True))')<cr>ggVGp:call PostExecuteRP()<cr>
            nnoremap <leader>rsim :%y<cr>:call ExecuteRP('print(r._sort_imports_via_isort(sys.stdin.read()))')<cr>ggVGp:call PostExecuteRP()<cr>
            nnoremap <leader>rbla :%y<cr>:call ExecuteRP('print(r._autoformat_python_code_via_black(sys.stdin.read()))')<cr>ggVGp:call PostExecuteRP()<cr>
            nnoremap <leader>tts :retab<cr>
            nnoremap <leader>sw :StripWhitespace<cr>
    
    "FIXES:
        "CLOSING WINDOWS:
            fun! CloseWindow()
                if exists("t:NERDTreeBufName") && winnr("$") == 2
                    "This seemingly simple functionality of, uh, closing a window can go awry when using NerdTreeTabs when closing the last open window when NERDTree exists
                    "This is a workaround
                    "TODO: Fix NerdTreeTabs's source code, maybe it will fix when we open a new tab with nerdtree open, then close it?
                    
                    :NERDTreeTabsToggle
                    :quit
                    " :NERDTreeTabsToggle
                    call timer_start(1, {-> execute('NERDTreeTabsToggle') }) " Wait a second before doing this or NERDTree won't come back again lol
                    "call timer_start(250, {-> execute('NERDTreeFocusToggle') }) " Put the cursor back
                else
                    :quit
                endif
            endfun
            
            nnoremap tq :call CloseWindow()<cr>
            nnoremap <esc>q :call CloseWindow()<cr>
        
        "MESSED UP SETTINGS:
            "Idk what caused these to change. One day I'll debug properly.
            :setlocal foldtext=NeatFoldText()
            :set fillchars+=vert:▎
            :nnoremap <Tab> <C-w>w
            :nnoremap <S-Tab> <C-w>W
            :set nopaste "Liteline says we start in paste?

            "Prevent vim from every trying to auto-wrap my code. Idk why it happens sporadically but this might fix it?
            :set textwidth=0
            :set wrapmargin=0
            augroup AutoView
                autocmd!
                " I hate when vim wraps my text automatically. I NEVER want this. Ever. 
                autocmd BufWinEnter ?* set textwidth=0 | set wrapmargin=0
            augroup END
            
            "The following command is a bit jank but pretty smart. It will make <c-o> map <c-i> back to <c-i>. Idk what plugin maps <c-i> to tab, but its annoying.
            "For some reason I couldn't get autocommands to fix it so I'll do this instead. And simply doing :nnoremap <c-i> <c-i> unfortunately didn't work. But this does.
            :nnoremap <c-o> :nnoremap <c-i <left>> <c-i <left>><cr><c-o>
            :nnoremap <s-tab> :nnoremap <tab <left>> <c-w <left>>w<cr><c-w>W

        "PYTHON PACKAGES:
            "Sometimes we can't install with pip directly into vim. No matter, if we run from RP we can just grab their site packages instead
            :silent! pyx import sys,os;sys.path.append(os.environ['RP_SITE_PACKAGES'])


" AI-WRITTEN FUNCTIONS:
    "CHOOSE GITGUTTER DIFF COMMIT \jG:
        function! GitGutterSelectDiffBase()
          " Check if git is available
          if !executable('git')
            echoerr "Git executable not found in PATH"
            return
          endif

          " Get the git commits with SHA and message (limit to 100)
          let git_output = system('git log --oneline -n 100')
          
          if v:shell_error
            echoerr "Failed to get git commits: " . git_output
            return
          endif
          
          let commits = split(git_output, '\n')
          
          " Create quickfix list
          let qf_list = []
          
          " Add 'main' option at the top
          call add(qf_list, {'text': 'MAIN: main (current branch)', 'lnum': 1})
          
          " Add commits to the quickfix list
          let lnum = 2
          for commit in commits
            let parts = matchlist(commit, '\(\S\+\)\s\+\(.*\)')
            if len(parts) >= 3
              let sha = parts[1]
              let msg = parts[2]
              call add(qf_list, {'text': sha . ': ' . msg, 'lnum': lnum})
              let lnum += 1
            endif
          endfor
          
          " Populate the quickfix list
          call setqflist(qf_list)
          
          " Open the quickfix window
          copen
          
          " Set the title of the quickfix window to include instructions
          let w:quickfix_title = 'Select a commit to set as GitGutter diff base (press Enter)'
          
          " Set up a buffer-local mapping for selection
          nnoremap <buffer> <CR> :call GitGutterSetDiffBase()<CR>
        endfunction

        function! GitGutterSetDiffBase()
          " Get the selected line info
          let qf_item = getqflist()[line('.') - 1]
          let line_text = qf_item.text
          
          " Extract SHA from the text (format is "SHA: message" or "MAIN: main (current branch)")
          let parts = matchlist(line_text, '\(\S\+\): \(.*\)')
          if len(parts) >= 3
            let sha_or_main = parts[1]
            
            " Check if 'MAIN' was selected
            if sha_or_main ==# 'MAIN'
              let g:gitgutter_diff_base = ''
            else
              let g:gitgutter_diff_base = sha_or_main
            endif
            
            " Close the quickfix window
            cclose
            
            " Update GitGutter
            GitGutter
            
            " Provide feedback
            if empty(g:gitgutter_diff_base)
              echo "GitGutter diff base set to index (current branch)"
            else
              echo "GitGutter diff base set to " . g:gitgutter_diff_base
            endif
          else
            echo "Failed to parse commit information"
          endif
        endfunction

"Plugin 'maralla/completor.vim'
"Plugin 'prabirshrestha/asyncomplete.vim'
" Plugin 'preservim/vim-wordchipper'


" Always show status bar and tab bar in vimdiff
autocmd VimEnter * if &diff | set laststatus=2 showtabline=2 | endif


"After absolutely everything else if not in vimdiff mode:
"    If multiple files specified in the vim command like 'vim file1 file2 file3' then open them as tabs not just buffers
function! OpenTabsLater(timer_id)
    if argc() > 1 && !&diff
        tab all
    endif
endfunction
autocmd VimEnter * call timer_start(100, 'OpenTabsLater')

