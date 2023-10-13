import socket
import sys


# Function to receive commands from the server with timeout
def receive_commands(client_socket):
    b = b""

    while True:
        # Breaks loop once complete data is received
        if b.endswith(b"\r\n"):
            break
        try:
            chunk = client_socket.recv(1024)
        except socket.timeout:
            sys.stderr.write("ERROR: Timeout waiting for commands from the server.\n")
            client_socket.close()
            sys.exit(1)

        b = b + chunk


# Function to send file to server
def send_file(client_socket, FILENAME):
    file = open(FILENAME, "rb") 
    
    # Loops until entire file sends
    while True:
        chunk = file.read(10000)
        
        if not chunk:
            file.close()
            break
        
        client_socket.send(chunk)
    
    

# Configuration
HOST = sys.argv[1]  # Get the server hostname or IP from command-line arguments

# Check if the provided port is within the valid range (0-65535)
try:
    PORT = int(sys.argv[2])  # Get the server port from command-line arguments
    if not (0 <= PORT <= 65535):
        raise ValueError("Invalid port number")
except ValueError as e:
    sys.stderr.write(f"ERROR: {str(e)}. Port must be between 0 and 65535.\n")
    sys.exit(1)

FILENAME = sys.argv[3]  # Get the filename to transfer from command-line arguments
TIMEOUT = 10  # Timeout for various operations in seconds

# Create a socket and set a timeout for connecting to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(TIMEOUT)

try:
    client_socket.connect((HOST, PORT))
except (socket.error, ConnectionRefusedError) as e:
    sys.stderr.write(f"ERROR: Connection to {HOST}:{PORT} failed. {str(e)}\n")
    client_socket.close()
    sys.exit(1)

# Receive commands from the server
receive_commands(client_socket)

# Send the first header: "confirm-accio\r\n"
try:
    client_socket.send(b"confirm-accio\r\n")
except socket.timeout:
    sys.stderr.write("ERROR: Timeout sending commands to the server.\n")
    client_socket.close()
    sys.exit(1)
    
# Receive commands from the server
receive_commands(client_socket)

# Send the second header: "confirm-accio-again\r\n\r\n"
try:
    client_socket.send(b"confirm-accio-again\r\n\r\n")
except socket.timeout:
    sys.stderr.write("ERROR: Timeout sending commands to the server.\n")
    client_socket.close()
    sys.exit(1)
    
# Send the file to the server
send_file(client_socket, FILENAME)

# Close the connection
client_socket.close()

# Exit with a success code
sys.exit(0)
