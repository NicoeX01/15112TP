from cmu_112_graphics import *
from makeLevels import Levels 
from pygame import mixer 
from generateLevels import Generator 
from smart import AI
import os
from playMusic import Sound   #pygame: plays music 
from bpm import bpmDetection
import math, random, time

'''
easy levels from: https://www.youtube.com/watch?v=yix2AVVUwe0&t=147s
hard levels from https://www.mathsisfun.com/games/sokoban.html 

image references: 
player: https://www.google.com/url?sa=i&url=http%3A%2F%2Fpixelartmaker.com%2Fart%2F2a37f4333343a54&psig=AOvVaw0W8BCU1l1ISkDcO6iYcu6S&ust=1620188573788000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLCzvPWWr_ACFQAAAAAdAAAAABAO
box & box placed (same image): https://www.google.com/url?sa=i&url=https%3A%2F%2Fpl.pinterest.com%2Fpin%2F560346378622910236%2F&psig=AOvVaw2rZES6JahzLe9IMM9ay2au&ust=1619908907529000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLi_iYqFp_ACFQAAAAAdAAAAABAD
wall: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.artstation.com%2Fartwork%2F3dVnEJ&psig=AOvVaw1Mot4Y-DK12ggaYVX00CJF&ust=1619908883005000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJDYt_6Ep_ACFQAAAAAdAAAAABAO
dot, ground, salmon: I made on Canva
tree (edited in canva): https://www.google.com/url?sa=i&url=https%3A%2F%2Fpwo-wiki.info%2Findex.php%2FMapping_Tutorials&psig=AOvVaw3PPqLQVEE1sXmWpvztfW1r&ust=1620067557683000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOiK-a3Wq_ACFQAAAAAdAAAAABAD

music: 
- https://www.youtube.com/watch?v=LtmZJwbLjb0   (mario)
- https://www.youtube.com/watch?v=VJLY4HqpIMU   (Grateful)
- https://www.youtube.com/watch?v=h6N1_GJAyFw   (the egg and I)
- https://youtu.be/mw_W3lo6xfQ                  (crisis core)
'''

def changeMode(app,x,y):
    w=100
    h=75
    if app.mode=="home":
        #choose levels page 
        if app.width//2<=x<=app.width//2+w and app.height/2<=y<=2.25*app.height/4:
            app.mode="chooseLevels"  
            app.gameMode="classic"
        #creative 
        elif app.width//2<=x<=app.width//2+w and app.height/2+h<=y<=2.25*app.height/4+h:
            app.mode="create"  
            app.gameMode="create"
        elif app.width//2<=x<=app.width//2+w and app.height/2+2*h<=y<=2.25*app.height/4+2*h:
            app.mode="chooseLevels"
            app.gameMode="smart"
        elif app.width//2<=x<=app.width//2+w and app.height/2+3*h<=y<=2.25*app.height/4+3*h:
            app.mode="chooseLevels"
            app.gameMode="rhythm"
    if app.mode=="create":
        if app.width//2-180<=x<=app.width//2+180 and app.height//5-50<=y<=app.height//5+50:
            app.mode="draw"  


    if clickBack(app,x,y):
        app.sound.stop()
        app.gameOver=False
        app.startPlaying=False
        b=Levels(app.level, False, "")
        app.board=b.makeBoard()
        if app.mode=="":
            if app.gameMode=="create":
                app.mode="create"
                initGame(app)
            elif app.gameMode=="rhythm":
                app.mode="chooseLevels"
            else: app.mode="chooseLevels" 
        elif app.mode=="draw":
            app.mode="create"  
            app.customBoard=b.makeEmptyBoard()
        elif app.mode=="create":
            app.mode="home" 
            app.homeStartedPlaying=False 
        elif app.mode=="chooseLevels":
            app.mode="home"  
            app.homeStartedPlaying=False 
        

def clickBack(app,x,y):
    if app.margin//2<=x<=app.margin+65 and app.margin<=y<=app.margin+40:
        return True
    return False

##### HOME PAGE #####
def home_mousePressed(app,event):
    changeMode(app,event.x,event.y)

def drawTitles(app,canvas):
    canvas.create_text(app.width//2,app.height//3,text="Sōko-ban 倉庫番",fill="salmon",font="Courier 60 bold")
    #Play --> levels
    w=100
    canvas.create_rectangle(app.width//2-w,app.height/2,app.width//2+w,2.25*app.height/4,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.width//2,2.125*app.height//4,text="Play",font="Courier 40 italic",fill="white")

    #Creative
    h=70
    canvas.create_rectangle(app.width//2-w,app.height/2+h,app.width//2+w,2.25*app.height/4+h,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.width//2,2.125*app.height//4+h,text="Create",font="Courier 40 italic",fill="white")
    
    #Smart 
    canvas.create_rectangle(app.width//2-w,app.height/2+2*h,app.width//2+w,2.25*app.height/4+2*h,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.width//2,2.125*app.height//4+2*h,text="Smart",font="Courier 40 italic",fill="white")

    #Rhythm
    canvas.create_rectangle(app.width//2-w,app.height/2+3*h,app.width//2+w,2.25*app.height/4+3*h,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.width//2,2.125*app.height//4+3*h,text="Rhythm",font="Courier 40 italic",fill="white")

def home_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="linen")
    drawTitles(app,canvas)

### CHOOSE LEVEL PAGE ###
def chooseLevels_mousePressed(app,event):
    changeMode(app,event.x,event.y)
     
def chooseLevels_keyPressed(app,event):
    if event.key.isdigit():
        app.level=event.key
        app.mode=""
        initGame(app)

def chooseLevels_timerFired(app):
    getLevelsFromFolder(app)

#get list of levels 
def getLevelsFromFolder(app):
    if app.gameMode!="create":
        fileFolder="levels"
    else:
        fileFolder="customLevels"
    removeTempFiles(fileFolder)
    app.levels=sorted(os.listdir(fileFolder))

#from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#removeTempFiles
def removeTempFiles(path, suffix='.DS_Store'): 
    if path.endswith(suffix):
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTempFiles(path + '/' + filename, suffix)

def chooseLevels_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="linen")
    canvas.create_rectangle(app.width//2-100,app.height//4-50,app.width//2+100,app.height//4+50,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.width//2,app.height//4,text=app.gameMode,font="Courier 30",fill="linen")
    drawButtons(app,canvas)
    drawLevelsScreen(app,canvas)
   
def drawLevelsScreen(app,canvas): #draw choose levels screen
    c=0
    r=0
    count=1
    x0,y0=app.width//2-200,app.height//2+100 
    for level in app.levels:
        if app.mode=="create":
            text=str(count)+": "+str(level[:level.index(".")])
            count+=1
        else:
            text=level[:level.index(".")]
        canvas.create_text(x0+c*300-100,y0+r*100-100,text=text,font="Courier 25",fill="salmon")
        c+=1
        if c==3:
            r+=1
            c=0

### CREATE BOARD PAGE ### 
def create_mousePressed(app,event):
    changeMode(app,event.x,event.y)
    
def create_keyPressed(app,event):
    if event.key.isdigit():
        app.level=app.levels[int(event.key)-1]
        app.mode=""
        initGame(app)
        
def create_timerFired(app):
    getLevelsFromFolder(app)

def create_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="linen")
    drawButtons(app,canvas)
    canvas.create_rectangle(app.width//2-180,app.height//5-50,app.width//2+180,app.height//5+50)
    canvas.create_text(app.width//2,app.height//5,text="Create New Level",fill="salmon",font="Courier 30")
    canvas.create_text(app.margin*6,app.height//3,text="Your Custom Levels: (Press 1,2,3... to choose)",fill="salmon",font="Courier 20")
    drawLevelsScreen(app,canvas)


##### SMART MODE #####


####################   MAIN GAME PAGE  #########################################
def initGame(app):
    app.levels=[]
    b=Levels(app.level, False, "")
    app.board=b.makeBoard()
    app.numDots=b.numDots
    app.dotPos=b.dotPos
    app.boxPos=b.boxPos
    app.song=app.song="music/"+random.choice(app.musicList)
    a = mixer.Sound(app.song)
    app.sound = Sound(app.song)
    #player info
    app.playerPosR,app.playerPosC=app.aiPosR,app.aiPosC=b.playerPos
    app.moves=0
    app.gameOver=False
    app.win=False
    app.randomGeneration=False
    app.hintsLeft=3
    app.hint=""
    app.showHint=False 
    app.prevPlayerPosR,app.prevPlayerPosC=app.playerPosR,app.playerPosC
    app.customBoard=b.makeEmptyBoard()

    #AI info
    app.aiBoard=copy.deepcopy(app.board)
    a=AI(app.aiBoard,copy.copy(app.boxPos),copy.copy(app.dotPos),(app.aiPosR,app.aiPosC),copy.copy(app.numDots))
    app.aiSol=a.findPath()
    app.aiMoves=0
    app.aiCount=0 
    app.aiPercent=0 
    app.aiWon=False
    app.startPlaying=False
    app.aiPrevR,app.aiPrevC=app.playerPosR,app.playerPosC
    app.initialTime=time.time()
    app.timePassed=0

    app.homeStartedPlaying=False 


def appStarted(app):
    app.level="4"  
    app.gameMode=""
    app.smartMode=False
    app.rows=app.cols=15
    app.cellSize=40
    app.margin=50
    app.marginBoard=(2*app.width/3-app.rows*app.cellSize)//2
    app.boardWidth=600
    app.boardHeight=600 
    
    
    #images 
    app.wall = app.loadImage('images/wall.jpg')
    app.player=app.loadImage('images/robot.png')
    app.box=app.loadImage('images/box.png')
    app.placed=app.loadImage('images/box_placed.png')
    app.dot=app.loadImage('images/dot.png')
    app.ground=app.loadImage('images/ground.png')
    app.salmon=app.loadImage('images/salmon.png')
    app.tree=app.loadImage('images/tree.png')
    
    # how blocks are represented: 
    # ground=" "
    # wall=w
    # box=b
    # already in place box = + 
    # player=p
    # red dot=.

    #creative mode
    app.shapes=[["w","r","p"],["r","r","r"],["b","r","."],["r","r","r"],["+","r","t"]]
    app.marginMenuX=2.2*app.width/3
    app.marginMenuY=app.marginBoard*3
    app.chosenShape=" "
    app.mode="home"

    app.musicList=os.listdir("music")
    app.song="music/"+random.choice(app.musicList)
    app.music=bpmDetection(app.song)
    app.bpm=app.music.get_file_bpm()

    mixer.init()

    app.cxPath=2.5*app.width//3
    app.cyPath=app.height//3
    app.thetaB=math.pi
    app.rPath=75
    app.rRotating=app.rTopCircle=app.rBottCircle=20
    app.cxRotating=2.5*app.width/3+app.rRotating*math.cos(app.thetaB)
    app.cyRotating=app.height//4-app.rRotating*math.sin(app.thetaB)
    app.rotatingColor="cornflower blue"
    app.cyLeftCircle=app.cyPath
    app.cxLeftCircle=app.cxPath-app.rPath
    app.cyRightCircle=app.cyPath
    app.cxRightCircle=app.cxPath+app.rPath
    app.cxTopCircle=app.cxPath
    app.cyTopCircle=app.cyPath-app.rPath
    app.cxBottCircle=app.cxPath
    app.cyBottCircle=app.cyPath+app.rPath
    app.playerTurn=True
    app.aiTurn=False

    initGame(app)
    
    
def keyPressed(app,event):
    if event.key=="c":
        app.mode="draw"
    if event.key=="Space":
        app.mode=""
        initGame(app)
    elif app.gameOver==True: return

    if event.key=="h" and app.hintsLeft!=0:
        app.showHint=True
        a=AI(app.board,copy.copy(app.boxPos),copy.copy(app.dotPos),(app.playerPosR,app.playerPosC),copy.copy(app.numDots))
        app.sol=a.findPath()
        if app.sol!=None:
            aR,aC=app.sol[0]
            app.hintsLeft-=1 
        else: 
            for dr,dc in [(-1,0),(0,-1),(0,1),(1,0)]:
                if (isLegal(app,app.playerPosR+dr,app.playerPosC+dc,dr,dc) and 
                    (app.playerPosR+dr!=app.prevPlayerPosR or app.playerPosC+dc!=app.prevPlayerPosC)):
                    aR,aC=app.playerPosR+dr,app.playerPosC+dc
                    break
            app.hintsLeft-=1
        try: 
            if aR-app.playerPosR==-1:
                app.hint="Up 1"
            elif aR-app.playerPosR==1:
                app.hint="Down 1"
            elif aC-app.playerPosC==-1:
                app.hint="Left 1"
            elif aC-app.playerPosC==1:
                app.hint="Right 1"
        except:
            app.hint="Unsolvable!"


    elif app.hintsLeft==0:
        app.hint="No more hints left!"

    if (event.key=="Up" or event.key=="Down" or event.key=="Right" or event.key=="Left"):
        if app.gameMode=="rhythm":
            if not hit(app,app.cxRotating,app.cyRotating):
                app.gameOver=True
                return 
        if event.key=="Up":
            dr,dc = (-1,0)
        elif event.key=="Down":
            dr,dc=(1,0)
        elif event.key=="Right":
            dr,dc=(0,1)
        elif event.key=="Left":
            dr,dc=(0,-1)

        tempR=app.playerPosR+dr
        tempC=app.playerPosC+dc

        if isLegal(app,tempR,tempC,dr,dc):
            app.moves+=1
            if isBox(app.board,tempR,tempC):
                app.board[tempR+dr][tempC+dc]="b"
                app.boxPos.append((tempR+dr,tempC+dc))
                app.boxPos.remove((tempR,tempC))
            app.board[app.playerPosR][app.playerPosC]=" "
            app.board[tempR][tempC]="p"
            app.prevPlayerPosR,app.prevPlayerPosC=app.playerPosR,app.playerPosC
            app.playerPosR+=dr
            app.playerPosC+=dc 
            if app.board[tempR+dr][tempC+dc]=="b" and (tempR+dr,tempC+dc) in app.dotPos:
                app.board[tempR+dr][tempC+dc]="+"
        
        #AI makes move 
        if app.gameMode=="smart":
            if (app.aiSol!=None) and app.aiMoves<len(app.aiSol)-1:
                #for i in range(2):
                aiR,aiC=app.aiSol[app.aiMoves] 
                a_dr,a_dc=aiR-app.aiPrevR,aiC-app.aiPrevC
                if isBox(app.aiBoard,aiR,aiC):
                    app.aiBoard[aiR+a_dr][aiC+a_dc]="b"

                    if app.aiBoard[aiR+a_dr][aiC+a_dc]=="b" and (aiR+a_dr,aiC+a_dc) in app.dotPos:
                        app.aiBoard[aiR+a_dr][aiC+a_dc]="+"
                        app.aiCount+=1
                app.aiBoard[aiR-a_dr][aiC-a_dc]=" "
                app.aiBoard[aiR][aiC]="p"
                    
                app.aiPrevR,app.aiPrevC=aiR,aiC
                app.aiMoves+=1


                app.aiPercent=100*app.aiCount//app.numDots
                if app.aiPercent==100:
                    app.aiWon=True
                    app.gameOver=True

# not legal if :
# it's a wall
# if there are 2 or more boxes in that direction (r,c) and (r+dr,c+dc)
# if r,c = a box but r+dr,c+dc = a wall 
def hit(app,cx,cy): #check if rotating circle is in correct position (colored block)
    if ((abs(app.cxTopCircle-cx)<=50 and abs(app.cyTopCircle-cy)<=50) or (abs(app.cxBottCircle-cx)<=50 and abs(app.cyBottCircle-cy)<=50)
        or (abs(app.cxLeftCircle-cx)<=50 and abs(app.cyLeftCircle-cy)<=50) or (abs(app.cxRightCircle-cx)<=50 and abs(app.cyRightCircle-cy)<=50)):
        return True
    return False 
def isLegal(app,r,c,dr,dc): 
    if app.board[r][c]=="w":
        return False
    elif ((app.board[r][c]=="b" or app.board[r][c]=="+") and 
         (app.board[r+dr][c+dc]=="b" or app.board[r+dr][c+dc]=="+" or app.board[r+dr][c+dc]=="w")):
        return False 
    return True

def isBox(board,r,c):
    if board[r][c]=='b' or board[r][c]=='+':
        return True  
    return False   

def mousePressed(app,event):
    row,col=getCell(app,event.x,event.y)
    w=150
    h=25
    if (2.5*app.width/3-w<=event.x<=2.5*app.width/3+w and 
        app.height-app.margin*2-h<=event.y<=app.height-app.margin*2+h):
        app.mode="draw"
        app.gameMode="create"

    changeMode(app,event.x,event.y)

def timerFired(app):
    if app.gameOver:
        app.sound.stop()
        return
    count=0
    if app.startPlaying==False and not app.gameOver:
        app.sound.start()
        app.startPlaying=True
    
    #test for gameOver 
    for r,c in app.dotPos:
        if app.board[r][c]=="+":
            count+=1
    if count==app.numDots:
        app.win=True
        app.gameOver=True

    app.timePassed=int(time.time()-app.initialTime)

    if app.gameMode=="rhythm":
        #calculated by testing/trial error  
        app.thetaB+=6*app.bpm*math.pi/7000
        app.cxRotating=app.cxPath+app.rPath*math.cos(app.thetaB)
        app.cyRotating=app.cyPath-app.rPath*math.sin(app.thetaB)
    
    
def getCell(app, x, y): #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    cellWidth  = cellHeight= app.cellSize
    row = int((y - app.marginBoard) / cellHeight)
    col = int((x - app.marginBoard) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col): #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    x0 = app.marginBoard + col * app.cellSize
    x1 = app.marginBoard + (col+1) * app.cellSize
    y0 = app.marginBoard + row * app.cellSize
    y1 = app.marginBoard + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

def drawCanvas(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="linen")

def drawBoard(app,canvas):
    for row in range(app.rows): 
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            setting=app.board[row][col]
            pic=getShape(app,setting)
            canvas.create_image(x0+20,y0+20, image=ImageTk.PhotoImage(pic))
    for r,c in app.dotPos:
        if app.board[r][c]==" ":
            (x0, y0, x1, y1) = getCellBounds(app, r, c)
            canvas.create_image(x0+20,y0+20, image=ImageTk.PhotoImage(app.dot))
                    
def drawText(app,canvas):
    d=m=0
    if app.gameMode=="smart":
        stats=[f"Level: {app.level}",
            f"Time: {app.timePassed}",
                f"AI Stats: {app.aiPercent}%"]
    else:
        stats=[f"Level: {app.level}",
                f"Moves: {app.moves}",
                f"Hints Left: {app.hintsLeft}"]
    if app.gameMode=="rhythm":
        instructions=['Instructions:',
                'You are allowed to miss beats, ',
                'but have to move on the beat.',
                'To restart, press Space.',
                'You may only move one box at a time.',
                'You may not move stacked boxes.'
               ]
    else:
        instructions=['Instructions:',
                'Your goal is to push boxes to red dots.',
                'To move around, use arrow keys.',
                'To restart, press Space.',
                'You may only move one box at a time.',
                'You may not move stacked boxes.',
                'Press h for a hint.'
               ]

    for sentence in stats:
        canvas.create_text(2.1*app.width/3,d+app.margin*2,text=sentence,
                        anchor="w",fill="royal blue",font="Courier 30 bold")
        d+=40

    for sentence in instructions:
        canvas.create_text(2.1*app.width/3,m+app.height//2+100,text=sentence,
                        anchor="w",fill="salmon",font="Courier 15")
        m+=20
    w=150
    h=25
    if app.showHint:
        canvas.create_text(2.5*app.width/3,app.margin*4.5,text=f"hint: {app.hint}",fill="royal blue",font="Courier 25")

    #creative mode button 
    canvas.create_rectangle(2.5*app.width/3-w,app.height-app.margin*2-h,
                            2.5*app.width/3+w,app.height-app.margin*2+h,
                            fill="salmon",outline="linen",width=1)
    canvas.create_text(2.5*app.width/3,app.height-app.margin*2,text="Creative Mode",
                    fill="white",font="Courier 30")

def drawButtons(app,canvas):
    #draw back button
    canvas.create_rectangle(app.margin//2,app.margin,app.margin+65,app.margin+40,fill="salmon",outline="linen",width=1)
    canvas.create_text(app.margin+20,app.margin+20,text="Back",fill="white",font="Courier 30")

def drawCircles(app,canvas):
    canvas.create_oval(app.cxTopCircle-app.rTopCircle,app.cyTopCircle-app.rTopCircle,
                        app.cxTopCircle+app.rTopCircle,app.cyTopCircle+app.rTopCircle,fill="salmon",outline="linen")

    canvas.create_oval(app.cxBottCircle-app.rBottCircle,app.cyBottCircle-app.rBottCircle,
                        app.cxBottCircle+app.rBottCircle,app.cyBottCircle+app.rBottCircle,fill="salmon",outline="linen")
    
    canvas.create_oval(app.cxRightCircle-app.rTopCircle,app.cyRightCircle-app.rTopCircle,
                        app.cxRightCircle+app.rTopCircle,app.cyRightCircle+app.rTopCircle,fill="salmon",outline="linen")

    canvas.create_oval(app.cxLeftCircle-app.rBottCircle,app.cyLeftCircle-app.rBottCircle,
                        app.cxLeftCircle+app.rBottCircle,app.cyLeftCircle+app.rBottCircle,fill="salmon",outline="linen")

    canvas.create_oval(app.cxRotating-app.rRotating,app.cyRotating-app.rRotating,
                        app.cxRotating+app.rRotating,app.cyRotating+app.rRotating,fill=app.rotatingColor,outline=app.rotatingColor)
def drawPath(app,canvas):
    canvas.create_oval(app.cxPath-app.rPath,app.cyPath-app.rPath,
                        app.cxPath+app.rPath,app.cyPath+app.rPath,
                        outline="black")

def redrawAll(app,canvas):
    drawCanvas(app,canvas)
    drawBoard(app,canvas)
    drawText(app,canvas)
    drawButtons(app,canvas)
    if app.gameMode=="rhythm":
        drawPath(app,canvas)
        drawCircles(app,canvas)

    if app.gameOver==True:
        if app.win:
            text="You Won!"
        elif app.aiWon:
            text="AI Won!"
        else: text="Game Over"
        canvas.create_text(app.width//2,app.height//2,text=text,font="Courier 50 bold")
        canvas.create_text(app.width//2,app.height//2+100,text="Press space to restart",font="Courier 20 bold")

    #sprite = app.sprites[app.spriteCounter]
    #canvas.create_image(2.5*app.width/3, app.height//2, image=ImageTk.PhotoImage(sprite))


##############################################################################   
def getMenuCell(app,x,y):
    cellWidth  = cellHeight = app.cellSize
    row = int((y - app.marginMenuY) / cellHeight)
    col = int((x - app.marginMenuX) / cellWidth)
    return (row, col)

def draw_keyPressed(app,event):
    if event.key=="q":
        app.mode=""
    pass

def draw_mousePressed(app,event):
    changeMode(app,event.x,event.y)
    if (app.marginMenuX<=event.x<=app.marginMenuX+3*app.cellSize and 
        app.marginMenuY<=event.y<=app.marginMenuY+5*app.cellSize):
        row,col=getMenuCell(app,event.x,event.y)
        app.chosenShape=app.shapes[row][col]
    if (app.marginBoard<=event.x<=app.boardWidth+app.marginBoard and 
        app.marginBoard<=event.y<=app.boardHeight+app.marginBoard): #player clicking on board
        row,col=getCell(app,event.x,event.y)
        if app.customBoard[row][col]!=" ":
            app.customBoard[row][col]=" "
        else:
            app.customBoard[row][col]=app.chosenShape
    if (2.5*app.width/3-100<=event.x<=2.5*app.width/3+100 and 
        app.height-app.margin*3-25<=event.y<=app.height-app.margin*3+25):
        app.randomGeneration=True
        randomLevel=Generator()
        generatedLevel=randomLevel.translatedBoard
        rBoard=Levels("",True,generatedLevel)
        app.randomBoard=rBoard.makeBoard()
        #app.board=randomBoard.makeBoard()
    if app.randomGeneration:
        app.customBoard=app.randomBoard
    
    w1=100
    h1=25
    if (2.5*app.width/3-w1<=event.x<=2.5*app.width/3+w1 and 
        app.height-app.margin*2-h1<=event.y<=app.height-app.margin*2+h1):
        filename = app.getUserInput('What would you like to name your customized level?')
        try:
            completeName=os.path.join("customLevels/",filename+".txt")
            customBoardTranslated=translateToText(app.customBoard)
            customLevel=open(completeName,"w")
            customLevel.write(customBoardTranslated)
            customLevel.close()
        except:
            app.message = 'File not saved. Try again by clicking Complete.'
            app.showMessage(app.message)

def translateToText(board):
    txt=""
    for row in range(len(board)):
        for col in range(len(board[0])):
            txt+=board[row][col]
        if row!=len(board)-1:
            txt+="\n"
    return txt

def getMenuCellBounds(app,row,col):
    x0 = app.marginMenuX + col * app.cellSize
    x1 = app.marginMenuX + (col+1) * app.cellSize
    y0 = app.marginMenuY + row * app.cellSize
    y1 = app.marginMenuY + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

def getShape(app,setting):
    if setting=="w":
        pic=app.wall
    elif setting=="p":
        pic=app.player
    elif setting==".":
        pic=app.dot
    elif setting==" ":
        pic=app.ground
    elif setting=="b":
        pic=app.box
    elif setting=="+":
        pic=app.placed
    elif setting=="r":
        pic=app.salmon
    elif setting=="t":
        pic=app.tree
    try: 
        return pic
    except:
        pic=app.ground
        return pic 

def drawMenu(app,canvas):
    instructions="- Choose a shape \n- Click on board to place \n- Click again to delete\n- When complete, click COMPLETE"
            
    canvas.create_text(2.25*app.width/3,app.margin*2,text="Creative Mode",font="Courier 40")
    canvas.create_text(2.25*app.width/3,app.marginMenuY-40,text="Choose what to place...",font="Courier 20")

    canvas.create_rectangle(app.marginMenuX-10,app.marginMenuY-10,app.marginMenuX+10+3*app.cellSize,
                            app.marginMenuY+10+app.cellSize*5,fill="salmon",outline="tan",width=2)
    
    for row in range(len(app.shapes)):
        for col in range(len(app.shapes[0])):
            x0,y0,x1,y1=getMenuCellBounds(app,row,col)
            setting=app.shapes[row][col]
            pic=getShape(app,setting)
            canvas.create_image(x0+20,y0+20, image=ImageTk.PhotoImage(pic))
    
    canvas.create_text(2.25*app.width/3,app.height-app.margin*4.5,text=instructions,font="Courier 15")
    
    w=100
    h=25
    canvas.create_rectangle(2.25*app.width/3-w,app.height-app.margin*3-h,
                            2.25*app.width/3+w,app.height-app.margin*3+h,
                            fill="salmon",outline="linen",width=1)
    canvas.create_text(2.25*app.width/3,app.height-app.margin*3,text="Random Board",
                    fill="white",font="Courier 20")
    canvas.create_rectangle(2.25*app.width/3-w,app.height-app.margin*2-h,
                            2.25*app.width/3+w,app.height-app.margin*2+h,
                            fill="salmon",outline="linen",width=1)
    canvas.create_text(2.25*app.width/3,app.height-app.margin*2,text="Complete",
                    fill="white",font="Courier 30")
    

def drawCustomBoard(app,canvas):
    for row in range(app.rows): 
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            setting=app.customBoard[row][col]
            pic=getShape(app,setting)
            canvas.create_image(x0+20,y0+20, image=ImageTk.PhotoImage(pic))




def draw_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="linen")
    drawCustomBoard(app,canvas)
    drawMenu(app,canvas)
    drawButtons(app,canvas)
 
runApp(width=1200,height=1000)
