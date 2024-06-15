import socket
import pickle
from Crypto.Cipher import AES

#Public and Private keys
n=3127
public_key=3
private_key=2011

#Creating Cipher
key=b"1234567890qwerty"
nonce=b"1234567890qwertt"
cipher = AES.new(key,AES.MODE_EAX,nonce)

#Function to encrypt data using public key
def encrypt(key):
    global public_key, n
    e = public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text = (encrypted_text*key)%n
        e -= 1
    return encrypted_text
    
#Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('',9999))

#Opening input file and storing data from file
with open("randomTextfile.txt","rb") as file:
    data = file.read()

#Encrypting key
encrypted_key=[]
for i in key:
    encrypted_key.append(encrypt(i))
    
#Encrypted nonce
encrypted_nonce=[]
for i in nonce:
    encrypted_nonce.append(encrypt(i))
    
#Encrypting text using Cipher
encrypted_using_cipher=cipher.encrypt(data)

client.send(pickle.dumps(encrypted_key))
client.send("<SEP>".encode())
client.send(pickle.dumps(encrypted_nonce))
client.send("<SEP>".encode())
client.sendall(encrypted_using_cipher)
client.send("<SEP>".encode())
client.close()