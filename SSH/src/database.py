import socket
from CryptoDome.Cipher import AES
from Crypto.Util.Padding import unpad




#I Implement Command line arguments here. If there are n arguments present in command line
#execute the code below


# The key (must be 16 bytes)
key = b'Sixteen byte key'
port = 1235

# Create a socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


# Associate the socket with the port
serverSock.bind(('', port)) 


# Start listening for incoming connections (we can have
# at most 100 connections waiting to be accepted before
# the server starts rejecting new connections)
serverSock.listen(4)


# Keep accepting connections forever
while True:


	print("Waiting for clients to connect...")
	
		# Accept a waiting connection
	cliSock, cliInfo = serverSock.accept()
	
	print("Client connected from: " + str(cliInfo))
	
		# Receive the data the client has to send.
		# This will receive at most 1024 bytes
	data = cliSock.recv(1024)
	
	#Read IV
	iv = data[:AES.block_size]

	decCipher = AES.new(key, AES.MODE_ECB, iv)

	username_length = data[:AES.block_size]
	username_start = AES.block_size + 1
	username_end = username_start + username_length
	username_cipher = data[username_start:username_end]

	password_length = data[:AES.block_size]
	password_start = username_end + 1
	password_cipher = data[password_start:password_start + password_length]

	
	encrypted_username = data[AES.block_size:AES.block_size*2]
	encrypted_password = data[AES.block_size*2]


	decrypted_username = unpad(decCipher.decrypt(encrypted_username), AES.block_size).decode()
	decrypted_password = unpad(decCipher.decrypt(encrypted_password), AES.block_size).decode()	
	

	print("Username: " + str(decrypted_username))
	print("Password: " + str(decrypted_password))

		# Hang up the client's connection
	cliSock.close()
