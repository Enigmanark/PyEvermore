import pygame
from pygame.locals import *
from src.weapon import Weapon

class Player:
    def __init__(self):
        self.x = 64
        self.y = 64
        self.dx = 0
        self.dy = 0
        self.speed = 100
        self.lastDir = "down"
        self.dir = "down"
        self.image = pygame.image.load("res/sprites/hero_1/walk_down.png")
        self.maxFrames = 4
        self.currentFrame = 0
        self.time = 0
        self.animTime = 0.25
        self.weapon = Weapon()
        self.weapon.loadImage("res/sprites/sword_1.png")

    def switchAnim(self):
        if self.dir == "down":
            self.image = pygame.image.load("res/sprites/hero_1/walk_down.png")
        elif self.dir == "up":
            self.image = pygame.image.load("res/sprites/hero_1/walk_up.png")

    def renderPlayer(self, surface):
        surface.blit(self.image, (self.x, self.y), pygame.Rect(32 * self.currentFrame, 0, 32, 32))

    def renderWeapon(self, surface):
        self.weapon.render(surface)

    def render(self, surface):
        if self.dir == "up":
            self.renderWeapon(surface)
            self.renderPlayer(surface)
        elif self.dir == "down":
            self.renderPlayer(surface)
            self.renderWeapon(surface)

    def update(self, delta, inputMap):
        self.animate(delta)
        #self.currentFrame = 3
        self.weapon.update(delta, self)
        self.doMove(delta)

    def preUpdate(self, delta, inputMap):
        self.getInput(delta, inputMap)

    def postUpdate(self, delta, inputMap):
        self.dx = 0
        self.dy = 0
        if self.lastDir != self.dir:
            self.lastDir = self.dir
            self.switchAnim()

    def getInput(self, delta, inputMap):
        if inputMap.w == True:
            self.dy = -1
            self.dir = "up"
        if inputMap.s == True:
            self.dy = 1
            self.dir = "down"
        if inputMap.a == True:
            self.dx = -1
        if inputMap.d == True:
            self.dx = 1

    def doMove(self, delta):
        nx = self.x + self.dx * self.speed * delta
        ny = self.y + self.dy * self.speed * delta
        self.x = nx
        self.y = ny

    def animate(self, delta):
        self.time += delta
        if self.time >= self.animTime:
            self.time = 0
            self.currentFrame += 1
            if self.currentFrame >= self.maxFrames:
                self.currentFrame = 0