# seat_booking.py

import datetime
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
import requests

from api import APIClient
from session import UserSession


class SeatBookingWindow(QWidget):
    booking_confirmed = pyqtSignal(dict)
    back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT - Seat Booking")
        self.setStyleSheet("background-color: #1e1e2d;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        # Title
        self.title_label = QLabel("Movie Title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Calibri", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: magenta;")
        self.main_layout.addWidget(self.title_label)

        # Description
        self.description_label = QLabel("Movie Description")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setFont(QFont("Calibri", 16))
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.description_label)

        # Time
        self.time_label = QLabel("Movie Time")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Calibri", 18))
        self.time_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.time_label)

        # Seat Grid
        grid_layout = QHBoxLayout()
        grid_layout.setAlignment(Qt.AlignCenter)

        self.seat_grid = QGridLayout()
        self.seat_grid.setSpacing(10)

        self.seats = {}
        rows = ["A", "B", "C", "D", "E"]
        cols = 13

        for i, row in enumerate(rows):
            row_label = QLabel(row)
            row_label.setFont(QFont("Calibri", 14, QFont.Bold))
            row_label.setStyleSheet("color: white;")
            self.seat_grid.addWidget(row_label, i + 1, 0)

            for col in range(1, cols + 1):
                seat_button = QPushButton()
                seat_button.setFixedSize(40, 40)
                seat_button.setStyleSheet(
                    "background-color: white; border-radius: 10px; border: 1px solid black;"
                )
                seat_button.setCheckable(True)
                seat_button.clicked.connect(self.toggle_seat)
                self.seats[(row, col)] = seat_button
                self.seat_grid.addWidget(seat_button, i + 1, col)

        for col in range(1, cols + 1):
            col_label = QLabel(str(col))
            col_label.setAlignment(Qt.AlignCenter)
            col_label.setFont(QFont("Calibri", 14, QFont.Bold))
            col_label.setStyleSheet("color: white;")
            self.seat_grid.addWidget(col_label, 0, col)

        grid_layout.addLayout(self.seat_grid)
        self.main_layout.addLayout(grid_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)

        buy_button = QPushButton("BUY")
        buy_button.setFont(QFont("Calibri", 20, QFont.Bold))
        buy_button.setStyleSheet(self.style_button("#007bff"))
        buy_button.clicked.connect(self.buy_seats)
        buttons_layout.addWidget(buy_button)

        back_button = QPushButton("BACK")
        back_button.setFont(QFont("Calibri", 20, QFont.Bold))
        back_button.setStyleSheet(self.style_button("#ff4d4d"))
        back_button.clicked.connect(self.back_to_menu)
        buttons_layout.addWidget(back_button)

        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)

    def style_button(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 20px;
        }}
        QPushButton:hover {{
            background-color: {self.lighten_color(color)};
        }}
        """

    def lighten_color(self, color):
        colors = {
            "#007bff": "#66b2ff",
            "#ff4d4d": "#ff9999",
        }
        return colors.get(color, color)

    def set_movie(self, movie):
        self.movie = movie
        self.movie_id = movie["id"]
        self.movie_name = movie["title"]
        self.movie_description = movie.get("description", "")
        self.movie_time = movie.get("time", "Unknown")

        # Format the movie time
        try:
            parsed_time = datetime.datetime.fromisoformat(self.movie_time)
            formatted_time = parsed_time.strftime("%B %d, %Y, %I:%M %p")
        except ValueError:
            formatted_time = self.movie_time  # Use the original if parsing fails

        self.title_label.setText(f"{self.movie_name}")
        self.description_label.setText(f"{self.movie_description}")
        self.time_label.setText(f"{formatted_time}")

        self.load_taken_seats()

    def load_taken_seats(self):
        api_client = APIClient()
        try:
            response = api_client.get(f"/movies/{self.movie_id}/taken_seats")
            if response.status_code == 200:
                taken_seats = response.json()
                self.display_taken_seats(taken_seats)
            else:
                QMessageBox.warning(self, "Error", "Failed to load taken seats.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not load taken seats: {e}")

    def display_taken_seats(self, taken_seats):
        self.reset_seats()  # Reset seat buttons
        # Mark booked seats
        for seat in taken_seats:
            seat_row = seat["seat_row"]
            seat_column = seat["seat_column"]
            btn = self.seats.get((seat_row, seat_column))
            if btn:
                btn.setEnabled(False)
                btn.setStyleSheet(
                    "background-color: gray; border-radius: 10px; border: 1px solid black;"
                )

    def reset_seats(self):
        for seat in self.seats.values():
            seat.setEnabled(True)
            seat.setChecked(False)
            seat.setStyleSheet(
                "background-color: white; border-radius: 10px; border: 1px solid black;"
            )

    def toggle_seat(self):
        button = self.sender()
        if button.isChecked():
            button.setStyleSheet(
                "background-color: green; border-radius: 10px; border: 1px solid black;"
            )
        else:
            button.setStyleSheet(
                "background-color: white; border-radius: 10px; border: 1px solid black;"
            )

    def buy_seats(self):
        selected_seats = [seat for seat, btn in self.seats.items() if btn.isChecked()]
        if not selected_seats:
            QMessageBox.warning(self, "No Seats", "Please select seats to buy.")
            return

        seat_numbers = [f"{s[0]}{s[1]}" for s in selected_seats]
        user_session = UserSession()
        user_id = user_session.user_id

        # Prepare data for the booking
        seats_to_book = [
            {"seat_row": s[0], "seat_column": s[1]} for s in selected_seats
        ]

        api_client = APIClient()
        try:
            response = api_client.post(
                "/bookings",
                json={
                    "user_id": user_id,
                    "movie_id": self.movie_id,
                    "seats": seats_to_book,
                },
            )
            if response.status_code == 201:
                # Mark selected seats as taken
                for seat in selected_seats:
                    btn = self.seats[seat]
                    btn.setEnabled(False)
                    btn.setChecked(False)
                    btn.setStyleSheet(
                        "background-color: gray; border-radius: 10px; border: 1px solid black;"
                    )

                # Prepare ticket information
                ticket_info = {
                    "name": user_session.username,
                    "movie": self.movie_name,
                    "time": self.movie_time,
                    "price": f"{len(seat_numbers) * 300}c",
                    "seats": seat_numbers,
                }
                QMessageBox.information(
                    self,
                    "Purchase Confirmed",
                    f"You have bought seats: {', '.join(seat_numbers)}",
                )
                self.booking_confirmed.emit(ticket_info)
            else:
                error = response.json().get("error", "Failed to book seats.")
                QMessageBox.warning(self, "Error", error)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not connect to server: {e}")

    def back_to_menu(self):
        # Logic to go back to movie selection
        self.back.emit()
