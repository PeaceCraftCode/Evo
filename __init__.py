import pygame
import gui
import utils
import json
import render
import os.path
from time import sleep

cfg = gui.CONFIG().configDict
sleep(1)
try:
    with open(os.path.join('configs',cfg['Name']+'.json'),'w') as fp:
        json.dump(cfg,fp)
except SystemError:
    exit()

#testing
wld = utils.World(cfg,800)
utils.gen_species(50,'herbivore',wld)

pygame.init()
sc = pygame.display.set_mode(wld.size)
mp = pygame.Surface(wld.size)
for x in range(wld.size[0]):
    for y in range(wld.size[0]):
        su = pygame.Surface([1,1])
        su.fill(((0, 87, 217),(220, 230, 151),(0, 122, 16),(119, 120, 119))[wld.map[x][y]])
        mp.blit(su,[x,y])

while True:
    sc.blit(mp,[0,0])
    for i in wld.objects:
        try:
            targ = utils.sort_array(i.get_target(40),2)[0]
            i.move(-targ[3],i.get_speed())
            pygame.draw.line(sc,[255,0,0],i.pos,targ[1])
        except IndexError:
            i.move_random()

        su = pygame.Surface([10,10])
        su.fill((255,0,0))
        sc.blit(su,[int(x)-5 for x in i.pos])
    pygame.display.flip()
    pygame.event.pump()
    