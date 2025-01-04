import math
import random
timestep=0.1


class particle:
  def __init__(self, index, time, x, y, vx, vy, pair):    
    self.time = float(time)
    self.index=str(index)
    self.x=float(x)
    self.y=float(y)
    self.vx=float(vx)
    self.vy=float(vy)
    self.pair=int(pair)
  def newvelocity(self):
    theta= random.random()*2*math.pi
    magnitude= random.random()*self.temp
    self.vx=magnitude*math.cos(theta)+self.vx*0.5
    self.vy=magnitude*math.sin(theta)+self.vy*0.5

  def change(self, t, x, y):
    self.index=str(t)
    self.vx=x
    self.vy=y

  def newposition(self):
    x=self.x+self.vx
    y=self.y+self.vy
    if(x<0):
      self.x= abs(self.vx-self.x)
      self.vx=-self.vx
    elif(x>500):
      self.x=500-((x-self.x)-(500-self.x))
      self.vx=-self.vx
    else:
      self.x=x
    if(y<0 or y>500):
      self.y= abs(self.vy-self.y)
      self.vy=-self.vy
    elif(y>500):
      self.y=500-(abs(self.vy-500+self.vy))
      self.vy=-self.vy
    else:
      self.y=y
    
  def getpos(self):
    b=[]
    b.append(self.x)
    b.append(self.y)
    return b
  def getvel(self):
    b=[]
    b.append(self.vx)
    b.append(self.vy)
    return b
  
  def gettype(self):
    return(self.index)
  
  def increase(self):
    self.time+=timestep
  def gettime(self):
    return(self.time)
  
  def getpair(self):
    return(self.pair)
