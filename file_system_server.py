import socket
import os


def create_server_socket(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    return server_socket

def run_server(server_socket):
    folder_name = input("Save folder as: ")
    server_socket.listen(1)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        handle_client(server_socket, client_socket, folder_name)
        client_socket.close()


def handle_client(server_socket, client_socket, folder_name):
    data = client_socket.recv(1024).decode()
    command = data.split("<END>")[0]
    print(command)
    if command.startswith("upload file"):
        file_name = input("Save file as: ")
        save_file(client_socket, folder_name, file_name, data.split("<END>")[1])
    elif command.startswith("request file"):
        get_file_from_folder(client_socket, folder_name, data.split("<END>")[0])


def save_file(client_socket, folder_name, file_name, data):
    os.makedirs(folder_name, exist_ok=True)
    with open(folder_name + "/" + file_name, "wb") as file:
        file.write(data.encode())
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
        print("saved file")


def get_file_from_folder(client_socket, folder_name, data):
    file_name = data.split(":")[1]
    full_path = os.path.join(folder_name, file_name)
    if os.path.isfile(full_path):
        with open(full_path, "rb") as file_to_send:
            while True:
                data = file_to_send.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        print("sent file")
    else:
        client_socket.sendall(b"File doesn't exist in the folder")


def main():
    ip_addr = input("The server IP address: ")
    port = int(input("The server port: "))
    new_socket = create_server_socket(ip_addr, port)
    run_server(new_socket)


if __name__ == "__main__":
    main()