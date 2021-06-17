from cmu_112_graphics import *
import random

class Generator():
    def __init__(self):
        self.rows=random.randint(10,14) 
        self.cols=random.randint(10,14) 
        self.board=[[False]*self.cols for i in range(self.rows)]
        self.numBox=3
        self.numEmptySpaces=0
        self.emptySpots=[]
        #self.wallCols=[]
        bestCount=0
        for i in range(10):
            board,count=Generator.generator(self)
            if count>bestCount:
                bestCount=count 
                bestBoard=board
        #print(bestCount)
        self.board=bestBoard
        #print(self.board)
        Generator.getEmptySpaces(self)
        Generator.modifyBoardRow(self)
        Generator.placePlayerCratesDots(self)
        Generator.fillBoard(self) #fill in missing rows/cols so that the board is 15x15 
        Generator.translateBoard(self) #translate board into letters
        #print(self.translatedBoard) 
        #Generator.fillBoard(self)

# randomly choose a size (8,13)
# 
# randomly choose a row, col (every other col/row to make sure there's a path) 
# inserts spaced 
    def generator(self): # makes board 
        #inspired by Tetris and https://github.com/mpSchrader/gym-sokoban/blob/master/gym_sokoban/envs/room_utils.py
        #shapes is a list of 5 shapes 
        #empty space = True
        #wall = False
        shapes = [
        [
            [False, False, False],
            [True, True, True],
            [False, False, False]
        ],
        [
            [False, True, False],
            [False, True, False],
            [False, True, False]
        ],
        [
            [False, False, False],
            [True, True, False],
            [False, True, False]
        ],
        [
            [False, False, False],
            [True, True, False],
            [True, True, False]
        ],
        [
            [False, False, False],
            [False, True, True],
            [False, True, False]
        ]]
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        direction = random.choice(directions) #chooses a random directino
        #print(direction)
        startingPosition=(random.randint(1,self.rows-1),random.randint(1,self.cols-1))
        #print(startingPosition)
        for i in range(5): #walk through the board
            direction=random.choice(directions) 
            dr,dc=direction
            r,c=startingPosition
            #check if new location is legal
            #print("new d: ", direction, (r,c))
            if Generator.isLegal(self,r+dr,c+dc):
                #print(r+dr,c+dc)
                startingPostion=(r+dr,c+dc) #change center Position (starting step location)
                
                shape=shapes[random.randint(0,4)] #randomly choose a shape for each step 
                startR,startC=r+dr-1,c+dc-1 #to make step center 
                
                #add shape to board
                #print("shape start:",shape,startR,startC)
                if Generator.isLegal(self,startR,startC) and Generator.isLegal(self,startR+3,startC+3):
                    #print("new d: ", direction, startingPostion,shape)
                    i=0
                    for row in range(startR,startR+3):
                        j=0
                        for col in range(startC,startC+3):
                            self.board[row][col]=shape[i][j]
                            j+=1
                        i+=1
                        #print(f"self.board{row,col}")
        count=0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col]==True:
                    count+=1
        return self.board,count
    
    def getSpaceInRow(self,r):
        count=0
        for col in range(len(self.board[r])):
            if self.board[r][col]==True:
                count+=1
        return count

    def getWall(self,r):
        count=0
        wallCols=[]
        for col in range(len(self.board[0])):
            if self.board[r][col]==False:
                wallCols.append(col)
        return wallCols

    #add spaces (in terms of rows) to board 
    def modifyBoardRow(self):
        for r in range(self.rows):
            numEmptySpacesInRow=Generator.getSpaceInRow(self,r) #number of empty spaces in a row
            #print(f"empty Spaces in row {r}: {numEmptySpacesInRow}")
            if numEmptySpacesInRow<=self.rows//2:
                #print("need more spots in row!")
                while numEmptySpacesInRow <= self.rows//2:
                    wallCols=Generator.getWall(self,r)
                    #print(wallCols)
                    newC=random.choice(wallCols) #choose from a list of wal pos in that row 
                    #print("new space to add: ",(r,newC))
                    self.emptySpots.append((r,newC))
                    #print("new emptySpace Locations: ",self.emptySpots)
                    numEmptySpacesInRow+=1
                    self.board[r][newC]=True
        #print("empty spots: ",self.emptySpots)
        #print(self.board)
                
    def modifyBoardCol(self):
        for emptySpace in self.emptySpots:
            r,c=emptySpace
            direction=[(0,-1),(-1,0),(0,1),(1,0)]
            try:
                s1R,s1C=r,c-1
                s2R,s2C=r-1,c
                s3R,s3C=r,c+1
                s4R,s4C=r+1,c
                adjacents=[(s1R,s1C),(s2R,s2C),(s3R,s3C),(s4R,s4C)]
                for surrR,surrC in adjacents:
                    if self.board[surrR][surrC]==False:
                        count+=1
                if count==4: #if space surrounded by 4 walls 
                    r=random.sample(adjacents,2) #randomly choose 2 to take out 
                    t1R,t1C=r[0]
                    t2R,t2C=r[1]
                    self.board[t1R][t1C]=True
                    self.board[t2R][t2C]=True
                elif count==3:
                    t1R,t1C=random.choice(adjacents)
                    self.board[t1R][t1C]=True
                    
            except:
                pass 
                    


        
    def isLegal(self,r,c):
        if 0<=r<self.rows and 0<=c<self.cols:
            return True
        return False

    def getEmptySpaces(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col]==True:
                    self.numEmptySpaces+=1
                    self.emptySpots.append((row,col))
        #print(self.emptySpots)

    def translateBoard(self):
        self.translatedBoard=""
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                setting=self.board[row][col]
                if setting==False:
                    self.translatedBoard+="w"
                elif setting==True:
                    self.translatedBoard+=" "
                else:
                    self.translatedBoard+=str(setting)
            if row!=len(self.board)-1:
                self.translatedBoard+="\n"
        #print(self.translatedBoard.splitlines())
    

          
    def placePlayerCratesDots(self): # places player and crates 
        #if not enough empty spaces 
        if self.numBox*2+1<self.numEmptySpaces:
            return "Not enough spaces"
        #randomly choose places to put dots
        #consecSpaces=Generator.getConsecutiveEmptySpaces(self)

    #complete board 
    def fillBoard(self):
        fullRow=["w","w","w","w","w","w","w","w","w","w","w","w","w","w","w"]
        if self.rows!=15:
            #print(len(self.board))
            rowsToFill=15-len(self.board)
            #print(rowsToFill)
        if self.cols!=15:
            colsToFill=15-len(self.board[0])
        for row in range(self.rows):
            for col in range(colsToFill):
                self.board[row].append("w")
        for row in range(rowsToFill):
            self.board.append(fullRow)
            #print("fill")
        #print("filled baord: ",self.board)
        #print(len(self.board))
        return self.board


#g=Generator()

# count=0
# print(len(b),len(b[0]))
# for row in range(5):
#     for col in range(5):
#         if b[row][col]==True:
#             count+=1
#         print(b[row])
# print(count)
#board=g.fillBoard()
#print(len(board),len(board[0]))
#b=[['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], ['w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
# for row in range(len(b)):
#     pass
#     print(b[row])
