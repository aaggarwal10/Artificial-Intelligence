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

gridX = 64
gridY = 36
gridBSize= 20
screen = pygame.display.set_mode([gridX*gridBSize,gridY*gridBSize])

hCycle = [-1 for i in range(gridX*gridY)]
hCycle[0] = 0

# Creates Hamiltonian Cycle on given Grid Size. Note: Grid Must have even dimensions.
def HamiltonianCyc(gridX,gridY):

    mX = gridX//2
    mY = gridY//2

    def mst(start,mX,mY):
        visited = [0 for i in range(mX*mY)]
        queue = [start]
        visited[start] = 1
        adjLst = [[] for i in range (mX*mY)]
        
        while len(queue)!=0:
            curNode=queue.pop(0)
            newPoses = getAdj(curNode,mX,mY)
            for pos in newPoses:
                newN = pos[0]+pos[1]*mX
                if not visited[newN]:
                    visited[newN]=1
                    adjLst[min(newN,curNode)].append(max(newN,curNode))
                    queue.append(newN)
        return adjLst

    def getAdj(curNode,mX,mY):
        mazePoints = []
        for y in range(mY):
            for x in range(mX):
                mazePoints.append([x,y])

        myPos = mazePoints[curNode]
                
        dirs = [[1,0],[0,1],[-1,0],[0,-1]]
        posPos = []
        for direc in dirs:
            newPosX = direc[0]+myPos[0]
            newPosY = direc[1]+myPos[1]
            if 0<=newPosX<mX and 0<=newPosY<mY:
                posPos.append([newPosX,newPosY])
        return posPos
    
    def formula(n,m,x):
        return (x//m)*n*4+4*(x%m)+n+1
    
    def transform(adLst,mX):
        n = mX*4-1
        adjDict={}
        for i in range(len(adLst)):
            for j in range(len(adLst[i])):
                adjDict.setdefault(formula(n,mX,i),[]).append(formula(n,mX,adLst[i][j]))
        return adjDict
    
    def makeMaze(start,mX,mY):
        grid = [["." for x in range(4*mX-1)] for y in range(4*mY-1)]
        
        gridPoints = []
        for y in range(4*mY-1):
            for x in range(4*mX-1):
                gridPoints.append([x,y])
            
        adjDict = transform(mst(start,mX,mY),mX)
        for startInd in adjDict:
            for endInd in adjDict[startInd]:
                startP = gridPoints[startInd]
                endP = gridPoints[endInd]
                if startP[0]==endP[0]:
                    for y in range(startP[1],endP[1]+1):
                        grid[y][startP[0]] = "#"
                else:
                    for x in range(startP[0],endP[0]+1):
                        grid[startP[1]][x] = "#"
        return grid
    def fillPath(start,mX,mY):
        maze = makeMaze(start,mX,mY)
        dirs = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]

        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x]=="#":
                    for direc in dirs:
                        nX = direc[0]+x
                        nY = direc[1]+y
                        if maze[nY][nX]==".":
                            maze[nY][nX]="1"
                            

        return maze

    def shrink(pathD,mX,gX):
        n=2*(mX*4-1)
        newDict = {}
        for key in pathD:
            k = gX*((key)//n) + (key%n)//2
            v = gX*((pathD[key])//n) + (pathD[key]%n)//2
            newDict[k]=v
        return newDict
        
    start = 5
    path = fillPath(start,mX,mY)

    sPoint = [0,0]
    que = [sPoint]
    path[0][0] = "0"
    pathDict = {}
    pathX = 4*mX-1
    while len(que)!=0:
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]
        curPoint = que.pop(0)

        for direc in dirs:
            nPX = curPoint[0]+direc[0]
            nPY = curPoint[1]+direc[1]
            nPX2 = curPoint[0]+direc[0]*2
            nPY2 = curPoint[1]+direc[1]*2
            if 0<=nPX<4*mX-1 and 0<=nPY<4*mY-1 and path[nPY][nPX]==path[nPY2][nPX2] == "1":
                path[nPY2][nPX2]="0"
                curNode = curPoint[0]+curPoint[1]*pathX
                nNode = nPX2+nPY2*pathX
                pathDict[curNode] = nNode
                que.append([nPX2,nPY2])
                break

    hamiltonCyc = shrink(pathDict,mX,gridX)
    hamiltonCyc[hamiltonCyc[list(hamiltonCyc.keys())[-1]]] = list(hamiltonCyc.keys())[0]
    
    return hamiltonCyc


    
    


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
