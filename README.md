Written in Python

To run this FTP client, in the command line type:

python myftp.py "server name"\
Where server name is the name of the server or its IP

This FTP client supports 6 commands:

|Commands|Explanation|
|-|-|
|ls                      |list files in current directory and the size of the list sent from the server in bytes|
|cd "remote directory"   |where remote directory is the directory to change to on the server|
|get "file name"         |where the file name is a file in the server to download onto local computer|
|put "file name"         |where the file name is a file in the local computer to upload to the server|
|delete "file name"      |where the file name is the file to delete off the server|
|quit                    |that ends the connection with the server and gracefully exits|