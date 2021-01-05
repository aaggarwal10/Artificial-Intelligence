import pygame
from random import *
import time
import itertools
import sys
import math
from HamCycle import HCyc
pygame.init()
sys.setrecursionlimit(3000)

class Snake:
    heading = 0 # 0: Right, 1: Up, 2: Left, 3: Down
    snakeParts = []
    dirs = [[1,0],[0,-1],[-1,0],[0,1]] #Directions corresponding to Heading Vals
    speed = 1
    partSize = 0
    foodPosition = []
    def __init__(self,speed,allP,gridBSize):
        self.snakeParts = [choice(allP)]
        self.heading = 0
        self.partSize = gridBSize
        self.foodPosition = self.getFoodPos(allPos,self.snakeParts)
    
    def pathDist(self,start,end,hCyc):
        c = 0
        while True:
            c+=1
            if start==end:
                break
            else:
                start = hCyc[start]
        return c

    def distDict(self,possPoints,foodNode,gX,hCyc):
        d = {}
        for point in possPoints:
            node = point[0]+gX*point[1]
            d[self.pathDist(node,foodNode,hCyc)] = point
        return d

    def bestMove(self,possPoints,foodNode,gX,hCyc,hNode):
        distD = self.distDict(possPoints,foodNode,gX,hCyc)
        for dist in sorted(distD):
            point = distD[dist]
            nNode = point[0]+point[1]*gX
            if hCyc[hNode]==nNode:
                return nNode
            else:
                c = 0
                start = nNode
                while True:
                    c += 1
                    if allPos[hCyc[start]] in self.snakeParts:
                        break
                    else:
                        start = hCyc[start]
                if len(self.snakeParts)<c:
                    return nNode
        return hCyc[hNode]
                        
                    
            
    def move_forw(self,allPos,gridX,gridY, hCyc):
        head = self.snakeParts[0][:]
        hNode = head[0]+head[1]*gridX
        foodNode = self.foodPosition[0]+self.foodPosition[1]*gridX

        posP = []
        for direc in self.dirs:
            nPX = head[0]+direc[0]
            nPY = head[1]+direc[1]
            nP = [nPX,nPY]
            if 0<=nPX<gridX and 0<=nPY<gridY and nP not in self.snakeParts:
                posP.append(nP)
        nNode = self.bestMove(posP,foodNode,gridX,hCyc,hNode)
        head = allPos[nNode]
        
        if self.foodPosition in self.snakeParts:
            self.foodPosition = self.getFoodPos(allPos,self.snakeParts)         
        else:
            self.snakeParts.pop()
        self.snakeParts=[head]+self.snakeParts

    def draw_snake_food(self,display,done):
        display.fill((0,0,0))
        fCol = (255,255,0)
            
        for part in range(len(self.snakeParts)):
            
            pygame.draw.rect(display,(0,0,0), (self.snakeParts[part][0]*self.partSize,self.snakeParts[part][1]*self.partSize,
                                                     self.partSize,self.partSize),2)
            pygame.draw.rect(display,(0,255,0), (self.snakeParts[part][0]*self.partSize+1,self.snakeParts[part][1]*self.partSize+1,
                                                     self.partSize-2,self.partSize-2))
            if part>0:
                posX = (self.snakeParts[part-1][0]*self.partSize+self.snakeParts[part][0]*self.partSize)/2+1
                posY = (self.snakeParts[part-1][1]*self.partSize+self.snakeParts[part][1]*self.partSize)/2+1
                pygame.draw.rect(display,(0,255,0), (posX,posY,
                                                     self.partSize-2,self.partSize-2))
                
        if not done:
            pygame.draw.rect(display,fCol, (self.foodPosition[0]*self.partSize,self.foodPosition[1]*self.partSize,
                                              self.partSize,self.partSize))                                              
            
            
    def change_heading(self,key):
        if key==pygame.K_RIGHT:
            self.heading = 0
        elif key==pygame.K_UP:
            self.heading = 1
        elif key==pygame.K_LEFT:
            self.heading = 2
        elif key==pygame.K_DOWN:
            self.heading = 3

    def getFoodPos(self,allPositions,posTaken):
        allPo = allPositions[:]
        shuffle(allPo)
        for pos in allPo:
            if pos not in posTaken:
                return [pos[0],pos[1]]
        return [0,0] #no positions left. perfect snake.

    def containsDups(self, lis):
        for i in range(len(lis)-1):
            if lis[i] in lis[i+1:]:
                return True
        return False

    def check_death(self, gX, gY):
        head = self.snakeParts[0]
        if self.containsDups(self.snakeParts):
            return True
        elif not (0<=head[0]<gX and 0<=head[1]<gY):
            return True
        else:
                return False

gridX = 18
gridY = 10
gridBSize= 20
screen = pygame.display.set_mode([gridX*gridBSize,gridY*gridBSize])
  
    
hCyc = HCyc(gridX,gridY).hcyc

allPos = []
for y in range(gridY):
    for x in range(gridX):
        allPos.append([x,y])


mySnake = Snake(1,allPos,gridBSize)
running = True
gameDone = False
speed = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if mySnake.check_death(gridX,gridY):
        gameDone = True
    for i in range(speed):
        if not gameDone:
            mySnake.move_forw(allPos,gridX,gridY,hCyc)
        mySnake.draw_snake_food(screen,gameDone)
    time.sleep(0.01)
    pygame.display.flip()
pygame.quit()
