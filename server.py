import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(('', 5052))
#become a server socket
serversocket.listen(5)

toggle = 0
(clientsocket, address) = serversocket.accept()

while 1:

    if toggle == 0:
        data = raw_input()
        if data == "switch":
            toggle = 1
            clientsocket.send(data)

        elif data == "bye":
            clientsocket.send(data)
            clientsocket.close()
            break
        else:
            clientsocket.send(data)
    else:

        msg = clientsocket.recv(1024)

        if msg == "bye":
            clientsocket.close()
            break

        elif msg == "switch":
            toggle = 0

        else:
            print "client sent: " , msg

