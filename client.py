import socket
import sys
import threading
import uuid

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Automatically fetch the local machine's IP (server IP)
IP_address = socket.gethostbyname(socket.gethostname())  # Replace with server IP if needed
Port = 8080  # Port number should match the server

server.connect((IP_address, Port))

# Generate a unique identifier for each client
client_id = str(uuid.uuid4())[:8]  # Generate a random unique identifier (8 characters)

# Send the client_id as the first message to the server
server.send(client_id.encode('utf-8'))

def receive_messages():
    while True:
        try:
            message = server.recv(2048).decode('utf-8')
            if message:
                print(message)
            else:
                # Connection has been closed
                server.close()
                break
        except:
            # In case of any error, close the connection
            server.close()
            break

def send_messages():
    while True:
        message = sys.stdin.readline()
        message_to_send = f"[{client_id}] {message}"  # Prefix messages with client ID
        server.send(message_to_send.encode('utf-8'))
        sys.stdout.write(f"<You ({client_id})> ")
        sys.stdout.write(message)
        sys.stdout.flush()

# Start the thread for receiving messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main thread for sending messages to the server
send_messages()
