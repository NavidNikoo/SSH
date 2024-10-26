import socket
import sys
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad



#I Implement Command line arguments here. If there are n arguments present in command line
#execute the code below
n = len(sys.argv)
if n == 3:

	# The key (must be 16 bytes)
	key = sys.argv[2]
	key = b'Sixteen byte key'
	port = int(sys.argv[1])

# Create a socket
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


# Associate the socket with the port
	serverSock.bind(('', port)) 


# Start listening for incoming connections (we can have
# at most 100 connections waiting to be accepted before
# the server starts rejecting new connections)
	serverSock.listen(100)

# Set up the AES encryption class
	decCipher = AES.new(key, AES.MODE_ECB)


# Keep accepting connections forever
	while True:


		print("Waiting for clients to connect...")
	
		# Accept a waiting connection
		cliSock, cliInfo = serverSock.accept()
	
		print("Client connected from: " + str(cliInfo))
	
		# Receive the data the client has to send.
		# This will receive at most 1024 bytes
		cliMsg = cliSock.recv(1024)
	
	
		plainText = decCipher.decrypt(cliMsg) 
		
		plainText = unpad(plainText, 16)  #Removes the 16 bit padding
	

		print("Client sent " + str(plainText.decode()))

		# Hang up the client's connection
		cliSock.close()