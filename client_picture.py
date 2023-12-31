import socket

from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QPushButton, QWidget, QVBoxLayout
)
from PyQt6 import QtGui, QtCore


def local_ipv4():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip_l = st.getsockname()[0]
    except Exception:
        ip_l = '127.0.0.1'
    finally:
        st.close()
    return ip_l
print(local_ipv4())

HOST = local_ipv4()
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
        
        self.effect_like = QSoundEffect()
        self.effect_like.setSource(QtCore.QUrl.fromLocalFile('bin/like_sound.wav'))
        self.effect_dislike = QSoundEffect()
        self.effect_dislike.setSource(QtCore.QUrl.fromLocalFile('bin/dislike_sound.wav'))
        self.like = QPushButton('Like!👍')
        self.dislike = QPushButton('Dislike!👎')
        self.like.clicked.connect(self.effect_like.play)
        self.dislike.clicked.connect(self.effect_dislike.play)
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