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

class Plant(Object):
    def objinit(self):
        self.curFoodPerc = 1.0
        self.alive = True
    def eat(self,consumer,perc=1.0):
        perc = cap(perc,upper=self.curFoodPerc)
        self.curFoodPerc -= perc
        consumer.food += perc * self.foodValue
        if self.curFoodPerc <= 0.0:
            self.alive = False




