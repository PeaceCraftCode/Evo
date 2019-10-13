import pygame
import gui
import utils
import json
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
utils.gen_species(20,'herbivore',wld)

print(wld.objects[0].get_target(200))

pygame.init()
sc = pygame.display.set_mode(wld.size)
for x in range(wld.size[0]):
    for y in range(wld.size[0]):
        su = pygame.Surface([1,1])
        su.fill(((0, 87, 217),(220, 230, 151),(0, 122, 16),(119, 120, 119))[wld.map[x][y]])
        sc.blit(su,[x,y])

for i in wld.objects:
    su = pygame.Surface([10,10])
    su.fill((255,0,0))
    sc.blit(su,[int(x)-5 for x in i.pos])

while True:
    pygame.display.flip()
    pygame.event.pump()