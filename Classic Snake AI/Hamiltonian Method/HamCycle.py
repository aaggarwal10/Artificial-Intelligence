from random import randint
class HCyc:
    hcyc = {}
    def __init__(self,gX,gY):
        
        mX = gX//2
        mY = gY//2
        self.hcyc = self.makeCyc(randint(0,mX*mY-1),mX,mY,gX)

    def mst(self,start,mX,mY):
        visited = [0 for i in range(mX*mY)]
        queue = [start]
        visited[start] = 1
        adjLst = [[] for i in range (mX*mY)]
        
        while len(queue)!=0:
            curNode=queue.pop(0)
            newPoses = self.getAdj(curNode,mX,mY)
            for pos in newPoses:
                newN = pos[0]+pos[1]*mX
                if not visited[newN]:
                    visited[newN]=1
                    adjLst[min(newN,curNode)].append(max(newN,curNode))
                    queue.append(newN)
        return adjLst

    def getAdj(self,curNode,mX,mY):
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
    
    def formula(self,n,m,x):
        return (x//m)*n*4+4*(x%m)+n+1
    
    def transform(self,adLst,mX):
        n = mX*4-1
        adjDict={}
        for i in range(len(adLst)):
            for j in range(len(adLst[i])):
                adjDict.setdefault(self.formula(n,mX,i),[]).append(self.formula(n,mX,adLst[i][j]))
        return adjDict
    
    def makeMaze(self,start,mX,mY):
        grid = [["." for x in range(4*mX-1)] for y in range(4*mY-1)]
        
        gridPoints = []
        for y in range(4*mY-1):
            for x in range(4*mX-1):
                gridPoints.append([x,y])
            
        adjDict = self.transform(self.mst(start,mX,mY),mX)
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
    
    def fillPath(self,start,mX,mY):
        maze = self.makeMaze(start,mX,mY)
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

    def shrink(self,pathD,mX,gX):
        n=2*(mX*4-1)
        newDict = {}
        for key in pathD:
            k = gX*((key)//n) + (key%n)//2
            v = gX*((pathD[key])//n) + (pathD[key]%n)//2
            newDict[k]=v
        return newDict

    def makeCyc(self,start,mX,mY,gridX):
        path = self.fillPath(start,mX,mY)

        sPoint = [0,0]
        que = [sPoint]
        path[0][0] = "0"
        pathDict = {}
        pathX = 4*mX-1
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]

        while len(que)!=0:
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

        hamiltonCyc = self.shrink(pathDict,mX,gridX)
        hamiltonCyc[hamiltonCyc[list(hamiltonCyc.keys())[-1]]] = list(hamiltonCyc.keys())[0]
        
        return hamiltonCyc
