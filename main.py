#be cool to add a temperature gradient and have heat transfer with this

import math
import random
import time
from particle import particle
import pygame
import sys


# win=GraphWin("Hello", 500,500)
# pt1=Point(200,200)
# cir1=Circle(pt1, 100)
# cir1.setFill("blue")
# pt2=Point(250,250)
# cir2=Circle(pt2, 100)
# cir2.setFill("red")
# cir1.draw(win)
# cir2.draw(win)
# win.getMouse()
# win.close()

# time interval for each update
timestep=0.1
processTime=9
particles=[]
extraProducts=[]
temp = 20
numEnzymes=10
numSubstrate=50
numProduct=0
numComplexes=0
EnzymeRad= 20
substrateRad=10

#for the line graph:
oldProd=numProduct
oldSub=numSubstrate


# temp=(input("Enter temperature" + "\n"))
# numpartA= int(input("Enter # of Particle A"+"\n"))
# numpartB= int(input("Enter # of Particle B"+"\n"))

for i in range(numEnzymes):
  particles.append(particle("E", 0, random.random()*500, random.random()*500, float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5),-1))
for i in range(numSubstrate):
  particles.append(particle("S", 0, random.random()*500, random.random()*500, float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5),-1))

def interactions():
    global numEnzymes
    global numComplexes
    global numProduct
    global numSubstrate
    i=-1
    important=[]
    for part in particles:
      i+=1
      j=-1
      let=part.gettype()
      if("C" in let):
         part.increase()
         a=part.gettime()
         #print(a)
         if(part.gettime()>=processTime):
            #print("Changed \n")
            partV=part.getvel()
            velx=partV[0]
            vely=partV[1]
            partP=part.getpos()
            posx=partP[0]
            posy=partP[1]
            part.change("E", velx, vely)
            pair=part.getpair()
            particles[pair].change("P",float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5))
            extraProducts.append(particle("p", 0, posx, posy, float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5),-1))
            
            numComplexes-=1
            numEnzymes+=1
            numProduct+=2
      for other in particles:
        j+=1
        str=part.gettype()+other.gettype()
        partPos=part.getpos()
        otherPos=other.getpos()
        xdiff=partPos[0]-otherPos[0]
        ydiff=partPos[1]-otherPos[1]
        dis=math.sqrt(xdiff**2+ydiff**2)
        if(dis<EnzymeRad+substrateRad):
            if('E' in str and 'S' in str):
              p=other.getpos()
              v=other.getvel()
              if(part.gettype()=='E'):
                 p=part.getpos()
                 v=part.getvel()

              px=p[0]
              py=p[1]
              vx=v[0]
              vy=v[1]
              particles[i]=(particle("C", 0, px, py, vx, vy,j))
              particles[j]=(particle("C", 0, px, py, vx, vy,i))
              numEnzymes-=1
              numSubstrate-=1
              numComplexes+=1
                
    # for k in range(len(important)):
    #     tuple=important[k]
    #     a=tuple[0]
    #     p=particles[a].getpos()
    #     px=p[0]
    #     py=p[1]
    #     v=particles[a].getvel()
    #     vx=v[0]
    #     vy=v[1]
    #     particles.append(particle("C", 0, px, py, vx, vy,temp))
    # list=[]
    # for k in range(len(important)):
    #     list.extend(important[k])
    # list.sort(reverse=True)
    # for index in list: del particles[index]        




pygame.init()
clock = pygame.time.Clock()

#Screen
screen_width=1000
screen_height=500
screen = pygame.display.set_mode((screen_width, screen_height))

keepRunning=True
pause= False

time=0
enzymesubstrate= pygame.image.load("C:/Users/kxia/Desktop/Kyler Coding/Enzyme Sim/enzymeimages/enzyme-substrate complex.png")
enzyme= pygame.image.load("C:/Users/kxia/Desktop/Kyler Coding/Enzyme Sim/enzymeimages/enzyme.png")
substrate= pygame.image.load("C:/Users/kxia/Desktop/Kyler Coding/Enzyme Sim/enzymeimages/substrate.png")
product= pygame.image.load("C:/Users/kxia/Desktop/Kyler Coding/Enzyme Sim/enzymeimages/product-2.png")

enzymesubstrate= pygame.transform.scale(enzymesubstrate, (2*EnzymeRad, 2*EnzymeRad))
enzyme= pygame.transform.scale(enzyme, (2*EnzymeRad, 2*EnzymeRad))
substrate= pygame.transform.scale(substrate, (2*substrateRad,2*substrateRad))
product= pygame.transform.scale(product, (substrateRad, substrateRad))

# Set up fonts
pygame.font.init()
font = pygame.font.SysFont('Arial', 15)
font2= pygame.font.SysFont('Arial', 10)
scalex=10
scaley=4


def displayGrids():
   for i in range(18):
      numx=500+(i+2)*25            
      pygame.draw.rect(screen, (255,255,255), (numx, 25, 1, 450))
      text = font2.render(str(int(i*25/scalex)), True, (255,255, 255)) 
      screen.blit(text, (numx, 475))
      numy=(i+1)*25
      pygame.draw.rect(screen, (255,255,255), (550, numy, 425, 1))
      text = font2.render(str(int(i*25/scaley)), True, (255,255, 255)) 
      screen.blit(text, (535, 500-(numy+3)))
   pygame.draw.rect(screen, (255,255,255), (550, 475, 425, 1))
   text = font2.render("Time (seconds)", True, (255,255, 255)) 
   screen.blit(text, (750, 488)) 
   text = font2.render("Number", True, (255,255, 255)) 
   screen.blit(text, (500, 250))    
   

while keepRunning:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      keepRunning = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_p:  # Press 'P' to toggle pause
        pause = not pause
  #check for updating
  #print("Updating")
  #Clear Screen
  #screen.fill((0,0,0))
  pygame.draw.rect(screen, (100,100,100), (0,0, 500,500))
  pygame.draw.rect(screen, (0,0,0), (500,0, 50,500))
  pygame.draw.rect(screen, (0,0,0), (500,475, 500,25))

  
  # Render text
  text_surface = font.render("Enzyme Sim.   "+" Time="+str(int(time))+", Temp= "+str(math.floor(temp)), True, (255, 255, 255))
  text2=font.render("Enzyme: "+ str(numEnzymes) + "    Substrate "+ str(numSubstrate)+"  Complexes: "+ str(numComplexes)+"    Product: "+ str(numProduct), True, (255, 255, 255))
 
  time+=timestep

  #Making images of particles
  for part in particles:
    b=part.getpos()

    #default to Substrate Color
    #Color1= pygame.Color(0,0,100)
    properImage=substrate
    letter=part.gettype()
    if(letter=="E"):
        #Color1= pygame.Color(0,100,0)
        properImage=enzyme
    if('C' in letter):
        #Color1= pygame.Color(100,0,0)
        properImage=enzymesubstrate
    if(letter=="P"):
        #Color1=pygame.Color(100,100,100)
        properImage=product

    screen.blit(properImage, b)
    #Aparticles[i].newvelocity()
    part.newposition()
  for part in extraProducts:
    b=part.getpos()
    screen.blit(product, b)
    #Aparticles[i].newvelocity()
    part.newposition()

  #The line graph
  pygame.draw.line(screen, (0,255,0), (550+scalex*(time-timestep), 500-(25+scaley*oldProd)),(550+scalex*time, 500-(25+scaley*numProduct)), 1)
  pygame.draw.line(screen, (255,0,0), (550+scalex*(time-timestep), 500-(25+scaley*oldSub)),(550+scalex*time, 500-(25+scaley*numSubstrate)), 1)
  oldProd=numProduct
  oldSub=numSubstrate

  interactions()
  productdata=[]
  substratedata=[]
  if(int(time)%3==0):
     productdata
  screen.blit(text_surface, (10, 10))
  screen.blit(text2, (10, 30))
  displayGrids()
  pygame.display.flip()

  clock.tick(1/timestep)

#   pygame.init()
#   screen2= pygame.display.set_mode((800, 600))

# while(True):
#   win= GraphWin("Diffusion",500,500)
#   for i in range(numpartA):
#       b=Aparticles[i].getpos()
#       pt=Point(b[0], b[1])
#       cir=Circle(pt, 5)
#       cir.setFill("red")
#       cir.draw(win)
#       Aparticles[i].newvelocity()
#       Aparticles[i].newposition()
 
#       b=Bparticles[i].getpos()
#       pt=Point(b[0], b[1])
#       cir=Circle(pt, 5)
#       cir.setFill("blue")
#       cir.draw(win)
#       Bparticles[i].newvelocity()
#       Bparticles[i].newposition()
#   win.getMouse()  
#   win.close()
