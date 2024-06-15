import socket
import pickle
from Crypto.Cipher import AES

#Public and Private keys
n=3127
public_key=3
private_key=2011

#Function to decrypt data using private key
def decrypt(message):
    global private_key, n
    d = private_key
    encrypted_text = 1
    while d > 0:
        encrypted_text = (encrypted_text*message)%n
        d -= 1
    return encrypted_text
    
#Creating Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost',9999))
server.listen()

client,address=server.accept()

#Accepting incoming data
full_data=b""
while(True):
    full_data=full_data+(client.recv(1024))
    if not client.recv(1024):
        break
        
full_data_list=full_data.split(b"<SEP>")

#Decrypting key
key=b""
for i in pickle.loads(full_data_list[0]):
    key=key+chr(decrypt(i)).encode()

#Decrypting nonce
nonce=b""
for i in pickle.loads(full_data_list[1]):
    nonce=nonce+chr(decrypt(i)).encode()

#Creating cipher
cipher = AES.new(key,AES.MODE_EAX,nonce)


# Writing text to file
with open("revtext.txt","wb") as f:
    f.write(cipher.decrypt(full_data_list[2]))

server.close()