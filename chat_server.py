import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Hardcode your IP address and Port here
IP_address = socket.gethostbyname(socket.gethostname())  # or use '127.0.0.1' for localhost
Port = 8080  # Use any available port you want

server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    # Receive client ID from the client as the first message
    client_id = conn.recv(2048).decode('utf-8')  # Assume the first message from client is the unique ID
    print(f"Client {client_id} connected from {addr[0]}")

    conn.send(b"Welcome to this chatroom!")  # Send bytes instead of a string

    while True:
        try:
            message = conn.recv(2048)
            if message:
                decoded_message = message.decode('utf-8')
                print(f"<{client_id}> {decoded_message}")
                message_to_send = f"<{client_id}> {decoded_message}"
                broadcast(message_to_send.encode('utf-8'), conn)  # Encode message before sending
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    
    # Start the client thread
    thread = threading.Thread(target=clientthread, args=(conn, addr))
    thread.start()

conn.close()
server.close()
