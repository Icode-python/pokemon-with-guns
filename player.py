from os import walk
import random

from pygame import sprite
from pygame.constants import JOYBUTTONDOWN
from tiles import Wall
import pygame
from settings import *
from particles import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, weapon="none"):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = PLAYER_HEALTH
        #self.walkDown = [pygame.image.load('assets/WalkDown1.png').convert_alpha(), pygame.image.load('assets/WalkDown2.png').convert_alpha(), pygame.image.load('assets/WalkDown3.png').convert_alpha(), pygame.image.load('assets/WalkDown4.png').convert_alpha()]
        #self.walkUp = [pygame.image.load('assets/WalkUp1.png').convert_alpha(),pygame.image.load('assets/WalkUp2.png').convert_alpha(),pygame.image.load('assets/WalkUp3.png').convert_alpha(),pygame.image.load('assets/WalkUp4.png').convert_alpha()]
        #self.walkLeft = [pygame.image.load('assets/WalkLeft1.png').convert_alpha(),pygame.image.load('assets/WalkLeft2.png').convert_alpha(),pygame.image.load('assets/WalkLeft3.png').convert_alpha(),pygame.image.load('assets/WalkLeft4.png').convert_alpha(),]
        #self.walkRight =[pygame.image.load('assets/WalkRight1.png').convert_alpha(),pygame.image.load('assets/WalkRight2.png').convert_alpha(),pygame.image.load('assets/WalkRight3.png').convert_alpha(),pygame.image.load('assets/WalkRight4.png').convert_alpha(),]

        #self.image = self.walkDown[0]
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.standleft = False
        self.standright = False
        self.standdown = True
        self.standup = False

        self.standing = True
        self.weapon = weapon
        self.weaponCoolDown = 5
        self.moveDelay = 0
        self.Battling = False
        self.walkCount = 0
        self.spriteChangeDelay = 0

        self.step = 1

    def update(self):
        self.collide_etc()
        self.get_keys()
        #self.draw()
        #self.rect.center = self.x * TILESIZE, self.y * TILESIZE
        self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE
        #self.walkDown.draw(self.game.screen,  index %s, self.walkDown.totalCells, )
    
    def draw(self):
        if self.walkCount + 1 >= 4:
            self.walkCount = 0
        if self.spriteChangeDelay >= 5:
            self.walkCount += 1
        if not(self.standing):
            if self.left:
                self.image = self.walkLeft[self.walkCount]
                self.spriteChangeDelay += 1 
            if self.right:
                self.image = self.walkRight[self.walkCount]
                self.spriteChangeDelay += 1 
            if self.up:
                self.image = self.walkUp[self.walkCount]
                self.spriteChangeDelay += 1 
            if self.down:
                self.image = self.walkDown[self.walkCount]
                self.spriteChangeDelay += 1
            
        else:
            if self.left:
                self.image = self.walkLeft[0]
            if self.right:
                self.image = self.walkRight[0]
            if self.up:
                self.image = self.walkUp[0]
            if self.down:
                self.image = self.walkDown[0]


    def move(self, dx, dy):
        self.moveDelay += 1
        if self.moveDelay >= PLAYER_SPEED and not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.moveDelay = 0
            self.footsteps()
            
    def footsteps(self):
        self.step = self.step * -1
        if self.down or self.up:
            Particle(self.game, self.rect.centerx + PARTICLEOFFSET * self.step, self.rect.centery, [WHITE, LIGHTGREY], None, False, PARTICLETIME)
        else:
            Particle(self.game, self.rect.centerx, self.rect.centery + PARTICLEOFFSET * self.step, [WHITE, LIGHTGREY], None, False, PARTICLETIME)

    def get_keys(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.standleft == False and self.standright == False and self.standdown == False:
                self.move(0, -1)
                self.up = True
                self.down = False
                self.left = False
                self.right = False

                self.standleft = False
                self.standright = False
                self.standdown = False
                self.standup = True
        if keys[pygame.K_s]:
            if self.standleft == False and self.standright == False and self.standup == False:
                self.move(0, 1)
                self.up = False
                self.down = True
                self.left = False
                self.right = False
                
                self.standleft = False
                self.standright = False
                self.standdown = True
                self.standup = False
        if keys[pygame.K_a]:
            if self.standdown == False and self.standright == False and self.standup == False:
                self.move(-1, 0)
                self.up = False
                self.down = False
                self.left = True
                self.right = False

                self.standleft = False
                self.standright = False
                self.standdown = True
                self.standup = False
        if keys[pygame.K_d]:
            if self.standleft == False and self.standdown == False and self.standup == False:
                self.move(1, 0)
                self.up = False
                self.down = False
                self.left = False
                self.right = True
                
                self.standleft = False
                self.standright = True
                self.standdown = False
                self.standup = False
        
        if keys[pygame.K_SPACE]:
            if len(self.game.Bullets) < self.weaponCoolDown:
                if self.weapon == "bullet":
                    self.game.bulletsound.play()      
                    if self.up is True:
                        Bullet(self.game,self.rect.centerx,self.rect.centery,0,-10,)
                    if self.down is True:
                        Bullet(self.game,self.rect.centerx,self.rect.centery,0,10,)
                    if self.right is True:
                        Bullet(self.game,self.rect.centerx,self.rect.centery,10,0,)
                    if self.left is True:
                        Bullet(self.game,self.rect.centerx,self.rect.centery,-10,0,)
        else:
            self.standing = True
            self.standleft = False
            self.standright = False
            self.standup = False
            self.standdown = False
            self.walkCount = 0

    def collide_with_walls(self, dx=0, dy=0):
        #self.rect.center = self.x + dx, self.y + dy
        for wall in self.game.walls:
            #if self.rect.colliderect(wall.rect):
            if wall.rect.x == self.rect.x + dx * TILESIZE and wall.rect.y == self.rect.y + dy * TILESIZE:
                self.rect.centery -= PLAYER_WIDTH / 2
                #self.rect.center = self.x + dx, self.y + dy
                return True
        
        for chest in self.game.chests:
            if self.rect.colliderect(chest.rect):
                self.rect.centery -= PLAYER_WIDTH/2
                chest.opened = True
        
        #self.rect.center = self.x - dx, self.y - dy
    
    def collide_etc(self):
        if pygame.sprite.spritecollideany(self, self.game.mobs):
           self.health -= 1
        if self.health <= 0:
            self.game.quit()
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, velx, vely):
        self.groups = game.all_sprites, game.vfx, game.Bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE / 4, TILESIZE / 4))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.kill_timer = 0

    def update(self):
        # self.collision()
        self.collision_else()
        if not self.collision_else():
            self.x += self.velx  # * self.game.dt
            self.y += self.vely  # * self.game.dt
        self.rect.center = self.x, self.y
        if pygame.sprite.spritecollideany(self, self.game.walls):
            for x in range(random.randint(PARTICLELIMIT/2, PARTICLELIMIT)):
                Particle(self.game, self.x + random.randint(-10, 10), self.y + random.randint(-10,10), [LIGHTBROWN, YELLOW], None, True)
            self.kill()
        
        
    def collision_else(self):
        if pygame.sprite.spritecollideany(self, self.game.mobs):
            for x in range(random.randint(PARTICLELIMIT/2, PARTICLELIMIT)):
                Particle(self.game, self.x + random.randint(-10, 10), self.y + random.randint(-10,10), [YELLOW,RED,WHITE], None, True)
            self.kill()
            return True
        else:
            return False