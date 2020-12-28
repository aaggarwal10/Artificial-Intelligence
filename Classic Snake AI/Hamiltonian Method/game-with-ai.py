import pygame
from random import *
import time
import itertools
import sys
import math

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
        self.snakeParts = [[3,3]]
        self.heading = 0
        self.partSize = gridBSize
        self.foodPosition = self.getFoodPos(allP,self.snakeParts)
    
    def move_forw(self,allPos):
        head = self.snakeParts[0][:]
        head[0]+=self.speed*self.dirs[self.heading][0]
        head[1]+=self.speed*self.dirs[self.heading][1]
        if head == self.foodPosition:
            self.foodPosition = self.getFoodPos(allPos,self.snakeParts)
        else:
            self.snakeParts.pop()
        self.snakeParts=[head]+self.snakeParts

    def draw_snake_food(self,display):
        display.fill((0,0,0))
        for part in self.snakeParts:
            pygame.draw.rect(display,(0,255,0), (part[0]*self.partSize,part[1]*self.partSize,
                                                     self.partSize,self.partSize))
        pygame.draw.rect(display,(255,255,0), (self.foodPosition[0]*self.partSize,self.foodPosition[1]*self.partSize,
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
        elif [head[0]+self.speed*self.dirs[self.heading][0],head[1]+self.speed*self.dirs[self.heading][1]] in self.snakeParts:
            return True
        elif not (0<=head[0]<gX and 0<=head[1]<gY):
            return True
        else:
            return False

gridX = 10
gridY = 10
gridBSize= 1
screen = pygame.display.set_mode([gridX*gridBSize,gridY*gridBSize])

hCycle = [-1 for i in range(gridX*gridY)]
hCycle[0] = 0
def HamiltonianCyc(k):
    global hCycle
    if k == len(hCycle)-1:
        return isConnected(hCycle[k],0)

    for nextNode in range(len(hCycle)):
        if isConnected(nextNode,k):
            hCycle[k+1]=nextNode
            if HamiltonianCyc(k+1):
                return True

            hCycle[k+1] = -1
            
    return False
    

def isConnected(n,k):
    global hCycle,gridX
    if hCycle[k]<0: return False
    elif n == 0 or  math.log2(n)%1 ==0:
        return ((n==hCycle[k]-1) or (n==hCycle[k]+gridX)
                or (n == hCycle[k]-gridX)) and (n not in hCycle[:k])
    elif math.log2(n+1)%1 ==0:
        return ((n==hCycle[k]+1) or (n==hCycle[k]+gridX)
                or (n == hCycle[k]-gridX)) and (n not in hCycle[:k])
    else:
        return ((n==hCycle[k]+1) or (n==hCycle[k]-1) or (n==hCycle[k]+gridX)
                or (n == hCycle[k]-gridX)) and (n not in hCycle[:k])

allPos = []
for y in range(gridY):
    for x in range(gridX):
        allPos.append([x,y])


mySnake = Snake(1,allPos,gridBSize)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            mySnake.change_heading(event.key)
    if mySnake.check_death(gridX,gridY):
        running=False
    mySnake.move_forw(allPos)
    mySnake.draw_snake_food(screen)
    pygame.draw.rect(screen,(255,255,255), (40,0, 20, 20))

    time.sleep(0.04)
    pygame.display.flip()
pygame.quit()
