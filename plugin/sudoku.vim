" Sudoku: solve sudokus
" Author: Timo Furrer <tuxtimo@gmail.com>
" Link:   http://github.com/timofurrer
"

let s:scriptdir = expand("<sfile>:h") . "/"

function! SolveSudoku(...)
  execute "pyfile ".s:scriptdir."sudoku.py"

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
