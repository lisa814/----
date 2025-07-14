import requests
import json
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from customtkinter import *
import os
import time
from PIL import Image
import threading


stop_event = threading.Event()

def log_message(msg):
    box.insert("end", msg + "\n")
    box.see("end")

def on_click_btn1():
    try:
        thread1 = threading.Thread(target=start_scanning, args=(entry1.get(), float(entry2.get()), entry3.get()), daemon=True)
        thread1.start()
        entry1.delete(0,"end")
        entry2.delete(0, "end")
        entry3.delete(0, "end")
        btn2.place(relx = 0.87, rely = 0.6, anchor = "center")
        btn1.place_forget()

    except Exception:
        log_message("Make sure to enter a valid path, your api key and a time interval")


def on_click_btn2():
    stop_event.set()
    log_message("Scan Stopped, finishing...")
    btn2.place_forget()
    btn1.place(relx = 0.5, rely = 0.2, anchor = "center")

window = CTk()
window.geometry("700x600")

set_appearance_mode("dark")

btn1 = CTkButton(master=window, text="Start", command=on_click_btn1, corner_radius=15, fg_color="transparent", hover_color="#0D8300",
                    border_color="#26FF00", border_width=1)
btn1.place(relx = 0.5, rely = 0.2, anchor = "center")

btn2 = CTkButton(master=window, text="Stop Scan", command=on_click_btn2, corner_radius=15, fg_color="transparent", hover_color="#FF0000",
                    border_color="#26FF00", border_width=1)

l1 = CTkLabel(master=window, text="Anti Virus App - Check Your Files")
l1.place(relx = 0.5, rely = 0.1, anchor = "center")

l2 = CTkLabel(master=window, text="Please enter the path to start from ==>")
l2.place(relx = 0.165, rely = 0.3, anchor = "center")
entry1 = CTkEntry(master=window)
entry1.place(relx = 0.45, rely = 0.3, anchor = "center")

l3 = CTkLabel(master=window, text="Please enter how often should the files be scanned ==>")
l3.place(relx = 0.23, rely = 0.4, anchor = "center")
entry2 = CTkEntry(master=window)
entry2.place(relx = 0.57, rely = 0.4, anchor = "center")

l4 = CTkLabel(master=window, text="Please enter your VirusTotal API key ==>")
l4.place(relx = 0.17, rely = 0.5, anchor = "center")
entry3 = CTkEntry(master=window)
entry3.place(relx = 0.45, rely = 0.5, anchor = "center")

box = CTkTextbox(master=window, width=650, height=200, corner_radius=5, wrap = "word")
box.place(relx = 0.5, rely = 0.8, anchor = "center")
    
img = CTkImage(light_image=Image.open("virus_img.jpg"), dark_image=Image.open("virus_img.jpg"), size=(150,100))
img_label = CTkLabel(master=window, text="", image=img) 
img_label.place(relx = 0.1, rely = 0.1, anchor = "center")


class MyHandler(FileSystemEventHandler):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def on_created(self, event):
        if not event.is_directory:
            id = scan_file(event.src_path, self.api_key)
            if get_analysis(id, self.api_key) > 0:
                log_message(f"Found malicious code in: {event.src_path}")
            else:
                log_message(f"File is safe: {event.src_path}")


def scan_file(file, api_key):
    url = "https://www.virustotal.com/api/v3/files"

    files = { "file": (file, open(file, "rb")) }
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    response = requests.post(url, files=files, headers=headers)
    response_dict = json.loads(response.text)
    id = response_dict["data"]["id"]
    return id


def get_analysis(analysis_id, api_key):
    url = "https://www.virustotal.com/api/v3/analyses/" + analysis_id 

    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    malicious = response_dict["data"]["attributes"]["stats"]["malicious"]
    return malicious


def start_periodic_scan(dir_path ,interval, api_key):
    while True:
        if not stop_event.is_set():
            for root, _, files in os.walk(dir_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    id = scan_file(file_path, api_key)
                    report = get_analysis(id, api_key)
                    if report > 0:
                        log_message(f"Found malicious code in: {file_path}")
                    else:
                        log_message(f"File is safe: {file_path}")
            time.sleep(interval)

    
def start_scanning(dir_path, interval, api_key):
    
    thread2 = threading.Thread(target=start_periodic_scan, args=(dir_path, interval, api_key), daemon=True)
    thread2.start()

    observ = Observer()
    event_handler = MyHandler(api_key)
    observ.schedule(event_handler, dir_path, recursive=True)
    observ.start()

    while not stop_event.is_set():
        time.sleep(1)

    observ.stop()
    observ.join()

    
def main():
    window.mainloop()


if __name__ == "__main__":
    main()

