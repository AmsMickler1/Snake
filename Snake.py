#Snake!
#Amber Mickler
#COP1000 Intro to Programming Python

import random
from tkinter import *

def mousePressed(event):
    canvas = event.widget.canvas
    redrawAll(canvas)

def keyPressed(event):
    canvas = event.widget.canvas
    canvas.data["ignoreNextTimerEvent"] = True  #For better timing
    #Keys that work all the time
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        canvas.data["bonus"] = 0
        init(canvas)
    elif (event.char == "d"):
        canvas.data["inDebugMode"] = not canvas.data["inDebugMode"]
    elif (event.char == "c"):
        changeColor(canvas)
    #Keys that only work if the game is not over
    if (canvas.data["isGameOver"] == False):
        if (event.keysym == "Up"):
            moveSnake(canvas, -1, 0)
        elif (event.keysym == "Down"):
            moveSnake(canvas, 1, 0)
        elif (event.keysym == "Left"):
            moveSnake(canvas, 0, -1)
        elif (event.keysym == "Right"):
            moveSnake(canvas, 0, 1)
    redrawAll(canvas)

def moveSnake(canvas, drow, dcol):
    #Move the snake one step forward in the given direction
    snakeBoard = canvas.data["snakeBoard"]
    canvas.data["snakeDrow"] = drow     #Store movement direction
    canvas.data["snakeDcol"] = dcol
    headRow = canvas.data["headRow"]
    headCol = canvas.data["headCol"]
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if (newHeadRow < 0 or newHeadRow >= len(snakeBoard) or
        newHeadCol < 0 or newHeadCol >= len(snakeBoard[0])):
        #Snake ran off the board
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] > 0):
        #Snake ran into itself
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] == -1):
        #Snake is eating food
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol] + 1
        canvas.data["headRow"] = newHeadRow
        canvas.data["headCol"] = newHeadCol
        canvas.data["score"] += 10
        placeFood(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] == -2):
        #Snake is eating bonus
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol] + 1
        canvas.data["headRow"] = newHeadRow
        canvas.data["headCol"] = newHeadCol
        canvas.data["score"] += 50
    else:
        #Move forward like normal
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol] + 1
        canvas.data["headRow"] = newHeadRow
        canvas.data["headCol"] = newHeadCol
        removeTail(canvas)

def removeTail(canvas):
    #Find every snake cell and subtract 1
    #The last piece of the snake becomes 0 and snake length shrinks by 1
    snakeBoard = canvas.data["snakeBoard"]
    for row in range(len(snakeBoard)):
        for col in range(len(snakeBoard[0])):
            if (snakeBoard[row][col] > 0):
                snakeBoard[row][col] -= 1

def gameOver(canvas):
    canvas.data["isGameOver"] = True

def timerFired(canvas):
    if (canvas.data["isGameOver"] == False and canvas.data["ignoreNextTimerEvent"] == False):
        #Only process timerFired if game is not over and a key has not been pressed
        moveSnake(canvas, canvas.data["snakeDrow"], canvas.data["snakeDcol"])
        redrawAll(canvas)
    canvas.data["ignoreNextTimerEvent"] = False
    delay = 75  #miliseconds
    canvas.after(delay, timerFired, canvas)   #Pause, then call timerFired again

def redrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    if (canvas.data["isGameOver"]):
        canvas.create_text(canvas.data["canvasWidth"]/2, canvas.data["canvasHeight"]/2,
                           text="Game Over!", font=("Helvetica", 32, "bold"), fill="white")

def drawSnakeBoard(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def changeColor(canvas):
    #Changes the color of the Snake, Food, and Bonus
    colors = [ "LightCoral", "Crimson", "Red", "FireBrick", "HotPink", "DeepPink",
               "Tomato", "OrangeRed", "Orange", "Gold", "Khaki", "Moccasin",
               "Lavender", "Magenta", "DarkViolet", "SlateBlue", "Lime", "SpringGreen",
               "ForestGreen", "OliveDrab", "MediumAquamarine", "LightSeaGreen", "Aqua",
               "Aquamarine", "SteelBlue", "RoyalBlue", "Cornsilk", "SandyBrown",
               "Wheat", "Chocolate", "Sienna", "Maroon", "Silver", "White"]
    canvas.data["snakeColor"] = colors[random.randint(0, len(colors) - 1)]
    canvas.data["foodColor"] = colors[random.randint(0, len(colors) - 1)]
    canvas.data["bonusColor"] = colors[random.randint(0, len(colors) - 1)]

def drawSnakeCell(canvas, snakeBoard, row, col):
    margin = canvas.data["margin"]
    cellSize = canvas.data["cellSize"]
    snake = canvas.data["snakeColor"]
    food = canvas.data["foodColor"]
    bonus = canvas.data["bonusColor"]
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black")
    canvas.create_text(20, 20, text=canvas.data["score"], font=("Helvetica", 10), fill="white")
    if (snakeBoard[row][col] > 0):
        #Draw part of the snake body
        canvas.create_rectangle(left, top, right, bottom, fill=snake, outline=snake)
    elif (snakeBoard[row][col] == -1):
        #Draw food
        canvas.create_oval(left, top, right, bottom, fill=food)
    elif (snakeBoard[row][col] == -2):
        #Draw bonus
        canvas.create_oval(left, top, right, bottom, fill=bonus)
    if (canvas.data["inDebugMode"]):
        #For debugging, draw the numbers for each cell
        canvas.create_text(left + cellSize/2, top + cellSize/2, text=str(snakeBoard[row][col]),
                           font=("Helvetica", 10), fill="white")

def loadSnakeBoard(canvas):
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    snakeBoard = [ ]
    for row in range(rows):
        snakeBoard += [[0] * cols]
    snakeBoard[int(rows/2)][int(cols/2)] = 1
    canvas.data["snakeBoard"] = snakeBoard
    findSnakeHead(canvas)
    placeFood(canvas)

def placeFood(canvas):
    #Place food (-1) in a random location on the board
    snakeBoard = canvas.data["snakeBoard"]
    while (True):
        #Keep looking for a location that is not taken up by the snake
        row = random.randint(0, len(snakeBoard) - 1)
        col = random.randint(0, len(snakeBoard[0]) - 1)
        if (snakeBoard[row][col] == 0):
            break
    if (canvas.data["bonus"] < 10):
        snakeBoard[row][col] = -1
        canvas.data["bonus"] += 1
    else:
        #Every 10th food placement also places a bonus piece
        snakeBoard[row][col] = -2
        canvas.data["bonus"] = 0
        placeFood(canvas)

def findSnakeHead(canvas):
    #Find the coordinates of the largest value in snakeBoard
    snakeBoard = canvas.data["snakeBoard"]
    headRow = 0
    headCol = 0
    for row in range(len(snakeBoard)):
        for col in range(len(snakeBoard[0])):
            if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                headRow = row
                headCol = col
    canvas.data["headRow"] = headRow
    canvas.data["headCol"] = headCol

def printInstructions():
    print("Snake!"
          "\nUse the arrow keys to move."
          "\nEat the food to grow and try not to run into the walls or yourself!"
          "\nPress 'd' for Debug Mode."
          "\nPress 'c' to change the Colors."
          "\nPress 'r' to Restart."
          "\nPress 'q' to Quit.")

def init(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data["inDebugMode"] = False
    canvas.data["isGameOver"] = False
    canvas.data["snakeDrow"] = 0
    canvas.data["snakeDcol"] = -1   #Start moving left
    canvas.data["ignoreNextTimerEvent"] = False
    canvas.data["snakeColor"] = "aqua"
    canvas.data["foodColor"] = "lime"
    canvas.data["bonusColor"] = "red"
    canvas.data["score"] = 0
    redrawAll(canvas)

def run(rows, cols):
    #Create the root and the canvas
    root = Tk()
    margin = 1
    cellSize = 15
    canvasWidth = 2 * margin + cols * cellSize
    canvasHeight = 2 * margin + rows * cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    #Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    #Set up canvas data and call init
    canvas.data = { }
    canvas.data["margin"] = margin
    canvas.data["cellSize"] = cellSize
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["rows"] = rows
    canvas.data["cols"] = cols
    canvas.data["bonus"] = 0
    init(canvas)
    #Set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(canvas)
    #And launch the App

run(30, 30)
