from tkinter import Tk, Canvas, PhotoImage, Button, messagebox, Entry, Label
import random, time

def createWindow(): # creates the window for the game and menu
    global ws, hs
    window = Tk()
    window.title("Coursework Game")

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x=(ws/2) - (ws/4)
    y=(hs/2) - (hs/4)
    window.geometry('%dx%d+%d+%d' % (ws/2, hs/2, x, y))

    return window

def createCircle(x, y, r, canvas, colour): # creates a circle on the canvas givem centre and radius (used for player icon)
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=colour)

def rightKey(event): # function when move right key pressed
    global direction
    direction = "right"

def leftKey(event): # function when move left key pressed
    global direction
    direction = "left"

def upKey(event): # function when move up key pressed
    global direction
    direction = "up"

def downKey(event): # function when move down key pressed
    global direction
    direction = "down"

def shootRight(event): # function when shoot right key pressed
    global shotDirection
    if shotDirection == "": # ensures user cannot change direction of shot after it has been fired
        shotDirection = "right"

def shootLeft(event): # function when shoot left key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "left"

def shootUp(event): # function when shoot up key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "up"

def shootDown(event): # function when shoot down key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "down"

def pause(event): # function when pause key is pressed
    global pause, borderx0, bordery0, pausetext, quitTextInstruction, saveTextInstruction
    if pause == True and boss == False: # when game unpaused, makes sure boss key has not been pressed to stop text popping up on screen
        pause = False
        canvas.delete(pausetext)
        canvas.delete(saveTextInstruction)
        canvas.delete(quitTextInstruction)
        #for i in range(1,3):
            #pausetext = canvas.create_text(borderx0+10, bordery0+10, fill="green", font="Times 20 bold", text=pauseTextStates[i], anchor="nw")
            #canvas.pack()
            #time.sleep(1)
    elif pause == False and boss == False: # when game paused, makes sure boss key has not been pressed to stop text popping up on screen
        pause = True 
        pausetext = canvas.create_text(borderx0+10, bordery0+10, fill="green", font="Times 20 bold", text = pauseTextStates[0], anchor="nw")
        # can only save and quit when game paused
        saveTextInstruction = canvas.create_text(borderx1+75, bordery0+90, fill="green", font="Times 20 bold", text = "O: Save") 
        quitTextInstruction = canvas.create_text(borderx1+75, bordery0+130, fill="green", font="Times 20 bold", text = "Q: Quit") 
        canvas.pack()

def bosskey(event):
    global boss, borderx0, bordery0, bossimage
    if boss == False:
        boss = True
        bossimage = canvas.create_image(0, 0, image=spreadsheetImage, anchor="nw")
        #bossimage = bossimage.resize(canvasWidth, canvasHeight)
    else:
        boss = False
        canvas.delete(bossimage)

def quitgame(event): # allows user to quit, only when game paused
    global pause
    if pause == True:
        exit()

def save(event): # saves game by putting current level in a text file
    global pause
    if pause == True:
        file = open("SaveFile.txt", "w")
        file.write(str(level))
        file.close()

def spawnEnemies(playerCoords, level, enemySize): # creates enemies, with amount being level number
    global enemy, enemyx, enemyy, borderx0, bordery0, borderx1, bordery1, enemies

    i = 0
    while i < (level):
        i = i + 1
        print(i)
        enemy = canvas.create_rectangle(0,0, enemySize, enemySize,fill="red" )
        enemyx = random.randint(borderx0, borderx1)
        enemyy = random.randint(bordery0, bordery1)

        canvas.move(enemy, enemyx, enemyy)

        # ensures enemy does not spawn on player, and gives room around the player so they are not instanty killed
        enemyCoords = canvas.coords(enemy)
        playerCoords[0] = playerCoords[0] - enemySize
        playerCoords[1] = playerCoords[1] - enemySize
        playerCoords[2] = playerCoords[2] + enemySize
        playerCoords[3] = playerCoords[3] + enemySize
            
        onPlayer = collision(enemyCoords, playerCoords)
        if onPlayer: # if an enemy spawns in area around player then enemy is deleted and spawned somewhere else
            i = i -1
            print(i)
            canvas.delete(enemy)
        else:
            enemies.append(enemy)
            print(i)
        print(enemies)

def enemyMove(): # defines movement of enemies
    global enemies
    enemyDirectionList = ["right", "left", "up", "down"]

    for i in range(len(enemies)): # gives enemy a random start direction for x and y axis
        directionOfEnemyx.append(enemyDirectionList[(random.randint(0,1))]) 
        directionOfEnemyy.append(enemyDirectionList[(random.randint(2,3))]) 


    for i in range(len(enemies)):
        enemyCoords = canvas.coords(enemies[i])

        if enemyCoords[0] < borderx0: # changes direction if hits border
            directionOfEnemyx[i] = "right"
        elif enemyCoords[2] > borderx1:
            directionOfEnemyx[i] = "left"

        if enemyCoords[1] < bordery0:
            directionOfEnemyy[i] = "down"      
        elif enemyCoords[3] > bordery1:
            directionOfEnemyy[i] = "up"


        if directionOfEnemyx[i] == "right": # set x and y based on direction
            x=1
        elif directionOfEnemyx[i] == "left":
            x=-1

        if directionOfEnemyy[i] == "up":
            y=-1
        elif directionOfEnemyy[i] == "down":
            y=1
        
        canvas.move(enemies[i], x, y)
     

def checkEdge(coords, direction): # check if player is at edge of game window, changes direction if they are
    if coords[0] < borderx0:
        direction = "right"
    elif coords[1] < bordery0:
        direction = "down"
    elif coords[2] > borderx1:
        direction = "left"
    elif coords[3] > bordery1:
        direction = "up"
    return direction

def collision(attacker, target): # checks coordinates to see if there has been a collision
    if attacker[0] < target[2] and attacker[2] > target[0] and attacker[1] < target[3] and attacker[3] > target[1]:
        return True
    return False
    
def shotCreate(shotSize, startCoords): # creates a shot if no shot already exists
    if len(shotList) == 0 and shotDirection != "":     
        shot = canvas.create_oval(0,0, shotSize/2, shotSize/2,fill="blue" )

        canvas.move(shot, startCoords[0], startCoords[1])
        shotList.append(shot)

def shotMove(): # handles the movement of a shot on the canvas
    global shotDirection
    shot = shotList[0]
    shotCoords = canvas.coords(shot)

    if not shotDirection == "":
        if shotDirection == "right":
            canvas.move(shot, 4, 0)
        elif shotDirection == "left":
            canvas.move(shot, -4, 0)
        elif shotDirection == "down":
            canvas.move(shot, 0, 4)
        elif shotDirection == "up":
            canvas.move(shot, 0, -4)

    # if shot at edge of game window, shot is removed so another can be fired
    if shotCoords[0] < borderx0 or shotCoords[2] > borderx1 or shotCoords[1] < bordery0 or shotCoords[3] > bordery1: 
            shotList.clear()
            canvas.delete(shot)
            shotDirection = "" # allows for another shot

def playGame(): # main game function and moving player
    if pause == False and boss == False:
        canvas.pack()
        global direction, level, score, shotDirection, gameOver
        playerCoords = canvas.coords(playerIcon)
        playerSize = (playerCoords[2]-playerCoords[0])


        if len(enemies) == 0: # if all enemies destroyed, level is increased
            level += 1
            ltxt = "Level: " + str(level)
            canvas.itemconfig(levelText, text=ltxt)
            spawnEnemies(playerCoords, level, playerSize)
        
        enemyMove()

        shotCreate(playerSize, playerCoords)
        if len(shotList) == 1: # only one shot at a time
            shotMove()

        if direction == "left": # moves player based on direction
            canvas.move(playerIcon, -1,0)
        elif direction == "right":
            canvas.move(playerIcon, 1,0)
        elif direction == "up":
            canvas.move(playerIcon, 0,-1)
        elif direction == "down":
            canvas.move(playerIcon, 0,1)

        
        direction = checkEdge(playerCoords, direction)

        

        for i in range(len(enemies)): # checks each enemy to see if there is a collision between it and the player
            enemyCoords = canvas.coords(enemies[i])
            playerCoords = canvas.coords(playerIcon)
            hit = collision(enemyCoords, playerCoords)
            if hit == True:
                gameOver = True
                file = open("SaveFile.txt", "w")
                file.write("0")
                file.close()

                writeLeaderboard()

        if len(shotList) == 1:
            tempEnemies = []
            for i in range(len(enemies)): # checks each enemy to see if there is a collision between it and the shot
                enemyCoords = canvas.coords(enemies[i])
                if len(shotList) == 1:
                    shotCoords = canvas.coords(shotList[0])
                    hit = collision(shotCoords, enemyCoords)
                else:
                    hit = False

                if hit == True:
                    canvas.delete(enemies[i])
                    score += 10
                    stxt = "Score: " + str(score)
                    canvas.itemconfig(scoreText, text=stxt)
                    canvas.delete(shotList[0])
                    shotList.clear()
                    shotDirection = "" # allows for another shot

                else:
                    tempEnemies.append(enemies[i])

            enemies.clear()
            for i in range(len(tempEnemies)):
                enemies.append(tempEnemies[i])
            
    if gameOver == False: # if game over menu loaded again, if not game continues
        window.after(5, playGame) # calls current function again
    else:
        window.destroy()

def writeLeaderboard(): # handles writing new player to the leaderbaord if they score high enough
    global score, level

    def submitName(): # when name submitted, player compared with stored players and added to list if score good enough
        playerName = nameEntry.get()
        leaderboardList = []
        leaderboardList2D = []
        file = open("Leaderboard.txt", "r") # read leaderboard file to list
        for line in file:
            line = line.rstrip()
            leaderboardList.append(line)
        file.close()

        for i in range(0, len(leaderboardList), 3): # puts leaderboard contents into 2d list, with name level and score
            tempList = []
            tempList.append(leaderboardList[i])
            tempList.append(leaderboardList[i+1])
            tempList.append(leaderboardList[i+2])

            leaderboardList2D.append(tempList)

        recentPlayer = []
        recentPlayer2D = []


        recentPlayer.append(str(playerName))
        recentPlayer.append(str(level))
        recentPlayer.append(str(score))
        recentPlayer2D.append(recentPlayer)

       # listsize = len(leaderboardList2D)
        listToSave = []
        added = False
        count = 0

        # puts recent player into leaderboard if their score gets them on it
        if len(leaderboardList2D) == 0:
            listToSave.append(recentPlayer2D[0])
        else:
            for i in range(len(leaderboardList2D)):
                if count != 9:
                    if int(recentPlayer2D[0][2]) >= int(leaderboardList2D[i][2]):
                        listToSave.append(recentPlayer2D[0])
                        count += 1
                        added = True
                        if i < 9 and len(leaderboardList2D) < 10: # makes sure that only 10 item are added to the list
                            for j in range(i, len(leaderboardList2D)):
                                listToSave.append(leaderboardList2D[j])
                                count += 1
                        elif i < 9 and len(leaderboardList2D) == 10: 
                            for j in range(i, len(leaderboardList2D)-1):
                                listToSave.append(leaderboardList2D[j])
                                count += 1
                        break
                    listToSave.append(leaderboardList2D[i])
            if len(listToSave) < 9 and added == False: # adds player to end of list if list size is less than 10 and they havent already been added
                listToSave.append(recentPlayer2D[0])

        file = open("Leaderboard.txt", "w") # write leaderboard to file
        for i in range(len(listToSave)):
            file.write(str(listToSave[i][0])+"\n")
            file.write(str(listToSave[i][1])+"\n")
            file.write(str(listToSave[i][2])+"\n")    
        file.close()

        leaderboardWriteWindow.destroy()
        

    leaderboardWriteWindow = Tk() # creates leaderboard screen
    leaderboardWriteWindow.title("Write to Leaderboard")

    lws = leaderboardWriteWindow.winfo_screenwidth()
    lhs = leaderboardWriteWindow.winfo_screenheight()

    lx=(lws/4) - (lws/8)
    ly=(lhs/4) - (lhs/8)
    leaderboardWriteWindow.geometry('%dx%d+%d+%d' % (lws/4, lhs/4, lx, ly))
    
    leaderboardWriteCanvas = Canvas(leaderboardWriteWindow, bg="black", width=ws/4, height=hs/4)

    endLevelText = leaderboardWriteCanvas.create_text(lx - (lx/2), ly/4, fill="green", font="Times 20 bold", text="Level: " + str(level))
    endScoreText = leaderboardWriteCanvas.create_text(lx - (lx/2), ly/2, fill="green", font="Times 20 bold", text="Score: " + str(score))

    L1 = Label(leaderboardWriteWindow, text="User Name")
    L1.pack( side = "left")
    nameEntry = Entry(leaderboardWriteWindow)
    nameEntry.pack(side = "left")

    submitButton = Button(leaderboardWriteCanvas, width=menuWidth*15, height=menuHeight*2, bg="green", text="Submit Name", command=submitName)
    submitButton.place(x=lx - (lx/2), y=ly, anchor="center")

    leaderboardWriteCanvas.pack()


def setNewGame(): # when new game button pressed
    global inMenu, levelZero, scoreZero
    inMenu = False
    levelZero = True
    scoreZero = True
    menu.destroy()

def setContinue(): # when new game button pressed
    global inMenu, levelZero, scoreZero
    file = open("SaveFile.txt", "r")
    tempLevel = file.read()
    if tempLevel == "0":
         messagebox.showinfo("", "No save game")
    else:
        inMenu = False
        levelZero = False
        scoreZero = False
        menu.destroy()
        
    file.close()

def leaderboard(): # function for displaying the leaderboard
    def quitLeaderboard():
        leaderboardWindow.destroy()

    leaderboardList = []
    leaderboardListIndex = ["1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "10. "]

    file = open("Leaderboard.txt", "r") # reads leaderboard file
    for line in file:
        line = line.rstrip()
        leaderboardList.append(line)
    file.close()

    leaderboardWindow = Tk() # creates leaderboard screen
    leaderboardWindow.title("Leaderboard")
    leaderboardWindow.configure(bg="black")

    lws = leaderboardWindow.winfo_screenwidth()
    lhs = leaderboardWindow.winfo_screenheight()

    lx=(lws/2) - (lws/4)
    ly=(lhs/2) - (lhs/4)
    leaderboardWindow.geometry('%dx%d+%d+%d' % (lws/2, lhs/2, lx, ly))
    
    leaderboardCanvas = Canvas(leaderboardWindow, bg="black", width=ws/2, height=hs/2)

    leaderboardText = leaderboardCanvas.create_text(lx, ly/5, fill="green", font="Times 20 bold", text="Top 10 Leaderboard")

    leaderboardNameText = leaderboardCanvas.create_text(lx/2, ly/3, fill="green", font="Times 20 bold", text="Name")
    leaderboardLevelText = leaderboardCanvas.create_text(lx, ly/3, fill="green", font="Times 20 bold", text="Level")
    leaderboardScoreText = leaderboardCanvas.create_text(lx+(lx/2), ly/3, fill="green", font="Times 20 bold", text="Score")
    
    spacing = ((lx/3) - (lx/5)) / 2
    spacingNumber = 0
    starty = ly/2
    for i in range(0, len(leaderboardList), 3): # displays leaderboard data 
        nametext = str(leaderboardListIndex[spacingNumber] + leaderboardList[i])
        leveltext = str(leaderboardList[i+1])
        scoretext = str(leaderboardList[i+2])

        nameTableText = leaderboardCanvas.create_text(lx/2, starty + (spacing*spacingNumber), fill="green", font="Times 15 bold", text=nametext)
        levelTableText = leaderboardCanvas.create_text(lx, starty + (spacing*spacingNumber), fill="green", font="Times 15 bold", text=leveltext)
        scoreTableText = leaderboardCanvas.create_text(lx+(lx/2), starty + (spacing*spacingNumber), fill="green", font="Times 15 bold", text=scoretext)

        spacingNumber = spacingNumber + 1

    leaderboardCanvas.pack()

    # button to close leaderboard
    Quit = Button(leaderboardCanvas, width=menuWidth*15, height=menuHeight*2, bg="green", text="Back", command=quitLeaderboard)
    Quit.place(x=lx, y=starty + (spacing*11), anchor="center")

    leaderboardWindow.mainloop()



active = True
while active == True: # allows program to be run again until user quits
    gameOver = False
    inMenu = True

    if inMenu == True: # creating and displaying menu
        menu = Tk() # creates menu screen
        menu.title("Menu")
        menu.configure(bg="black")

        ws = menu.winfo_screenwidth()
        hs = menu.winfo_screenheight()

        x=(ws/2) - (ws/4)
        y=(hs/2) - (hs/4)
        menu.geometry('%dx%d+%d+%d' % (ws/2, hs/2, x, y))
        
        menuCanvas = Canvas(menu, bg="black", width=ws/2, height=hs/2)

        buttons = []

        menuWidth = menu.winfo_width()
        menuHeight = menu.winfo_height()

        titleText = menuCanvas.create_text(x, y/5, fill="green", font="Times 20 bold", text = "Menu")
        menuCanvas.pack()

        buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="New Game", command=setNewGame))
        buttons[0].place(x=x, y=100, anchor="center")

        buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="Continue", command=setContinue))
        buttons[1].place(x=x, y=150, anchor="center")  

        buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="Leaderboard", command=leaderboard))
        buttons[2].place(x=x, y=200, anchor="center")

        buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="Quit", command=lambda: exit()))
        buttons[3].place(x=x, y=250, anchor="center")

        menu.mainloop()

        

    if inMenu == False: # when menu not open game starts to be created
        window = createWindow() # creates window
        window.focus_force()

        canvas = Canvas(window, bg="black", width=ws/2, height=hs/2) # creates canvas

        window.update()
        canvasWidth = window.winfo_width()
        canvasHeight = window.winfo_height()

        # puts border on canvas and gets coorinates of tope left and bottom right corners
        border = canvas.create_rectangle(20,20, canvasWidth-150, canvasHeight-20, outline="green")
        borderCoords = canvas.coords(border)
        borderx0 = borderCoords[0]
        bordery0 = borderCoords[1]
        borderx1 = borderCoords[2]
        bordery1 = borderCoords[3]

        # initialises level and level text created
        if levelZero: # when new game level will start at zero
            level = 0 
        else: # when continue game gets saved level
            file=open("SaveFile.txt", "r")
            level = int(file.read())
            level = level - 1 # have to take away one as level is incremented when game starts
            file.close()
        lTxt = "Level: " + str(level)
        levelText = canvas.create_text(borderx1+75, bordery1-50, fill="green", font="Times 20 bold", text = lTxt) 

        # initialises score and score text created
        if scoreZero: # when new game score starts at zero
            score = 0 
        else:
            score = int(10*((1/2)*(level)*(level+1))) # if there is save game sets level to start of that level
        sTxt = "Score: " + str(score)
        scoreText = canvas.create_text(borderx1+75, bordery1-10, fill="green", font="Times 20 bold", text = sTxt) 

        pauseTextInstruction = canvas.create_text(borderx1+75, bordery0+10, fill="green", font="Times 20 bold", text = "P: Pause") 
        bossTextInstruction = canvas.create_text(borderx1+75, bordery0+50, fill="green", font="Times 20 bold", text = "B: Boss Key") 
        canvas.pack()

        playerIcon = createCircle((borderx1+borderx0)/2, (bordery1+bordery0)/2, 10, canvas, "green") # creates player icon

        # binds keys to functions has both upper and lower case for keys so program works if caps lock is on or not
        canvas.bind("<a>", leftKey)
        canvas.bind("<d>", rightKey)
        canvas.bind("<w>", upKey)
        canvas.bind("<s>", downKey)
        canvas.bind("<A>", leftKey)
        canvas.bind("<D>", rightKey)
        canvas.bind("<W>", upKey)
        canvas.bind("<S>", downKey)

        canvas.bind("<Left>", shootLeft)
        canvas.bind("<Right>", shootRight)
        canvas.bind("<Up>", shootUp)
        canvas.bind("<Down>", shootDown)

        canvas.bind("<p>", pause)
        canvas.bind("<q>", quitgame)
        canvas.bind("<b>", bosskey)
        canvas.bind("<o>", save)
        canvas.bind("<P>", pause)
        canvas.bind("<Q>", quitgame)
        canvas.bind("<B>", bosskey)
        canvas.bind("<O>", save)
        canvas.focus_set()

        # initialises directiosn and shot list
        direction = "up"
        shotDirection = ""
        shotList = []

        # initialises lists for enemies and directions of enemies
        enemies = []
        directionOfEnemyx = []
        directionOfEnemyy = []

        pause = False
        boss = False
        spreadsheetImage = PhotoImage(file="blankspreadsheet.png") # source: https://commons.wikimedia.org/wiki/File:WPS_Office_v11.2_Spreadsheet.png
        pauseTextStates = ["Paused", "Unpausing in: 3", "Unpausing in: 2", "Unpausing in: 1"]
        playGame()

        window.mainloop()