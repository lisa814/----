from pynput import keyboard
from pynput import mouse
import socket
import threading
import cv2
from PIL import Image
import io
import numpy as np
import screeninfo


def control_keyboard(ip, port):

    def on_press(key):
        print(key)
        try:
            client_socket.sendall(key.char.encode())
        except AttributeError:
            client_socket.sendall(str(key).encode())

    def on_release(key):
        if key == keyboard.Key.esc:
            return False
        
    keyboard_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_socket.bind((ip, port))
    keyboard_socket.listen(1)
    client_socket, addr = keyboard_socket.accept()
    print(f"New connection: {addr}")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    keyboard_socket.close()


def control_mouse(ip, port):

    def on_move(x, y):
        client_socket.sendall((f"{x},{y}\n".encode()))
    
    def on_click(x, y, button, pressed):
        if pressed:
            client_socket.sendall(f"Click on button {button}\n".encode())
        else:
            client_socket.sendall(f"Release button {button}\n".encode())

    def on_scroll(x, y, dx, dy):
        client_socket.sendall(f"Scroll by {dx},{dy}\n".encode())

    mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_socket.bind((ip, port))
    mouse_socket.listen(1)
    client_socket, addr = mouse_socket.accept()
    print(f"New connection: {addr}")


    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

    mouse_socket.close()


def get_screen_display(ip, port, scale):
    screen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_socket.bind((ip, port))
    screen_socket.listen(1)
    client_socket, addr = screen_socket.accept()
    print(f"New connection: {addr}")
    image_bytes = b""


    while True:
        size = client_socket.recv(4)
        size = int.from_bytes(size, byteorder="big")
        while len(image_bytes) < size:
            image_bytes += client_socket.recv(1024)
        display_image(image_bytes, scale)
        image_bytes = b""

    


def display_image(image_bytes, scale):
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    resized_image = cv2.resize(image, (int(width * scale), int(height * scale)))
    cv2.imshow("Remote Screen", resized_image)
    cv2.waitKey(1)


def main():
    
    socket_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_temp.bind(("192.168.68.109", 4352))
    socket_temp.listen(1)
    client_socket, addr = socket_temp.accept()
    dimentions = client_socket.recv(1024).decode()
    width, height = map(int, dimentions.split(","))
    monitor = screeninfo.get_monitors()[0]
    screen_height = monitor.height
    screen_width = monitor.width
    print(f"{screen_width}, {screen_height}")
    scale = int(min(screen_width / width, screen_height / height))
    print(scale)
    client_socket.sendall(scale.to_bytes(4, byteorder="big"))
    client_socket.close()


    keyboard_thread = threading.Thread(target=control_keyboard, args=("192.168.68.109", 1337))
    mouse_thread = threading.Thread(target=control_mouse, args=("192.168.68.109", 1234))
    screen_thread = threading.Thread(target=get_screen_display, args=("192.168.68.109", 7653, scale))

    keyboard_thread.start()
    mouse_thread.start()
    screen_thread.start()

    keyboard_thread.join()
    mouse_thread.join()
    screen_thread.join()



if __name__ == "__main__":
    main()