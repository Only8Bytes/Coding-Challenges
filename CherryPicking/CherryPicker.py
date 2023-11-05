from graphics import *
import random
import time

LINE_THICKNESS = 2
CIRCLE_RADIUS = 10
CELL_SIZE = 30
PADDING = 50
puzzle = None
pathsDown = []
pathsUp = []

def prettyPrint(matrix):
  for x in range(len(matrix)):
    for y in range(len(matrix)):
      print('{0:<10}'.format(matrix[y][x]), end='')
    print()

def drawCherry(x, y):
  c = Circle(Point(PADDING + CELL_SIZE * (x) + CELL_SIZE/2, PADDING + CELL_SIZE * (y) + CELL_SIZE/2), CIRCLE_RADIUS)
  c.setFill('red')
  c.draw(win)

def drawThorn(x, y):
  c = Circle(Point(PADDING + CELL_SIZE * (x) + CELL_SIZE/2, PADDING + CELL_SIZE * (y) + CELL_SIZE/2), CIRCLE_RADIUS)
  c.setFill('green')
  c.draw(win)

def drawTiles(size):
  for x in range(size):
    for y in range(size):
      if (puzzle[x][y] == 0):
        continue
      if (puzzle[x][y] == 1):
        drawCherry(x, y)
      elif (puzzle[x][y] == -1):
        drawThorn(x, y)

def generateTiles(size):
  global puzzle
  puzzle = [[None for i in range(size)] for i in range(size)]
  for x in range(size):
    for y in range(size):
      if (x == 0 and y == 0 or x == size - 1 and y == size - 1):
        puzzle[x][y] = 0
        continue
      puzzle[x][y] = random.randint(-1, 1)

  prettyPrint(puzzle)
      

def drawGrid(size):
  global win

  def drawLine(p1, p2):
    line = Line(p1, p2)
    line.setWidth(LINE_THICKNESS)
    line.draw(win)

  win = GraphWin("Cherry Picking", PADDING * 2 + CELL_SIZE * size, PADDING * 2 + CELL_SIZE * size)

  for x in range(size + 1):
    drawLine(Point(PADDING + CELL_SIZE * x, PADDING), Point(PADDING + CELL_SIZE * x, PADDING + CELL_SIZE * size))

  for y in range(size + 1):
    drawLine(Point(PADDING, PADDING + CELL_SIZE * y), Point(PADDING + CELL_SIZE * size, PADDING + CELL_SIZE * y, ))

def GeneratePuzzle(size):
  drawGrid(size)
  if (puzzle == None):
    generateTiles(size)
  drawTiles(size)

def Solve():
  print('start solving')
  global pathsDown
  global pathsUp
  global puzzle

  def DFS(path, x, y):
    if (puzzle[x][y] == -1):
      return path
    path.append([x, y])
    if x < len(puzzle) - 1:
      DFS(path, x + 1, y)

    if y < len(puzzle) - 1:
      DFS(path, x, y + 1)
    if y == len(puzzle) - 1 and x == y:
      print(path)
      pathsDown.append(path.copy())
      pathsUp.append(path[::-1])
    
    path.pop()

    return path

  def CountCherriesOnPath(x, y):
    # on the way up ignore any cherries grabbed on the way down
    # keep track of current maximum number of cherries picked up
    # keep track of current combination of paths giving the maximum number of cherries
    cherries = 0
    for tile in pathsDown[x]:
      if (puzzle[tile[0]][tile[1]] == 1):
        cherries += 1
    for tile in pathsUp[y]:
      if (tile not in pathsDown[x] and puzzle[tile[0]][tile[1]] == 1):
        cherries += 1
    return cherries

  def CountAllCherries(paths):
    maxCherries = 0
    for x in range(paths):
      for y in range(paths):
        cherries = CountCherriesOnPath(x, y)
        if (cherries > maxCherries):
          maxCherries = cherries
    return maxCherries

  DFS([], 0, 0)
  print(str(len(pathsDown)) + ' paths found')
  cherries = CountAllCherries(len(pathsDown))
  print('cherries counted')
  print(cherries)
  # print maximum number of cherries


GeneratePuzzle(7)
time.sleep(3)
Solve()
win.getMouse()
win.close()