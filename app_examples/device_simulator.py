import socket
import argparse
import time

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-a", "--address", required=True,
   help="Server IP Address or URL")
ap.add_argument("-p", "--port", required=True,
   help="Server Port")
ap.add_argument("-d", "--deviceid", required=True,
   help="Device ID")

args = vars(ap.parse_args())

HOST = args['address']  
PORT = int(args['port']) 
device_id = args['deviceid']

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the remote host and port
sock.connect((HOST, PORT))

print("conectado")

# Send a request to the host
sock.send((device_id+"\n").encode()[:-1])

# Get the host's response, no more than, say, 1,024 bytes
response_data = sock.recv(1024)

sresponse = response_data.decode("utf-8") 
print(sresponse)

if(sresponse == "fail"):
   sock.close()
   exit()

#sending 10 values
for i in range(10):
   print("Enviando valor: "+str(i))
   sock.send((str(i)+"\n").encode()[:-1])
   time.sleep(1)

# Terminate
sock.close( )