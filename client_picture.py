# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
import socket
# from PyQt6.QtGui import QPixmap
import os

HOST = socket.gethostname()
PORT = 40808
number = 1

# class PictureWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         number = 1
#         self.setWindowTitle("Picture Window")
#         self.setGeometry(200, 300, 400, 300)
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout()
#         self.image_label = QLabel()
#         self.image_label.setFixedSize(800, 600)
#         self.pix = 'client_pictures/' + str(number) + '.jpg'
#         print('gg')     
#         self.pixmap1 = QPixmap(self.pix)
#         self.image_label.setPixmap(self.pixmap1)
#         layout.addWidget(self.image_label)
#         central_widget.setLayout(layout)

        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b'I connected.')
    data = client.recv(10000000000)
    file = open('client_pictures/' + str(number) + '.jpg', 'wb')
    file.write(data)
    os.startfile(r'C:/Users/Alkin/web/web_lab_1/client_pictures/' + str(number) + '.jpg')
    number += 1
    file.close()
    while True:
        file = open('client_pictures/' + str(number) + '.jpg', 'wb')
        data = client.recv(10000000000)
        print(data)
        file.write(data)
        os.startfile(r'C:/Users/Alkin/web/web_lab_1/client_pictures/' + str(number) + '.jpg')
        file.close()
        number += 1
        # app = QApplication([])
        # window = PictureWindow()
        # PictureWindow.show()
        # app.exec()