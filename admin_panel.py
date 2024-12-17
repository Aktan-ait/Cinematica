# admin_panel.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QDateTimeEdit,
)
from PyQt5.QtCore import pyqtSignal, QDateTime

import requests
from api import APIClient


class AdminPanel(QWidget):
    logout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setStyleSheet("background-color: #1e1e2d; color: white;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Admin Panel")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff44ff;")
        layout.addWidget(title_label)

        # Movie Title Input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Movie Title")
        self.title_input.setStyleSheet(self.style_line_edit())
        layout.addWidget(self.title_input)

        # Description Input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet(self.style_text_edit())
        layout.addWidget(self.description_input)

        # Time Input
        self.date_time_input = QDateTimeEdit()
        self.date_time_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.date_time_input.setCalendarPopup(True)
        self.date_time_input.setStyleSheet(
            """
            QDateTimeEdit {
                background-color: #333;
                color: white;
                font-size: 24px;
                border-radius: 10px;
                padding: 5px;
            }
            """
        )
        layout.addWidget(self.date_time_input)

        # Add Movie Button
        add_movie_button = QPushButton("Add Movie")
        add_movie_button.setStyleSheet(self.style_button("#28a745"))
        add_movie_button.clicked.connect(self.add_movie)
        layout.addWidget(add_movie_button)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet(self.style_button("#dc3545"))
        logout_button.clicked.connect(self.logout.emit)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def style_line_edit(self):
        return """
        QLineEdit {
            background-color: #26262e;
            color: white;
            border: 1px solid #26262e;
            padding: 10px;
            font-size: 16px;
        }
        """

    def style_text_edit(self):
        return """
        QTextEdit {
            background-color: #26262e;
            color: white;
            border: 1px solid #26262e;
            padding: 10px;
            font-size: 16px;
        }
        """

    def style_button(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 18px;
            padding: 10px;
            border: none;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {self.lighten_color(color)};
        }}
        """

    def lighten_color(self, color):
        # Simple color lightening function
        colors = {"#28a745": "#5ec77d", "#dc3545": "#e66875"}
        return colors.get(color, color)

    def add_movie(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        date_time = self.date_time_input.dateTime().toString("yyyy-MM-ddTHH:mm:ss")

        if not title:
            QMessageBox.warning(self, "Input Error", "Title is required.")
            return

        api_client = APIClient()
        try:
            response = api_client.post(
                "/movies",
                json={
                    "title": title,
                    "description": description,
                    "time": date_time,
                },
            )
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Movie added successfully.")
                # Clear input fields
                self.title_input.clear()
                self.description_input.clear()
                self.date_time_input.setDateTime(QDateTime.currentDateTime())

                # Optionally, refresh movies list or perform other actions...
            else:
                error = response.json().get("error", "Failed to add movie.")
                QMessageBox.warning(self, "Error", error)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not connect to server: {e}")

    def init_seats_for_movie(self, movie_id):
        api_client = APIClient()
        try:
            response = api_client.post(
                f"/movies/{movie_id}/seats/init",
                json={
                    "rows": ["A", "B", "C", "D", "E"],
                    "columns": 13,
                },
            )
            if response.status_code == 201:
                print(f"Seats initialized for movie_id {movie_id}.")
            else:
                print(f"Failed to initialize seats for movie_id {movie_id}.")
        except requests.RequestException as e:
            print(f"Error initializing seats: {e}")

    def load_movies(self):
        # Optional: Implement if you wish to display the list of movies
        pass
