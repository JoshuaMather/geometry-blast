from tkinter import Tk, Canvas, PhotoImage, Button, messagebox, Entry, Label
import random
import time


def createWindow():  # creates the window for the game and menu
    global ws, hs
    window = Tk()
    window.title("Coursework Game")

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws/2) - (ws/4)
    y = (hs/2) - (hs/4)
    window.geometry('%dx%d+%d+%d' % (ws/2, hs/2, x, y))

    return window


def createCircle(x, y, r, canvas, colour):
    # creates a circle on the canvas givem centre and radius
    # (used for player icon)
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=colour)


def rightKey(event):  # function when move right key pressed
    global direction
    direction = "right"


def leftKey(event):  # function when move left key pressed
    global direction
    direction = "left"


def upKey(event):  # function when move up key pressed
    global direction
    direction = "up"


def downKey(event):  # function when move down key pressed
    global direction
    direction = "down"


def shootRight(event):  # function when shoot right key pressed
    global shotDirection
    # ensures user cannot change direction of shot after it has been fired
    if shotDirection == "":
        shotDirection = "right"


def shootLeft(event):  # function when shoot left key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "left"


def shootUp(event):  # function when shoot up key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "up"


def shootDown(event):  # function when shoot down key pressed
    global shotDirection
    if shotDirection == "":
        shotDirection = "down"


def pausegame(event):  # function when pause key is pressed
    global pause, borderx0, bordery0, pausetext, quitTextInstruction,\
           saveTextInstruction, canvas
    # when game unpaused, makes sure boss key has not been pressed
    # to stop text popping up on screen
    if pause is True and boss is False:
        pause = False
        canvas.delete(pausetext)
        canvas.delete(saveTextInstruction)
        canvas.delete(quitTextInstruction)
        canvas.pack()
        for i in range(1, 4):
            pausetext =\
                canvas.create_text(
                                   borderx0+10, bordery0+10, fill="green",
                                   font="Times 20 bold",
                                   text=pauseTextStates[i],
                                   anchor="nw")
            canvas.update()
            time.sleep(1)
            canvas.delete(pausetext)
    # when game paused, makes sure boss key has not been pressed
    # to stop text popping up on screen
    elif pause is False and boss is False:
        pause = True
        pausetext =\
            canvas.create_text(
                               borderx0+10, bordery0+10, fill="green",
                               font="Times 20 bold", text=pauseTextStates[0],
                               anchor="nw")
        # can only save and quit when game paused
        saveTextInstruction =\
            canvas.create_text(
                               borderx1+75, bordery0+90, fill="green",
                               font="Times 20 bold", text="O: Save")

        quitTextInstruction =\
            canvas.create_text(
                               borderx1+75, bordery0+130, fill="green",
                               font="Times 20 bold", text="Q: Quit")
        canvas.pack()


def bosskey(event):
    global boss, borderx0, bordery0, bossimage
    if boss is False:
        boss = True
        bossimage = canvas.create_image(0, 0,
                                        image=spreadsheetImage,
                                        anchor="nw")
    else:
        boss = False
        canvas.delete(bossimage)


def quitgame(event):  # allows user to quit, only when game paused
    global pause
    if pause is True:
        exit()


def save(event):  # saves game by putting current level in a text file
    global pause
    if pause is True:
        file = open("SaveFile.txt", "w")
        file.write(str(level))
        file.close()


def invincibility(event):  # sets a boolean to make the player invincible
    global invincible
    if invincible is False:
        invincible = True
    else:
        invincible = False


def slowmotion(event):  # sets a boolean to make the game slow motion
    global slowmo
    if slowmo is False:
        slowmo = True
    else:
        slowmo = False


def infiniteshots(event):  # sets a boolean for infinite shots cheat
    global infiniteShot, shotList, shotDirection
    if infiniteShot is False:
        # when cheat turned on current shot removed
        infiniteShot = True
        if len(shotList) == 1:
            shotDirection = ""
            canvas.delete(shotList[0])
            shotList.clear()
    else:
        infiniteShot = False
        # when cheat turned off cheated shots removed
        cheatShotDirection.clear()
        for i in range(len(cheatShotList)):
            canvas.delete(cheatShotList[i])
        cheatShotList.clear()


def spawnEnemies(playerCoords, level, enemySize):
    # creates enemies, with amount being level number
    global enemy, enemyx, enemyy, borderx0, bordery0,\
           borderx1, bordery1, enemies
    # when enemy killed they are removed from canvas but not list
    # clearing list here saves space
    enemies.clear()

    # ensures enemy does not spawn on player
    # and gives room around the player so they are not instanty killed
    playerCoords[0] = playerCoords[0] - 2*(enemySize)
    playerCoords[1] = playerCoords[1] - 2*(enemySize)
    playerCoords[2] = playerCoords[2] + 2*(enemySize)
    playerCoords[3] = playerCoords[3] + 2*(enemySize)

    for i in range(level):
        validpos = False
        while validpos is False:
            enemy = canvas.create_rectangle(0, 0, enemySize,
                                            enemySize, fill="red")
            enemyx = random.randint(borderx0, borderx1)
            enemyy = random.randint(bordery0, bordery1)

            canvas.move(enemy, enemyx, enemyy)

            enemyCoords = canvas.coords(enemy)

            onPlayer = collision(enemyCoords, playerCoords)

            # if an enemy spawns in area around player then enemy is deleted
            # and spawned somewhere else
            if onPlayer:
                canvas.delete(enemy)
                validpos = False
            else:
                enemies.append(enemy)
                validpos = True


def enemyMove():  # defines movement of enemies
    global enemies
    enemyDirectionList = ["right", "left", "up", "down"]

    # gives enemy a random start direction for x and y axis
    for i in range(len(enemies)):
        directionOfEnemyx.append(enemyDirectionList[(random.randint(0, 1))])
        directionOfEnemyy.append(enemyDirectionList[(random.randint(2, 3))])

    for i in range(len(enemies)):
        enemyCoords = canvas.coords(enemies[i])

        # changes direction if hits border
        if enemyCoords[0] < borderx0:
            directionOfEnemyx[i] = "right"
        elif enemyCoords[2] > borderx1:
            directionOfEnemyx[i] = "left"

        if enemyCoords[1] < bordery0:
            directionOfEnemyy[i] = "down"
        elif enemyCoords[3] > bordery1:
            directionOfEnemyy[i] = "up"

        if i < len(enemies) - 1:  # checks for enemy collision
            # gets coordinates of next enemy in lift
            nextEnemyCoords = canvas.coords(enemies[i+1])

            overlap = collision(enemyCoords, nextEnemyCoords)

            # swaps enemy direction if there is a collision
            if overlap is True:
                if directionOfEnemyx[i] == "right":
                    directionOfEnemyx[i] = "left"
                elif directionOfEnemyx[i] == "left":
                    directionOfEnemyx[i] = "right"

                if directionOfEnemyy[i] == "up":
                    directionOfEnemyy[i] = "down"
                elif directionOfEnemyy[i] == "down":
                    directionOfEnemyy[i] = "up"

                if directionOfEnemyx[i+1] == "right":
                    directionOfEnemyx[i+1] = "left"
                elif directionOfEnemyx[i+1] == "left":
                    directionOfEnemyx[i+1] = "right"

                if directionOfEnemyy[i+1] == "up":
                    directionOfEnemyy[i+1] = "down"
                elif directionOfEnemyy[i+1] == "down":
                    directionOfEnemyy[i+1] = "up"

        # set x and y based on direction
        if directionOfEnemyx[i] == "right":
            x = 1
        elif directionOfEnemyx[i] == "left":
            x = -1

        if directionOfEnemyy[i] == "up":
            y = -1
        elif directionOfEnemyy[i] == "down":
            y = 1

        canvas.move(enemies[i], x, y)


def enemyCollision(enemy1, enemy2):
    # checks for collisions between enemies
    if(enemy1[0] > enemy2[2] or enemy2[0] > enemy1[2]):
        return False
    if(enemy1[1] < enemy2[3] or enemy2[1] < enemy1[3]):
        return False
    return True


def checkEdge(coords, direction):
    # check if player is at edge of game window
    # changes direction if they are
    if coords[0] < borderx0:
        direction = "right"
    elif coords[1] < bordery0:
        direction = "down"
    elif coords[2] > borderx1:
        direction = "left"
    elif coords[3] > bordery1:
        direction = "up"
    return direction


def collision(attacker, target):
    # checks coordinates to see if there has been a collision
    if (attacker[0] < target[2] and
            attacker[2] > target[0] and
            attacker[1] < target[3] and
            attacker[3] > target[1]):
            return True
    return False


def shotCreate(shotSize, startCoords):
    global shotDirection
    if infiniteShot is False:
        # creates a shot if no shot already exists
        if len(shotList) == 0 and shotDirection != "":
            shot = canvas.create_oval(
                                      0, 0, shotSize/2,
                                      shotSize/2, fill="blue")

            canvas.move(shot, startCoords[0], startCoords[1])
            shotList.append(shot)
    else:
        # creates shots when infinite shots cheat activated
        if shotDirection != "":
            shot = canvas.create_oval(
                                      0, 0, shotSize/2,
                                      shotSize/2, fill="blue")

            canvas.move(shot, startCoords[0], startCoords[1])
            cheatShotList.append(shot)
            cheatShotDirection.append(shotDirection)
            shotDirection = ""


def shotMove():  # handles the movement of a shot on the canvas
    global shotDirection

    if infiniteShot is False:
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

        # if shot at edge of game window
        # shot is removed so another can be fired
        if (shotCoords[0] < borderx0 or
                shotCoords[2] > borderx1 or
                shotCoords[1] < bordery0 or
                shotCoords[3] > bordery1):
                shotList.clear()
                canvas.delete(shot)
                shotDirection = ""  # allows for another shot
    else:  # when infinite shots cheat is on
        tempShot = []
        tempDirection = []
        for i in range(len(cheatShotList)):
            shot = cheatShotList[i]
            shotDirectionC = cheatShotDirection[i]
            shotCoords = canvas.coords(shot)
            if shotDirectionC == "right":
                canvas.move(shot, 4, 0)
            elif shotDirectionC == "left":
                canvas.move(shot, -4, 0)
            elif shotDirectionC == "down":
                canvas.move(shot, 0, 4)
            elif shotDirectionC == "up":
                canvas.move(shot, 0, -4)

            # if shot at edge of game window
            #  shot is removed so another can be fired
            if (shotCoords[0] < borderx0 or
                shotCoords[2] > borderx1 or
                shotCoords[1] < bordery0 or
                shotCoords[3] > bordery1):
                    canvas.delete(shot)
            else:
                tempShot.append(shot)
                tempDirection.append(shotDirectionC)

        cheatShotList.clear()
        cheatShotDirection.clear()
        for i in range(len(tempShot)):
            cheatShotList.append(tempShot[i])
            cheatShotDirection.append(tempDirection[i])


def playGame():  # main game function and moving player
    global direction, level, score, shotDirection, gameOver
    if pause is False and boss is False:
        canvas.pack()
        playerCoords = canvas.coords(playerIcon)
        playerSize = (playerCoords[2]-playerCoords[0])

        if len(enemies) == 0:  # if all enemies destroyed, level is increased
            level += 1
            ltxt = "Level: " + str(level)
            canvas.itemconfig(levelText, text=ltxt)
            spawnEnemies(playerCoords, level, playerSize)

        enemyMove()

        shotCreate(playerSize, playerCoords)
        if len(shotList) == 1:  # only one shot at a time
            shotMove()

        if infiniteShot is True and len(cheatShotList) != 0:
            # infinite shots
            shotMove()

        if direction == "left":  # moves player based on direction
            canvas.move(playerIcon, -1, 0)
        elif direction == "right":
            canvas.move(playerIcon, 1, 0)
        elif direction == "up":
            canvas.move(playerIcon, 0, -1)
        elif direction == "down":
            canvas.move(playerIcon, 0, 1)

        playerCoords = canvas.coords(playerIcon)
        direction = checkEdge(playerCoords, direction)

        # will only check for a collision if invincible cheat is off
        if invincible is False:
            # checks each enemy to see if there is a collision
            # between it and the player
            for i in range(len(enemies)):
                enemyCoords = canvas.coords(enemies[i])
                playerCoords = canvas.coords(playerIcon)
                hit = collision(enemyCoords, playerCoords)
                if hit is True:
                    gameOver = True
                    file = open("SaveFile.txt", "w")
                    file.write("0")
                    file.close()

                    writeLeaderboard()

        if len(shotList) == 1:
            tempEnemies = []
            # checks each enemy to see if there is a collision
            # between it and the shot
            for i in range(len(enemies)):
                enemyCoords = canvas.coords(enemies[i])
                if len(shotList) == 1:
                    shotCoords = canvas.coords(shotList[0])
                    hit = collision(shotCoords, enemyCoords)
                else:
                    hit = False

                if hit is True:
                    canvas.delete(enemies[i])
                    score += 10
                    stxt = "Score: " + str(score)
                    canvas.itemconfig(scoreText, text=stxt)
                    canvas.delete(shotList[0])
                    shotList.clear()
                    shotDirection = ""  # allows for another shot
                else:
                    tempEnemies.append(enemies[i])

            enemies.clear()
            for i in range(len(tempEnemies)):
                enemies.append(tempEnemies[i])

        if infiniteShot is True and len(cheatShotList) != 0:
            # when infinite shots enabled cycles through
            # enemies and shot to see if there is a hit
            tempEnemies = []
            hitenemy = ""
            for i in range(len(enemies)):
                enemyCoords = canvas.coords(enemies[i])
                for j in range(len(cheatShotList)):
                    shotCoords = canvas.coords(cheatShotList[j])
                    hit = collision(shotCoords, enemyCoords)
                    if hit is True:
                        canvas.delete(enemies[i])
                        score += 10
                        stxt = "Score: " + str(score)
                        canvas.itemconfig(scoreText, text=stxt)
                        hitenemy = enemies[i]
                tempEnemies.append(enemies[i])
            enemies.clear()
            for i in range(len(tempEnemies)):
                if hitenemy != tempEnemies[i]:
                    enemies.append(tempEnemies[i])
    # if game over menu loaded again, if not game continues
    if slowmo is True:
        interval = 20
    else:
        interval = 5

    if gameOver is False:
        window.after(interval, playGame)  # calls current function again
    else:
        window.destroy()


def writeLeaderboard():
    # handles writing new player to the leaderbaord if they score high enough
    global score, level

    # when name submitted, player compared with stored players
    # and added to list if score good enough
    def submitName():
        playerName = nameEntry.get()
        leaderboardList = []
        leaderboardList2D = []
        file = open("Leaderboard.txt", "r")  # read leaderboard file to list
        for line in file:
            line = line.rstrip()
            leaderboardList.append(line)
        file.close()

        # puts leaderboard contents into 2d list, with name level and score
        for i in range(0, len(leaderboardList), 3):
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
                    if int(recentPlayer2D[0][2]) >=\
                                int(leaderboardList2D[i][2]):
                        listToSave.append(recentPlayer2D[0])
                        count += 1
                        added = True
                        # makes sure that only 10 item are added to the list
                        if i < 9 and len(leaderboardList2D) < 10:
                            for j in range(i, len(leaderboardList2D)):
                                listToSave.append(leaderboardList2D[j])
                                count += 1
                        elif i < 9 and len(leaderboardList2D) == 10:
                            for j in range(i, len(leaderboardList2D)-1):
                                listToSave.append(leaderboardList2D[j])
                                count += 1
                        break
                    listToSave.append(leaderboardList2D[i])
            # adds player to end of list if list size is less than 10
            # and they havent already been added
            if len(listToSave) < 9 and added is False:
                listToSave.append(recentPlayer2D[0])

        file = open("Leaderboard.txt", "w")  # write leaderboard to file
        for i in range(len(listToSave)):
            file.write(str(listToSave[i][0])+"\n")
            file.write(str(listToSave[i][1])+"\n")
            file.write(str(listToSave[i][2])+"\n")
        file.close()

        leaderboardWriteWindow.destroy()

    leaderboardWriteWindow = Tk()  # creates leaderboard screen
    leaderboardWriteWindow.title("Write to Leaderboard")

    lws = leaderboardWriteWindow.winfo_screenwidth()
    lhs = leaderboardWriteWindow.winfo_screenheight()

    lx = (lws/4) - (lws/8)
    ly = (lhs/4) - (lhs/8)
    leaderboardWriteWindow.geometry('%dx%d+%d+%d' % (lws/4, lhs/4, lx, ly))

    leaderboardWriteCanvas =\
        Canvas(leaderboardWriteWindow,
               bg="black", width=ws/4, height=hs/4)

    endLevelText =\
        leaderboardWriteCanvas.create_text(
                                           lx - (lx/2), ly/4, fill="green",
                                           font="Times 20 bold",
                                           text="Level: " + str(level))

    endScoreText =\
        leaderboardWriteCanvas.create_text(
                                           lx - (lx/2), ly/2, fill="green",
                                           font="Times 20 bold",
                                           text="Score: " + str(score))

    L1 = Label(leaderboardWriteWindow, text="User Name")
    L1.pack(side="left")
    nameEntry = Entry(leaderboardWriteWindow)
    nameEntry.pack(side="left")

    submitButton =\
        Button(leaderboardWriteCanvas, width=menuWidth*15,
               height=menuHeight*2, bg="green", text="Submit Name",
               command=submitName)
    submitButton.place(x=lx - (lx/2), y=ly, anchor="center")

    leaderboardWriteCanvas.pack()


def setNewGame():  # when new game button pressed
    global inMenu, levelZero, scoreZero
    inMenu = False
    levelZero = True
    scoreZero = True
    menu.destroy()


def setContinue():  # when new game button pressed
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


def leaderboard():  # function for displaying the leaderboard
    def quitLeaderboard():
        leaderboardWindow.destroy()

    leaderboardList = []
    leaderboardListIndex = ["1. ", "2. ", "3. ",
                            "4. ", "5. ", "6. ",
                            "7. ", "8. ", "9. ", "10. "]

    file = open("Leaderboard.txt", "r")  # reads leaderboard file
    for line in file:
        line = line.rstrip()
        leaderboardList.append(line)
    file.close()

    leaderboardWindow = Tk()  # creates leaderboard screen
    leaderboardWindow.title("Leaderboard")
    leaderboardWindow.configure(bg="black")

    lws = leaderboardWindow.winfo_screenwidth()
    lhs = leaderboardWindow.winfo_screenheight()

    lx = (lws/2) - (lws/4)
    ly = (lhs/2) - (lhs/4)
    leaderboardWindow.geometry('%dx%d+%d+%d' % (lws/2, lhs/2, lx, ly))

    leaderboardCanvas = Canvas(leaderboardWindow,
                               bg="black", width=ws/2, height=hs/2)

    leaderboardText =\
        leaderboardCanvas.create_text(
                                      lx, ly/5, fill="green",
                                      font="Times 20 bold",
                                      text="Top 10 Leaderboard")

    leaderboardNameText =\
        leaderboardCanvas.create_text(
                                      lx/2, ly/3, fill="green",
                                      font="Times 20 bold", text="Name")

    leaderboardLevelText =\
        leaderboardCanvas.create_text(
                                      lx, ly/3, fill="green",
                                      font="Times 20 bold", text="Level")

    leaderboardScoreText =\
        leaderboardCanvas.create_text(
                                      lx+(lx/2), ly/3, fill="green",
                                      font="Times 20 bold", text="Score")

    spacing = ((lx/3) - (lx/5)) / 2
    spacingNumber = 0
    starty = ly/2
    for i in range(0, len(leaderboardList), 3):  # displays leaderboard data
        nametext = str(leaderboardListIndex[spacingNumber] +
                       leaderboardList[i])
        leveltext = str(leaderboardList[i+1])
        scoretext = str(leaderboardList[i+2])

        nameTableText =\
            leaderboardCanvas.create_text(
                                          lx/2,
                                          starty + (spacing*spacingNumber),
                                          fill="green", font="Times 15 bold",
                                          text=nametext)

        levelTableText =\
            leaderboardCanvas.create_text(
                                          lx, starty + (spacing*spacingNumber),
                                          fill="green", font="Times 15 bold",
                                          text=leveltext)

        scoreTableText =\
            leaderboardCanvas.create_text(
                                          lx+(lx/2),
                                          starty + (spacing*spacingNumber),
                                          fill="green", font="Times 15 bold",
                                          text=scoretext)

        spacingNumber = spacingNumber + 1

    leaderboardCanvas.pack()

    # button to close leaderboard
    Quit =\
        Button(leaderboardCanvas, width=menuWidth*15,
               height=menuHeight*2, bg="green", text="Back",
               command=quitLeaderboard)
    Quit.place(x=lx, y=starty + (spacing*11), anchor="center")

    leaderboardWindow.mainloop()

active = True
while active is True:  # allows program to be run again until user quits
    gameOver = False
    inMenu = True

    if inMenu is True:  # creating and displaying menu
        menu = Tk()  # creates menu screen
        menu.title("Menu")
        menu.configure(bg="black")

        ws = menu.winfo_screenwidth()
        hs = menu.winfo_screenheight()

        x = (ws/2) - (ws/4)
        y = (hs/2) - (hs/4)
        menu.geometry('%dx%d+%d+%d' % (ws/2, hs/2, x, y))

        menuCanvas = Canvas(menu, bg="black", width=ws/2, height=hs/2)

        buttons = []

        menuWidth = menu.winfo_width()
        menuHeight = menu.winfo_height()

        titleText =\
            menuCanvas.create_text(
                                   x, y/5, fill="green",
                                   font="Times 20 bold", text="Menu")
        menuCanvas.pack()

        buttons.append(Button(
                              menu, width=menuWidth*15, height=menuHeight*2,
                              bg="green", text="New Game",
                              command=setNewGame))
        buttons[0].place(x=x, y=100, anchor="center")

        buttons.append(Button(
                              menu, width=menuWidth*15, height=menuHeight*2,
                              bg="green", text="Continue",
                              command=setContinue))
        buttons[1].place(x=x, y=150, anchor="center")

        buttons.append(Button(
                              menu, width=menuWidth*15, height=menuHeight*2,
                              bg="green", text="Leaderboard",
                              command=leaderboard))
        buttons[2].place(x=x, y=200, anchor="center")

        buttons.append(Button(
                              menu, width=menuWidth*15, height=menuHeight*2,
                              bg="green", text="Quit", command=lambda: exit()))
        buttons[3].place(x=x, y=250, anchor="center")

        controlsList = ["W: up", "A: Right", "D: Left", "S: Down",
                        "Up Arrow: Shoot Up", "Right Arrow: Shoot Right",
                        "Lef Arrow: Shoot Left", "Down Arrow: Shoot Down"]

        ypos = y/5
        menuCanvas.create_text(
                               x/2, ypos, fill="green",
                               font="Times 20 bold", text="Controls")

        menuCanvas.create_text(
                               x+(x/2), ypos+y/5, fill="green",
                               font="Times 15 bold",
                               text="Pause game to save or quit")
        for i in range(8):
            ypos += y/5
            menuCanvas.create_text(
                                   x/2, ypos, fill="green",
                                   font="Times 15 bold", text=controlsList[i])
        menu.mainloop()

    if inMenu is False:  # when menu not open game starts to be created
        window = createWindow()  # creates window
        window.focus_force()

        # creates canvas
        canvas = Canvas(window, bg="black", width=ws/2, height=hs/2)

        window.update()
        canvasWidth = window.winfo_width()
        canvasHeight = window.winfo_height()

        # puts border on canvas and gets coorinates of top left
        # and bottom right corners
        border =\
            canvas.create_rectangle(
                                    20, 20, canvasWidth-150,
                                    canvasHeight-20, outline="green")
        borderCoords = canvas.coords(border)
        borderx0 = borderCoords[0]
        bordery0 = borderCoords[1]
        borderx1 = borderCoords[2]
        bordery1 = borderCoords[3]

        # initialises level and level text created
        if levelZero:  # when new game level will start at zero
            level = 0
        else:  # when continue game gets saved level
            file = open("SaveFile.txt", "r")
            level = int(file.read())
            # have to take away one as level is incremented when game starts
            level = level - 1
            file.close()
        lTxt = "Level: " + str(level)
        levelText =\
            canvas.create_text(
                               borderx1+75, bordery1-50, fill="green",
                               font="Times 20 bold", text=lTxt)

        # initialises score and score text created
        if scoreZero:  # when new game score starts at zero
            score = 0
        else:
            # if there is save game sets level to start of that level
            score = int(10*((1/2)*(level)*(level+1)))
        sTxt = "Score: " + str(score)
        scoreText =\
            canvas.create_text(
                               borderx1+75, bordery1-10, fill="green",
                               font="Times 20 bold", text=sTxt)

        pauseTextInstruction =\
            canvas.create_text(
                               borderx1+75, bordery0+10, fill="green",
                               font="Times 20 bold", text="P: Pause")

        bossTextInstruction =\
            canvas.create_text(
                               borderx1+75, bordery0+50, fill="green",
                               font="Times 20 bold", text="B: Boss Key")
        canvas.pack()

        # creates player icon
        playerIcon = createCircle((borderx1+borderx0)/2,
                                  (bordery1+bordery0)/2, 10, canvas, "green")

        # binds keys to functions has both upper and lower case for keys
        # so program works if caps lock is on or not
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

        canvas.bind("<p>", pausegame)
        canvas.bind("<q>", quitgame)
        canvas.bind("<b>", bosskey)
        canvas.bind("<o>", save)
        canvas.bind("<P>", pausegame)
        canvas.bind("<Q>", quitgame)
        canvas.bind("<B>", bosskey)
        canvas.bind("<O>", save)

        # cheat codes keys
        canvas.bind("<i>", invincibility)
        canvas.bind("<I>", invincibility)
        canvas.bind("<c>", slowmotion)
        canvas.bind("<C>", slowmotion)
        canvas.bind("<x>", infiniteshots)
        canvas.bind("<X>", infiniteshots)
        canvas.focus_set()

        # initialises directiosn and shot list
        direction = "up"
        shotDirection = ""
        shotList = []
        cheatShotList = []
        cheatShotDirection = []

        # initialises lists for enemies and directions of enemies
        enemies = []
        directionOfEnemyx = []
        directionOfEnemyy = []

        pause = False
        boss = False

        # source:
        # https://commons.wikimedia.org/wiki/File:WPS_Office_v11.2_Spreadsheet.png
        spreadsheetImage = PhotoImage(file="blankspreadsheet.png")

        pauseTextStates = ["Paused", "Unpausing in: 3",
                           "Unpausing in: 2", "Unpausing in: 1"]

        # initially cheats off
        invincible = False
        slowmo = False
        infiniteShot = False
        playGame()

        window.mainloop()
