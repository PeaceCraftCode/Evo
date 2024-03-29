import time
import random
import math
from noise import pnoise2
import pygame

GENEMINMAXMEAN = { #Dictionary of [min,max,mean,std. dev] of genes.
    'size': [1,100,50,10],
    'attractiveness': [.2,2,1,.2],
    'neckLength': [.1, 5,.5,.1], #meters
    'ageSpeed': [.0000556, .000556, .000185,.00008], #% per tick
    'legLength': [.2,1.5,.8,.4], #meters
    'turnChance': [.0001,.0009,.0003,.00005], #out of 1
    'swimSpeedMod': [0.2,1.5,0.8,0.4],
    'swimAbility': [800,5000,1500,100]
}

def cap(value,upper=1.0,lower=0.0): #keeps <value> between upper and lower bounds
    if value > upper:
        value = upper
    elif value < lower:
        value = lower
    return value

def doPythag(pos1,pos2): #find the pythagorean distance between 2 points
    return math.sqrt((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2)

def getAngle(pos1,pos2): #find angle between 2 points, based on a +x vector
    return math.degrees(math.atan2(pos1[1]-pos2[1], pos2[0]-pos1[0]))

def sort_array(array,index): #sort 2d list based on one index
    sortedinit = sorted([i[index] for i in array])
    out = []
    for i in sortedinit:
        c = 0
        for n in array:
            if n[index] == i:
                out.append(n)
                break
            c += 1

        del array[c]
    return out

class World: #World class, manages pathfinding requests
    def gen_world(self,size,config):
        mp = []
        random.seed(random.randint(0,500000))
        octaves = random.random()
        # octaves = (random.random() * 0.5) + 0.5
        freq = 500 * octaves
        for x in range(size):
            mp.append([])
            for y in range(size):
                n = math.sqrt(abs((pnoise2(x/freq, y / freq, 2))))
                if n < config['WaterLevel']/100:
                    c = 0
                elif n < config['BeachLevel']/100:
                    c = 1
                elif n < config['GrassLevel']/100:
                    c = 2
                else:
                    c = 3
                mp[x].append(c)
        return mp
            
    def __init__(self,config,size):
        self.config = config
        self.objects = []
        self.size = (size,size) #world size, 1 #, square
        self.map = self.gen_world(size,config)

class Object: #basic object class, subclass to add functionality
    def objinit(self):
        pass
    def __init__(self,pos,world,**kwargs):
        self.pos = list(pos)
        self.alive = True
        self.world = world
        self.world.objects.append(self)
        for k in kwargs.keys():
            setattr(self,k,kwargs[k])
        self.objinit()
    
    def get_visibility(self): #get visibility coeff, used in find_target()
        return 1

    def tick(self): #to run every tick
        pass
    
    def check_passable(self,pos):
        if pos[0] > self.world.size[0] or pos[0] < 0 or pos[1] > self.world.size[1] or pos[1] < 0:
            return False
        return True

    def move(self,direct,spd): #move spd pointed direct
        xd = (math.cos(math.radians(direct)))/spd
        yd = (math.sin(math.radians(direct)))/spd

        if self.check_passable((self.pos[0]+xd,self.pos[1]+yd)):
            self.pos[0]+=xd
            self.pos[1]+=yd
            return True
        return False

class Plant(Object): #basic plant, pass type and foodValue args
    def objinit(self):
        self.curFoodPerc = 1.0
        self.justGrew = False
        self.height = 1
        if self.type == 'tree':
            self.height = random.randint(self.world.config['TreeMinHeight'],self.world.config['TreeMaxHeight'])

    def eat(self,consumer,perc=1.0): #get eaten
        perc = cap(perc,upper=self.curFoodPerc)
        self.curFoodPerc -= perc
        consumer.food += perc * self.foodValue #these vars (foodValue, growTime, & growAmt) are created by the routine in lines 15-16. They are not explicitly defined unless you call the class with them.
        if self.curFoodPerc <= 0.0:
            self.alive = False
    
    def get_size(self): #calculate size
        return self.foodValue * 5 * (self.curFoodPerc/2 + .5)

    def tick(self): #run every game tick
        if round(time.time()) % self.growTime == 0 and not self.justGrew and self.curFoodPerc < 1.0:
            self.curFoodPerc += self.growAmt

class Animal(Object): #basic animal, pass specGenes (default species genes), deviation (percentage of range)
    def objinit(self):
        global GENEMINMAXMEAN
        self.genes = {}
        self.age = 0.25
        self.direction = random.choice([-1,1])*random.uniform(0,180)
        for gene in self.specGenes.keys():
            self.genes[gene] = cap((self.specGenes[gene] + random.uniform(-self.deviation,self.deviation)*(GENEMINMAXMEAN[gene][1]-GENEMINMAXMEAN[gene][0])),
                                   GENEMINMAXMEAN[gene][1],
                                   GENEMINMAXMEAN[gene][0]
                               ) #generate unique genes based of specGenes and deviation
        self.visibility = self.genes['attractiveness'] * math.sqrt(self.genes['neckLength'])/.7
    
    def get_target(self,r): #find all objects in radius
        found = []
        for obj in self.world.objects:
            #print(obj,doPythag(self.pos,obj.pos) <= r * (math.sqrt(obj.get_size())/5) * obj.visibility)
            if doPythag(self.pos,obj.pos) <= r * (math.sqrt(obj.get_size())/7) * obj.visibility and self != obj: #calc is arbitrary and may be altered
                #print(obj.genes,r * (math.sqrt(obj.get_size())/7) * obj.visibility)
                found.append([
                    obj,
                    obj.pos,
                    doPythag(self.pos,obj.pos),
                    getAngle(self.pos,obj.pos)
                ])

        return found
    
    def get_size(self): #calculate size based on age
        return self.genes['size'] * cap(self.age * 4)

    def get_speed(self): #calc speed based on size, leg length, and (eventually) environment
        if self.world.map[int(self.pos[0])][int(self.pos[1])] == 0:
            waterMod = 0.1 * self.genes['swimSpeedMod']**2
            return self.genes['legLength'] * (math.sqrt(self.get_size())/4) / waterMod
        else:
            return self.genes['legLength'] * (math.sqrt(self.get_size())/4) / self.genes['swimSpeedMod']**2

    def tick(self): #tick loop, add more here
        self.age += self.genes['ageSpeed']
    
    def move_random(self):
        if random.random() > self.genes['turnChance']:
            move_result = self.move(self.direction,self.get_speed())
        else:
            self.direction += random.uniform(0,90)
            if self.direction < 0:
                self.direction = -180 - self.direction
            if self.direction > 180:
                self.direction = -(self.direction-180)
            move_result = self.move(self.direction,self.get_speed())
        while not move_result:
            self.direction += random.uniform(0,90)
            if self.direction < 0:
                self.direction = -180 - self.direction
            if self.direction > 180:
                self.direction = -(self.direction-180)
            move_result = self.move(self.direction,self.get_speed())

def gen_species(num,tp,world,fail=10): #generate <num> animals of type <tp> in <world>, all animals are one species.
    global GENEMINMAXMEAN
    for i in range(num):
        genes = { g:cap(random.normalvariate(GENEMINMAXMEAN[g][2],GENEMINMAXMEAN[g][3]), GENEMINMAXMEAN[g][1],GENEMINMAXMEAN[g][0]) for g in GENEMINMAXMEAN.keys() }
        failed = False
        fc = 0
        while True:
            pos = (random.uniform(0,world.size[0]),random.uniform(0,world.size[1]))
            if world.map[int(pos[0])][int(pos[1])] != 0:
                break
            if fc == fail:
                failed = True
                break
            fc += 1
        if failed:
            continue
        Animal(pos,world,specGenes=genes,deviation=random.uniform(0.002,0.1))


