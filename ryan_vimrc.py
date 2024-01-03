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

" Toggle NERDTree
    nmap <F5> : NERDTreeTabsToggle <CR>
    " nmap <F5> : NERDTreeToggle <CR>


"Tons of vim color schemes
Plugin 'dracula/vim'
Plugin 'franbach/miramare'
Plugin 'ghifarit53/tokyonight-vim'
Plugin 'sickill/vim-monokai'
"Plugin 'noah/vim256-color' " 256-color schemes for vim
Plugin 'RyannDaGreat/vim-wombat256mod'
Plugin 'kyoz/purify' ", { 'rtp': 'vim' }
function! Fansi()
    " Color schemes are disabled because it lags over SSH. Probably because it uses more bandwidth for 256 colors?
    "      See https://github.com/noah/vim256-color/tree/master/colors
    "     Use: Type ':color t\' and you'll see a list of themes to choose from
    "      NOTE: The default color theme is set torwards the bottom of the .vimrc file, in a function that's run after loading vim

    " set termguicolors "For RLAB. I'm basically always using truecolor terminals nowadays...

    " highlight Normal ctermfg=grey ctermbg=240

    if !exists("g:colors_name")
         colorscheme wombat256mod
         set t_Co=256 "Enable 256 colors in vim
    elseif g:colors_name=='wombat256mod'

        colorscheme        wombat256mod_grb
    elseif g:colors_name=='wombat256mod_grb'

        " colorscheme        wombat256mod_rbg
    " elseif g:colors_name=='wombat256mod_rbg'

        " colorscheme        wombat256mod_brg
    " elseif g:colors_name=='wombat256mod_brg'

        colorscheme        wombat256mod_bgr
    elseif g:colors_name=='wombat256mod_bgr'

        " colorscheme        wombat256mod_gbr
    " elseif g:colors_name=='wombat256mod_gbr'

        " colorscheme        distinguished
    " elseif g:colors_name=='distinguished'

    "     colorscheme        hybrid
    " elseif g:colors_name=='hybrid'

        colorscheme        jellybeans
    elseif g:colors_name=='jellybeans'

        colorscheme        darcula
    elseif g:colors_name=='Darcula'

        colorscheme        miramare
    elseif g:colors_name=='miramare'

        colorscheme        monokai
    elseif g:colors_name=='monokai'

        colorscheme        tokyonight
    elseif g:colors_name=='tokyonight'

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

        colorscheme        dracula
    elseif g:colors_name=='dracula'

        colorscheme        default
    elseif g:colors_name=='default'

        colorscheme        wombat256mod
    endif
    
    "SET BACKGROUND BRIGHTNESS:
    " highlight Normal ctermbg=233
    highlight Normal ctermbg=234

    "UPDATE GITGUTTER COLORS: https://github.com/airblade/vim-gitgutter/issues/614
    highlight DiffAdd guifg=black guibg=wheat1
    highlight DiffChange guifg=black guibg=skyblue1
    highlight DiffDelete guifg=black guibg=gray45 gui=none
    let g:gitgutter_override_sign_column_highlight = 0
    highlight clear SignColumn
    highlight GitGutterDelete guifg=#ff2222 ctermfg=red cterm=bold ctermbg=234
    highlight GitGutterAdd    guifg=#009900 ctermfg=green cterm=bold ctermbg=234
    highlight GitGutterChange guifg=#bbbb00 ctermfg=yellow cterm=bold ctermbg=234
    highlight GitGutterChangeDelete ctermfg=4

    highlight ALEErrorSign ctermfg=199 cterm=bold


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

" Increase vim's command history size. By default it only stores the 15 most recent commands.
" https://vi.stackexchange.com/questions/2920/how-to-further-increase-cmdline-history-size
set viminfo=!,'10000,<50,s10,h,:10000

" Allows for shortcuts that let you select in functions, classes, etc
" https://github.com/jeetsukumaran/vim-pythonsense
Plugin 'jeetsukumaran/vim-pythonsense'

" https://github.com/mduan/python.vim
" This is complementary to vim-pythonsense
" Adds shortcuts for jumping between python blocks etc  
" Plugin 'mduan/python.vim'
Plugin 'RyannDaGreat/python.vim' "I removed all ] shortcuts from it as they interfere with my own shortcuts


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

set shortmess-=S "Show the count of the search like item 5/10 etc https://stackoverflow.com/questions/4668623/show-count-of-matches-in-vim

Plugin 'simeji/winresizer' "Use control+e to resize windows

" KEY MAPPINGS:
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
        nmap <F4><F4> : MinimapToggle <CR>
        nmap <leader>j<leader>j : MinimapToggle <CR>

        " Toggle Gitgutter
        nmap <F4>g : GitGutterToggle <CR>
        nmap <leader>jg : GitGutterToggle <CR>

        " Outliner
        nnoremap <F4>o :Voom python<cr>:set syntax=python<cr>
        nnoremap <leader>jo :Voom python<cr>:set syntax=python<cr>

        "Doesn't work - idk why
        " " NerdTree
        " nnoremap <F4>b : NERDTreeTabsToggle <CR>
        " nnoremap <leader>jb : NERDTreeTabsToggle <CR>

        "Linting Toggle
        map <leader>jl :ALEToggle<return>

        " Lines Toggle
        map <leader>jn :windo set nu!<return>



"Added Nov1 2023
    "GIT STUFF
        "NERDTREE
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
        "GIT GUTTER: [h, ]h
            Plugin 'airblade/vim-gitgutter'
            silent! call gitgutter#disable() " Disable it by default
            set updatetime=100 " This is the recommended update interval from airblade/gitgutter's github page. By default, it's 4 seconds.
            nmap ]h <Plug>(GitGutterNextHunk)
            nmap [h <Plug>(GitGutterPrevHunk)
            omap ih <Plug>(GitGutterTextObjectInnerPending)
            omap ah <Plug>(GitGutterTextObjectOuterPending)
            xmap ih <Plug>(GitGutterTextObjectInnerVisual)
            xmap ah <Plug>(GitGutterTextObjectOuterVisual)
            nmap <leader>hu <Plug>(GitGutterUndoHunk)
            " Git Gutter"
            set updatetime=250
            let g:gitgutter_max_signs = 500
            " No mapping
            let g:gitgutter_map_keys = 0
            " Colors
            let g:gitgutter_override_sign_column_highlight = 0
            highlight clear SignColumn
            highlight GitGutterDelete guifg=#ff2222 ctermfg=1
            highlight GitGutterAdd    guifg=#009900 ctermfg=2
            highlight GitGutterChange guifg=#bbbb00 ctermfg=3
            highlight GitGutterChangeDelete ctermfg=4
        "GITIGNORE SYTAX HIGHLIGHTING
            Plugin 'gisphm/vim-gitignore' " Highlight .gitignore files
    "PYTHON STUFF
        "IMPORT SORT: ^i
            "DISABLED Because it slowed down startup (only a tiny bit - like .04 seconds)
            " if has('python3')
            "     Plugin 'fisadev/vim-isort' " You need pip install isort for this to work. Activate with control+i in visual mode, or the :ISort command
            " endif
        "MACCHIATO: ⌥l
            Plugin 'smbl64/vim-black-macchiato' "Autformat specific sections of python code using   pip install black-macchiato
            autocmd FileType python xmap <buffer> <Esc>l <plug>(BlackMacchiatoSelection)
            autocmd FileType python nmap <buffer> <Esc>l <plug>(BlackMacchiatoCurrentLine)
        "RPY FILES
            autocmd BufRead,BufNewFile *.rpy set filetype=python "Treat .rpy files as python files
        "OUTLINER
            Plugin 'vim-voom/VOoM' " Add an outliner for python so we can quickly jump between functions and classes
            nnoremap <F9> :Voom python<cr>:set syntax=python<cr>
        "JEDI: \g, K, \u, ^[space], \r
            if has('python3') "On Macs, this doesn't work. Don't spam errors.
                Plugin 'davidhalter/jedi-vim' " This adds python-specific refactoring abilities
            endif
        "LINTING: \jl, ]l, [l
            "ALE:
                "Python linting! Toggle with F3
                "NOTE: To be useful, I need to dig into this and disable stupid errors...
                Plugin 'dense-analysis/ale'
                let g:ale_enabled=0 "Disable ale by default
                let g:ale_linters={'python':['pyflakes']} " I coudn't care less about the other linters...flake8 has pep8 in it, so screw it...just use pyflakes which is a subset of flake8
                autocmd VimEnter * nnoremap ]l :ALENextWrap<cr>
                autocmd VimEnter * nnoremap [l :ALEPreviousWrap<cr>
                "]l and [l stand for next lint and prev lint
                let g:ale_set_highlights = 0 "Ale's in-text highlights are really bad; they're always at the beginning or end of a line and don't indicate anything important that the gutter doesn't
                highlight clear ALEErrorSign
                hi  ALEErrorSign ctermfg=Red
                let g:ale_python_pyflakes_executable = 'pyflakes3' "https://vi.stackexchange.com/questions/20508/switch-pyflakes-linter-from-python2-to-python3-in-ale
            "FLAKE8:
                " "This one isn't as good yet...might delete from my vimrc...I've had more luck with ALE: despite it's horrible defaults, it's actually pretty nice once configured
                " Plugin 'nvie/vim-flake8' "Let us analyze our python code...
                " "NOTE: To be useful, I need to dig into this and disable stupid errors...
                " autocmd FileType python nmap <buffer> <esc><F3> :call flake8#Flake8()<CR>
                " " Errors to ignore: https://stackoverflow.com/questions/59241007/flake8-disable-all-formatting-rules
                " let g:syntastic_python_flake8_args='--ignore=E101,E111,E112,E113,E114,E115,E116,E121,E122,E123,E124,E125,E126,E127,E128,E129,E131,E133,E201,E202,E203,E211,E221,E222,E223,E224,E225,E226,E227,E228,E231,E241,E242,E251,E261,E262,E265,E266,E271,E272,E273,E274,E301,E302,E303,E304,E401,E402,E501,E502,E701,E702,E703,E704,E711,E712,E713,E714,E721,E731,E901,E902,W191,W291,W292,W293,W391,W503,W601,W602,W603,W604' "This doesn't actually seem to help...
    "EDITING
        "LINE WRAP: f7
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
            map <F7> :call ToggleWrap()<CR>
        " INDENTATION:
            " Disabled because it doesn't work very well - it made my vimrc use tabs, and rp have 2-spaces-indent.
            " Plugin 'tpope/vim-sleuth' "Auto-detects what indentation the file uses
    "NAVIGATION
        "SEARCHING: * 
            " Allows us to search for text with * from visual mode
            Plugin 'bronson/vim-visual-star-search' " How was this not already a thing? 
        "WINDOW PANE JUMPING: -
            " When you press -, letters appear on each pane - and you press the letter of the one you want to jump to
            Plugin 'https://github.com/t9md/vim-choosewin'
            nmap  -  <Plug>(choosewin)
            let g:choosewin_overlay_enable = 1
        "TAB KEY:
            nnoremap <Tab> <C-w>w
            nnoremap <S-Tab> <C-w>W
        "FILE HISTORY: \p
            let MRU_Max_Menu_Entries=10000 "They said it would get slow if this is a large number. Let's find out...
            Plugin 'yegappan/mru' "Let us have more than vim's default 10 recent files
            nnoremap <leader>p :MruRefresh<cr>:MRU<cr>
            " autocmd BufEnter * silent! MruRefresh " Always get rid of files that no longer exist from the MRU. Clean up the temp files that no longer exist...
        "SESSIONS: \ss \sl \sg
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

        "NERDTREE VISUAL MODE
            Plugin 'PhilRunninger/nerdtree-visual-selection' " Lets us use visual selection mode in NERDTree, then do operations such as 'T' for loading tab on all files in that selection
        "TABLINE: \xtn
            " Plugin 'mg979/vim-xtabline' "Make the tabline prettier with separators etc. Supports renaming tabs, searching through tabs, saving bookmarks, custom themes and more. \x? will show you the help menu.
            Plugin 'RyannDaGreat/vim-xtabline' "I modified it because I don't like it adding annoying keyboard shortcuts I can't get rid of, like backspace in normal mode

            "FIX THE DEFAULT TAB HIGHLIGHTING: (this plugin makes it really hard to see the highlighted tab in the default color scheme)
            function! SetDefaultTabbarTheme()
                hi TabLine     ctermfg=255 ctermbg=238 cterm=NONE "an  inactive tab
                hi TabLineSel  ctermfg=17  ctermbg=190 cterm=NONE "the selected tab
                hi TabLineFill ctermfg=255 ctermbg=238 cterm=NONE "the unused   portion of the tab line (not enough tabs)
                hi XTFill      ctermbg=black cterm=bold "the background of the tab bar
                hi XTSelect    ctermbg=blue ctermfg=black
                hi XTSelectMod ctermbg=blue ctermfg=yellow cterm=bold
                hi XTNum cterm=bold
                hi XTNumSel cterm=bold ctermbg=blue ctermfg=black

                hi Folded ctermbg=black cterm=italic
                hi StatusLine ctermfg=white "selected status line
                hi StatusLineNC ctermfg=blue  "unselected status line
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

    "EXPERIMENTAL
        "Peekaboo will show you the contents of the registers on the sidebar when you hit " or @ in normal mode or <CTRL-R> in insert mode. The sidebar is automatically closed on subsequent key strokes.
        "You can toggle fullscreen mode by pressing spacebar.
        Plugin 'junegunn/vim-peekaboo'

        " Plugin 'RyannDaGreat/vim-signature' "This takes a non-trivial time to start (not bad, but not super fast either). I don't really use marks - this plugin's purpose is to preview where marks are in the gutter.

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



        "Paste NoPaste: An alternative to 'set paste' and 'set nopaste' that preserves indent etc
            " Define global variables to store settings
            let g:original_tabstop = 0
            let g:original_shiftwidth = 0
            let g:original_softtabstop = 0
            let g:original_expandtab = 0

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

            " Define Paste command
            command Paste call SaveSettings() | set paste

            " Define NoPaste command
            command NoPaste set nopaste | call RestoreSettings()





