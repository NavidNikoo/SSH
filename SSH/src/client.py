import socket
import sys
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad

#I Implement Command line arguments here. If there are n arguments present in command line
#execute the code below
n = len(sys.argv)

if n == 4:

	# The key (must be 16 bytes)
	key = sys.argv[3]
	key = b'Sixteen byte key'
	port = int(sys.argv[2])
	Server_IP = sys.argv[1]
	
# Set up the AES encryption class
	encCipher = AES.new(key, AES.MODE_ECB)

	msg = input('Please enter a message to send to the server: ')

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
	msg = pad(msg.encode(), 16) #pad the message as a byte and it will be blocks of bytes.
	#the reason why it is blocks of bytes is because I am using AES which encrypts and decrypts using block cipher
	
	#encrypt the padded message
	cipherText = encCipher.encrypt(msg)

	# Send the message to the server
	cliSock.send(cipherText)


	print("Cipher text: ", cipherText)


#to start it I would do start up the server first 
#then I would run client and type my message
#once i send my message, the server retrieves it and displays it
#tomorrow i will implement a non hard coded server port. Moreover, I will have the user enter the port.
