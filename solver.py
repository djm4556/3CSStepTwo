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

DELAY = 1

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
  log(row, col)  # Actual press
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
  
  # Comment out when testing easy digits
  if(digit in (0, 1, 4, 7)):
    print("Easy digits are not fully coded yet!")
    return finish()  # Note: it may be required to solve for easy digits
  
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

def magenta(board):
  for row in range(0, 5):
    for col in range(0, 5):
      if(board[row][col] == 5):
        return row, col
  return -1, -1

def center_make_magenta(board):
  cell = magenta(board)
  while(cell[0] == -1):
    check(2, 2)
    cell = magenta(board)
  check(cell)

def corners():
  global state, trial, digit, color
  magentas = 6  # Track number of times magenta was pressed (6=0)
  for corner in ((0, 0, 0, 1), (0, 4, 1, 4), (4, 0, 3, 0), (4, 4, 4, 3)):
  # Corner data in order (row, col, altering_row, altering_col)
    while(state[corner[2]][corner[3]] != 0):
    # Set up cells adjacent to the corners
      while(state[corner[0]][corner[1]] not in (0, 4)):
        # To do that, get the corner to red/blue and hit it
        center_make_magenta(state)
        magentas %= 6
        magentas += 1
      check(corner[0], corner[1])
    while((state[corner[0]][corner[1]] + 6 - magentas) % 6 != color):
    # Get the corner to its target state relative to magenta presses
    # (+6 prevents possible negative modulo issues)
      check(corner[2], corner[3])
  # Finally, undo all the magentas
  for i in range(0, 6-magentas):
    center_make_magenta(state)

def edges():
  global state, trial, digit, color
  return

def ace135():
  global state, trial, digit, color
  return

def midedges():
  global state, trial, digit, color
  return

def greens():
  global state, trial, digit, color
  return

def cyans():
  global state, trial, digit, color
  return

def yellows():
  global state, trial, digit, color
  return