import pygame 
from settings import *

class NPC(pygame.sprite.Sprite):
  def __init__(self, game, scene, group, pos, z, name):
    super().__init__(group)
    self.game = game
    self.scene = scene
    self.z = z
    self.name = name
    self.frame_index = 0
    self.import_images(f'assets/characters/{self.name}/')
    self.image = self.animations['idle'][self.frame_index]
    self.rect = self.image.get_frect(topleft = pos)
    self.hitbox = self.rect.copy().inflate(-self.rect.width / 2, -self.rect.height / 2)
    self.speed = 60
    self.force = 2000
    self.acc = vec()
    self.vel = vec()
    self.fric = -15

  def import_images(self, path):
    self.animations = self.game.get_animations(path)
    for animation in self.animations.keys():
      full_path = path + animation
      self.animations[animation] = self.game.get_images(full_path)

  def animate(self, state, fps, loop=True):
    self.frame_index += fps
    if self.frame_index >= len(self.animations[state]):
      if loop:
        self.frame_index = 0
      else:
        self.frame_index = min(self.frame_index, len(self.animations[state]) - 1)

    self.image = self.animations[state][int(self.frame_index)]

  def get_collide_list(self, group):
    collidable_list = pygame.sprite.spritecollide(self, group, False)
    return collidable_list

  def collision(self, axis, group):
    for sprite in self.get_collide_list(group):
      if self.hitbox.colliderect(sprite.hitbox):
        if axis == 'x':
          if self.vel.x >= 0 : self.hitbox.right = sprite.hitbox.left
          if self.vel.x < 0 : self.hitbox.left = sprite.hitbox.right
          self.rect.centerx = self.hitbox.centerx
        if axis == 'y':
          if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top
          if self.vel.y < 0: self.hitbox.top = sprite.hitbox.bottom
          self.rect.centery = self.hitbox.centery

  def physics(self, dt):
    self.acc.x += self.vel.x * self.fric
    self.vel.x += self.acc.x * dt
    self.hitbox.centerx += self.vel.x * dt + (self.vel.x / 2) * dt
    self.rect.centerx = self.hitbox.centerx
    self.collision('x', self.scene.block_sprites)

    self.acc.y += self.vel.y * self.fric
    self.vel.y += self.acc.y * dt
    self.hitbox.centery += self.vel.y * dt + (self.vel.y / 2) * dt 
    self.rect.centery = self.hitbox.centery
    self.collision('y', self.scene.block_sprites)

    if self.vel.magnitude() >= self.speed:
      self.vel = self.vel.normalize() * self.speed


  def update(self, dt):
    self.physics(dt)
    if self.vel.magnitude() < 1:
      self.animate('idle', 15 * dt)
    else:
      self.animate('run', 15 * dt)

  def draw(self, screen):
    pass


class Player(NPC):
  def __init__(self, game, scene, group, pos, z, name):
    super().__init__(game, scene, group, pos, z, name)
  
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
    super().update(dt)

