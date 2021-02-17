import pygame
from pygame.locals import *
from src.level import Level
from src.inputMap import InputMap
from src.globals import *

class Game:
    def __init__(self, window_width, window_height, design_width, design_height, title):
        self.running = True
        self.on_init(window_width, window_height, design_width, design_height, title)
        self.level = Level(window_width, window_height)
        self.lastTime = 0
        self.cameraScale = 3
        self.inputMap = InputMap()
        self.post_init(title)

    def run(self):
        while self.running:
            self.processEvents()
            self.update()
            self.render()
            self.fpsClock.tick(self.fpsLimit)
            print(self.fpsClock.get_fps())
        self.cleanUp()

    def processEvents(self):
        self.inputMap.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[K_d]:
            self.inputMap.d = True
        if keys[K_a]:
            self.inputMap.a = True
        if keys[K_s]:
            self.inputMap.s = True
        if keys[K_w]:
            self.inputMap.w = True

    def update(self):
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        delta = (t - self.lastTime) / 1000.0
        self.lastTime = t

        self.level.process(delta, self.inputMap)

    def render(self):
        self.backBuffer.fill((0, 0, 0))
        self.cameraBuffer.fill((0,0,0))
        #Render the world to the backBuffer
        self.level.render(self.backBuffer)
        #Render the world at camera coords
        self.cameraBuffer.blit(self.backBuffer, (0, 0),
            pygame.Rect(0 - self.level.camera.x, 0 - self.level.camera.y, self.level.camera.width, self.level.camera.height))
        
        #Render just the area the camera occupies
        xp = 0 + (self.width / 2) - self.design_width / 2
        xy =  0 + (self.height / 2) - self.design_height / 2
        r = pygame.Rect(xp, xy, self.design_width, self.design_height)
        self.captureBuffer.blit(self.cameraBuffer, (0, 0), r)

        #Scale the render to the design width and height to zoom it
        self.scaleBuffer = pygame.transform.scale(self.captureBuffer, 
            (self.design_width * self.cameraScale, self.design_height * self.cameraScale))
        
        #blit to screen
        self.screen.blit(self.scaleBuffer, (0,0))
        
        pygame.display.update()

    def cleanUp(self):
        pygame.quit()

    def on_init(self, width, height, dw, dh, title):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.design_width = dw
        self.design_height = dh
        self.dSize = self.design_width, self.design_height
        self.screen = pygame.display.set_mode(self.size)

    def post_init(self, title):
        pygame.display.set_caption(title)
        self.backBuffer = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        self.cameraBuffer = pygame.Surface((self.width, self.height))
        self.captureBuffer = pygame.Surface((self.design_width, self.design_height))
        self.scaleBuffer = pygame.Surface(self.dSize)
        self.fpsLimit = 60
        self.fpsClock = pygame.time.Clock()