let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <silent> <Plug>(peekaboo) :call peekaboo#aboo()
inoremap <silent> <Plug>(ale_complete) :ALEComplete
map! <D-v> *
nmap  cp
nnoremap  :WinResizerStartResize
nmap  <Plug>MoveCharLeft
vmap  <Plug>MoveBlockLeft
nnoremap 	 w
vmap <NL> <Plug>MoveBlockDown
nmap <NL> <Plug>MoveLineDown
vmap  <Plug>MoveBlockUp
nmap  <Plug>MoveLineUp
nmap  <Plug>MoveCharRight
vmap  <Plug>MoveBlockRight
xmap <nowait>  <Plug>(VM-Find-Subword-Under)
nmap <nowait>  <Plug>(VM-Find-Under)
nnoremap <silent>  :CtrlP
nnoremap <silent> z :ZoomToggle
nnoremap w 
nmap q tq
xnoremap # :call VisualStarSearchSet('?')?=@/
nnoremap <silent> '[ :call signature#mark#Goto("prev", "line", "alpha")
nnoremap <silent> '] :call signature#mark#Goto("next", "line", "alpha")
xnoremap * :call VisualStarSearchSet('/')/=@/
nmap - <Plug>(choosewin)
noremap ; :
vmap < <gv
vmap > >gv
nnoremap [l :ALEPreviousWrap
nnoremap <silent> [= :call signature#marker#Goto("prev", "any",  v:count)
nnoremap <silent> [- :call signature#marker#Goto("prev", "same", v:count)
nnoremap <silent> [` :call signature#mark#Goto("prev", "spot", "pos")
nnoremap <silent> [' :call signature#mark#Goto("prev", "line", "pos")
nnoremap [f zk
nmap [h <Plug>(GitGutterPrevHunk)
nnoremap [b :bprevious
nnoremap \x <Nop>
nnoremap <silent> \xsn :XTabNewSession
nnoremap <silent> \xsd :XTabDeleteSession
nnoremap <silent> \xss :XTabSaveSession
nnoremap <silent> \xsl :XTabLoadSession
nnoremap <silent> \xtd :XTabDeleteTab
nnoremap <silent> \xts :XTabSaveTab
nnoremap <silent> \xtl :XTabLoadTab
nnoremap <silent> \xbd :XTabDeleteBuffers
nnoremap <silent> \xbr :XTabResetBuffer
nnoremap \xbn :XTabNameBuffer 
nnoremap \xbi :XTabIconBuffer 
nnoremap \xtn :XTabNameTab 
nnoremap \xti :XTabIconTab 
nnoremap <silent> \xtr :XTabResetTab
nnoremap \xT :XTabTheme 
nnoremap <silent> \xR :XTabResetAll
nnoremap <silent> \x? :XTabMenu
nnoremap <silent> \x- :XTabPaths! =v:count
nnoremap <silent> \x+ :XTabPaths =v:count
nnoremap <silent> \x/ :XTabFiltering
nnoremap <silent> \x. :XTabToggleLabels
nnoremap <silent> \xd :XTabTodo
nnoremap <silent> \xK :XTabCleanUp!
nnoremap <silent> \xk :XTabCleanUp
nnoremap <silent> \xh :XTabHideBuffer
nnoremap <silent> \x[ :XTabMoveBufferPrev =v:count1
nnoremap <silent> \x] :XTabMoveBufferNext =v:count1
nnoremap <silent> \xm :XTabMoveBuffer =v:count1
nnoremap <silent> \xp :XTabPinBuffer
nnoremap <silent> \xU :XTabReopenList
nnoremap <silent> \xu :XTabReopen
nnoremap <silent> \x\ :XTabLast
nnoremap <silent> \xx :XTabPurge
nnoremap <silent> \xz :XTabListBuffers
nnoremap <silent> \xa :XTabListTabs
nnoremap <silent> \xq :XTabCloseBuffer
vnoremap \* :call VisualStarSearchSet('/'):execute 'noautocmd vimgrep /' . @/ . '/ **'
nnoremap \* :execute 'noautocmd vimgrep /\V' . substitute(escape(expand("<cword>"), '\'), '\n', '\\n', 'g') . '/ **'
nmap \j <Plug>(CommandTJump)
nmap \b <Plug>(CommandTBuffer)
nmap \t <Plug>(CommandT)
nmap <silent> \ig <Plug>IndentGuidesToggle
map \f <Plug>(operator-esearch-prefill)
nmap \ff <Plug>(esearch)
nnoremap <silent> \mt :MinimapToggle
nnoremap <silent> \mc :MinimapClose
nnoremap <silent> \mu :MinimapUpdate
nnoremap <silent> \mm :Minimap
nmap \q <Plug>(quickr_preview_qf_close)
xmap <nowait> \\c <Plug>(VM-Visual-Cursors)
nmap <nowait> \\gS <Plug>(VM-Reselect-Last)
nmap <nowait> \\/ <Plug>(VM-Start-Regex-Search)
nmap <nowait> \\\ <Plug>(VM-Add-Cursor-At-Pos)
xmap <nowait> \\a <Plug>(VM-Visual-Add)
xmap <nowait> \\f <Plug>(VM-Visual-Find)
xmap <nowait> \\/ <Plug>(VM-Visual-Regex)
xmap <nowait> \\A <Plug>(VM-Visual-All)
nmap <nowait> \\A <Plug>(VM-Select-All)
nnoremap \rbla :%y:call ExecuteRP('print(r._autoformat_python_code_via_black(sys.stdin.read()))')ggVGp
nnoremap \rsim :%y:call ExecuteRP('print(r._sort_imports_via_isort(sys.stdin.read()))')ggVGp
nnoremap \rrms :%y:call ExecuteRP('print(r._removestar(sys.stdin.read(),max_line_length=1000000,quiet=True))')ggVGp
nnoremap \rpa :call ExecuteRP('print(clipboard_to_string())')"0pg;
nnoremap \lpa :call ExecuteRP('print(local_paste())')"0pg;
nnoremap \wpa :call ExecuteRP('print(web_paste())')"0pg;
nnoremap \lco :%y:call ExecuteRP('local_copy(sys.stdin.read())')
vnoremap \lco y:call ExecuteRP('local_copy(sys.stdin.read())')gv
nnoremap \wco :%y:call ExecuteRP('web_copy(sys.stdin.read())')
vnoremap \wco y:call ExecuteRP('web_copy(sys.stdin.read())')gv
nnoremap \rco :call ExecuteRP('string_to_clipboard(sys.stdin.read())')
vnoremap \rco :%y:call ExecuteRP('string_to_clipboard(sys.stdin.read())')gv
nnoremap \tpa :let @0 = system("tmux save-buffer -")"0pg;
nnoremap \tco :.y:call system("tmux load-buffer -", @0)
vnoremap \tco y:call system("tmux load-buffer -", @0)gv
nnoremap \bf :NERDTreeFind
nnoremap \bt :BuffergatorTabsOpen
nnoremap \bb :BuffergatorOpen
nnoremap <silent> \bq :Bdelete menu
nnoremap \jF :call DecreaseFoldColumn()
nnoremap \jf :call IncreaseFoldColumn()
nnoremap \sg :call source ~/.session.vim
nnoremap \sl :call LoadSession()
nnoremap \ss :mks! .session.vim:mks! ~/.session.vim
nnoremap \p :MruRefresh:enew:MRU
nmap \ji :IndentLinesToggle 
nnoremap \ssb :set syntax=bash
nnoremap \ssz :set syntax=zsh
nnoremap \ssh :set syntax=html
nnoremap \ssl :set syntax=latex
nnoremap \ssm :set syntax=markdown
nnoremap \ssc :set syntax=cpp
nnoremap \ssp :set syntax=python
nnoremap \ssj :set syntax=javascript
nnoremap \ssv :set syntax=vim
nnoremap \sss :set syntax=
nnoremap \	9 :set expandtab:set tabstop=9:set shiftwidth=9
nnoremap \	8 :set expandtab:set tabstop=8:set shiftwidth=8
nnoremap \	7 :set expandtab:set tabstop=7:set shiftwidth=7
nnoremap \	6 :set expandtab:set tabstop=6:set shiftwidth=6
nnoremap \	5 :set expandtab:set tabstop=5:set shiftwidth=5
nnoremap \	4 :set expandtab:set tabstop=4:set shiftwidth=4
nnoremap \	3 :set expandtab:set tabstop=3:set shiftwidth=3
nnoremap \	2 :set expandtab:set tabstop=2:set shiftwidth=2
nnoremap \	1 :set expandtab:set tabstop=1:set shiftwidth=1
nnoremap \		 :set noexpandtab
nnoremap \	  :set expandtab
map \jw :call ToggleWrap()
nnoremap \jW :call ToggleSpaceVisualization()
vnoremap \ev :call ExtractVariable()
nnoremap \gB :Git blame
nnoremap \gb :call gitblame#echo()
nmap \hu <Plug>(GitGutterUndoHunk)
map \jn :windo set nu!
map \jl :ALEToggle
nnoremap \jo :Voom python:set syntax=python:set nonu
nmap \jg : GitGutterToggle 
nmap \j\j : MinimapToggle 
nnoremap \js :if &laststatus == 2:set laststatus=1:else:set laststatus=2:endif
nnoremap \jt :if &showtabline == 2:set showtabline=1:else:set showtabline=2:endif
nmap \<C-P> :CtrlPMRU
nmap \ :CtrlPMRU
nmap \co gg"+yGzz
nnoremap ]l :ALENextWrap
nnoremap <silent> ]= :call signature#marker#Goto("next", "any",  v:count)
nnoremap <silent> ]- :call signature#marker#Goto("next", "same", v:count)
nnoremap <silent> ]` :call signature#mark#Goto("next", "spot", "pos")
nnoremap <silent> ]' :call signature#mark#Goto("next", "line", "pos")
nnoremap ]f zj
nmap ]h <Plug>(GitGutterNextHunk)
nnoremap ]b :bnext
nnoremap <silent> `[ :call signature#mark#Goto("prev", "spot", "alpha")
nnoremap <silent> `] :call signature#mark#Goto("next", "spot", "alpha")
xmap ah <Plug>(GitGutterTextObjectOuterVisual)
omap ah <Plug>(GitGutterTextObjectOuterPending)
nnoremap <silent> cdt :XTabTD
nnoremap <silent> cdl :XTabLD
nnoremap <silent> cd? :XTabInfo
nnoremap <silent> cdw :XTabWD
nnoremap <silent> cdc :XTabCD =v:count
nnoremap <silent> dm :call signature#utils#Remove(v:count)
nmap fh :call Fansi()
map g: <Plug>(PythonsensePyWhere)
vmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
nmap gcu <Plug>Commentary<Plug>Commentary
nmap gcc <Plug>CommentaryLine
omap gc <Plug>Commentary
nmap gc <Plug>Commentary
xmap gc <Plug>Commentary
nmap g> <Plug>(swap-next)
nmap g< <Plug>(swap-prev)
xmap gs <Plug>(swap-interactive)
nmap gs <Plug>(swap-interactive)
nnoremap gB :BuffergatorMruCycleNext
nnoremap gb :BuffergatorMruCyclePrev
nnoremap gT :if tabpagenr() == tabpagenr('$'):tabmove 0:else:tabmove +1:endif
nnoremap gR :if tabpagenr() == 1:tabmove $:else:tabmove -1:endif
nnoremap gt :tabnext
nnoremap gr :tabprevious
xmap ih <Plug>(GitGutterTextObjectInnerVisual)
omap ih <Plug>(GitGutterTextObjectInnerPending)
nnoremap <silent> m? :call signature#marker#List(v:count, 0)
nnoremap <silent> m/ :call signature#mark#List(0, 0)
nnoremap <silent> m<BS> :call signature#marker#Purge()
nnoremap <silent> m  :call signature#mark#Purge("all")
nnoremap <silent> m- :call signature#mark#Purge("line")
nnoremap <silent> m. :call signature#mark#ToggleAtLine()
nnoremap <silent> m, :call signature#mark#Toggle("next")
nnoremap <silent> m :call signature#utils#Input()
nmap tq :quit
nmap tc :tab close
nmap ts :tab split
nmap tn :tabnew
nmap td :tab split
vnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(expand((exists("g:netrw_gx")? g:netrw_gx : '<cfile>')),netrw#CheckIfRemote())
xnoremap <silent> <Plug>(peekaboo) :call peekaboo#aboo()
nnoremap <silent> <Plug>(peekaboo) :call peekaboo#aboo()
nmap <BS> <Plug>(XT-Select-Buffer)
nnoremap <silent> <expr> <Plug>(XT-Select-Buffer) v:count ? xtabline#cmds#select_buffer(v:count-1) : ":\buffer #\r"
nnoremap <silent> <Plug>(choosewin) :call choosewin#start(range(1, winnr('$')))
nnoremap <silent> <Plug>(ale_info_preview) :ALEInfo -preview
nnoremap <silent> <Plug>(ale_info_clipboard) :ALEInfo -clipboard
nnoremap <silent> <Plug>(ale_info_echo) :ALEInfo -echo
nnoremap <silent> <Plug>(ale_info) :ALEInfo
nnoremap <silent> <Plug>(ale_repeat_selection) :ALERepeatSelection
nnoremap <silent> <Plug>(ale_code_action) :ALECodeAction
nnoremap <silent> <Plug>(ale_filerename) :ALEFileRename
nnoremap <silent> <Plug>(ale_rename) :ALERename
nnoremap <silent> <Plug>(ale_import) :ALEImport
nnoremap <silent> <Plug>(ale_documentation) :ALEDocumentation
nnoremap <silent> <Plug>(ale_hover) :ALEHover
nnoremap <silent> <Plug>(ale_find_references) :ALEFindReferences
nnoremap <silent> <Plug>(ale_go_to_implementation_in_vsplit) :ALEGoToImplementation -vsplit
nnoremap <silent> <Plug>(ale_go_to_implementation_in_split) :ALEGoToImplementation -split
nnoremap <silent> <Plug>(ale_go_to_implementation_in_tab) :ALEGoToImplementation -tab
nnoremap <silent> <Plug>(ale_go_to_implementation) :ALEGoToImplementation
nnoremap <silent> <Plug>(ale_go_to_type_definition_in_vsplit) :ALEGoToTypeDefinition -vsplit
nnoremap <silent> <Plug>(ale_go_to_type_definition_in_split) :ALEGoToTypeDefinition -split
nnoremap <silent> <Plug>(ale_go_to_type_definition_in_tab) :ALEGoToTypeDefinition -tab
nnoremap <silent> <Plug>(ale_go_to_type_definition) :ALEGoToTypeDefinition
nnoremap <silent> <Plug>(ale_go_to_definition_in_vsplit) :ALEGoToDefinition -vsplit
nnoremap <silent> <Plug>(ale_go_to_definition_in_split) :ALEGoToDefinition -split
nnoremap <silent> <Plug>(ale_go_to_definition_in_tab) :ALEGoToDefinition -tab
nnoremap <silent> <Plug>(ale_go_to_definition) :ALEGoToDefinition
nnoremap <silent> <Plug>(ale_fix) :ALEFix
nnoremap <silent> <Plug>(ale_detail) :ALEDetail
nnoremap <silent> <Plug>(ale_lint) :ALELint
nnoremap <silent> <Plug>(ale_reset_buffer) :ALEResetBuffer
nnoremap <silent> <Plug>(ale_disable_buffer) :ALEDisableBuffer
nnoremap <silent> <Plug>(ale_enable_buffer) :ALEEnableBuffer
nnoremap <silent> <Plug>(ale_toggle_buffer) :ALEToggleBuffer
nnoremap <silent> <Plug>(ale_reset) :ALEReset
nnoremap <silent> <Plug>(ale_disable) :ALEDisable
nnoremap <silent> <Plug>(ale_enable) :ALEEnable
nnoremap <silent> <Plug>(ale_toggle) :ALEToggle
nnoremap <silent> <Plug>(ale_last) :ALELast
nnoremap <silent> <Plug>(ale_first) :ALEFirst
nnoremap <silent> <Plug>(ale_next_wrap_warning) :ALENext -wrap -warning
nnoremap <silent> <Plug>(ale_next_warning) :ALENext -warning
nnoremap <silent> <Plug>(ale_next_wrap_error) :ALENext -wrap -error
nnoremap <silent> <Plug>(ale_next_error) :ALENext -error
nnoremap <silent> <Plug>(ale_next_wrap) :ALENextWrap
nnoremap <silent> <Plug>(ale_next) :ALENext
nnoremap <silent> <Plug>(ale_previous_wrap_warning) :ALEPrevious -wrap -warning
nnoremap <silent> <Plug>(ale_previous_warning) :ALEPrevious -warning
nnoremap <silent> <Plug>(ale_previous_wrap_error) :ALEPrevious -wrap -error
nnoremap <silent> <Plug>(ale_previous_error) :ALEPrevious -error
nnoremap <silent> <Plug>(ale_previous_wrap) :ALEPreviousWrap
nnoremap <silent> <Plug>(ale_previous) :ALEPrevious
nnoremap <Plug>(BlackMacchiatoCurrentLine) :BlackMacchiato
xnoremap <Plug>(BlackMacchiatoSelection) :'<,'>BlackMacchiato
nnoremap <silent> <Plug>GitGutterPreviewHunk :call gitgutter#utility#warn('Please change your map <Plug>GitGutterPreviewHunk to <Plug>(GitGutterPreviewHunk)')
nnoremap <silent> <Plug>(GitGutterPreviewHunk) :GitGutterPreviewHunk
nnoremap <silent> <Plug>GitGutterUndoHunk :call gitgutter#utility#warn('Please change your map <Plug>GitGutterUndoHunk to <Plug>(GitGutterUndoHunk)')
nnoremap <silent> <Plug>(GitGutterUndoHunk) :GitGutterUndoHunk
nnoremap <silent> <Plug>GitGutterStageHunk :call gitgutter#utility#warn('Please change your map <Plug>GitGutterStageHunk to <Plug>(GitGutterStageHunk)')
nnoremap <silent> <Plug>(GitGutterStageHunk) :GitGutterStageHunk
xnoremap <silent> <Plug>GitGutterStageHunk :call gitgutter#utility#warn('Please change your map <Plug>GitGutterStageHunk to <Plug>(GitGutterStageHunk)')
xnoremap <silent> <Plug>(GitGutterStageHunk) :GitGutterStageHunk
nnoremap <silent> <expr> <Plug>GitGutterPrevHunk &diff ? '[c' : ":\call gitgutter#utility#warn('Please change your map \<Plug>GitGutterPrevHunk to \<Plug>(GitGutterPrevHunk)')\"
nnoremap <silent> <expr> <Plug>(GitGutterPrevHunk) &diff ? '[c' : ":\execute v:count1 . 'GitGutterPrevHunk'\"
nnoremap <silent> <expr> <Plug>GitGutterNextHunk &diff ? ']c' : ":\call gitgutter#utility#warn('Please change your map \<Plug>GitGutterNextHunk to \<Plug>(GitGutterNextHunk)')\"
nnoremap <silent> <expr> <Plug>(GitGutterNextHunk) &diff ? ']c' : ":\execute v:count1 . 'GitGutterNextHunk'\"
xnoremap <silent> <Plug>(GitGutterTextObjectOuterVisual) :call gitgutter#hunk#text_object(0)
xnoremap <silent> <Plug>(GitGutterTextObjectInnerVisual) :call gitgutter#hunk#text_object(1)
onoremap <silent> <Plug>(GitGutterTextObjectOuterPending) :call gitgutter#hunk#text_object(0)
onoremap <silent> <Plug>(GitGutterTextObjectInnerPending) :call gitgutter#hunk#text_object(1)
nnoremap <C-E> :WinResizerStartResize
nmap <C-L> <Plug>MoveCharRight
nmap <C-H> <Plug>MoveCharLeft
vmap <C-L> <Plug>MoveBlockRight
vmap <C-H> <Plug>MoveBlockLeft
nnoremap <silent> <Plug>(CommandTTag) :CommandTTag
nnoremap <silent> <Plug>(CommandTSearch) :CommandTSearch
nnoremap <silent> <Plug>(CommandTMRU) :CommandTMRU
nnoremap <silent> <Plug>(CommandTLine) :CommandTLine
nnoremap <silent> <Plug>(CommandTCommand) :CommandTCommand
nnoremap <silent> <Plug>(CommandTJump) :CommandTJump
nnoremap <silent> <Plug>(CommandTHistory) :CommandTHistory
nnoremap <silent> <Plug>(CommandTHelp) :CommandTHelp
nnoremap <silent> <Plug>(CommandTBuffer) :CommandTBuffer
nnoremap <silent> <Plug>(CommandT) :CommandT
nnoremap <silent> <Plug>(startify-open-buffers) :call startify#open_buffers()
nmap <silent> <Plug>CommentaryUndo :echoerr "Change your <Plug>CommentaryUndo map to <Plug>Commentary<Plug>Commentary"
noremap <silent> <expr> <Plug>(operator-esearch-exec) esearch#exec({'remember': 1})
noremap <silent> <expr> <Plug>(operator-esearch-prefill) esearch#prefill({'remember': 1})
xmap <Plug>(esearch) <Plug>(operator-esearch-prefill)
nnoremap <silent> <Plug>(esearch) :call esearch#init({'remember': 1})
nnoremap <silent> <Plug>(quickr_preview_qf_close) :cclose:lclose
nnoremap <silent> <C-P> :CtrlP
nmap <nowait> <C-LeftMouse> <Plug>(VM-Mouse-Cursor)
nmap <nowait> <C-Down> <Plug>(VM-Add-Cursor-Down)
nmap <nowait> <M-C-RightMouse> <Plug>(VM-Mouse-Column)
xmap <nowait> <C-N> <Plug>(VM-Find-Subword-Under)
nmap <nowait> <C-Up> <Plug>(VM-Add-Cursor-Up)
nmap <nowait> <S-Right> <Plug>(VM-Select-l)
nmap <nowait> <S-Left> <Plug>(VM-Select-h)
nmap <nowait> <C-RightMouse> <Plug>(VM-Mouse-Word)
nmap <nowait> <C-N> <Plug>(VM-Find-Under)
nnoremap <silent> <Plug>(VM-Select-BBW) :call vm#commands#motion('BBW', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-gE) :call vm#commands#motion('gE', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-ge) :call vm#commands#motion('ge', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-E) :call vm#commands#motion('E', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-e) :call vm#commands#motion('e', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-B) :call vm#commands#motion('B', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-b) :call vm#commands#motion('b', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-W) :call vm#commands#motion('W', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-w) :call vm#commands#motion('w', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-l) :call vm#commands#motion('l', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-k) :call vm#commands#motion('k', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-j) :call vm#commands#motion('j', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Select-h) :call vm#commands#motion('h', v:count1, 1, 0)
nnoremap <silent> <Plug>(VM-Mouse-Column) :call vm#commands#mouse_column()
nmap <silent> <Plug>(VM-Mouse-Word) <Plug>(VM-Left-Mouse)<Plug>(VM-Find-Under)
nmap <silent> <Plug>(VM-Mouse-Cursor) <Plug>(VM-Left-Mouse)<Plug>(VM-Add-Cursor-At-Pos)
nnoremap <silent> <Plug>(VM-Left-Mouse) <LeftMouse>
xnoremap <silent> <Plug>(VM-Visual-Regex) :call vm#commands#find_by_regex(2):call feedkeys('/', 'n')
nnoremap <silent> <Plug>(VM-Slash-Search) @=vm#commands#find_by_regex(3)
nnoremap <silent> <Plug>(VM-Start-Regex-Search) @=vm#commands#find_by_regex(1)
nnoremap <silent> <Plug>(VM-Find-Under) :call vm#commands#ctrln(v:count1)
xnoremap <silent> <Plug>(VM-Visual-Reduce) :call vm#visual#reduce()
xnoremap <silent> <Plug>(VM-Visual-Add) :call vm#commands#visual_add()
xnoremap <silent> <Plug>(VM-Visual-Cursors) :call vm#commands#visual_cursors()
nnoremap <silent> <Plug>(VM-Select-All) :call vm#commands#find_all(0, 1)
nnoremap <silent> <Plug>(VM-Reselect-Last) :call vm#commands#reselect_last()
nnoremap <silent> <Plug>(VM-Select-Cursor-Up) :call vm#commands#add_cursor_up(1, v:count1)
nnoremap <silent> <Plug>(VM-Select-Cursor-Down) :call vm#commands#add_cursor_down(1, v:count1)
nnoremap <silent> <Plug>(VM-Add-Cursor-Up) :call vm#commands#add_cursor_up(0, v:count1)
nnoremap <silent> <Plug>(VM-Add-Cursor-Down) :call vm#commands#add_cursor_down(0, v:count1)
nnoremap <silent> <Plug>(VM-Add-Cursor-At-Word) :call vm#commands#add_cursor_at_word(1, 1)
nnoremap <silent> <Plug>(VM-Add-Cursor-At-Pos) :call vm#commands#add_cursor_at_pos(0)
xmap <silent> <expr> <Plug>(VM-Visual-Find) vm#operators#find(1, 1)
noremap <silent> <Plug>(swap-textobject-a) :call swap#textobj#select('a')
noremap <silent> <Plug>(swap-textobject-i) :call swap#textobj#select('i')
nnoremap <silent> <Plug>(swap-next) :call swap#prerequisite('n', repeat([['#', '#+1']], v:count1))g@l
nnoremap <silent> <Plug>(swap-prev) :call swap#prerequisite('n', repeat([['#', '#-1']], v:count1))g@l
xnoremap <silent> <Plug>(swap-interactive) :call swap#prerequisite('x')gvg@
nnoremap <silent> <Plug>(swap-interactive) :call swap#prerequisite('n')g@l
nnoremap <C-I> 	
nnoremap <S-Tab> W
nmap <F6> :IndentLinesToggle 
map <F7> :call ToggleWrap()
nnoremap <F4>o :Voom python:set syntax=python
nmap <F4>g : GitGutterToggle 
nmap <F4><F4> : MinimapToggle 
nnoremap <F4>s :if &laststatus == 2:set laststatus=1:else:set laststatus=2:endif
nnoremap <F4>t :if &showtabline == 2:set showtabline=1:else:set showtabline=2:endif
vmap <C-K> <Plug>MoveBlockUp
vmap <C-J> <Plug>MoveBlockDown
nmap <C-K> <Plug>MoveLineUp
nmap <C-J> <Plug>MoveLineDown
nnoremap <silent> <C-W>z :ZoomToggle
noremap <MiddleDrag> <LeftDrag>
noremap <MiddleMouse> <4-LeftMouse>
nmap <F5> : NERDTreeTabsToggle 
nmap <F3> : set invrelativenumber 
nnoremap <F9> :Voom python:set syntax=python
nmap <C-C> cp
nmap <F8><F8> :Obsession ~/.Session.vim
nmap <F8> :source ~/.Session.vim:Obsession ~/.Session.vim
vmap <BS> "-d
vmap <D-x> "*d
vmap <D-c> "*y
vmap <D-v> "-d"*P
nmap <D-v> "*P
inoremap h 
inoremap l ll
let &cpo=s:cpo_save
unlet s:cpo_save
set backspace=indent,eol,start
set confirm
set fileencodings=ucs-bom,utf-8,default,latin1
set fillchars=vert:|,fold:-,vert:▎
set helplang=en
set hlsearch
set listchars=tab:▸\\
set mouse=a
set pastetoggle=<F2>
set runtimepath=
set runtimepath+=~/.vim
set runtimepath+=~/.vim/bundle/Vundle.vim
set runtimepath+=~/.vim/bundle/vim-obsession
set runtimepath+=~/.vim/bundle/vim-swap
set runtimepath+=~/.vim/bundle/sudo-gui.vim
set runtimepath+=~/.vim/bundle/rainbow_csv
set runtimepath+=~/.vim/bundle/vim-visual-multi
set runtimepath+=~/.vim/bundle/ctrlp.vim
set runtimepath+=~/.vim/bundle/vim-javascript
set runtimepath+=~/.vim/bundle/quickr-preview.vim
set runtimepath+=~/.vim/bundle/vim-minimap
set runtimepath+=~/.vim/bundle/vim-esearch
set runtimepath+=~/.vim/bundle/vim-indent-guides
set runtimepath+=~/.vim/bundle/nerdtree
set runtimepath+=~/.vim/bundle/vim-nerdtree-tabs
set runtimepath+=~/.vim/bundle/vim-commentary
set runtimepath+=~/.vim/bundle/vim-startify
set runtimepath+=~/.vim/bundle/command-t
set runtimepath+=~/.vim/bundle/sparkup/vim/
set runtimepath+=~/.vim/bundle/taghelper.vim
set runtimepath+=~/.vim/bundle/vim
set runtimepath+=~/.vim/bundle/miramare
set runtimepath+=~/.vim/bundle/tokyonight-vim
set runtimepath+=~/.vim/bundle/vim-monokai
set runtimepath+=~/.vim/bundle/vim-wombat256mod
set runtimepath+=~/.vim/bundle/purify
set runtimepath+=~/.vim/bundle/vim-move
set runtimepath+=~/.vim/bundle/python.vim
set runtimepath+=~/.vim/bundle/winresizer
set runtimepath+=~/.vim/bundle/nerdtree-git-plugin
set runtimepath+=~/.vim/bundle/vim-gitgutter
set runtimepath+=~/.vim/bundle/vim-gitignore
set runtimepath+=~/.vim/bundle/git-blame.vim
set runtimepath+=~/.vim/bundle/vim-fugitive
set runtimepath+=~/.vim/bundle/vim-black-macchiato
set runtimepath+=~/.vim/bundle/VOoM
set runtimepath+=~/.vim/bundle/ale
set runtimepath+=~/.vim/bundle/python-syntax
set runtimepath+=~/.vim/bundle/indentLine
set runtimepath+=~/.vim/bundle/vim-visual-star-search
set runtimepath+=~/.vim/bundle/vim-choosewin
set runtimepath+=~/.vim/bundle/vim-pythonsense
set runtimepath+=~/.vim/bundle/vim-indent-object
set runtimepath+=~/.vim/bundle/mru
set runtimepath+=~/.vim/bundle/vim-signature
set runtimepath+=~/.vim/bundle/nerdtree-visual-selection
set runtimepath+=~/.vim/bundle/restore_view.vim
set runtimepath+=~/.vim/bundle/vim-auto-origami
set runtimepath+=~/.vim/bundle/close-buffers.vim
set runtimepath+=~/.vim/bundle/vim-buffergator
set runtimepath+=~/.vim/bundle/vim-xtabline
set runtimepath+=~/.vim/bundle/vim-peekaboo
set runtimepath+=/usr/local/share/vim/vimfiles
set runtimepath+=/usr/local/share/vim/vim81
set runtimepath+=/usr/local/share/vim/vimfiles/after
set runtimepath+=~/.vim/after
set runtimepath+=~/.vim/bundle/Vundle.vim
set runtimepath+=~/.vim/bundle/Vundle.vim/after
set runtimepath+=~/.vim/bundle/vim-obsession/after
set runtimepath+=~/.vim/bundle/vim-swap/after
set runtimepath+=~/.vim/bundle/sudo-gui.vim/after
set runtimepath+=~/.vim/bundle/rainbow_csv/after
set runtimepath+=~/.vim/bundle/vim-visual-multi/after
set runtimepath+=~/.vim/bundle/ctrlp.vim/after
set runtimepath+=~/.vim/bundle/vim-javascript/after
set runtimepath+=~/.vim/bundle/quickr-preview.vim/after
set runtimepath+=~/.vim/bundle/vim-minimap/after
set runtimepath+=~/.vim/bundle/vim-esearch/after
set runtimepath+=~/.vim/bundle/vim-indent-guides/after
set runtimepath+=~/.vim/bundle/nerdtree/after
set runtimepath+=~/.vim/bundle/vim-nerdtree-tabs/after
set runtimepath+=~/.vim/bundle/vim-commentary/after
set runtimepath+=~/.vim/bundle/vim-startify/after
set runtimepath+=~/.vim/bundle/command-t/after
set runtimepath+=~/.vim/bundle/sparkup/vim//after
set runtimepath+=~/.vim/bundle/taghelper.vim/after
set runtimepath+=~/.vim/bundle/vim/after
set runtimepath+=~/.vim/bundle/miramare/after
set runtimepath+=~/.vim/bundle/tokyonight-vim/after
set runtimepath+=~/.vim/bundle/vim-monokai/after
set runtimepath+=~/.vim/bundle/vim-wombat256mod/after
set runtimepath+=~/.vim/bundle/purify/after
set runtimepath+=~/.vim/bundle/vim-move/after
set runtimepath+=~/.vim/bundle/python.vim/after
set runtimepath+=~/.vim/bundle/winresizer/after
set runtimepath+=~/.vim/bundle/nerdtree-git-plugin/after
set runtimepath+=~/.vim/bundle/vim-gitgutter/after
set runtimepath+=~/.vim/bundle/vim-gitignore/after
set runtimepath+=~/.vim/bundle/git-blame.vim/after
set runtimepath+=~/.vim/bundle/vim-fugitive/after
set runtimepath+=~/.vim/bundle/vim-black-macchiato/after
set runtimepath+=~/.vim/bundle/VOoM/after
set runtimepath+=~/.vim/bundle/ale/after
set runtimepath+=~/.vim/bundle/python-syntax/after
set runtimepath+=~/.vim/bundle/indentLine/after
set runtimepath+=~/.vim/bundle/vim-visual-star-search/after
set runtimepath+=~/.vim/bundle/vim-choosewin/after
set runtimepath+=~/.vim/bundle/vim-pythonsense/after
set runtimepath+=~/.vim/bundle/vim-indent-object/after
set runtimepath+=~/.vim/bundle/mru/after
set runtimepath+=~/.vim/bundle/vim-signature/after
set runtimepath+=~/.vim/bundle/nerdtree-visual-selection/after
set runtimepath+=~/.vim/bundle/restore_view.vim/after
set runtimepath+=~/.vim/bundle/vim-auto-origami/after
set runtimepath+=~/.vim/bundle/close-buffers.vim/after
set runtimepath+=~/.vim/bundle/vim-buffergator/after
set runtimepath+=~/.vim/bundle/vim-xtabline/after
set runtimepath+=~/.vim/bundle/vim-peekaboo/after
set shiftwidth=4
set shortmess=filnxtToOI
set showbreak=↪\\
set smartindent
set statusline=%<%f\ %h%m%r\ %1*%{taghelper#curtag()}%*%=%-14.(%l,%c%V%)\ %P
set switchbuf=usetab
set tabline=%!xtabline#render#tabline()
set tabstop=4
set undofile
set updatetime=250
set viminfo=!,'10000,<50,s10,h,:10000
set wildignore=*.pyc
set wildmenu
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/rp
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
edit r.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
let s:cpo_save=&cpo
set cpo&vim
imap <buffer> <expr> <C-R> peekaboo#peek(1, "\",  0)
nmap <buffer> l <Plug>(BlackMacchiatoCurrentLine)
xmap <buffer> l <Plug>(BlackMacchiatoSelection)
xmap <buffer> <expr> " peekaboo#peek(v:count1, '"',  1)
nmap <buffer> <expr> " peekaboo#peek(v:count1, '"',  0)
nmap <buffer> <expr> @ peekaboo#peek(v:count1, '@', 0)
xmap <buffer> ad <Plug>(PythonsenseOuterDocStringTextObject)
omap <buffer> ad <Plug>(PythonsenseOuterDocStringTextObject)
omap <buffer> af <Plug>(PythonsenseOuterFunctionTextObject)
xmap <buffer> af <Plug>(PythonsenseOuterFunctionTextObject)
omap <buffer> ac <Plug>(PythonsenseOuterClassTextObject)
xmap <buffer> ac <Plug>(PythonsenseOuterClassTextObject)
xmap <buffer> id <Plug>(PythonsenseInnerDocStringTextObject)
omap <buffer> id <Plug>(PythonsenseInnerDocStringTextObject)
omap <buffer> if <Plug>(PythonsenseInnerFunctionTextObject)
xmap <buffer> if <Plug>(PythonsenseInnerFunctionTextObject)
omap <buffer> ic <Plug>(PythonsenseInnerClassTextObject)
xmap <buffer> ic <Plug>(PythonsenseInnerClassTextObject)
nnoremap <buffer> <silent> <Plug>(PythonsensePyWhere) :Pywhere
onoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonFunction) V:call pythonsense#move_to_python_object('\(def\|async def\)', 1, 0, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 1, 0, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 1, 0, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonFunction) V:call pythonsense#move_to_python_object('\(def\|async def\)', 0, 0, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 0, 0, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 0, 0, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonFunction) V:call pythonsense#move_to_python_object('\(def\|async def\)', 1, 1, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 1, 1, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 1, 1, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonFunction) V:call pythonsense#move_to_python_object('\(def\|async def\)', 0, 1, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 0, 1, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonFunction) :call pythonsense#move_to_python_object('\(def\|async def\)', 0, 1, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonClass) V:call pythonsense#move_to_python_object("class", 1, 0, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonClass) :call pythonsense#move_to_python_object("class", 1, 0, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPreviousPythonClass) :call pythonsense#move_to_python_object("class", 1, 0, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonClass) V:call pythonsense#move_to_python_object("class", 0, 0, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonClass) :call pythonsense#move_to_python_object("class", 0, 0, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseStartOfPythonClass) :call pythonsense#move_to_python_object("class", 0, 0, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonClass) V:call pythonsense#move_to_python_object("class", 1, 1, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonClass) :call pythonsense#move_to_python_object("class", 1, 1, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseEndOfPythonClass) :call pythonsense#move_to_python_object("class", 1, 1, "n")
onoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonClass) V:call pythonsense#move_to_python_object("class", 0, 1, "o")
vnoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonClass) :call pythonsense#move_to_python_object("class", 0, 1, "v")
nnoremap <buffer> <silent> <Plug>(PythonsenseStartOfNextPythonClass) :call pythonsense#move_to_python_object("class", 0, 1, "n")
vnoremap <buffer> <silent> <Plug>(PythonsenseInnerDocStringTextObject) :cal pythonsense#python_docstring_text_object(1)
vnoremap <buffer> <silent> <Plug>(PythonsenseOuterDocStringTextObject) :cal pythonsense#python_docstring_text_object(0)
vnoremap <buffer> <silent> <Plug>(PythonsenseInnerClassTextObject) :call pythonsense#python_class_text_object(1, "v")gv
vnoremap <buffer> <silent> <Plug>(PythonsenseOuterClassTextObject) :call pythonsense#python_class_text_object(0, "v")gv
vnoremap <buffer> <silent> <Plug>(PythonsenseInnerFunctionTextObject) :call pythonsense#python_function_text_object(1, "v")gv
vnoremap <buffer> <silent> <Plug>(PythonsenseOuterFunctionTextObject) :call pythonsense#python_function_text_object(0, "v")gv
onoremap <buffer> <silent> <Plug>(PythonsenseInnerDocStringTextObject) :call pythonsense#python_docstring_text_object(1)
onoremap <buffer> <silent> <Plug>(PythonsenseOuterDocStringTextObject) :call pythonsense#python_docstring_text_object(0)
onoremap <buffer> <silent> <Plug>(PythonsenseInnerClassTextObject) :call pythonsense#python_class_text_object(1, "o")
onoremap <buffer> <silent> <Plug>(PythonsenseOuterClassTextObject) :call pythonsense#python_class_text_object(0, "o")
onoremap <buffer> <silent> <Plug>(PythonsenseInnerFunctionTextObject) :call pythonsense#python_function_text_object(1, "o")
onoremap <buffer> <silent> <Plug>(PythonsenseOuterFunctionTextObject) :call pythonsense#python_function_text_object(0, "o")
imap <buffer> <expr>  peekaboo#peek(1, "\",  0)
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),0],:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:%,:XCOMM,n:>,fb:-
setlocal commentstring=/*%s*/
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
set cursorline
setlocal cursorline
setlocal cursorlineopt=both
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal noexpandtab
if &filetype != ''
setlocal filetype=
endif
setlocal fixendofline
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=NeatFoldText()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=
setlocal indentkeys=0{,0},0),0],:,0#,!^F,o,O,e
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
set list
setlocal list
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal scrolloff=-1
setlocal shiftwidth=4
setlocal noshortname
setlocal sidescrolloff=-1
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != ''
setlocal syntax=
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tagfunc=
setlocal tags=
setlocal termwinkey=
setlocal termwinscroll=10000
setlocal termwinsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal varsofttabstop=
setlocal vartabstop=
setlocal wincolor=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/rp
tabnext 1
badd +0 /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/rp/r.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToOI
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
