# State, and trial are 5*5 arrays of colors, 012345 = RYGCBM for both
# Press takes (row, col, actual), use actual=False for trial
# Reset takes no arguments, use after trial checks

import tkinter as tk
import time
LETTERS = "ABCDE"
NUMBERS = [
  "█████"+
  "█   █"+
  "█   █"+
  "█   █"+
  "█████",

  "  █  "+
  "  █  "+
  "  █  "+
  "  █  "+
  "  █  ",

  "█████"+
  "    █"+
  "█████"+
  "█    "+
  "█████",

  "█████"+
  "    █"+
  "█████"+
  "    █"+
  "█████",

  "█   █"+
  "█   █"+
  "█████"+
  "    █"+
  "    █",

  "█████"+
  "█    "+
  "█████"+
  "    █"+
  "█████",

  "█████"+
  "█    "+
  "█████"+
  "█   █"+
  "█████",

  "█████"+
  "    █"+
  "    █"+
  "    █"+
  "    █",

  "█████"+
  "█   █"+
  "█████"+
  "█   █"+
  "█████",

  "█████"+
  "█   █"+
  "█████"+
  "    █"+
  "█████"
]  # Formations of 3CS digits (big)

DELAY = 0.5

def log(row, col):
  global presses, press
  time.sleep(DELAY)  # Wait, then press
  cell = " " + LETTERS[col] + str(row + 1)
  print(cell[1:])  # Logging part
  presses += cell
  press(row, col, True)

def finish():
  global presses, buttons, extras
  print("press" + (" [no presses needed]" if presses == "" else presses))
  for row in buttons:
    for button in row:
      button["state"] = tk.NORMAL
  for button in extras:
    button["state"] = tk.NORMAL
  print("SOLVE COMPLETE - BUTTONS UNLOCKED")
  return None

def _check():  # Check without pressing (1 if good, 0 if neutral, -1 if bad)
  global state, digit, color
  for test_color in range(0, 6):
    cells = ""  # Get each color's pattern
    for row in state:
      for cell in row:
        cells += "█" if cell == test_color else " "
    for test_digit in range(0, 10):  # Check all digits
      if(cells == NUMBERS[test_digit]):  # Formation found!
        print("A formation was found in the grid!")
        return 1 if test_digit == digit and color ==\
          test_color else -1  # Check if it matches the target
  return 0  # No formation found in any color/digit combo

def check(row, col=None):  # Press something and check it, workaround if needed
  global press
  if(col == None):  # Array extraction
    col = row[1]
    row = row[0]
  press(row, col, False)  # Trial press
  result = _check()
  if(result == -1):  # Workaround
    workaround(row, col)
    result = _check()
    if(result == -1):  # Workaround failure?
      print("Error: workaround failed to avoid incorrect formation!")
      exit(1)
  else:  # Actual press (safe)
    log(row, col)
  return result == 1

def workaround(row, col):  # If an incorrect digit is made, avoid it
  print("Error: workaround not implemented!")
  exit(2)

def solve(_buttons, _extras, _state, _trial, _press, _reset, _digit, _color):
  # Declaration of all global variables
  global buttons, extras, state, trial, press, reset, digit, color, presses, STEP
  buttons, extras, state, trial, press, reset, digit, color, presses, STEP =\
    _buttons, _extras, _state, _trial, _press, _reset, _digit, _color, "", 1
  if(_check() == 1):  # Already solved?
    print("Already solved? Really?")
    return presses
  corners()  # A1, A5, E1, E5
  if(_check == 1): return finish()
  STEP = 2
  edges()  # A3, C1, C5, E3
  if(_check == 1): return finish()
  STEP = 3
  ace135()  # C3 + finish ACE135 setup
  if(_check == 1): return finish()
  STEP = 4
  midedges()  # B3, C2, C4, D3
  if(_check == 1): return finish()
  STEP = 5
  greens()  # A2, A4, E2, E4
  if(_check == 1): return finish()
  STEP = 6
  cyans()  # B1, B5, D1, D5
  if(_check == 1): return finish()
  STEP = 7
  yellows()  # B2, B4, D2, D4
  if(_check != 1):  # Failed to solve?
    print("Warning: algorithm failed to solve formation!")
  return finish()  # Print presses even if failed to solve

def hit_corners():  # Helper method for hitting all four corners
  check(0, 0)
  check(0, 4)
  check(4, 0)
  check(4, 4)

def hit_altering():  # Helper method for hitting all altering cells from step 1
  check(0, 3)
  check(1, 0)
  check(3, 4)
  check(4, 1)

def magenta(board):  # Magenta detection (all magentas work the same)
  for row in range(0, 5):
    for col in range(0, 5):
      if(board[row][col] == 5):
        return row, col
  return -1, -1

def center_make_magenta():  # One way of magenta creation/pressing
  cell = magenta(state)
  while(cell[0] == -1):
    check(2, 2)
    cell = magenta(state)
  check(cell)

def corners():
  global state
  # Corner data in order (row, col, altering_row, altering_col)
  for corner in ((0, 0, 1, 0), (0, 4, 0, 3), (4, 0, 4, 1), (4, 4, 3, 4)):
    # 1. Set up cells adjacent to the corners (helpful here and later)
    while(state[corner[2]][corner[3]] != 0):
      # To do that, get the corner to red/blue and hit it
      while(state[corner[0]][corner[1]] not in (0, 4)):
        center_make_magenta()
      check(corner[0], corner[1])
    # 2. Get the corner to the same state as A1
    while(state[corner[0]][corner[1]] != state[0][0]):
      check(corner[2], corner[3])

def edges():
  global state
  # 1. Get all corners to red/blue and hit each of them once
  while(state[0][0] not in (0, 4)):
    center_make_magenta()
  hit_corners()
  # Now the altering cells from step 1 are all yellow
  # Edge data in order (row, col, mid_row, mid_col, altering_row, altering_col)
  for edge in ((0, 2, 1, 2, 0, 3), (2, 0, 2, 1, 1, 0), (
    2, 4, 2, 3, 3, 4), (4, 2, 3, 2, 4, 1)):
    # 2. Set up the mid-edges (helpful here and later)
    while(state[edge[2]][edge[3]] != 0):
      # This is known to be yellow
      check(edge[4], edge[5])
    # 3. Get the edge to the same state as A1
    while(state[edge[0]][edge[1]] != state[0][0]):
      check(edge[2], edge[3])

def ace135():
  global state, digit, color
  # 1. Hit all corners 5 times
  for i in range(0, 5):
    hit_corners()
  global DELAY
  #DELAY = 1
  # Now the altering cells are red again
  # 2A. If the digit is 0, a separate order of alterations can make it faster
  if(digit == 0):
    # First ensure the center isn't the target color
    # (Keep alignment of the edges and corners together!)
    if(state[2][2] == color):
      check(1, 2)
      check(2, 1)
      check(2, 3)
      check(3, 2)
      center_make_magenta()
    # Then simply use the altering cells to make the 0 correctly colored
    while(state[0][0] != color):
      hit_altering()
    return
  # 2. Align the center and other squares (useless if digit is 4)
  while(state[0][0] != state[2][2] and digit != 4):
    hit_altering()
  # 3. Get the edges to the target color
  # (Center will remain aligned if both possible and desired)
  while(state[0][2] != color):
    check(1, 2)
    check(2, 1)
    check(2, 3)
    check(3, 2)
  # 4. Fix certain squares for certain digits
  if(digit == 1):
    # For 1, disalign the left and right edges (and corners in step 5)
    check(2, 1)
    while(state[2][2] != color):
      check(2, 3)
  elif(digit == 4):
    # For 4, disalign the top and bottom edges, and the BL corner
    check(1, 2)
    while(state[2][2] != color):  # Also align center here
      check(3, 2)
    while(state[4][2] == color or state[4][0] == state[0][0]):
      check(4, 1)
  elif(digit == 7):
    # For 7, disalign the cells that aren't on the top or right edge
    # B4's diagonals are those exact cells, so hit B4
    while(state[3][1] in (0, 5)):
      # Of course, it can't be red/magenta when hit
      while(state[4][0] in (0, 5)):
        center_make_magenta()
      check(4, 0)
    check(3, 1)
  # 5. Dis/align the corners to the target color depending on the digit
  # (1: while aligned, alter / else: while unaligned, alter)
  while((state[0][0] == color) == (digit == 1)):
    # Don't use A5 to check the corner states, it may need to be disaligned
    center_make_magenta()

def midedges():
  global state, digit, color
  return

def greens():
  global state, digit, color
  return

def cyans():
  global state, digit, color
  return

def yellows():
  global state, digit, color
  return