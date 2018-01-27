import socket

server = socket.socket()

port = 5050
server.connect(('127.0.0.1', 5052))

toggle = 0
while 1:

    if toggle == 0:
        msg = server.recv(1024)
        if msg == "bye":
            server.close()
            break

        elif msg == "switch":
            toggle = 1

        else:
            print "server sent : ", msg

    else:

        msg = raw_input()
        if msg == "switch":
            toggle = 1
            server.send(msg)

        elif msg == "bye":
            server.send(msg)
            server.close()
            break
        else:
            server.send(msg)
