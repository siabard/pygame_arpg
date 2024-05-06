import pygame 
from settings import *
from character_state import *

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
    self.move = {'left': False, 'right': False, 'up': False, 'down': False}
    self.state = Idle(self)

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

  def get_direction(self):
    angle = self.vel.angle_to(vec(0, 1))
    angle = (angle + 360) % 360

    if 45 <= angle < 135: return "right"
    elif 135 <= angle < 225: return "up"
    elif 225 <= angle < 315: return "left"
    else: return "down"
  
  def movement(self):
    self.acc.x = 0
    self.acc.y = 0

    if self.move['left']: self.acc.x += -self.force
    if self.move['right']: self.acc.x += -self.force
    if self.move['up']: self.acc.y += -self.force
    if self.move['down']: self.acc.y += self.force

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

  def physics(self, dt, fric):
    self.acc.x += self.vel.x * fric
    self.vel.x += self.acc.x * dt
    self.hitbox.centerx += self.vel.x * dt + (self.vel.x / 2) * dt
    self.rect.centerx = self.hitbox.centerx
    self.collision('x', self.scene.block_sprites)

    self.acc.y += self.vel.y * fric
    self.vel.y += self.acc.y * dt
    self.hitbox.centery += self.vel.y * dt + (self.vel.y / 2) * dt 
    self.rect.centery = self.hitbox.centery
    self.collision('y', self.scene.block_sprites)

    if self.vel.magnitude() >= self.speed:
      self.vel = self.vel.normalize() * self.speed

  def change_state(self):
    new_state = self.state.enter_state(self)
    if new_state: self.state = new_state
    else: self.state 

  def do_animate(self, dt):
    if self.vel.magnitude() < 1:
      self.animate('idle', 15 * dt)
    else:
      self.animate('run', 15 * dt)
    
    if self.get_direction() == 'left': self.image = pygame.transform.flip(self.image, True, False)


  def update(self, dt):
    self.change_state()
    self.state.update(dt, self)

