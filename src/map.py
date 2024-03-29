from src.mapRenderer import MapRenderer
from pytmx.util_pygame import load_pygame
import pygame
from pygame.locals import *
from src.globals import *
from src.player import Player
from src.enemy import Enemy
from src.WanderAI import WanderAI

class Map:
    def __init__(self, path, cam):
        self.tiled_map = load_pygame(path)
        self.staticColliders = []
        self.entities = []
        self.camera = cam

    def load(self):
        self.player = Player()
        self.entities.append(self.player)
        self.loadStaticColliders()
        self.getPlayerStart()
        self.loadEntities()
        self.loadEnemySpawnAreas()
        self.mapRenderer = MapRenderer(self.player)

    def preUpdate(self, delta, inputMap):
        for entity in self.entities:
            if isinstance(entity, Player):
                entity.preUpdate(delta, inputMap)
            else:
                entity.preUpdate(delta)

    def loadEntities(self):
        ents = self.tiled_map.get_layer_by_name("Enemies")
        for e in ents:
            if e.name == "GreenSlime":
                enemy = Enemy("res/sprites/green_slime.png", e)
                enemy.setPixelPosition(e.x, e.y)
                enemy.applyWalkAI(WanderAI(enemy, 1.5, 3.5, 25))
                self.entities.append(enemy)

    def loadEnemySpawnAreas(self):
        spawns = self.tiled_map.get_layer_by_name("SpawnAreas")
        for s in spawns:
            name = s.name
            rect = pygame.Rect(s.x, s.y, s.width, s.height)
            for e in self.entities:
                if isinstance(e, Enemy):
                    if e.entityObject.properties["SpawnArea"] == name:
                        e.spawnRect = rect

    def update(self, delta):
        for entity in self.entities:
            entity.update(delta)
        self.checkPlayerWeaponCollision(delta)
        self.checkEntityStaticCollision(delta)
        self.checkEntityWithEntityCollision(delta)

    def postUpdate(self, delta):
        for entity in self.entities:
            entity.postUpdate(delta)

    def loadStaticColliders(self):
        colliders = self.tiled_map.get_layer_by_name("Blocked")
        for collider in colliders:
            self.staticColliders.append(pygame.Rect(collider.x, collider.y, collider.width, collider.height))

    def checkEntityWithEntityCollision(self, delta):
        for enCheck in self.entities:
            if not enCheck.dx == 0 or not enCheck.dy == 0:
                for e in self.entities:
                    if not enCheck.id == e.id:
                        if enCheck.getMoveRect(delta).colliderect(e.rect):
                            if isinstance(enCheck, Player):
                                enCheck.dy = 0
                                enCheck.dx = 0
                                enCheck.walking = False
                            elif not enCheck.walkAI == None:
                                enCheck.walkAI.stopWalking()

    def checkEntityStaticCollision(self, delta):
        for static in self.staticColliders:
            for en in self.entities:
                if static.colliderect(en.getMoveRect(delta)):
                    en.dx = 0
                    en.dy = 0
                    en.walking = False
    
    def checkPlayerWeaponCollision(self, delta):
        if self.player.weapon.attacking:
            collider = self.player.weapon.rect
            for ent in self.entities:
                if ent.collisionMask == ENEMY_MASK:
                    if collider.colliderect(ent.rect):
                        ent.takeHit(self.player.weapon.damage, self.player.dir)

    def getPlayerStart(self):
        obj = self.tiled_map.get_object_by_name("Start")
        tx = int(obj.x / TILE_SIZE)
        ty = int(obj.y / TILE_SIZE)
        self.player.x = tx * TILE_SIZE
        self.player.y = ty * TILE_SIZE

    def render(self, surface):
        self.mapRenderer.render(self.camera, self.tiled_map, surface, self.entities)