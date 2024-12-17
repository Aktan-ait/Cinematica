from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets
import random
import string

import requests

from api import APIClient


class RegistrationWindow(QWidget):
    registration_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT Registration")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1e1e2d;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignCenter)

        
        title_layout = QHBoxLayout()
        mov_label = QLabel('<span style="color: white;">MOV</span> <span style="color: #ff00ff; font-weight: bold; ">AIT</span>')
        mov_label.setFont(QFont("Calibri", 48, QFont.Bold))
        mov_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        # ait_label = QLabel("AIT")
        # ait_label.setFont(QFont("Calibri", 48, QFont.Bold))
        # ait_label.setStyleSheet("color: #ff00ff;")
        title_layout.addWidget(mov_label)
        # title_layout.addWidget(ait_label)
        self.main_layout.addLayout(title_layout)

        
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        self.username_field.setStyleSheet(self.style_line_edit())
        self.main_layout.addWidget(self.username_field)

        
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet(self.style_line_edit())
        self.main_layout.addWidget(self.password_field)

        self.verify_password_field = QLineEdit()
        self.verify_password_field.setPlaceholderText("Verify Password")
        self.verify_password_field.setEchoMode(QLineEdit.Password)
        self.verify_password_field.setStyleSheet(self.style_line_edit())
        self.main_layout.addWidget(self.verify_password_field)

        
        self.captcha_code = self.generate_captcha()
        self.captcha_label = QLabel(f"CAPTCHA: {self.captcha_code}")
        self.captcha_label.setFont(QFont("Calibri", 16))
        self.captcha_label.setStyleSheet("color: white;")
        self.captcha_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.captcha_label)

        self.captcha_field = QLineEdit()
        self.captcha_field.setPlaceholderText("Enter CAPTCHA")
        self.captcha_field.setStyleSheet(self.style_line_edit())
        self.main_layout.addWidget(self.captcha_field)

        
        register_button = QPushButton("Register")
        register_button.setStyleSheet(self.style_button())
        register_button.clicked.connect(self.handle_registration)
        self.main_layout.addWidget(register_button)

        
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Calibri", 14))
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.message_label)

        self.setLayout(self.main_layout)

    def style_line_edit(self):
        return """
        QLineEdit {
            background-color: #ffffff;
            border: 2px solid #555;
            border-radius: 25px;
            padding: 10px;
            font-size: 18px;
            color: #333;
        }
        QLineEdit:focus {
            border: 2px solid #007bff;
        }
        """

    def style_button(self):
        return """
        QPushButton {
            background-color: #007bff;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
            border-radius: 25px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QPushButton:pressed {
            background-color: #003d80;
        }
        """

    def generate_captcha(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def handle_registration(self):
        username = self.username_field.text().strip()
        password = self.password_field.text()
        verify_password = self.verify_password_field.text()
        captcha_input = self.captcha_field.text().strip()

        self.message_label.clear()

        if not username or not password or not verify_password:
            self.show_message("All fields must be filled.", "red")
            return

        if password != verify_password:
            self.show_message("Passwords do not match.", "red")
            return

        if captcha_input != self.captcha_code:
            self.show_message("Incorrect CAPTCHA.", "red")
            self.captcha_code = self.generate_captcha()
            self.captcha_label.setText(f"CAPTCHA: {self.captcha_code}")
            self.captcha_field.clear()
            self.captcha_field.setFocus()
            return

        api_client = APIClient()

        try:
            response = api_client.post(
                "/register", json={"username": username, "password": password}
            )
            data = response.json()
            QtWidgets.QMessageBox.information(self, "Success", data["message"])
            self.registration_success.emit()
        except requests.RequestException as e:
            error = e.response.json().get("error") if e.response else str(e)
            self.show_message(error, "red")

    def show_message(self, message, color):
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"color: {color}; font-size: 16px;")
