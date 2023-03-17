from tkinter import Tk, Canvas, PhotoImage, Button
import random

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

def spawnEnemies(playerCoords, level, enemySize): # creates enemies, with amount being level number
    global enemy, enemyx, enemyy, borderx0, bordery0, borderx1, bordery1, enemies

    for i in range(level):
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
        if onPlayer:
            i= i -1
            canvas.delete(enemy)
        else:
            enemies.append(enemy)

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
    canvas.pack()
    global direction, level, score, shotDirection
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
            exit()

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
        
    
    window.after(5, playGame) # calls current function again

def setNewGame(): # when new game button pressed
    global inMenu
    inMenu = False
    menu.destroy()

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

    buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="Continue"))
    buttons[1].place(x=x, y=150, anchor="center")  

    buttons.append(Button(menu, width=menuWidth*15, height=menuHeight*2, bg="green", text="Leaderboard"))
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

    level = 0 # initialises level and level text created
    lTxt = "Level: " + str(level)
    levelText = canvas.create_text(borderx1+80, bordery1-50, fill="green", font="Times 20 bold", text = lTxt) 

    score = 0 # initialises score and score text created
    sTxt = "Score: " + str(score)
    scoreText = canvas.create_text(borderx1+80, bordery1-10, fill="green", font="Times 20 bold", text = sTxt) 
    canvas.pack()

    playerIcon = createCircle((borderx1+borderx0)/2, (bordery1+bordery0)/2, 10, canvas, "green") # creates player icon

    # binds keys to functions
    canvas.bind("<a>", leftKey)
    canvas.bind("<d>", rightKey)
    canvas.bind("<w>", upKey)
    canvas.bind("<s>", downKey)

    canvas.bind("<Left>", shootLeft)
    canvas.bind("<Right>", shootRight)
    canvas.bind("<Up>", shootUp)
    canvas.bind("<Down>", shootDown)
    canvas.focus_set()

    # initialises directiosn and shot list
    direction = "up"
    shotDirection = ""
    shotList = []

    # initialises lists for enemies and directions of enemies
    enemies = []
    directionOfEnemyx = []
    directionOfEnemyy = []


    playGame()

    window.mainloop()