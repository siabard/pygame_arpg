import pygame 
from settings import * 

class State:
  def __init__(self, game):
    self.game = game
    self.prev_state = None 
  
  def enter_state(self):
    if len(self.game.states) > 1:
      self.prev_state = self.game.states[-1]
    self.game.states.append(self)

  def exit_state(self):
    self.game.states.pop()

  def update(self, dt):
    pass 

  def draw(self, screen):
    pass
  
class SplashScreen(State):
  def __init__(self, game):
    super().__init__(game)
  
  def update(self, dt):
    if INPUTS['space']:
      Scene(self.game).enter_state()
      self.game.reset_inputs()

  def draw(self, screen):
    screen.fill(COLORS['blue'])
    self.game.render_text('Splash Screen, Please Press Space', COLORS['white'], self.game.font, (WIDTH / 2, HEIGHT / 2), centered=True)


class Scene(State):
  def __init__(self, game):
    super().__init__(game)
  
  def update(self, dt):
     if INPUTS['space']:
      self.exit_state()
      self.game.reset_inputs() 

  def draw(self, screen):
    screen.fill(COLORS['green'])
    self.game.render_text('Welcome to the game scene', COLORS['black'], self.game.font, (WIDTH / 2, HEIGHT / 2), centered=True)