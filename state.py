import pygame 
from player import Player
from transition import *
from settings import * 
from characters import *
from objects import  Wall, Collider
from camera import Camera
from pytmx.util_pygame import load_pygame
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
      Scene(self.game, '0', '0').enter_state()
      self.game.reset_inputs()

  def draw(self, screen):
    screen.fill(COLORS['blue'])
    self.game.render_text('Splash Screen, Please Press Space', COLORS['white'], self.game.font, (WIDTH / 2, HEIGHT / 2), centered=True)


class Scene(State):
  def __init__(self, game, current_scene, entry_point):
    super().__init__(game)

    self.current_scene = current_scene
    self.entry_point = entry_point

    self.camera = Camera(self)
    self.update_sprites = pygame.sprite.Group()
    self.drawn_sprites = pygame.sprite.Group()
    self.block_sprites = pygame.sprite.Group()
    self.exit_sprites = pygame.sprite.Group()

    self.transition = Transition(self)

    self.tmx_data = load_pygame(f'scenes/{current_scene}/{current_scene}.tmx')
    self.create_scene()
  
  def create_scene(self):
    layers = []
    for layer in self.tmx_data.layers:
      layers.append(layer.name)

    if 'blocks' in layers:
      for x, y, surf  in self.tmx_data.get_layer_by_name('blocks').tiles():
        Wall([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), 'blocks', surf)
    
    if 'entries' in layers:
      for obj in self.tmx_data.get_layer_by_name('entries'):
        if obj.name == self.entry_point:
          self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'player')
          self.target = self.player

    if 'exits' in layers:
      for obj in self.tmx_data.get_layer_by_name('exits'):
        Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

    if 'entities' in layers:
      for obj in self.tmx_data.get_layer_by_name('entities'):
        if obj.name == "npc":
          self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'npc')

  def update(self, dt):
    self.update_sprites.update(dt)
    self.camera.update(dt, self.target)
    self.transition.update(dt)

  def draw(self, screen):
    self.camera.draw(screen, self.drawn_sprites)
    self.transition.draw(screen)
    self.debugger([
      str('FPS: ' + str(round(self.game.clock.get_fps(), 2))),
      str('Vel: ' + str(round(self.player.vel, 2))),
      str('Ang: ' + str(self.player.get_direction())),
      str('State: ' + str(self.player.state))
    ])
  
  def debugger(self, debug_list):
    for index, name in enumerate(debug_list):
      self.game.render_text(name, COLORS['white'], self.game.font, (10, 20 * index ), centered=False)
  
  def go_to_scene(self):
    Scene(self.game, self.new_scene, self.entry_point).enter_state()