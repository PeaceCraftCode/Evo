import pygame, utils, os.path

class Renderer:
    def __init__(self, World,sz):
        pygame.init()
        #load surfaces to blit tiles
        self.tiles = [
                    pygame.image.load(os.path.join('Assets','water.png')),
                    pygame.image.load(os.path.join('Assets','sand.png')),
                    pygame.image.load(os.path.join('Assets','grass.png')),
                    pygame.image.load(os.path.join('Assets','rock.png'))
        ]

        #create scrn obj

        self.sz = [round(i / 16)*16 for i in sz]

        self.world = World
        self.create_map_array()

    def create_map_array(self):
        self.mapArray = [[] for i in range(self.sz[0])]
        for x in range(len(self.world.map)):
            for y in self.world.map[x]:
                self.mapArray[x].append(self.tiles[y])
        print(len(self.mapArray))
    
    def get_sub_array(self,pos):
        x,y = tuple(pos)
        sub = [[self.tiles[0] for yi in range(int(self.sz[1]/16))] for xi in range(int(self.sz[0]/16))]
        for xi in range(int(self.sz[0]/16)):
            for yi in range(int(self.sz[1]/16)):
                try:
                    sub[xi][yi] = self.mapArray[x+xi][y+yi]
                except IndexError:
                    pass
        return sub

    def render(self,pos):
        screen = pygame.Surface(self.sz)
        array = self.get_sub_array(pos)
        xn,yn=0,0
        for x in range(0,screen.get_width(),16):
            for y in range(0,screen.get_height(),16):
                try:
                    screen.blit(array[xn][yn],(x,y))
                except IndexError:
                    pass
                yn+=1
            xn+=1
            yn = 0
        return screen
        
