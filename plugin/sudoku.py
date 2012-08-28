import vim
import sys
import os
import time
import copy

class Sudokuer:
  FIELD_WIDTH  = 9
  FIELD_HEIGHT = 9

  MIN_NUMBER   = 1
  MAX_NUMBER   = 9

  def solve( self ):
    self.isSolved  = False
    self.startTime = time.time( )
    self.__solve( 0, 0 )

  def readFile( self, filename ):
    if not os.path.exists( filename ):
      print( "Given sudoku file ('%s') does not exist!"%( filename ))
      return False

    f = open( filename, "r" )
    self.playground = [[int( c ) for c in l[:9]] for l in f.readlines( )]
    f.close( )
    self.orig_playground = copy.deepcopy( self.playground )
    return True

  def readList( self, list ):
    self.playground = [[int( c ) for c in l[:9]] for l in list]
    self.orig_playground = copy.deepcopy( self.playground )
    return True

  def __solve( self, x, y ):
    if self.isSolved: return False

    if x == Sudokuer.FIELD_WIDTH:
      y += 1
      x  = 0
      if y == Sudokuer.FIELD_HEIGHT: return True

    if self.playground[y][x] > 0: return self.__solve( x + 1, y )

    for i in range( Sudokuer.MIN_NUMBER, Sudokuer.MAX_NUMBER + 1 ):
      if not self.__check( x, y, i ):
        self.playground[y][x] = i
        if self.__solve( x + 1, y ):
          self.__solved( ) # Sudoku solved
    self.playground[y][x] = 0
    return False

  def __check( self, x, y, value ):
    return ( self.__checkRow( y, value ) or self.__checkColumn( x, value ) or self.__checkBox( x, y, value ))

  def __checkRow( self, y, value ):
    for i in range( Sudokuer.FIELD_WIDTH ):
      if self.playground[y][i] == value: return True
    return False

  def __checkColumn( self, x, value ):
    for i in range( Sudokuer.FIELD_HEIGHT ):
      if self.playground[i][x] == value: return True
    return False

  def __checkBox( self, x, y, value ):
    box_x = int( x / 3 ) * 3
    box_y = int( y / 3 ) * 3
    for i in range( box_y, box_y + 3 ):
      for j in range( box_x, box_x + 3 ):
        if self.playground[i][j] == value: return True
    return False

  def __solved( self ):
    self.isSolved = True
    self.endTime  = time.time( )
    self.duration = self.endTime - self.startTime
    print( "Found solution in %f seconds"%( self.duration ))
    self.writeToBuffer( )

  def writeToBuffer( self ):
    vim.command( "vnew" )
    buffer = vim.buffers[-1]
    buffer[0] = "+---+---+---+---+---+---+---+---+---+"
    bufferline = 0
    for i in range( Sudokuer.FIELD_HEIGHT ):
      buffer.append( "|" )
      for j in range( Sudokuer.FIELD_WIDTH ):
        buffer[bufferline + 1] += " %d |"%( self.playground[i][j] )
      buffer.append( "+---+---+---+---+---+---+---+---+---+" )
      bufferline += 2
