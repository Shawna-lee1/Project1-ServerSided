import sys
import socket
import os
import select
import time
import signal

# Define a flag to track whether a signal was received
shutdown_signal_received = False  # Correct variable name

# Signal handler function to handle SIGQUIT, SIGTERM, and SIGINT
def signal_handler(sig, frame):
    global shutdown_signal_received

    if sig in [signal.SIGQUIT, signal.SIGTERM, signal.SIGINT]:
        print(f"Received signal {sig}. Gracefully shutting down...")
        shutdown_signal_received = True

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)

    try:
        PORT = int(sys.argv[1])
        if not 0 <= PORT <= 65535:
            sys.stderr.write("ERROR: Invalid port range\n")
            sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    try:
        server_socket.bind(("0.0.0.0", port))
    except OSError as e:
        if e.errno == 98:
            sys.stderr.write("ERROR: Address already in use\n")
            sys.exit(1)

    server_socket.listen(10)

    print("Server is running. To gracefully shut down, press Ctrl+C or send a termination signal...")

    while not shutdown_signal_received:  # Correct variable name
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Send "accio\r\n" command
        client_socket.send(b"accio\r\n")

        received_data = b""  # Initialize an empty bytes object to store the received data
        total_received_bytes = 0

        try:
            client_socket.setblocking(0)  # Set the socket to non-blocking mode
            start_time = time.time()

            while not shutdown_signal_received:  # Correct variable name
                ready, _, _ = select.select([client_socket], [], [], 10)

                if not ready:
                    # No data received for over 10 seconds
                    print("Timeout: No data received. Aborting connection.")
                    client_socket.send(b"ERROR\r\n")
                    break

                data_chunk = client_socket.recv(4096)
                if not data_chunk:
                    break

                received_data += data_chunk
                total_received_bytes += len(data_chunk)

                while b'\r' in received_data or b'\n' in received_data:
                    if b'\r' in received_data:
                        line, received_data = received_data.split(b'\r', 1)
                    else:
                        line, received_data = received_data.split(b'\n', 1)
                    line_text = line.decode('utf-8')
                    line_text = line_text.strip()
                    if line_text:
                        print(f"Received {len(line)} bytes")
                        print(f"Received data: {line_text}")

            print(f"Total received bytes: {total_received_bytes}")

        except KeyboardInterrupt:
            print("Received Ctrl+C. Gracefully shutting down...")
            break

        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    main()
 
