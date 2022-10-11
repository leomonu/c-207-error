
from cgitb import reset, text
from email.mime import image
from glob import glob
import socket
from tkinter import *
from threading import Thread
from turtle import title
from PIL import ImageTk, Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None


canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None
gameWindow = None
leftBoxes = []
rightBoxes = []
playerType = None
dice = None
rollButton = None
finishLine = None

playerType = None
playerTurn = None

player1name = "Joining"
player2name = "Joining"

player1Label = None
player2Label = None

player1Score = 0
player2Score = 0

player1ScoreLabel = None
player2ScoreLabel = None

resetButton = None
winningMsg = None
winingFunctionCall = 0


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    playerWindow()


def playerWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global rollButton
    global winningMsg
    global resetButton

    gameWindow = Tk()
    gameWindow.title("Ludo Game Screen")
    gameWindow.attributes("-fullscreen", True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./assets/background.png")

    canvas2 = Canvas(gameWindow, width=500, height=500)
    canvas2.pack(fill="both", expand=True)
    canvas2.create_image(0, 0, image=bg, anchor="nw")
    canvas2.create_text(screen_width/2, screen_height/5,
                        text="Ludo Game", font={"Chalkboard SE", 80}, fill="white")

    createLeftBoard()
    createRightBoard()
    finishBox()

    rollButton = Button(gameWindow, text="ROLL THE DICE", fg="black", font=("Chalkboard SE", 50), width=20, height=1, command=rollingDice)
    rollButton.place(x=screen_width/2-260, y=screen_height/2+250)

    winningMsg = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=10, height=2)
    # resetButton.place(x=screen_width/2-85,y=screen_height/2+300)

    dice = canvas2.create_text(screen_width/2-40, screen_height/2+100, text="\u2680", font=("Chalkboard SE", 200), fill="white")
    
    global playerTurn
    global playerType
    global playerName
    global player1name
    global player2name
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel


    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width/2-260, y=screen_height/2+250)
    else:
        rollButton.pack_forget()

        # Creating name board
    player1Label = canvas2.create_text(400,  screen_height/2 + 100, text = player1name, font=("Chalkboard SE",80), fill='#fff176' )
    player2Label = canvas2.create_text(screen_width - 300, screen_height/2 + 100, text = player2name, font=("Chalkboard SE",80), fill='#fff176' )

     # Creating Score Board
    player1ScoreLabel = canvas2.create_text(400,  screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )

    gameWindow.resizable(True, True)

    gameWindow.mainloop()

def restGame():
    global SERVER
    SERVER.send("reset game".encode())

def handleResetGame():
    global canvas2
    global playerType
    global gameWindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global rightBoxes
    global leftBoxes
    global finishLine
    global resetButton
    global winningMsg
    global winingFunctionCall

    canvas2.itemconfigure(dice, text='\u2680')

    # Handling Reset Game
    if(playerType == 'player1'):
        # Creating roll dice button
        rollButton = Button(gameWindow, text="ROLL THE DICE", fg="black", font=("Chalkboard SE", 50), width=20, height=1, command=rollingDice)
        rollButton.place(x=screen_width/2-260, y=screen_height/2+250)
        playerTurn = True

    if(playerType == 'player2'):
        playerTurn = False

    for rBox in rightBoxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox  in leftBoxes[1:]:
        lBox.configure(bg='white')


    finishLine.configure(bg='green')
    canvas2.itemconfigure(winningMsg, text="")
    resetButton.destroy()

    # Again Recreating Reset Button for next game
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=10, height=2)
    winingFunctionCall = 0

def rollingDice():
    global playerType
    global playerTurn
    global rollButton

    # https://graphemica.com/characters/tags/dice
    dicePick = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
    diceChoices = random.choice(dicePick)
    print(diceChoices)

    if (playerType == 'player1'):
        SERVER.send(f'{diceChoices}player2Turn'.encode())

    if (playerType == 'player2'):
        SERVER.send(f'{diceChoices}player1Turn'.encode())


def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget("bg")
        if boxColor == color:
            return boxes.index(box)

    return False


def movePlayer1(steps):
    global leftBoxes
    global boxPosition

    boxPosition = checkColorPosition(leftBoxes[1:, "red"])
    if boxPosition:
        diceValue = steps
        colorRedBoxIndex = boxPosition
        totalSteps = 10

        remainingSteps = totalSteps-colorRedBoxIndex

        if steps == remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")

            global finishLine
            finishLine.configure(bg="red")
            greeting = f'Red Wins The Game'
            SERVER.send(greeting.encode('utf-8'))

        elif steps < remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")

                nextStep = (colorRedBoxIndex+1)+diceValue

                leftBoxes[nextStep].configure(bg="red")
        else:
            print("Move False")

    else:
        leftBoxes[steps].configure(bg="red")


def movePlayer2(steps):
    global rightBoxes
    global boxPosition

    boxPosition = checkColorPosition(rightBoxes[1:, "blue"])
    if boxPosition:
        diceValue = steps
        colorBlueBoxIndex = boxPosition
        totalSteps = 10

        remainingSteps = totalSteps-colorBlueBoxIndex

        if steps == remainingSteps:
            for box in rightBoxes[1:]:
                box.configure(bg="white")

            global finishLine
            finishLine.configure(bg="blue")
            greeting = f'Blue Wins The Game'
            SERVER.send(greeting.encode('utf-8'))

        elif steps < remainingSteps:
            for box in rightBoxes[1:]:
                box.configure(bg="white")

                nextStep = (colorBlueBoxIndex+1)+diceValue

                rightBoxes[nextStep].configure(bg="blue")
        else:
            print("Move False")

    else:
        rightBoxes[steps].configure(bg="blue")


def createLeftBoard():
    global gameWindow
    global leftBoxes
    global screen_height
    global screen_width

    xpos = 20
    for i in range(0, 11):
        if i == 0:
            boxLabel = Label(gameWindow, font={
                             "Chalkboard SE", 80}, bg="red", width=2, height=1, borderwidth=0)

            boxLabel.place(x=xpos, y=screen_height/2-150)

            leftBoxes.append(boxLabel)
            xpos += 30

        else:
            boxLabel = Label(gameWindow, font={
                             "Chalkboard SE", 80}, bg="white", width=2, height=2, borderwidth=0)

            boxLabel.place(x=xpos, y=screen_height/2-150)

            leftBoxes.append(boxLabel)
            xpos += 75


def createRightBoard():
    global gameWindow
    global rightBoxes
    global screen_height
    global screen_width

    xpos = 1100
    for i in range(0, 11):
        if i == 10:
            boxLabel = Label(gameWindow, font={
                             "Chalkboard SE", 80}, bg="blue", width=2, height=1, borderwidth=0)

            boxLabel.place(x=xpos, y=screen_height/2-150)

            rightBoxes.append(boxLabel)
            xpos += 30
        else:
            boxLabel = Label(gameWindow, font={
                             "Chalkboard SE", 80}, bg="white", width=2, height=2, borderwidth=0)

            boxLabel.place(x=xpos, y=screen_height/2-150)

            rightBoxes.append(boxLabel)
            xpos += 75


def finishBox():
    global gameWindow
    global screen_height
    global screen_width
    global finishLine

    finishLine = Label(gameWindow, font={
                       "Chalkboard SE", 80}, bg="green", width=8, height=4, borderwidth=0, text="Home")
    finishLine.place(x=screen_width/2-70, y=screen_height/2-150)


def handleWin(msg):
    global playerType
    global playerName
    global rollButton
    global screen_width
    global screen_height
    global resetButton
    global winningMsg

    if ("red" in msg):
        if(playerType=="player1"):
            rollButton.destroy()
    if ("blue" in msg):
        if(playerType=="player2"):
            rollButton.destroy()

    message=message.split(".")[0]+"."
    canvas2.itemconfigure(winningMsg,text=message)
    resetButton.place(x=screen_width/2-260, y=screen_height/2+250)

def updateScore(message):
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel


    if('red' in message):
        player1Score +=1

    if('blue' in message):
        player2Score +=1

    canvas2.itemconfigure(player1ScoreLabel, text = player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text = player2Score)



# Teacher write code here for askPlayerName()
def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_height
    global screen_width

    nameWindow = Tk()
    nameWindow.title("Ludo Masters")
    nameWindow.attributes("-fullscreen", True)

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./assets/background.png")

    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(screen_width/2, screen_height/5,
                        text="ENTER NAME", font={"Chalkboard SE", 80}, fill="white")

    nameEntry = Entry(nameWindow, width=25, justify="center",
                      font={"Chalkboard SE", 90}, bg="white")
    nameEntry.place(x=screen_width/2-100, y=screen_height/3)

    button = Button(nameWindow, text="save", font={
                    "Chalkboard SE", 90}, bg="yellow", command=saveName)
    button.place(x=screen_width/2-30, y=screen_height/2)

    nameWindow.resizable(True, True)

    nameWindow.mainloop()

def recivedMsg():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow
    global player1name
    global player2name
    global player1Label
    global player2Label
    global winingFunctionCall



    while True:
        message = SERVER.recv(2048).decode()

        if('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif('player_names' in message):

            players = eval(message)
            players = players["player_names"]
            for p in players:
                if(p["type"] == 'player1'):
                    player1name = p['name']
                if(p['type'] == 'player2'):
                    player2name = p['name']

        elif('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')
        #--------- Boilerplate Code Start--------
        elif('wins the game.' in message and winingFunctionCall == 0):
            winingFunctionCall +=1
            handleWin(message)
            # Addition Activity
            updateScore(message)
        elif(message == 'reset game'):
            handleResetGame()
        #--------- Boilerplate Code End--------


        #creating rollbutton
        if('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gameWindow, text="ROLL THE DICE", fg="black", font=("Chalkboard SE", 50), width=20, height=1, command=rollingDice)
            rollButton.place(x=screen_width/2-260, y=screen_height/2+250)
        elif('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gameWindow, text="ROLL THE DICE", fg="black", font=("Chalkboard SE", 50), width=20, height=1, command=rollingDice)
            rollButton.place(x=screen_width/2-260, y=screen_height/2+250)


        # Student Activity
        # Deciding player turn
        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue = diceChoices.index(message[0]) + 1

            if('player2Turn' in message):
                movePlayer1(diceValue)


            if('player1Turn' in message):
                movePlayer2(diceValue)

        # Additional Activity
        # Creating Name Board
        if(player1name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label, text=player1name)

        if(player2name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label, text=player2name)



def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 8000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    # Creating First Window
    askPlayerName()


setup()
