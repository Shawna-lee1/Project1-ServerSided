import socket #Enables network operations like creating a server
import sys #Provides access to some variables used by the interpreter like command-line arguments
import signal #Allows you to handle asynchronous events or signals.
import time #provide various time-related functions.




### Step 1: Command Line Processing and Signal Handling

not_stopped = True #This global variable acts as a flag to control the main server loop.

#This function is designed to handle signals by changing not_stopped to False and printing a message. 
#It will be triggered by signal events like keyboard interrupts (Ctrl+C).
def signal_handler(sig, frame): 
    global not_stopped
    not_stopped = False
    print(f"\nServer shutting down... Signal: {sig}, Frame: {frame}")

#This function continuously reads data from a client socket until it encounters a carriage return and newline ("\r\n").
#If socket reading times out, it handles the exception and closes the socket.
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
            #sys.exit(1)

        b = b + chunk

#receives data from the client socket and accumulates the total number of bytes received.
def handle_client_connection(client_socket):
    total_bytes_received = 0
    while True:
        data = client_socket.recv(1024) # Buffer size 1024 bytes
        if not data:
            break
        total_bytes_received += len(data)

    print(f"Total bytes received: {total_bytes_received}")


### Step 2: Server Socket Initialization and Connection Accepting

#This function creates, binds, and returns a server socket listening on all available interfaces (0.0.0.0) and a specified port.
def create_server_socket(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)
    return server_socket

def main():
    # Signal handling
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Command-line argument processing
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Invalid arguments\n")
        sys.exit(1)

    try:
        PORT = int(sys.argv[1])
        if not 0 <= PORT <= 65535:
            sys.stderr.write("ERROR: Invalid port range\n")
            sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)

    try:
        server_socket = create_server_socket(PORT)
        print(f"Server listening on port {PORT}...")
    except Exception as e:
        sys.stderr.write(f"ERROR: {str(e)}\n")
        sys.exit(1)
    
    while not_stopped:
        try:
            server_socket.settimeout(1)
            #print("Before accept\n")
            client_socket, client_address = server_socket.accept()
            #print("After accept\n")
            client_socket.settimeout(10)
            
            print(f"Connection from {client_address}...")
            
            client_socket.send(b"accio\r\n")

            receive_commands(client_socket)

            client_socket.send(b"confirm-accio-again\r\n\r\n")

            receive_commands(client_socket)
            
            handle_client_connection(client_socket)
            
            client_socket.close()
            print("Connection closed.")
            
        except socket.timeout:
            #sys.stderr.write("ERROR: No data received for 10 seconds.\n")
            sys.stderr.write(".")
        except Exception as e:
            sys.stderr.write(f"ERROR: {str(e)}\n")

### Step 4: Handle Client Connection and Data Receiving
def handle_client_connection(client_socket):
    total_bytes_received = 0
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        total_bytes_received += len(data)

    print(f"Total bytes received: {total_bytes_received}")

if __name__ == "__main__":
    main()
