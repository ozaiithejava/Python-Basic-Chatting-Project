import socket
import select

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started. Listening on port 12345...")

    sockets_list = [server_socket]
    clients = {}  # {client_socket: client_username}

    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                username = client_socket.recv(1024).decode()
                sockets_list.append(client_socket)
                clients[client_socket] = username

                print(f"{username} connected from: {client_address[0]}:{client_address[1]}")

            else:
                message = notified_socket.recv(1024).decode()
                username = clients[notified_socket]
                
                if message:
                    print(f"{username}: {message}")

                    if message == "/q":
                        print(f"{username} disconnected.")
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        notified_socket.close()

    server_socket.close()

if __name__ == "__main__":
    start_server()
