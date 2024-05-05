import pygame, sys
import os

from settings import *
from state import * 

class Game:
  def __init__(self):

    pygame.init()
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    self.font = pygame.font.Font(FONT, TILESIZE)
    self.running = True
    self.fps = 60

    # State machine
    self.states = []
    self.splash_screen = SplashScreen(self)
    self.states.append(self.splash_screen) 

  def render_text(self, text, color, font, pos, centered=False):
    surf = font.render(str(text), False, color)
    rect = surf.get_rect(center = pos) if centered else surf.get_rect(topleft = pos)
    self.screen.blit(surf, rect)

  def get_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        pygame.quit()
        sys.exit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          INPUTS['escape'] = True
          self.running = False 
        elif event.key == pygame.K_SPACE:
          INPUTS['space'] = True
        elif event.key in [pygame.K_a, pygame.K_LEFT]:
          INPUTS['left'] = True
        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
          INPUTS['right'] = True
        elif event.key in [pygame.K_w, pygame.K_UP]:
          INPUTS['up'] = True
        elif event.key in [pygame.K_s, pygame.K_DOWN]:
          INPUTS['down'] = True
        elif event.key == pygame.K_LCTRL:
          INPUTS['left_click'] = True
        elif event.key == pygame.K_RCTRL:
          INPUTS['right_click'] = True


      if event.type == pygame.KEYUP:
        if event.key == pygame.K_ESCAPE:
          INPUTS['escape'] = False
        elif event.key == pygame.K_SPACE:
          INPUTS['space'] = False
        elif event.key in [pygame.K_a, pygame.K_LEFT]:
          INPUTS['left'] = False
        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
          INPUTS['right'] = False
        elif event.key in [pygame.K_w, pygame.K_UP]:
          INPUTS['up'] = False
        elif event.key in [pygame.K_s, pygame.K_DOWN]:
          INPUTS['down'] = False

      if event.type == pygame.MOUSEWHEEL:
        if event.y == 1:
          INPUTS['scroll_up'] = True
        elif event.y == -1:
          INPUTS['scroll_down'] = True

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          INPUTS['left_click'] = True
        elif event.button == 3:
          INPUTS['right_click'] = True
        elif event.button == 4:
          INPUTS['scroll_up'] = True
        elif event.button == 2:
          INPUTS['scroll_down'] = True
      
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          INPUTS['left_click'] = False
        elif event.button == 3:
          INPUTS['right_click'] = False
        elif event.button == 4:
          INPUTS['scroll_up'] = False
        elif event.button == 2:
          INPUTS['scroll_down'] = False

  def get_images(self, path):
    images = []
    for file_name in os.listdir(path):
      if file_name.endswith('.png'):
        images.append(pygame.image.load(path + '/' + file_name).convert_alpha())
    return images

  def get_animations(self, path):
    animations = {}
    for file_name in os.listdir(path):
      animations.update({file_name: self.get_images(path + file_name)})
    return animations
  
  def reset_inputs(self):
    for key in INPUTS:
      INPUTS[key] = False

  def loop(self):
    while self.running:
      dt = self.clock.tick(self.fps) / 1000
      self.get_input()
      self.update(dt)
      self.draw()
      self.custom_cursor(self.screen)
      pygame.display.update() 

  def update(self, dt):
    self.states[-1].update(dt)

  def draw(self):
    self.states[-1].draw(self.screen)

  def custom_cursor(self, screen):
    pygame.mouse.set_visible(False)
    cursor_img = pygame.image.load('assets/cursor.png').convert_alpha()
    cursor_img.set_alpha(150)
    cursor_rect = cursor_img.get_rect(center=pygame.mouse.get_pos())
    screen.blit(cursor_img, cursor_rect.center)

if __name__ == '__main__':
  game = Game()
  game.loop()