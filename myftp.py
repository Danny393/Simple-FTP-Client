#import socket module to be able to create network sockets
from socket import socket, AF_INET, SOCK_STREAM


#establish basic client side socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#get server name from user and the port number for FTP 21 through TCP connection
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

#this is mainly done to get the IP Address of the client for TCP connections
#and marks the end of basic client to server connection
ipAddress, dataPort = clientSocket.getsockname()

###################################################################################
#this will provide a PORT command with a new port each time we use a TCP connection
#this PORT command needs to be generated each time to make sure we are not using a busy port
def getPortIPString(IP, freePort):
    start = 0
    end = 0
    i = 0
    h = []
    while(end < len(IP)):
        if(IP[end] == '.'):
            h.insert(i,IP[start:end])
            i = i + 1
            start = end + 1
        end = end + 1
    h.insert(i, IP[start:])

    #this will encode the port number the client socket is using
    p2 = int(freePort) % 256
    p1 = (int(freePort) - p2) / 256
    p1 = int(p1)

    #premade PORT command to keep FTP loop clean
    portCommand = "PORT " + h[0] + ',' + h[1] + ',' + h[2] + ',' + h[3] + ',' + str(p1) + ',' + str(p2)

    return portCommand

########################
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

    #case for cd, simple CWD command
    elif len(userInput) >= 2 and userInput[:2] == "cd":

        clientSocket.send(bytes("CWD " + userInput[3:] + "\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

    #case for ls, need to listen for connection using a server side socket running on client
    elif userInput == "ls":

        #socket made to aquire data from a server and client will act as a server when this socket is in use
        dataSocket = socket(AF_INET, SOCK_STREAM)

        #sets data socket to free port
        dataSocket.bind((ipAddress, 0))

        #generated PORT command based on new data socket port
        portIPString = getPortIPString(ipAddress, dataSocket.getsockname()[1])

        #tell server to prepare a TCP connection with client socket at client port and IP
        clientSocket.send(bytes(portIPString+"\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #NLST command that will require TCP connection and will tell server that the client is ready for data
        clientSocket.send(bytes("NLST\r\n", "ascii"))

        #start listening for TCP connection request
        dataSocket.listen(1)

        #TCP connection being accepted on client side from server for data transfer
        connectionSocket, address = dataSocket.accept()

        #TCP warning for incoming data
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #data receiving
        list = connectionSocket.recv(1024)
        print("Receiving data from: " + str(address[0]) + "\n\n" +str(list.decode("ascii")))

        #TCP closing message
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        print("bytes received:", len(list))

        #close data and connection socket
        connectionSocket.close()
        dataSocket.close()

    #case for get, very similar to ls, but we check for the error code to make sure
    #we don't soft lock the system and deal with each response code (Error and Success)
    elif(len(userInput) >= 4 and userInput[:3] == "get"):

        downloadFile = userInput[4:]
        print(downloadFile)

        dataSocket = socket(AF_INET, SOCK_STREAM)
        dataSocket.bind((ipAddress, 0))
        portIPString = getPortIPString(ipAddress, dataSocket.getsockname()[1])

        clientSocket.send(bytes(portIPString+ "\r\n", "ascii"))
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        clientSocket.send(bytes("RETR " + downloadFile + "\r\n", "ascii"))
        dataSocket.listen(1)

        #this is where we need to branch if we get an error code or success code
        data = clientSocket.recv(1024)
        print(str(data)[2:-5])

        #if we get the error code then we print an error message and then close sockets
        if str(data)[2:5] == "550":
            print("File does not exist or directory cannot be downloaded")

        #else we accept the connection and download the file contents, assuming the file is .txt
        else:
            connectionSocket, address = dataSocket.accept()
            file = connectionSocket.recv(1024)
            print("Receiving data from: " + str(address[0]))

            newFile = open(downloadFile, "w+")
            newFile.write(str(file.decode("ascii")))
            newFile.close()

            data = clientSocket.recv(1024)
            print(str(data)[2:-5])

            print("bytes received:", len(file))

        connectionSocket.close()
        dataSocket.close()

    #put command
    elif(len(userInput) >= 3 and userInput[:3] == "put"):
        print("Hello")

    #delete command
    elif(len(userInput) >= 6 and userInput[:6] == "delete"):
        print("Hello")        

clientSocket.close()