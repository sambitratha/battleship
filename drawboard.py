import pygame
import socket
import thread
import pygame.locals as locals
import time

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)
yellow = (255, 100, 100)

xmargin  = 100
ymargin  = 100

rows = 10
cols = 10

font = pygame.font.Font("EraserRegular.ttf",24)
servername = "server"
clientname = "client"

windowheight = 900
windowlength = 1000

height = (windowheight - 2*ymargin)/cols
width  = (windowlength - 2*xmargin)/rows
gap = 5

def getStringObject(s,centerx,centery,textColor,bgColor):
    textObj = font.render(s,True,textColor,bgColor)
    textRect = textObj.get_rect()
    textRect.center = (centerx, centery)
    return [textObj , textRect]

def draw(DISPLAY, serverstate, clientstate, serverboard, clientboard, person, moves, currentmove):

    myboard = False
    board = None
    state = None
    if person == "server":
        if currentmove == "server":
            board = clientboard
            state = clientstate
            myboard = False
        else:
            board = serverboard
            state = serverstate
            myboard = True
    else:
        if currentmove == "client":
            board = serverboard
            state = serverstate
            myboard = False
        else:
            board = clientboard
            state = clientstate
            myboard = True

    for row in range(rows):
        for col in range(cols):
            color = yellow
            startx = xmargin + width*col + gap*col
            starty = ymargin + height*row + gap*row
            if myboard:
                if board[row][col] != 0:
                    if state[row][col] == 0:
                        color = grey
                    elif state[row][col] == 1:
                        color = black
                    else:
                        color = red

            else:
                if board[row][col] != 0:
                    if state[row][col] == 1:
                        color = black
                    elif state[row][col] == 2:
                        color = red



            pygame.draw.rect(DISPLAY, color, (startx, starty, width, height))

            if board[row][col] == 0 and state[row][col] == 1:
                [to, tr] = getStringObject("X", startx + width/2, starty + height/2, black, yellow)
                DISPLAY.blit(to, tr)


    [tobject, trect] = getStringObject(currentmove + "'s move", windowlength/2, 50, red, white)
    DISPLAY.blit(tobject,trect)


