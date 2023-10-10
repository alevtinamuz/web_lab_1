from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import socket

HOST = socket.gethostname() 
PORT = 40808
number = 0

class ButtonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Button window')
        button = QPushButton('Press on the button to view the picture.')
        button.move(50, 50)
        button.clicked.connect(self.ButtonClick)
        self.setCentralWidget(button)
    def ButtonClick(self):
        number += 1
        file = open('server_pictures/' +number + '.jpg', 'rb')
        picture = file.read(1024)
        connection.send(picture) 
            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    connection, address = server.accept()
    with connection:
        print(f'Connected by {address}')
        while True:
            data = connection.recv(1024)
            print(f'Recieved: {data.decode()}')
            connection.sendall(data)
            app = QApplication([])
            window = ButtonWindow()
            window.show()
            app.exec()
            
            
    