from settings import *
from characters import NPC
from state import *
from character_state import * 

class Player(NPC):
  def __init__(self, game, scene, group, pos, z, name):
    super().__init__(game, scene, group, pos, z, name)
    self.state = Idle(self)
  
  def movement(self):
    self.acc.x = 0
    self.acc.y = 0

    if INPUTS['left']:
      self.acc.x += -self.force
    if INPUTS['right']:
      self.acc.x += self.force
    if INPUTS['up']:
      self.acc.y += -self.force 
    if INPUTS['down']:
      self.acc.y += self.force
    
  def do_animate(self, dt):
    if self.vel.magnitude() < 1:
      self.animate('idle', 15 * dt)
    else:
      self.animate('run', 15 * dt)
    
    if self.get_direction() == 'left': self.image = pygame.transform.flip(self.image, True, False)

  def vec_to_mouse(self, speed):
    mouse = pygame.mouse.get_pos()
    direction = vec(mouse) - vec(self.rect.center) + vec(self.scene.camera.offset)  
    if direction.length() > 0: direction.normalize_ip()
    return direction * speed
  
  def exit_scene(self):
    for exit in self.scene.exit_sprites:
      if self.hitbox.colliderect(exit.rect):
        self.scene.new_scene = SCENE_DATA[int(self.scene.current_scene)][int(exit.number)]
        self.scene.entry_point = exit.number
        self.scene.transition.exiting = True
        
  def update(self, dt):
    self.get_direction()
    self.exit_scene()
    self.change_state()
    self.state.update(dt, self)