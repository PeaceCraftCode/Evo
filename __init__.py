import pygame
import gui
import utils
import json
import os.path

cfg = gui.CONFIG()

with open(os.path.join('configs',cfg.configDict['Name']+'.json'),'w') as fp:
    json.dump(cfg.configDict,fp)