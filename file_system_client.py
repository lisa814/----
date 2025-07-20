import socket
import os


def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket

def upload_file(client_socket, file_path):
    file_name = os.path.split(file_path)[1]
    client_socket.sendall(b"upload file:" + file_name.encode() + b"<END>")
    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)
    client_socket.close()
        
        
def request_file(client_socket, file_name):
    client_socket.sendall(b"request file:" + f"{file_name}".encode() + b"<END>")
    with open("." + "/" + file_name, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    client_socket.close()

def main():
    ip_addr = input("The server IP address: ")
    port = int(input("The server port: "))
    client_socket1 = start_client(ip_addr, port)
    file_path = input("Please enter the path of the file to upload: ")
    upload_file(client_socket1, file_path)
    client_socket2 = start_client(ip_addr, port)
    request_file(client_socket2, "book report.docx")


if __name__ == "__main__":
    main()