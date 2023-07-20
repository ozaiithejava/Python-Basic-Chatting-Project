import socket
import threading

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to server at localhost:12345")

    username = input("Enter your username: ")
    client_socket.sendall(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.sendall(message.encode())

        if message == "/q":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
