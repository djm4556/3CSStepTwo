# State, and trial are 5*5 arrays of colors, 012345 = RYGCBM for both
# Press takes (row, col, actual), use actual=False for trial
# Reset takes no arguments, use after trial checks

import time
COLORS = "RYGCBM"
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

def log(row, col):  # Make a press and log it
  presses += (" " + LETTERS[col] + str(row + 1))
  press(row, col, True)
  time.sleep(DELAY)

def _check():  # Check without pressing (1 if good, 0 if neutral, -1 if bad)
  for test_color in range(0, 6):
    cells = ""  # Get each color's pattern
    for row in state:
      for cell in row:
        cells += "█" if cell == test_color else " "
    for test_digit in range(0, 10):  # Check all digits
      if(cells == NUMBERS[test_digit]):  # Formation found!
        print("A formation was found in the grid!")
        return 1 if test_digit == digit and color in COLORS[
          test_color] + "APS" else -1  # Check if it matches the target
  return 0  # No formation found in any color/digit combo

def check(row, col):  # Press something and check it, workaround if needed
  press(row, col, False)
  result = _check()
  if(result == -1):
    workaround(row, col)
    result = _check()
    if(result == -1):
      print("Error: workaround failed to avoid incorrect formation!")
      exit(1)
  log(row, col)
  return result == 1

def workaround(row, col):  # If an incorrect digit is made, avoid it
  print("Error: workaround not implemented!")
  exit(2)

def solve(_state, _trial, _press, _reset, _digit, _color):
  # Declaration of all global variables
  global state, trial, press, reset, digit, color, presses, STEP
  state, trial, press, reset, digit, color, presses, STEP =\
    _state, _trial, _press, _reset, _digit, _color, "", 1
  if(_check() == 1):  # Already solved?
    print("Already solved? Really?")
    return presses
  
  # Comment out when testing easy digits
  if(str(digit) in "0147"):
    print("Easy digits are not fully coded yet!")
    return presses  # Note: it may be required to solve for easy digits
  
  corners()  # A1, A5, E1, E5
  if(_check == 1): return presses
  STEP = 2
  edges()  # A3, C1, C5, E3
  if(_check == 1): return presses
  STEP = 3
  ace135()  # C3 + finish ACE135 setup
  if(_check == 1): return presses
  STEP = 4
  midedges()  # B3, C2, C4, D3
  if(_check == 1): return presses
  STEP = 5
  greens()  # A2, A4, E2, E4
  if(_check == 1): return presses
  STEP = 6
  cyans()  # B1, B5, D1, D5
  if(_check == 1): return presses
  STEP = 7
  yellows()  # B2, B4, D2, D4
  if(_check != 1):  # Failed to solve?
    print("Warning: algorithm failed to solve formation!")
  return presses  # Return list of presses no matter what

def corners():
  pass

def edges():
  pass

def ace135():
  pass

def midedges():
  pass

def greens():
  pass

def cyans():
  pass

def yellows():
  pass