import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QTextEdit, QFileDialog
import config


class PasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Секрет')

        layout = QVBoxLayout()

        self.password_label = QLabel('Введите пароль:')
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.submit_button = QPushButton('Подтвердить')
        self.submit_button.clicked.connect(self.check_password)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.show()

    def check_password(self):
        password = self.password_input.text()
        if password == config.PASSWORD:
            self.close()
            editor_window.show()
        else:
            QMessageBox.warning(self, 'Неверный пароль', 'Неправильный пароль')

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.open_file()

    def initUI(self):
        self.setWindowTitle("Редактор")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        try:
            with open("secret.txt", "r") as file:
                decryptor = EncoderDecoder(config.KEY)
                content = file.read()
                self.text_edit.setPlainText(decryptor.decrypt(content))
        except FileNotFoundError:
            file = open("secret.txt", "w")
            file.close()

    def save_file(self):
        with open('secret.txt', "w") as file:
            encryptor = EncoderDecoder(config.KEY)
            content = self.text_edit.toPlainText()
            file.write(encryptor.encrypt(content))
        self.close()

class EncoderDecoder:
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        encrypted_message = ""
        for char in message:
            encrypted_char = chr(ord(char) + len(self.key))
            encrypted_message += encrypted_char
        return encrypted_message

    def decrypt(self, encrypted_message):
        decrypted_message = ""
        for char in encrypted_message:
            decrypted_char = chr(ord(char) - len(self.key))
            decrypted_message += decrypted_char
        return decrypted_message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    password_window = PasswordWindow()
    editor_window = EditorWindow()
    password_window.show()
    sys.exit(app.exec_())
