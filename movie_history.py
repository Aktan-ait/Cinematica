# movie_history.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
import requests
from PyQt5 import QtWidgets

from api import APIClient
from session import UserSession


class MovieHistoryWindow(QWidget):
    back_to_menu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT - Movie History")
        self.setStyleSheet("background-color: black; color: white;")
        self.purchase_history = []
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        # Title
        title_label = QLabel("MOVAIT")
        title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ff44ff;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        subtitle_label = QLabel("Movie History")
        subtitle_label.setStyleSheet("font-size: 28px; color: white; padding: 10px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(subtitle_label)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Back Button
        back_button = QPushButton("BACK TO MENU")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4444ff;
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #6666ff;
            }
            """
        )
        back_button.clicked.connect(self.back_to_menu.emit)
        self.main_layout.addWidget(back_button)

        self.setLayout(self.main_layout)

    def set_purchase_history(self, purchase_history):
        self.purchase_history = purchase_history
        self.update_history_display()

    def update_history_display(self):
        # Clear previous history
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        if not self.purchase_history:
            no_history_label = QLabel("No purchase history yet.")
            no_history_label.setStyleSheet(
                "font-size: 18px; color: white; padding: 10px;"
            )
            no_history_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(no_history_label)
        else:
            for ticket_info in self.purchase_history:
                movie_layout = QHBoxLayout()

                # Movie Details
                details_label = QLabel(
                    f"🎥 {ticket_info['movie']}\n"
                    f"🪑 Seats: {', '.join(ticket_info['seats'])}\n"
                    f"⏰ Time: {ticket_info['time']}\n"
                    f"💲 Price: {ticket_info['price']}"
                )
                details_label.setFont(QFont("Arial", 18))
                details_label.setStyleSheet(
                    """
                    color: white;
                    padding: 10px;
                    border: 2px solid white;
                    border-radius: 10px;
                    background-color: #333;
                    """
                )
                movie_layout.addWidget(details_label)

                self.scroll_layout.addLayout(movie_layout)

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.load_purchase_history()

    def load_purchase_history(self):
        user_session = UserSession()
        user_id = user_session.user_id

        api_client = APIClient()
        try:
            response = api_client.get(f"/users/{user_id}/bookings")
            if response.status_code == 200:
                bookings = response.json()
                self.purchase_history = bookings
                self.update_history_display()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load bookings.")
        except requests.RequestException as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Could not connect to server: {e}"
            )

    def update_history_display(self):
        # Clear previous history
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        if not self.purchase_history:
            no_history_label = QLabel("No purchase history yet.")
            # (styling code)
            self.scroll_layout.addWidget(no_history_label)
        else:
            for booking in self.purchase_history:
                movie_layout = QHBoxLayout()

                # Movie Details
                details_label = QLabel(
                    f"🎥 {booking['movie_title']}\n"
                    f"🪑 Seat: {booking['seat_row']}{booking['seat_column']}\n"
                    f"⏰ Time: {booking['movie_time']}\n"
                    f"📅 Booking Time: {booking['booking_time']}"
                )
                details_label.setFont(QFont("Arial", 18))
                details_label.setStyleSheet(
                    """
                    color: white;
                    padding: 10px;
                    border: 2px solid white;
                    border-radius: 10px;
                    background-color: #333;
                    """
                )
                movie_layout.addWidget(details_label)

                self.scroll_layout.addLayout(movie_layout)
