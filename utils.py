import time
import random

def cap(value,upper=1.0,lower=0.0): #keeps <value> between upper and lower bounds
    if value > upper:
        value = upper
    elif value < lower:
        value = lower
    return value

class Object: #basic object class, subclass to add functionality
    def objinit(self):
        pass
    def __init__(self,pos,**kwargs):
        self.pos = pos
        for k in kwargs.keys():
            setattr(self,k,kwargs[k])
        self.objinit()
    def tick(self):
        pass

class Plant(Object): #basic plant
    def objinit(self):
        self.curFoodPerc = 1.0
        self.alive = True
        self.justGrew = False
    def eat(self,consumer,perc=1.0):
        perc = cap(perc,upper=self.curFoodPerc)
        self.curFoodPerc -= perc
        consumer.food += perc * self.foodValue #these vars (foodValue, growTime, & growAmt) are created by the routine in lines 15-16. They are not explicitly defined unless you call the class with them.
        if self.curFoodPerc <= 0.0:
            self.alive = False
    def tick(self):
        if round(time.time()) % self.growTime == 0 and not self.justGrew and self.curFoodPerc < 1.0:
            self.curFoodPerc += self.growAmt

class Animal(Object):
    def objinit(self):
        self.genes = {}
        for gene in self.specGenes.keys():
            self.genes[gene] = self.specGenes[gene] + random.uniform(-self.deviation,self.deviation)
        


