import time
import random
import math

GENEMINMAXMEAN = { #Dictionary of [min,max,mean,std. dev] of genes.
    'size' : [1,100,50,10],
    'attractiveness' : [.2,2,1,.2],
    'neckLength' : [.1, 5,.5,.1],
    'ageSpeed' : [.0000556, .000556, .000185,.00008]
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
    def __init__(self,config,size):
        self.config = config
        self.objects = []
        self.size = size #world size, tuple

class Object: #basic object class, subclass to add functionality
    def objinit(self):
        pass
    def __init__(self,pos,world,**kwargs):
        self.pos = pos
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

    def move(self,direct,spd): #move spd pointed direct
        xd = (math.cos(math.radians(direct)))/spd
        yd = (math.sin(math.radians(direct)))/spd
        self.pos[0]+=xd
        self.pos[1]+=yd

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
                print(obj.genes,r * (math.sqrt(obj.get_size())/7) * obj.visibility)
                found.append([
                    obj,
                    obj.pos,
                    doPythag(self.pos,obj.pos),
                    getAngle(self.pos,obj.pos)
                ])

        return found
    
    def get_size(self): #calculate size based on age
        return self.genes['size'] * cap(self.age * 4)

    def tick(self): #tick loop, add more here
        self.age += self.genes['ageSpeed']

def gen_species(num,tp,world): #generate <num> animals of type <tp> in <world>, all animals are one species.
    global GENEMINMAXMEAN
    for i in range(num):
        genes = { g:cap(random.normalvariate(GENEMINMAXMEAN[g][2],GENEMINMAXMEAN[g][3]), GENEMINMAXMEAN[g][1],GENEMINMAXMEAN[g][0]) for g in GENEMINMAXMEAN.keys() }
        Animal((random.uniform(0,world.size[0]),random.uniform(0,world.size[1])),world,specGenes=genes,deviation=random.uniform(0.002,0.1))


#testing
wld = World({},[1000,1000])
gen_species(20,'herbivore',wld)

print(wld.objects[0].get_target(100))

