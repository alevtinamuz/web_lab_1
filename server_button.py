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
        global number
        number += 1
        picture = open('server_pictures/' + str(number) + '.jpg', 'rb')
        picture_bytes = picture.read()
        picture.close()
        connection.send(picture_bytes)
        
            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    connection, address = server.accept()
    print(f'Connected by {address}')
    with connection:
        while True:
            data = connection.recv(10000000000)
            print(f'Recieved: {data.decode()}')
            app = QApplication([])
            window = ButtonWindow()
            window.show()
            app.exec()
            
            
    