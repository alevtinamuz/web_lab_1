from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
import socket
from PyQt6.QtGui import QPixmap

HOST = socket.gethostname()
PORT = 40808
number = 0
tmp = 0

class PictureWindow(QMainWindow):
    def __init__(self):
        number = 1
        super().__init__()
        self.acceptDrops()
        self.setWindowTitle("Picture Window")
        self.setGeometry(200, 300, 400, 300)
        self.label = QLabel(self)
        self.pixmap = QPixmap('client_pictures/' + str(number) + '.jpg')
        number += 1
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.show()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b'I connected.')
    file = open('client_pictures/' + str(number) + '.jpg', 'wb')
    while True:
        data = client.recv(1024)
        file.write(data)
        App = QApplication([])
    
        # create the instance of our Window
        window = PictureWindow()
    
        # start the app
        App.exec()