import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverName = input("Please enter the host name of the server you want to connect to:\n")
serverPort  = 21

clientSocket.connect((serverName, serverPort))
data = clientSocket.recv(2024)

print("Connected to", serverName,"server with response", data)

clientSocket.close()