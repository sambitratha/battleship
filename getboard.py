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

xmargin  = 100
ymargin  = 100

rows = 10
cols = 10

servername = "server"
clientname = "client"

windowheight = 900
windowlength = 1000

height = (windowheight - 2*ymargin)/cols
width  = (windowlength - 2*xmargin)/rows
gap = 5

board = [[0 for i in range(rows)] for j in range(cols)]


def getCurrent(DISPLAY,length, board, ref):
    #print "get current called"
    counter  = 0
    for event in pygame.event.get():
        if counter == length:
            return (board, ref)
        if event.type == locals.MOUSEBUTTONUP:
            print "mouse moved"
            print "counter incremented"
            (mousex, mousey) = event.pos
            r = (mousex - xmargin)/(width + gap)
            c = (mousey - ymargin)/(height + gap)
            board[r][c] = 1
            if length not in ref:
                ref[length] = [(r, c)]
            else:
                ref[length].append((r,c))
            counter += 1
    print "fucked"


def get(DISPLAY):
    ref = {}
    print getCurrent(DISPLAY, 2, board, ref)

