import socket
from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

#I Implement Command line arguments here. If there are n arguments present in command line
#execute the code below

	# The key (must be 16 bytes)
key = b'Sixteen byte key'
port = 1235
Server_IP = "127.0.0.1"
	
# Set up the AES encryption class
iv = random.new().read(AES.block_size)
encCipher = AES.new(key, AES.MODE_CBC, iv)

Username = input('Username: ')
password = input('Password: ')

# The client's socket
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Attempt to connect to the server
cliSock.connect((Server_IP, port))
#server needs to be started first and then client

# Send the message to the server
# NOTE: the user input is of type string
# Sending data over the socket requires.
# First converting the string into bytes.
# encode() function achieves this.
Username = pad(Username.encode(), AES.block_size) #pad the message as a byte and it will be blocks of bytes. The reason why it is blocks of bytes is because I am using AES which encrypts and decrypts using block cipher
password = pad(password.encode(), AES.block_size)

#encrypt the padded message
userNameCipher = encCipher.encrypt(Username)
passwordCipher = encCipher.encrypt(password)

#Find length of username 
username_length = len(userNameCipher)
password_length = len(passwordCipher)



	# Send the message to the server
cliSock.send(iv + bytes[username_length] + userNameCipher + bytes[password_length] + passwordCipher)


print(userNameCipher + iv)
print(passwordCipher + iv)




