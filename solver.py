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
centers = 0  # Not actually used until yellows method

DELAY = 0.01  # Delay between presses (for seeing the solve in action)

def log(row, col):  # Press a button and log it
  global presses, press, centers
  time.sleep(DELAY)  # Wait, then press
  cell = " " + LETTERS[col] + str(row + 1)
  if(cell == " C3"):  # Center detection
    centers += 1
    centers %= 6
  #print(cell[1:])  # Logging part
  presses += cell
  press(row, col, True)

def finish():  # Finish the solve, including unlocking buttons
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
  global state, trial, digit, color
  for test_color in range(0, 6):
    cells = ""  # Get each color's pattern
    for row in trial:
      for cell in row:
        cells += "█" if cell == test_color else " "
    for test_digit in range(0, 10):  # Check all digits
      if(cells == NUMBERS[test_digit]):  # Formation found!
        print("A formation was found in the grid! (may print multiple times)")
        return 1 if test_digit == digit and color ==\
          test_color else -1  # Check if it matches the target
  return 0  # No formation found in any color/digit combo

def check(row, col=None):  # Press something and check it, workaround if needed
  global press, reset
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
  reset()  # Update trial grid with actual press/es
  return result == 1

def workaround(row, col):  # If an incorrect digit is made, avoid it
  print("Error: workaround not implemented!")
  exit(2)

# The main solve method, which is broken into parts
def solve(_buttons, _extras, _state, _trial, _press, _reset, _digit, _color):
  # Declaration of all global variables (except centers)
  global buttons, extras, state, trial, press, reset, digit, color, presses, STEP
  buttons, extras, state, trial, press, reset, digit, color, presses, STEP =\
    _buttons, _extras, _state, _trial, _press, _reset, _digit, _color, "", 1
  if(_check() == 1):  # Already solved?
    print("Already solved? Really?")
    return presses
  corners()  # A1, A5, E1, E5
  if(_check() == 1): return finish()
  STEP = 2
  edges()  # A3, C1, C5, E3
  if(_check() == 1): return finish()
  STEP = 3
  ace135()  # C3 + finish ACE135 setup
  if(_check() == 1): return finish()
  STEP = 4
  midedges()  # B3, C2, C4, D3
  if(_check() == 1): return finish()
  STEP = 5
  greens()  # A2, A4, E2, E4
  if(_check() == 1): return finish()
  STEP = 6
  cyans()  # B1, B5, D1, D5
  if(_check() == 1): return finish()
  STEP = 7
  yellows()  # B2, B4, D2, D4
  if(_check() != 1):  # Failed to solve?
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

def make_magenta(row=2, col=2):  # Way of magenta creating/pressing
  cell = magenta(state)  # (Defaults to using center)
  while(cell[0] == -1):
    check(row, col)
    cell = magenta(state)
  check(cell)

# Main solve step 1
def corners():
  global state
  # Data in order (row, col, altering_row, altering_col)
  for corner in ((0, 0, 1, 0), (0, 4, 0, 3), (4, 0, 4, 1), (4, 4, 3, 4)):
    # 1. Set up cells adjacent to the corners (helpful here and later)
    while(state[corner[2]][corner[3]] != 0):
      # To do that, get the corner to red/blue and hit it
      while(state[corner[0]][corner[1]] not in (0, 4)):
        make_magenta()
      check(corner[0], corner[1])
    # 2. Get the corner to the same state as A1
    while(state[corner[0]][corner[1]] != state[0][0]):
      check(corner[2], corner[3])

# Main solve step 2
def edges():
  global state
  # 1. Get all corners to red/blue and hit each of them once
  while(state[0][0] not in (0, 4)):
    make_magenta()
  hit_corners()
  # Now the altering cells from step 1 are all yellow
  # Data in order (row, col, mid_row, mid_col, altering_row, altering_col)
  for edge in ((0, 2, 1, 2, 0, 3), (2, 0, 2, 1, 1, 0), (
    2, 4, 2, 3, 3, 4), (4, 2, 3, 2, 4, 1)):
    # 2. Set up the mid-edges (helpful here and later)
    while(state[edge[2]][edge[3]] != 0):
      # This is known to be yellow
      check(edge[4], edge[5])
    # 3. Get the edge to the same state as A1
    while(state[edge[0]][edge[1]] != state[0][0]):
      check(edge[2], edge[3])

# Main solve step 3
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
      make_magenta()
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
        make_magenta()
      check(4, 0)
    check(3, 1)

# Main solve step 4
def midedges():
  global state, digit, color
  # Data in order (row, col, altering_row, altering_col, corner_row, corner_col)
  for midedge in ((1, 2, 0, 3, 0, 4), (2, 1, 1, 0, 0, 0), (
    2, 3, 3, 4, 4, 4), (3, 2, 4, 1, 4, 0)):
    # While the mid-edge is (aligned if absent / disaligned if present)...
    while((state[midedge[0]][midedge[1]] == color) == (
      NUMBERS[digit][midedge[0] * 5 + midedge[1]] == " ")):
      # Set its altering cell to yellow using a corner then alter the mid-edge
      while(state[midedge[2]][midedge[3]] != 1):
        # The corner must be red/blue first, use another corner to make magenta
        while(state[midedge[4]][midedge[5]] not in (0, 4)):
          make_magenta(4, (4 if midedge[0] == 3 else 0))
        check(midedge[4], midedge[5])
      check(midedge[2], midedge[3])

# Main solve step 5
def greens():  # Short for "altered by green corners"
  global state, digit, color
  # Data in order (row, col, corner_row, corner_col)
  for green in ((1, 0, 0, 0), (1, 4, 0, 4), (3, 0, 4, 0), (3, 4, 4, 4)):
    # While the green is (aligned if absent / disaligned if present)...
    while((state[green[0]][green[1]] == color) == (
      NUMBERS[digit][green[0] * 5 + green[1]] == " ")):
      # Set its corner to green and hit it
      while(state[green[2]][green[3]] != 2):
        make_magenta()
      check(green[2], green[3])

# Main solve step 6
def cyans():  # Short for "altered by cyan corners"
  global state, digit, color
  # Data in order (row, col, corner_row, corner_col)
  for cyan in ((0, 1, 0, 0), (0, 3, 0, 4), (4, 1, 4, 0), (4, 3, 4, 4)):
    # While the cyan is (aligned if absent / disaligned if present)...
    while((state[cyan[0]][cyan[1]] == color) == (
      NUMBERS[digit][cyan[0] * 5 + cyan[1]] == " ")):
      # Set its corner to cyan and hit it
      while(state[cyan[2]][cyan[3]] != 3):
        make_magenta()
      check(cyan[2], cyan[3])
  # Also fix mid-edges here for easy checking (max 6 checks/5 presses)
  for i in range(0, 5):
    aligned = True  # Alignment test
    for midedge in ((1, 2), (2, 1), (2, 3), (3, 2)):
      if((state[midedge[0]][midedge[1]] == color) == (
        NUMBERS[digit][midedge[0] * 5 + midedge[1]] == " ")):
        aligned = False
        break
    if(aligned):  # If aligned, return, otherwise try again
      return
    if(i == 5):  # If not aligned after 5 presses, something's wrong
      print("Warning: Mid-edge fixing in cyans method failed!")
      return
    check(2, 2)

# Main solve step 7 (last step)
def yellows():  # Short for "altered by yellow corners"
  global state, digit, color, centers
  # Fast way for yellow center
  if(state[2][2] == 1):
    # Dis/align the corners to the target color depending on the digit
    # (1: while aligned, alter / else: while unaligned, alter)
    while((state[0][0] == color) == (digit == 1)):
      make_magenta()
    # Already solved?
    if(_check() == 1):
      return
    # If not, press center to solve (max 4 presses)
    for i in range(0, 4):
      if(check(2, 2)):
        return
    # If that fails, something's wrong
    print("Warning: Yellow center solve in yellows method failed!")
    return
  # Normal way (actually uses corners)
  # Data in order (row, col, corner_row, corner_col)
  centers = 0  # Start tracking center presses
  for yellow in ((1, 1, 0, 0), (1, 3, 0, 4), (3, 1, 4, 0), (3, 3, 4, 4)):
    # While the yellow is aligned (since yellows are always absent)...
    while((state[yellow[0]][yellow[1]] - centers + 6) % 6 == color):
      # Set its corner to yellow and hit it
      while(state[yellow[2]][yellow[3]] != 1):
        make_magenta()
      check(yellow[2], yellow[3])
  # Fix corners and possibly cells near center
  while((state[0][0] == color) == (digit == 1)):
    make_magenta()
  # Already solved?
  if(_check() == 1):
    return
  for i in range(0, 5):  # Max 5 presses
    if(check(2, 2)):
      return
  # If that fails, something's wrong
  print("Warning: Non-yellow center solve in yellows method failed!")