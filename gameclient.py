import pygame
import socket
import thread
import pygame.locals as locals
import time
pygame.init()

import getboard
import drawboard as canvas

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)

xmargin  = 100
ymargin  = 100
rows = 10
cols = 10

windowheight = 900
windowlength = 1000
height = (windowheight - 2*ymargin)/cols
width  = (windowlength - 2*xmargin)/rows
gap = 5


DISPLAYSURF = pygame.display.set_mode((windowlength,windowheight), 0, 32)
pygame.display.set_caption('client!')


clientsocket = None
turn = "server"

serverstate = [[0 for i in range(rows)] for j in range(cols)]
clientstate = [[0 for i in range(rows)] for j in range(cols)]
clientboard = [[0 for i in range(rows)] for j in range(cols)]



def getstring(board):
    s = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            s += str(board[i][j])

    return s

def getboardfromstring(s):
    print len(s), s
    board = [[0 for i in range(rows)] for j in range(cols)]
    for i in range(rows):
        for j in range(cols):
            print "i = ", i , "j = ", j, s[i*cols + j]
            board[i][j] = int(s[i*cols + j])
    return board


def getClientBoard():
    global serverboard
    for length in range(2, 4):
        for cur in range(length):
            print "enter coordinates : "
            [x, y] = map(int, raw_input().strip().split(' '))
            clientboard[x - 1][y - 1] = length + 3


def init_connection():
    global clientsocket, serverboard
    clientsocket = socket.socket()
    clientsocket.connect(('127.0.0.1',5054))
    serverboard = getboardfromstring(clientsocket.recv(1024))
    clientsocket.send(getstring(clientboard))

def check():
    global serverstate
    for val in range(5, 7):
        flag = False
        for row in range(rows):
            for col in range(cols):
                if serverboard[row][col] == val and serverstate[row][col] == 0:
                    flag = True
                    break

        if not flag:
            for row in range(rows):
                for col in range(cols):
                    if serverboard[row][col] == val:
                        serverstate[row][col] = 2


def isover():
    global turn
    flagserver = True
    flagclient = True
    for row in range(rows):
        for col in range(cols):
            if clientboard[row][col] != 0 and clientstate[row][col] == 0:
                flagserver = False
            if serverboard[row][col] != 0 and serverstate[row][col] == 0:
                flagclient = False

    if flagserver:
        turn = "overserver"
    if flagclient:
        turn = "overclient"



def main():
    global clientstate, serverstate, turn
    while 1:
        DISPLAYSURF.fill(white)
        isover()
        canvas.draw(DISPLAYSURF, serverstate, clientstate, serverboard, clientboard, "client", 0, turn)
        pygame.display.update()

        if turn == "server":
            message = clientsocket.recv(1024)
            print "message = ",message
            if len(message) != 101:
                continue
            if message[0] == '1':
                turn = "client"
            clientstate = getboardfromstring(message[1:])

        for event in pygame.event.get():
            if event.type == locals.QUIT:
                clientsocket.close()
                return

            if event.type == locals.K_g:
                pygame.quit()

            if event.type == locals.MOUSEBUTTONDOWN:
                if turn == "client":
                    print "oh damn"
                    (mousex, mousey) = event.pos
                    c = (mousex - xmargin)/(width + gap)
                    r = (mousey - ymargin)/(height + gap)
                    if serverboard[r][c] == 0:
                        turn = "server"
                    serverstate[r][c] = 1
                    check()
                    front = "0"
                    if turn == "server":
                        front = "1"
                    clientsocket.send(front + getstring(serverstate))


getClientBoard()
init_connection()
main()
