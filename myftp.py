import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverName = input("Please enter the host name of the server you want to connect to:\n")
serverPort  = 21

clientSocket.connect((serverName, serverPort))
data = clientSocket.recv(1024)

print("Connected to", serverName,"server with response")
print(str(data)[2:-5])

username = input("Enter username: ")
clientSocket.send(bytes("USER " + username + "\r\n", "ascii"))
data = clientSocket.recv(1024)
print(str(data)[2:-5])

password = input("Enter password: ")
clientSocket.send(bytes("PASS " + password + "\r\n", 'ascii'))
data = clientSocket.recv(1024)
print(str(data)[2:-5])

loop = True
while loop:
    userInput = input("myftp> ")

    if userInput == "quit":
        loop = False
        clientSocket.send(bytes("QUIT\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

clientSocket.close()