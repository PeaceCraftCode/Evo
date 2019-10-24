import pygame, utils, os.path

class Renderer:
    def __init__(self, World):
        pygame.init()
        #load surfaces to blit tiles
        self.water = pygame.image.load(os.path.join('Assets','water.png'))
        self.sand = pygame.image.load(os.path.join('Assets','sand.png'))
        self.grass = pygame.image.load(os.path.join('Assets','grass.png'))
        self.rock = pygame.image.load(os.path.join('Assets','rock.png'))

        #create scrn obj
        self.screen = pygame.display.set_mode([len(World.map)*16]*2)
        self.world = World