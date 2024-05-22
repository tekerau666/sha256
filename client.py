import base64
import hashlib
import random
import string

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtNetwork import QTcpSocket
import sys
import re

from cryption import hash_data_sha256, check_data_sha256

from interface import Ui_MainWindow


class Client(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Client, self).__init__()
        self.setupUi(self)

        # # Инициализируем поля ввода
        self.client_name = ''
        # Скрываем группы, которые должны быть видимы только после подключения

        # Подключаем обработчики событий
        self.serverConnectionButton.clicked.connect(self.connect_to_server)
        self.sendButton.clicked.connect(self.send_message)
        self.disconnectButton.clicked.connect(self.disconnect_from_server)

        # Создаем сокет для сетевого взаимодействия
        self.socket = QTcpSocket(self)
        self.socket.readyRead.connect(self.on_ready_read)
        self.socket.disconnected.connect(self.on_disconnected)

    def connect_to_server(self):
        ip = self.ipAddressLineEdit.text()
        port = int(self.portLineEdit.text())

        self.socket.connectToHost(ip, port)
        if self.socket.waitForConnected(5000):
            self.client_name = self.nameLineEdit.text() if self.nameLineEdit.text() else 'guest'
            # Показываем чат после подключения
            self.chatGroupBox.setVisible(True)
            self.serverConnectionGroupBox.setVisible(False)
        else:
            self.statusLabel.setText("Failed to connect to the server.")

    def disconnect_from_server(self):
        self.socket.disconnectFromHost()
        # Показываем группу подключения после отключения
        self.chatGroupBox.setVisible(False)
        self.serverConnectionGroupBox.setVisible(True)

    def on_ready_read(self):
        # Читаем данные из сокета
        data = self.socket.readAll().data().decode()
        # Обрабатываем полученные данные
        self.handle_server_message(data)

    def send_message(self):
        # Получаем текст из поля ввода сообщения
        message = self.messageLineEdit.text()
        if not message:
            return

        # Получаем хеш-значение и исходные данные
        hash_value, original_data = hash_data_sha256(message)

        # Если сообщение не "ошибочный", отправляем исходное сообщение, иначе обрабатываем как ошибку
        if message == 'ошибочный':
            date_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
            encrypted_message = f"[{date_time}] {self.client_name}:{original_data} ({hash_value})"
        else:
            date_time = QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm:ss')
            full_message = f"[{date_time}] {self.client_name}: {message}"
            encrypted_message = f"{full_message} ({hash_value}) "

        # Отправляем сообщение на сервер
        self.socket.write(encrypted_message.encode())
        # Очищаем поле ввода сообщения
        self.messageLineEdit.clear()
    def on_disconnected(self):
        self.statusLabel.setText("Disconnected from the server.")
        self.chatGroupBox.setVisible(False)
        self.serverConnectionGroupBox.setVisible(True)

    def handle_server_message(self, message):
        self.chatTextEdit.append(message)



# Основная часть программы
app = QApplication([])
client = Client()
client.show()
sys.exit(app.exec())
