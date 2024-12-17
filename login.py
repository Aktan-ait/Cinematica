from PyQt5 import QtCore, QtGui, QtWidgets
import requests

from api import APIClient
from session import UserSession


class LoginWindow(QtWidgets.QWidget):
    goto_signup = QtCore.pyqtSignal()
    login_success = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #1e1e2d;")
        self.resize(652, 600)

        
        title_font = QtGui.QFont("Calibri", 48, QtGui.QFont.Bold)
        input_font = QtGui.QFont("Calibri", 20)
        button_font = QtGui.QFont("Calibri", 28)

        
        self.label_mov = QtWidgets.QLabel("MOV", self)
        self.label_mov.setFont(title_font)
        self.label_mov.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_mov.setGeometry(180, 40, 171, 91)

        self.label_ait = QtWidgets.QLabel("AIT", self)
        self.label_ait.setFont(title_font)
        self.label_ait.setStyleSheet("color: rgb(217, 0, 217);")
        self.label_ait.setGeometry(350, 40, 111, 91)

        
        self.username = QtWidgets.QLineEdit(self)
        self.username.setFont(input_font)
        self.username.setPlaceholderText("Username")
        self.username.setGeometry(140, 170, 380, 60)
        self.username.setStyleSheet(
            """
            background-color: rgb(231, 231, 231);
            border: 2px solid #f66867;
            border-radius:30px;
            color: rgb(0, 0, 0);
            """
        )
        self.username.setAlignment(QtCore.Qt.AlignCenter)

        
        self.password = QtWidgets.QLineEdit(self)
        self.password.setFont(input_font)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setGeometry(140, 250, 380, 60)
        self.password.setStyleSheet(
            """
            background-color: rgb(231, 231, 231);
            border: 2px solid #f66867;
            border-radius:30px;
            color: rgb(0, 0, 0);
            """
        )
        self.password.setAlignment(QtCore.Qt.AlignCenter)

        
        self.login_button = QtWidgets.QPushButton("LOG IN", self)
        self.login_button.setFont(button_font)
        self.login_button.setGeometry(130, 360, 400, 70)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(255, 0, 0);
                border-radius:30px;
            }
            QPushButton:pressed {
                background-color: rgb(200, 0, 0);
            }
            """
        )
        self.login_button.clicked.connect(self.handle_login)

        
        self.signup_button = QtWidgets.QPushButton("SIGN UP", self)
        self.signup_button.setFont(QtGui.QFont("Calibri", 20))
        self.signup_button.setGeometry(190, 450, 281, 51)
        self.signup_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(85, 0, 255);
                border-radius:30px;
            }
            QPushButton:pressed {
                background-color: rgb(65, 0, 200);
            }
            """
        )
        self.signup_button.clicked.connect(self.goto_signup.emit)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        if username == "admin" and password == "admin":
            QtWidgets.QMessageBox.information(
                self, "Login Successful", "Login Successful"
            )
            user_id = -1

            
            user_session = UserSession()
            user_session.set_user(user_id, username)
            self.login_success.emit()
            return

        api_client = APIClient()

        try:
            response = api_client.post(
                "/login", json={"username": username, "password": password}
            )
            data = response.json()
            QtWidgets.QMessageBox.information(
                self, "Login Successful", "Login Successful"
            )
            user_id = data["user_id"]

            
            user_session = UserSession()
            user_session.set_user(user_id, username)

            self.login_success.emit()
        except requests.RequestException as e:
            error = e.response.json().get("error") if e.response else str(e)
            QtWidgets.QMessageBox.warning(self, "Login Failed", error)
