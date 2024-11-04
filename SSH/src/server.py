import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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

	decCipher = AES.new(key, AES.MODE_CBC, iv)

	username_length = int.from_bytes(data[AES.block_size:AES.block_size + 4], "big")
	username_start = AES.block_size + 4
	username_end = username_start + username_length
	username_cipher = data[username_start:username_end]

	password_start = username_end + 4
	password_length = int.from_bytes(data[username_end:password_start], "big")
	password_end = password_start + password_length
	password_cipher = data[password_start:password_end]
	
	
	decrypted_username = unpad(decCipher.decrypt(username_cipher), AES.block_size).decode()
	decrypted_password = unpad(decCipher.decrypt(password_cipher), AES.block_size).decode()	
	

	print("Username: " + str(decrypted_username))
	print("Password: " + str(decrypted_password))

	# Hang up the client's connection
	cliSock.close()
