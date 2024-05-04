import pygame 
from settings import *

class NPC(pygame.sprite.Sprite):
  def __init__(self, game, scene, group, pos, name):
    super().__init__(group)
    self.game = game
    self.scene = scene
    self.name = name
    self.image = pygame.Surface((TILESIZE, TILESIZE * 1.5))
    self.image.fill(COLORS['red'])
    self.rect = self.image.get_frect(topleft = pos)
    self.speed = 60
    self.force = 2000
    self.acc = vec()
    self.vel = vec()
    self.fric = -15

  def physics(self, dt):
    self.acc.x += self.vel.x * self.fric
    self.vel.x += self.acc.x * dt
    self.rect.centerx += self.vel.x * dt + (self.vel.x / 2) * dt

    self.acc.y += self.vel.y * self.fric
    self.vel.y += self.acc.y * dt
    self.rect.centery += self.vel.y * dt + (self.vel.y / 2) * dt

    if self.vel.magnitude() >= self.speed:
      self.vel = self.vel.normalize() * self.speed


  def update(self, dt):
    self.physics(dt)

  def draw(self, screen):
    pass


class Player(NPC):
  def __init__(self, game, scene, group, pos, name):
    super().__init__(game, scene, group, pos, name)
  
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

    
  def update(self, dt):
    self.movement()
    self.physics(dt)

