import socket
import argparse


# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-a", "--address", required=True,
   help="Server IP Address or URL")
ap.add_argument("-p", "--port", required=True,
   help="Server Port")
args = vars(ap.parse_args())

HOST = args['address']  
PORT = int(args['port']) 

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the remote host and port
sock.connect((HOST, PORT))

print("conectado")

# Send a request to the host
sock.send("app\n".encode()[:-1])

# Get the host's response, no more than, say, 1,024 bytes
response_data = sock.recv(1024)

print(response_data.decode("utf-8"))

# Send a request to the host
sock.send("123456789\n".encode()[:-1])

# Get the host's response, no more than, say, 1,024 bytes
response_data = sock.recv(1024)

print(response_data.decode("utf-8"))

# Get the host's response, no more than, say, 1,024 bytes
response_data = sock.recv(1024).decode("utf-8")

print(f"Dado recebido: {response_data}")

# Terminate
sock.close( )