import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
import socket

HOST = socket.gethostname()
PORT = 40808

# class PictureWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b'I connected.')
    while True:
        data = client.recv(1024)
        print(f"Recieved: {data.decode()}")
