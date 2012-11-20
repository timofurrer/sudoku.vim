" Sudoku: solve sudokus
" Author: Timo Furrer <tuxtimo@gmail.com>
" Link:   http://github.com/timofurrer

if !has("python")
  "echo "Error: Required vim compiled with +python"
  finish
endif

let s:scriptdir = expand("<sfile>:h") . "/"
execute "pyfile ".s:scriptdir."sudoku.py"

if has("autocmd")
  " set filetype
  autocmd BufNewFile,BufRead *.sdk,*.sudoku set filetype=sudoku

  " map solve sudoku to Shift + F6
  autocmd FileType sudoku map  <S-F6> :call SolveSudoku()<CR>
  autocmd FileType sudoku imap <S-F6> <ESC>:call SolveSudoku()<CR>
endif

function! SolveSudoku(...)
python << EOF

import vim

sdker = Sudokuer( )

if int( vim.eval( "a:0" )) == 0:
  res = sdker.readList( vim.current.buffer.range( 1, 9 ))
else:
  res = sdker.readFile( vim.eval( "a:1" ))
if res: sdker.solve( )

EOF
endfunction
