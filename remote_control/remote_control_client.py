import socket
import PIL.ImageGrab
from pynput import keyboard
from pynput import mouse
import PIL
import time
import io
import threading
import screeninfo

def keyboard_listen(ip, port):
    keyboard_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_socket.connect((ip, port))

    while True:
        data = keyboard_socket.recv(1024).decode()
        handle_client_keyboard(data)

def handle_client_keyboard(data):
    print(data)
    keyboard_controller = keyboard.Controller()
    try:
        keyboard_controller.press(data)

    except ValueError:
        split_data = data.split(".")
        key = getattr(keyboard.Key, split_data[1], None)
        keyboard_controller.press(key)


def mouse_listen(ip, port, scale):
    mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"{ip}, {port}")
    mouse_socket.connect((ip, port))
    buffer = b""

    while True:
        while b"\n" not in buffer:
            buffer += mouse_socket.recv(1024)
        data, buffer = buffer.split(b"\n", 1)
        handle_client_mouse(data.decode(), scale)


def handle_client_mouse(data, scale):
    mouse_controller = mouse.Controller()
    print(data)

    if data.startswith("Click on button"):
        data = data.replace("Click on button", "").strip()
        mouse_controller.press(mouse.Button.left if data == "Button.left" else mouse.Button.right)
    elif data.startswith("Release button"):
        data = data.replace("Release button", "").strip()
        mouse_controller.release(mouse.Button.left if data == "Button.left" else mouse.Button.right)
    elif data.startswith("Scroll by"):
        dx, dy = map(int, data.replace("Scroll by", "").split(","))
        mouse_controller.scroll(dx * scale, dy * scale)
    else:    
        x, y = map(int, data.split(","))
        mouse_controller.position = (x * scale ,y * scale)


def screen_connect(ip, port):
    screen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_socket.connect((ip, port))

    while True:
        screen_shot = PIL.ImageGrab.grab()
        buffer = io.BytesIO()
        screen_shot.save(buffer, format="JPEG")
        screen_shot_bytes = buffer.getvalue()
        screen_socket.sendall(len(screen_shot_bytes).to_bytes(4, byteorder="big"))
        screen_socket.sendall(screen_shot_bytes)
        time.sleep(0.2)


def main():
    socket_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_temp.connect(("192.168.68.109", 4352))
    monitor = screeninfo.get_monitors()[0]
    screen_height = monitor.height
    screen_width = monitor.width
    socket_temp.sendall(f"{screen_width},{screen_height}".encode())
    scale =  socket_temp.recv(4)
    scale = int.from_bytes(scale, byteorder = "big")
    print(scale)
    scale = int(scale)
    socket_temp.close()
    
    keyboard_thread = threading.Thread(target=keyboard_listen, args=("192.168.68.109", 1337))
    mouse_thread = threading.Thread(target=mouse_listen, args=("192.168.68.109", 1234, scale))
    screen_thread = threading.Thread(target=screen_connect, args=("192.168.68.109", 7653))

    keyboard_thread.start()
    mouse_thread.start()
    screen_thread.start()

    keyboard_thread.join()
    mouse_thread.join()
    screen_thread.join()

    
if __name__ == "__main__":
    main()