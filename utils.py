import time
import random
import math

def cap(value,upper=1.0,lower=0.0): #keeps <value> between upper and lower bounds
    if value > upper:
        value = upper
    elif value < lower:
        value = lower
    return value

def doPythag(pos1,pos2): #find the pythagorean distance between 2 points
    return math.sqrt((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2)

def getAngle(pos1,pos2):
    return math.degrees(math.atan2(pos1[1]-pos2[1], pos2[0]-pos1[0]))

def sort_array(array,index):
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
    def __init__(self,config):
        self.config = config
        self.objects = []

class Object: #basic object class, subclass to add functionality
    def objinit(self):
        pass
    def __init__(self,pos,world,**kwargs):
        self.pos = pos
        self.world = world
        self.world.objects.append(self)
        for k in kwargs.keys():
            setattr(self,k,kwargs[k])
        self.objinit()
    def tick(self):
        pass
    def move(self,direct,spd): #move spd pointed direct
        xd = (math.cos(math.radians(direct)))/spd
        yd = (math.sin(math.radians(direct)))/spd
        self.pos[0]+=xd
        self.pos[1]+=yd

class Plant(Object): #basic plant
    def objinit(self):
        self.curFoodPerc = 1.0
        self.alive = True
        self.justGrew = False
    def eat(self,consumer,perc=1.0): #get eaten
        perc = cap(perc,upper=self.curFoodPerc)
        self.curFoodPerc -= perc
        consumer.food += perc * self.foodValue #these vars (foodValue, growTime, & growAmt) are created by the routine in lines 15-16. They are not explicitly defined unless you call the class with them.
        if self.curFoodPerc <= 0.0:
            self.alive = False
    def tick(self): #run every game tick
        if round(time.time()) % self.growTime == 0 and not self.justGrew and self.curFoodPerc < 1.0:
            self.curFoodPerc += self.growAmt

class Animal(Object): #basic animal
    def objinit(self):
        self.genes = {}
        for gene in self.specGenes.keys():
            self.genes[gene] = self.specGenes[gene] + random.uniform(-self.deviation,self.deviation)
    
    def find_targets(self,r): #fina all objects in radius
        found = []
        for obj in self.world.objects:
            if doPythag(self.pos,obj.pos) <= r and self != obj:
                found.append([
                    obj,
                    obj.pos,
                    doPythag(self.pos,obj.pos),
                    getAngle(self.pos,obj.pos)
                ])
        return found
    
    def get_target_trajectory(self,r):
        targs = self.find_targets(r)
        if len(targs) > 0:
            return sort_array(targs,2)[0]
    

wld = World({})
ans = []
for i in range(10):
    ans.append(Animal([random.randint(-50,50),random.randint(-50,50)],wld,specGenes={},deviation=1))

print(ans[0].get_target_trajectory(50))

