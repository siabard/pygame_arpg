import pygame
from settings import * 

class Transition:
  def __init__(self, scene):
    self.scene = scene
    self.fade_surf = pygame.Surface((WIDTH, HEIGHT))
    self.exiting = False 
    self.fade_speed = 200
    self.alpha = 255
  
  def update(self, dt):
    if self.exiting:
      self.alpha = min(255, self.alpha + self.fade_speed * dt)
      if self.alpha >= 255:
        self.scene.go_to_scene()
    else:
      self.alpha = max(0, self.alpha - self.fade_speed * dt)
  
  def draw(self, screen):
    self.fade_surf.fill(COLORS['black'])
    self.fade_surf.set_alpha(self.alpha)
    screen.blit(self.fade_surf, (0, 0))