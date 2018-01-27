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

serversocket = None
clientsocket = None
address = None


DISPLAYSURF = pygame.display.set_mode((windowlength,windowheight), 0, 32)
pygame.display.set_caption('server!')

serverstate = [[0 for i in range(rows)] for j in range(cols)]
clientstate = [[0 for i in range(rows)] for j in range(cols)]
serverboard = [[0 for i in range(rows)] for j in range(cols)]
clientboard = None

turn = "server"

def getstring(board):
    s = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            s += str(board[i][j])

    return s

def getboardfromstring(s):
    board = [[0 for i in range(rows)] for j in range(cols)]
    for i in range(rows):
        for j in range(cols):
            board[i][j] = int(s[i*cols + j])
    return board


def getServerBoard():
    global serverboard
    for length in range(2, 4):
        for cur in range(length):
            print "enter coordinates : "
            [x, y] = map(int, raw_input().strip().split(' '))
            serverboard[x - 1][y - 1] = length + 3



def init_connection():
    global serversocket, clientsocket, address, serverboard, clientboard
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 5054))
    serversocket.listen(5)
    (clientsocket, address) = serversocket.accept()
    clientsocket.send(getstring(serverboard))
    clientboard = getboardfromstring(clientsocket.recv(1024))


def check():
    global clientstate
    for val in range(5, 7):
        flag = False
        for row in range(rows):
            for col in range(cols):
                if clientboard[row][col] == val and clientstate[row][col] == 0:
                    flag = True
                    break

        if not flag:
            for row in range(rows):
                for col in range(cols):
                    if clientboard[row][col] == val:
                        clientstate[row][col] = 2




def main():
    global serverstate, clientstate, turn
    while 1:
        DISPLAYSURF.fill(white)

        if turn == "client":
            message = clientsocket.recv(1024)
            print message
            if len(message) != 101:
                continue
            print "message = ", message
            serverstate = getboardfromstring(message[1:])
            if message[0] == '1':
                turn = "server"

        for event in pygame.event.get():
            if event.type == locals.QUIT:
                serversocket.close()
                clientsocket.close()
                return

            if event.type == locals.K_g:
                pygame.quit()

            if event.type == locals.MOUSEBUTTONDOWN:

                if turn == "server":
                    #print "oh damn"
                    (mousex, mousey) = event.pos
                    c = (mousex - xmargin)/(width + gap)
                    r = (mousey - ymargin)/(height + gap)
                    clientstate[r][c] = 1
                    if clientboard[r][c] == 0:
                        turn = "client"
                    front = "0"
                    if turn == "client":
                        front = "1"
                    check()
                    #print "to send = ", front + getstring(clientstate)
                    clientsocket.send(front + getstring(clientstate))


        canvas.draw(DISPLAYSURF, serverstate, clientstate, serverboard, clientboard, "server", 0, turn)
        pygame.display.update()



getServerBoard()
init_connection()
main()
