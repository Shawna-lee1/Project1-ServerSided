import socket
import sys
import signal
import time

not_stopped = True

def signal_handler(sig, frame):
  global not_stopped
  not_stopped = False
  print(f"\nServer shutting down... Signal: {sig}, Frame: {frame}")

def create_server_socket(port):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind(('0.0.0.0', port))
  server_socket.listen(10)
  return server_socket
  
def handle_client_connection(client_socket):
  total_bytes_received = 0
  while True:
    data = client_socket.recv(1024)
    if not data:
      break
    total_bytes_received += len(data)
  print(f"Total bytes received: {total_bytes_received}\n")
    
def main():
  # Signal handling
  signal.signal(signal.SIGQUIT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)
    
  # command line arg processing
  if len(sys.argv) != 2:
    sys.stderr.write("ERROR: Invalid arguments\n")
    sys.exit(1)
    
  try:
    PORT = int(sys.argv[1])
  except ValueError:
    sys.stderr.write("ERROR: Invalid port number\n")
    sys.exit(1)
    
  try:
    server_socket = create_server_socket(PORT)
    print(f"Server listening on port {PORT}...")
  except Exception as e:
    sys.stderr.write(f"ERROR: {str(e)}\n")  # this is a format string
    sys.exit(1)
    
  while not_stopped:
    try:
      server_socket.settimeout(1)
      client_socket, client_address = server_socket.accept()
      client_socket.settimeout(10)
      
      print(f"Connection from {client address}...")
      
      client_socket.send(b"accio\r\n")
      
      handle_client_connection(client_socket)
      client_socket.close()
      print("Connection closed.")
    except socket_timeout:
      sys.stderr.write(".")
    except Exception as e:
      sys.stderr.write(f"ERROR: {str(e)}\n")
      
if __name__ == "__main__":
  main()
