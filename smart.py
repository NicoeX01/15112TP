from makeLevels import Levels
import copy 
class AI():
    def __init__(self,board,boxPos,dotPos,playerPos,numDots):
        self.board=copy.deepcopy(board)
        self.boxPos=copy.copy(boxPos) #list of box locations 
        self.dotPos=copy.copy(dotPos) #list of dot locations 
        
        self.playerPos=playerPos #(row,col) of player location 
        self.cols=len(self.board[0])
        self.rows=len(self.board)
        self.numBoxPlaced=0         #number of boxes on dots 
        self.numDot=numDots       #number of dots 

        self.prevGameState={} #list; represents prev gameState 
        #self.currGameState={(self.playerPos):self.boxPos} #list; represents current gameState
        
        self.deadlocks=AI.deadlockDetector(self) #list of deadlocks 
        self.boxMoved=False

    #returns a list of locations that are deadlocks
    def deadlockDetector(self): 
        deadlocks=[]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                directions=[(0,-1),(-1,0),(0,1),(1,0)]
                i=1
                for dr,dc in directions:
                    s1R,s1C=row+dr,col+dc
                    if i==4:
                        s2R,s2C=directions[0]
                    else: 
                        s2R,s2C=directions[i]
                    s2R,s2C=row+s2R,col+s2C
                    if AI.isLegal(self,s1R,s1C) and AI.isLegal(self,s2R,s2C):
                        #check for corner 
                        if (self.board[row][col]==" " and self.board[s1R][s1C]=="w" 
                                                and self.board[s2R][s2C]=="w"):
                            deadlocks.append((row,col))
                    i+=1
        
        return deadlocks


    @staticmethod 
    def isLegal(self, row,col):
        if 0<=row<self.rows and 0<=col<self.cols:
            return True
        return False

    def findPath(self):
        # base case : num Dots = num Boxes placed 
        # recursive : go to player pos + try 4 directions 
        # for each direction: check if it's legal move, check if you are moving or pushing 
        # if pushing: check if the new box location is a deadlock 
        #   if yes: don't add it to moves 
        #   if no: add to move 
        # if moving: check if you've been on that block before; if no, move 
        return AI.helper(self,self.playerPos,[])

    def helper(self,playerPos,sol):
        if self.numBoxPlaced==self.numDot:
            return sol 
        
        d=[(0,-1),(-1,0),(0,1),(1,0)]
        for dr,dc in d:
            mode=""
            pR,pC=playerPos
            #check if it's legal move
            tempR,tempC=pR+dr,pC+dc 

            if AI.isMoveLegal(self,tempR,tempC,dr,dc) and (AI.gameStateChanges(self,tempR,tempC) or AI.isBox(self,tempR,tempC)):
                #save curr to history before updating curr box location
                local=copy.copy(self.boxPos)
                if (pR,pC) not in self.prevGameState:
                    self.prevGameState[(pR,pC)]=[sorted(local)]
                else:
                    if sorted(local) not in self.prevGameState[(pR,pC)]:
                        self.prevGameState[(pR,pC)].append(sorted(local))

                #pushing 
                if AI.isBox(self,tempR,tempC) and (tempR+dr,tempC+dc) not in self.deadlocks:
                    mode="pushing"
                    boxR,boxC=tempR+dr,tempC+dc
                    #print("pushing...", "new box pos: ",(boxR,boxC))
                    isDeadlock=False
                    #update player and box location:  
                    self.board[boxR][boxC]="b"
                    self.board[tempR][tempC]="p"
                    
                    #update current game state by adding new box location and removing old 
                    self.boxPos.append((boxR,boxC))
                    try:
                        self.boxPos.remove((tempR,tempC))
                    except:
                        self.boxPos.pop()

                    #if original (pR,pC) was a dot, change to dot  
                    if (pR,pC) in self.dotPos:
                        self.board[pR][pC]="."
                    else: self.board[pR][pC]=" "

                    if (boxR,boxC) in self.dotPos:  # if box is on dot
                        self.board[boxR][boxC]="+"
                        self.numBoxPlaced+=1

                    self.board[tempR][tempC]="p"
                    if (pR,pC) in self.dotPos:
                        self.board[pR][pC]="."
                    else: self.board[pR][pC]=" "

                    #updates player pos 
                    pR,pC=tempR,tempC 
                    sol.append((tempR,tempC))
                    res=AI.helper(self,(tempR,tempC),sol)

                # "moving"
                elif not AI.isBox(self, tempR, tempC):
                    mode="moving"
                    self.board[tempR][tempC]="p"
                    if (pR,pC) in self.dotPos:
                        self.board[pR][pC]="."
                    else: self.board[pR][pC]=" "

                    #updates player pos 
                    pR,pC=tempR,tempC 
                    sol.append((tempR,tempC))
                    res=AI.helper(self,(tempR,tempC),sol)

                
                if mode!="":
                    if res!=None:
                        return res 

                    else:  #undo moves
                        if mode=="pushing":
                            origboxR,origboxC=tempR,tempC #reset box location                             
                            #undo box moving 
                            if self.board[boxR][boxC]=="b":
                                self.board[boxR][boxC]=" "
                                self.board[origboxR][origboxC]="b"
                            elif self.board[boxR][boxC]=="+":
                                self.board[boxR][boxC]="."
                                self.board[origboxR][origboxC]="b"
                                self.numBoxPlaced-=1
                            self.boxPos.pop()
                            #self.dotPos.append((origboxR,origboxC))
                            self.boxPos.insert(0, (origboxR,origboxC))

                        self.board[pR][pC]=" " 
                        pR,pC=pR-dr,pC-dc
                        self.board[pR][pC]="p" 
                        sol.pop()
        return None

    def isMoveLegal(self,r,c,dr,dc):
        if (r>=self.rows) or r<0 or c>=self.cols or c<0 or self.board[r][c]=="w":
            return False
        elif ((self.board[r][c]=="b" or self.board[r][c]=="+") and 
            (self.board[r+dr][c+dc]=="b" or self.board[r+dr][c+dc]=="+" or self.board[r+dr][c+dc]=="w")):
            return False 
        return True

    #checks if game state changes 
    def gameStateChanges(self,tempR,tempC):
        if (tempR,tempC) in self.prevGameState:
            if sorted(self.boxPos) in self.prevGameState[(tempR,tempC)]:
                return False
        return True

    def isBox(self,r,c):
        if self.board[r][c]=='b' or self.board[r][c]=='+':
            return True  
        return False

    def checkState(self,r,c):
        if self.board[r][c]=="w":
            return "Illegal"
        elif ((self.board[r][c]=="b" or self.board[r][c]=="+") and 
            (self.board[r+dr][c+dc]=="b" or self.board[r+dr][c+dc]=="+" or self.board[r+dr][c+dc]=="w")):
            return "Illegal"
        elif self.board[r][c]=='b' or self.board[r][c]=='+':
            return "Push"
        elif self.board[r][c]=='.' or self.board[r][c]==' ':
            return "Moving"

# b=Levels("test1", False, "")
# board=b.makeBoard()
# numDots=b.numDots
# dotPos=b.dotPos
# boxPos=b.boxPos
# posR,posC=b.playerPos

# a=AI(board,boxPos,dotPos,(posR,posC),numDots)
# a.findPath()



