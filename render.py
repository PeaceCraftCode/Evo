import pygame, utils, os.path

class Renderer:
    def __init__(self, World):
        pygame.init()
        #load surfaces to blit tiles
        self.tiles = [
                    pygame.image.load(os.path.join('Assets','water.png')),
                    pygame.image.load(os.path.join('Assets','sand.png')),
                    pygame.image.load(os.path.join('Assets','grass.png')),
                    pygame.image.load(os.path.join('Assets','rock.png'))
        ]

        #create scrn obj
        self.screen = pygame.display.set_mode([len(World.map)*16]*2)
        self.world = World
        self.create_map_array()

    def create_map_array(self):
        self.mapArray = [[] for i in range(self.screen.get_width())]
        for x in range(len(self.world.map)):
            for y in self.world.map[x]:
                self.mapArray[x].append(self.tiles[y])
    
    def get_sub_array(self,pos):
        x,y = tuple(pos)
        sub = [[self.tiles[0] for yi in range(yi)] for xi in range(xi)]
        for xi in range(x):
            for yi in range(y):
                sub[xi][yi] = self.mapArray[x+xi][y+yi]
        return sub

    def render(self,pos):
        array = self.get_sub_array(pos)
        xn,yn=0,0
        for x in range(self.screen.get_width(),step=16):
            for y in range(self.screen.get_height(),step=16):
                self.screen.blit(array[xn][yn],(x,y))
                yn+=1
            xn+=1
        
