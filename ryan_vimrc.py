"Ryan Burgert's Default ~/.vimrc (Designed for use with Python)

" Goals:
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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
nmap <F8>     :source ~/.Session.vim<CR>:Obsession ~/.Session.vim<CR>
nmap <F8><F8> :Obsession ~/.Session.vim<CR>

nmap td :tab split<cr>
nmap tn :tabnew<cr>
nmap ts :tab split<cr>
nmap tc :tab close<cr>
nmap tq :quit<cr>
nmap \co gg"+yG<c-o>zz
nmap <esc>q tq
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

"Adds indent guide lines
Plugin 'Yggdroot/indentLine'
"Disable by default...
let g:indentLine_enabled = 0 
nmap <F6> : IndentLinesToggle <CR>

" What does this do? Does it work? TODO find out
Plugin 'gmarik/sudo-gui.vim'


" In visual mode, allow < and > to indent multiple times without having to manually reselect the text
vmap < <gv
vmap > >gv

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
"Fuzzy search recent files
nmap <leader><C-p> :CtrlPMRU<CR>



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

" Plugin 'gsiano/vmux-clipboard' " Allows us to synchronize yanks between separate VIM processes (useful in TMUX for example)
" let mapleader = ","
" map <silent> <leader>y :WriteToVmuxClipboard<cr>
" map <silent> <leader>p :ReadFromVmuxClipboard<cr>
" map <silent> y :WriteToVmuxClipboard<cr>
" map <silent> p :ReadFromVmuxClipboard<cr>

Plugin 'ronakg/quickr-preview.vim' " When in a Quickfix window (aka the search result preview window, like you'd see if using \u or \ff), let us use \[space] to preview a result in multiple lines

Plugin 'severin-lemaignan/vim-minimap' " Adds a minimap to vim. Can be seen by pressing 'F4'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo

""" I love incsearch, but it was slow when editing rp
" Plugin 'haya14busa/incsearch.vim'
" map /  <Plug>(incsearch-forward)
" map ?  <Plug>(incsearch-backward)
" map g/ <Plug>(incsearch-stay)

Plugin 'eugen0329/vim-esearch' " The vim-easysearch plugin. This plugin adds the ability to search for text in files with the \ff command

Plugin 'davidhalter/jedi-vim' " This adds python-specific refactoring abilities

Plugin 'nathanaelkane/vim-indent-guides'

" Plugin 'christoomey/vim-system-copy' "This doesn't seem to work...

" Plugin 'tpope/vim-fugitive' 

Plugin 'scrooloose/nerdtree' "File explorer. Get it by pressing F5
Plugin 'jistr/vim-nerdtree-tabs' "Make NERDTree persist across different tabs

Plugin 'tpope/vim-commentary' "Allows commenting out code with 'gcc' etc

Plugin 'mhinz/vim-startify' "Shows the startup menu
" Plugin 'dkprice/vim-easygrep' "Currently disabled until I figure out a good way to use it
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub

Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.

Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" https://github.com/mgedmin/taghelper.vim
Plugin 'mgedmin/taghelper.vim'
set statusline=%<%f\ %h%m%r\ %1*%{taghelper#curtag()}%*%=%-14.(%l,%c%V%)\ %P

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
"set fillchars+=vert:\
" set fillchars+=vert:⁞
    hi VertSplit ctermbg=black ctermfg=darkgray
    hi VertSplit ctermbg=darkcyan ctermfg=black
    set fillchars=vert:\|
    hi LineNr ctermfg=darkcyan
    hi LineNr ctermfg=gray
    hi LineNr ctermfg=darkgray
    hi LineNr ctermbg=black
    hi CursorLineNR cterm=bold ctermfg=lightcyan

function ToggleWrap()
 if (&wrap == 1)
   set nowrap
 else
   set wrap
 endif
endfunction
map <F7> :call ToggleWrap()<CR>
map! <F9> ^[:call ToggleWrap()<CR>


"let us toggle paste mode with the shortcut key:
    set pastetoggle=<F2>
    set list "Initially, we're not in list mode, so we <F3
    nmap <F9> : set list! <CR> : hi ryan_tabs ctermfg=DarkGray <CR> : match ryan_tabs /\t/ <CR>
" Let us see tabs and spaces when we're NOT in paste mode...
    set showbreak=↪\ 
    set listchars=tab:▸\ 
    hi ryan_tabs ctermfg=DarkGray
    match ryan_tabs /\t/
" Toggle relative line number
    nmap <F3> : set invrelativenumber <CR>

" Toggle Minimap
    nmap <F4> : MinimapToggle <CR>

" Toggle NERDTree
    nmap <F5> : NERDTreeTabsToggle <CR>
    " nmap <F5> : NERDTreeToggle <CR>


"Tons of vim color schemes
Plugin 'noah/vim256-color' " 256-color schemes for vim
function! Fansi()
    " Color schemes are disabled because it lags over SSH. Probably because it uses more bandwidth for 256 colors?
    "      See https://github.com/noah/vim256-color/tree/master/colors
    "     Use: Type ':color t\' and you'll see a list of themes to choose from
    "      NOTE: The default color theme is set torwards the bottom of the .vimrc file, in a function that's run after loading vim
    if !exists("g:colors_name")
         colorscheme wombat256mod
         set t_Co=256 "Enable 256 colors in vim
    elseif g:colors_name=='wombat256mod'

        colorscheme        distinguished
    elseif g:colors_name=='distinguished'

        colorscheme        hybrid
    elseif g:colors_name=='hybrid'

        colorscheme        jellybeans
    elseif g:colors_name=='jellybeans'

        colorscheme        flattown
    elseif g:colors_name=='flattown'

        colorscheme        apprentice
    elseif g:colors_name=='apprentice'

        colorscheme        badwolf
    elseif g:colors_name=='badwolf'

        colorscheme        molokai
    elseif g:colors_name=='molokai'

        colorscheme        vilight
    elseif g:colors_name=='vilight'

        colorscheme        babymate256
    elseif g:colors_name=='babymate256'

        colorscheme        codeschool
    elseif g:colors_name=='codeschool'

        colorscheme        default
    elseif g:colors_name=='default'

        colorscheme        wombat256mod
    endif
    
    "Display the color
    echo g:colors_name

endfunction
nmap fh :call<space>Fansi()<cr>



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
let g:jedi#rename_command = "<leader>r"
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


" Allows for shortcuts that let you select in functions, classes, etc
" https://github.com/jeetsukumaran/vim-pythonsense
Plugin 'jeetsukumaran/vim-pythonsense'

" https://github.com/mduan/python.vim
" This is complementary to vim-pythonsense
" Adds shortcuts for jumping between python blocks etc  
Plugin 'mduan/python.vim'

" Allows us to select entire python blocks, with vai (visualselect all indent) etc and vii (visual select in indent)
Plugin 'michaeljsmith/vim-indent-object'

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
nnoremap <silent> <C-W>z :ZoomToggle<CR>

syntax on
