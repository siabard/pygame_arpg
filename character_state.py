from settings import * 
import pygame

class Idle:
  def __init__(self, character):
    character.from_index = 0

  def enter_state(self, character):
    if character.vel.magnitude() > 1:
      return Run(character)
    if INPUTS['right_click']:
      return Dash(character)

  def update(self, dt, character):
    character.do_animate(dt)
    character.movement()
    character.physics(dt, character.fric)


class Run:
  def __init__(self, character):
    Idle.__init__(self, character)

  def enter_state(self, character):
    if character.vel.magnitude() < 1:
      return Idle(character)
    
    if INPUTS['right_click']:
      return Dash(character)

  def update(self, dt, character):
    character.do_animate(dt)
    character.movement()
    character.physics(dt, character.fric)



class Dash:
  def __init__(self, character):
    Idle.__init__(self, character)
    INPUTS['right_click'] = False
    self.timer = 1
    self.dash_pending = False
    self.vel = character.vec_to_mouse(200)

  def enter_state(self, character):
    if INPUTS['right_click']:
      self.dash_pending = True 

    if self.timer <= 0:
      if self.dash_pending:
        return Run(character)
      else:
        return Idle(character)

  def update(self, dt, character):
    self.timer -= dt
    character.animate('dashing', 15 * dt, False)
    if character.get_direction() == 'left': character.image = pygame.transform.flip(character.image, True, False)

    character.physics(dt, -5)
    character.acc = vec()
    character.vel = self.vel