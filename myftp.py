#import socket module to be able to create network sockets
import socket

#establish basic client side socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get server name from user and the port number for FTP connection is 21
serverName = input("Please enter the host name of the server you want to connect to:\n")
serverPort  = 21

#connect to hostname of server provided
clientSocket.connect((serverName, serverPort))

#all data reads will be info/messages from server
data = clientSocket.recv(1024)

#server welcome message
print("Connected to", serverName,"server with response")
print(str(data)[2:-5])

#ask for user name with USER command and print server response
username = input("Enter username: ")
clientSocket.send(bytes("USER " + username + "\r\n", "ascii"))
data = clientSocket.recv(1024)
print(str(data)[2:-5])

#ask for user password with PASS command and print server response
password = input("Enter password: ")
clientSocket.send(bytes("PASS " + password + "\r\n", 'ascii'))
data = clientSocket.recv(1024)
print(str(data)[2:-5])

#read in the IP address and port of the host FTP socket connection
ipAddress, dataPort = clientSocket.getsockname()

#this will split the IP address of the client
start = 0
end = 0
i = 0
h = []
while(end < len(ipAddress)):
    if(ipAddress[end] == '.'):
        h.insert(i,ipAddress[start:end])
        i = i + 1
        start = end + 1
    end = end + 1
h.insert(i, ipAddress[start:])

#this will encode the port number the client socket is using
p2 = int(dataPort) % 256
p1 = (int(dataPort) - p2) / 256
p1 = int(p1)

#premade PORT command to keep FTP loop clean
portIPString = "PORT " + h[0] + ',' + h[1] + ',' + h[2] + ',' + h[3] + ',' + str(p1) + ',' + str(p2)

#socket made to aquire data from a server and client will act as a server when this socket is in use
dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataSocket.bind((ipAddress, dataPort))

#actual FTP command loop
loop = True
while loop:
    userInput = input("myftp> ")

    #case for quit, simple QUIT command
    if userInput == "quit":
        loop = False
        clientSocket.send(bytes("QUIT\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

    #case for ls, need to listen for connection using a server side socket running on client
    if userInput == "ls":
        #tell server to prepare a TCP connection with client socket at client port and IP
        clientSocket.send(bytes(portIPString+"\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #NLST command that will require TCP connection and will tell server that the client is ready for data
        clientSocket.send(bytes("NLST\r\n", "ascii"))

        #start listening for TCP connection
        dataSocket.listen(1)

        #TCP warning for incoming data
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #TCP connection being accepted on client side from server for data transfer
        connectionSocket, address = dataSocket.accept()

        #data receiving
        data = connectionSocket.recv(1024)
        print("Receiving data from: " + str(address[0]) + "\n\n" +str(data.decode("ascii")))

        #TCP closing message
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #close the TCP connection
        connectionSocket.close()

clientSocket.close()
dataSocket.close()