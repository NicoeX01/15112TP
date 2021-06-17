from generateLevels import Generator
class Levels():
    def __init__(self,level,randomLevel,generatedLevel):
        self.randomLevel=randomLevel
        self.generatedLevel=generatedLevel
        if not self.randomLevel:
            self.level=level 
        self.dotPos=[]
        self.boxPos=[]
        self.pPos=[]
        
    def makeBoard(self):
        if not self.randomLevel:
            print(self.level)
            try:
                rawBoard=open(f"levels/{self.level}.txt","r")
            except:
                rawBoard=open(f"customlevels/{self.level}","r")
            terrain=(rawBoard.read()).splitlines()
            rawBoard.close()
        else:
            #print("generated level",self.generatedLevel)
            terrain=self.generatedLevel.splitlines()
        self.board=[[]*len(terrain) for i in range(len(terrain))]
        for row in range(len(terrain)):
            for col in range(len(terrain)):
                self.board[row].append(terrain[row][col])
                if terrain[row][col]=="p":
                    self.playerPos=(row,col)
                    self.pPos.append((row,col))
                if terrain[row][col]=="." or terrain[row][col]=="+":
                    self.dotPos.append((row,col))
                if terrain[row][col]=="b" or terrain[row][col]=="+":
                    self.boxPos.append((row,col))
        self.numDots=len(self.dotPos)
        return self.board

    def makeEmptyBoard(self):
        #makes empty board for player to draw on 
        self.emptyBoard=[[" "]*15 for i in range(15)] #15 is the set # of col/row
        for i in range(15):
            self.emptyBoard[0][i]="w"
            self.emptyBoard[14][i]="w"
            self.emptyBoard[i][0]="w"
            self.emptyBoard[i][14]="w"
        #print(self.emptyBoard)
        return self.emptyBoard

 

 
        
