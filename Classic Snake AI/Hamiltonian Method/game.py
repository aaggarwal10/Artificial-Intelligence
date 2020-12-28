import pygame
from random import *
import time
import itertools

pygame.init()

gridX = 64
gridY = 36
gridBSize=20
screen = pygame.display.set_mode([gridX*gridBSize,gridY*gridBSize])




class Snake:
    heading = 0 # 0: Right, 1: Up, 2: Left, 3: Down
    snakeParts = []
    dirs = [[1,0],[0,-1],[-1,0],[0,1]] #Directions corresponding to Heading Vals
    speed = 1
    partSize = 0
    foodPosition = []
    def __init__(self,speed,gridSizeX, gridSizeY,gridBSize):
        self.snakeParts = [[3,3]]
        self.heading = 0
        self.partSize = gridBSize
        self.foodPosition = self.getFoodPos(gridSizeX,gridSizeY,self.snakeParts)
    
    def move_forw(self,gX,gY):
        head = self.snakeParts[0][:]
        head[0]+=self.speed*self.dirs[self.heading][0]
        head[1]+=self.speed*self.dirs[self.heading][1]
        if head == self.foodPosition:
            self.foodPosition = self.getFoodPos(gX,gY,self.snakeParts)
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

    def getFoodPos(self,gX,gY,posTaken):
        allPositions = list(itertools.product(*[[x for x in range(gX)],[y for y in range(gY)]]))
        shuffle(allPositions)
        for pos in allPositions:
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
    
mySnake = Snake(1,gridX,gridY,gridBSize)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            mySnake.change_heading(event.key)
    if mySnake.check_death(gridX,gridY):
        running=False
    mySnake.move_forw(gridX,gridY)
    mySnake.draw_snake_food(screen)
    time.sleep(0.04)
    pygame.display.flip()
pygame.quit()
