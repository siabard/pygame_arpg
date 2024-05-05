from pygame.math import Vector2 as vec 


WIDTH, HEIGHT = 400, 224
TILESIZE = 16
FONT = 'assets/pixel_emulator.ttf'

# Dictionary for key bindings
INPUTS = {
  'escape': False,
  'space': False,
  'up': False,
  'down': False, 
  'left': False,
  'right': False,
  'left_click': False,
  'right_click': False,
  'scroll_up': False,
  'scroll_down': False
}

# Dictionary for colors
COLORS = {
  'black': (0, 0, 0),
  'white': (255, 255, 255),
  'red': (255, 100, 100),
  'green': (100, 255, 100),
  'blue': (100, 100, 255),
}