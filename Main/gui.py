import tkinter as tk
import socket
import psutil
import time

def get_host_name():
    return socket.gethostname()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_cpu_percent():
    return psutil.cpu_percent()

def get_ram_info():
    mem = psutil.virtual_memory()
    total = mem.total / (1024.0 ** 3)
    used = mem.used / (1024.0 ** 3)
    return round(used, 2), round(total, 2)

def get_disk_info():
    disk = psutil.disk_usage("/")
    total = disk.total / (1024.0 ** 3)
    used = disk.used / (1024.0 ** 3)
    return round(used, 2), round(total, 2)

def update_info():
    host_name_label.config(text=f"Host Name: {get_host_name()}")
    ip_address_label.config(text=f"IP Address: {get_ip_address()}")
    cpu_percent_label.config(text=f"CPU Usage: {get_cpu_percent()}%")
    ram_used, ram_total = get_ram_info()
    ram_label.config(text=f"RAM Used (GB): {ram_used} / {ram_total}")
    disk_used, disk_total = get_disk_info()
    disk_label.config(text=f"Disk Used (GB): {disk_used} / {disk_total}")
    current_time.config(text= "Current Time: " + time.strftime("%H:%M:%S"))
    root.after(1000, update_info)

root = tk.Tk()
root.geometry("480x320")
root.title("System Information")
root.config(bg='white')

host_name_label = tk.Label(root, font=("Arial", 22), bg='white')
host_name_label.pack()

ip_address_label = tk.Label(root, font=("Arial", 22), bg='white')
ip_address_label.pack()

cpu_percent_label = tk.Label(root, font=("Arial", 22), bg='white')
cpu_percent_label.pack()

ram_label = tk.Label(root, font=("Arial", 22), bg='white')
ram_label.pack()

disk_label = tk.Label(root, font=("Arial", 22), bg='white')
disk_label.pack()

current_time = tk.Label(root, font=("Arial", 22), bg='white')
current_time.pack()
update_info()

root.mainloop()