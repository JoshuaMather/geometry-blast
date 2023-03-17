from tkinter import Tk, Canvas, PhotoImage, Button, Label
from random import randint
import os




def createWindow():
    global ws, hs
    window = Tk()
    window.title("Coursework Game")

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x=(ws/2) - (ws/4)
    y=(hs/2) - (hs/4)
    window.geometry('%dx%d+%d+%d' % (ws/2, hs/2, x, y))

    return window

def createCircle(x, y, r, canvas):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill="green")

def rightKey(event):
    global direction
    direction = "right"

def leftKey(event):
    global direction
    direction = "left"

def upKey(event):
    global direction
    direction = "up"

def downKey(event):
    global direction
    direction = "down"

def checkEdge(coords, direction):
    if coords[0] < borderx0:
        direction = "right"
    elif coords[1] < bordery0:
        direction = "down"
    elif coords[2] > borderx1:
        direction = "left"
    elif coords[3] > bordery1:
        direction = "up"
    return direction

def playerMove():
    canvas.pack()
    global direction 
    playerCoords = canvas.coords(playerIcon)


    if direction == "left":
        canvas.move(playerIcon, -1,0)
    elif direction == "right":
        canvas.move(playerIcon, 1,0)
    elif direction == "up":
        canvas.move(playerIcon, 0,-1)
    elif direction == "down":
        canvas.move(playerIcon, 0,1)
    
    print(playerCoords[0])
    direction = checkEdge(playerCoords, direction)

    window.after(5, playerMove)

window = createWindow()

canvas = Canvas(window, bg="black", width=ws/2, height=hs/2)

window.update()
canvasWidth = window.winfo_width()
canvasHeight = window.winfo_height()

border = canvas.create_rectangle(20,20, canvasWidth-150, canvasHeight-20, outline="green")
borderCoords = canvas.coords(border)
borderx0 = borderCoords[0]
bordery0 = borderCoords[1]
borderx1 = borderCoords[2]
bordery1 = borderCoords[3]

level = 0
lTxt = "Level: " + str(level)
levelText = canvas.create_text(borderx1+60, bordery1-50, fill="green", font="Times 20 bold", text = lTxt) 

score = 0
sTxt = "Score: " + str(score)
scoreText = canvas.create_text(borderx1+60, bordery1-10, fill="green", font="Times 20 bold", text = sTxt) 
canvas.pack()

playerIcon = createCircle((borderx1+borderx0)/2, (bordery1+bordery0)/2, 10, canvas)

canvas.bind("<a>", leftKey)
canvas.bind("<d>", rightKey)
canvas.bind("<w>", upKey)
canvas.bind("<s>", downKey)
canvas.focus_set()

direction = "up"
playerMove()

window.mainloop()