import socket
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QPushButton, QWidget, QVBoxLayout
)
from PyQt6 import QtGui, QtCore

HOST = socket.gethostname()
PORT = 40808
number = 0
tmp = 0

class SocketThread(QtCore.QThread):
    data_received = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        global number
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(b'I connected.')
            while True:
                if number == 11:
                    number = 0
                number += 1
                file = open('client_pictures/' + str(number) + '.jpg', 'wb')
                data = client.recv(10000000000)
                file.write(data)
                file.close()
                self.data_received.emit('client_pictures/' + str(number) + '.jpg')
                
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Picture')
        
        self.like = QPushButton('Like!👍')
        self.dislike = QPushButton('Dislike!👎')
        self.like.clicked.connect(self.message_like)
        self.dislike.clicked.connect(self.message_dislike)
        self.like.setFixedSize(500, 60)
        self.dislike.setFixedSize(500, 60)
        
        self.picture = QLabel()
        self.picture.setPixmap(QtGui.QPixmap('client_pictures/' + str(tmp) + '.jpg').scaled(500, 500))
        self.picture.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.like)
        self.layout.addWidget(self.dislike)
        self.layout.addWidget(self.picture)
        
        self.socket_thread = SocketThread()
        self.socket_thread.data_received.connect(self.update_pictures)
        self.socket_thread.start()
    
    def message_like(self):
        message = b'Client liked this picture.'
        

    def message_dislike(self):
        message = b'Client dislike this picture'
        
    
    def update_pictures(self):
        global tmp
        if number == 10:
            tmp = 0
        tmp += 1
        self.picture.setPixmap(QtGui.QPixmap('client_pictures/' + str(tmp) + '.jpg').scaled(500, 500))
        
app = QApplication([])
w = MainWindow()
w.show()
app.exec()