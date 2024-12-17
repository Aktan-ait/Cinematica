# ticket.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class TicketWindow(QWidget):
    finish = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT - Ticket")
        self.setStyleSheet("background-color: #000000;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)

        # Title
        title_label = QLabel("MOVAIT TICKET")
        title_label.setFont(QFont("Calibri", 36, QFont.Bold))
        title_label.setStyleSheet("color: magenta;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Ticket Details
        self.name_label = QLabel("")
        self.movie_label = QLabel("")
        self.time_label = QLabel("")
        self.price_label = QLabel("")
        self.seat_label = QLabel("")

        for label in [
            self.name_label,
            self.movie_label,
            self.time_label,
            self.price_label,
            self.seat_label,
        ]:
            label.setFont(QFont("Calibri", 24))
            label.setStyleSheet("color: white;")
            label.setAlignment(Qt.AlignCenter)
            self.main_layout.addWidget(label)

        # Finish Button
        finish_button = QPushButton("EXIT")
        finish_button.setFont(QFont("Calibri", 18, QFont.Bold))
        finish_button.setStyleSheet(
            """
            QPushButton {
                background-color: red;
                color: white;
                padding: 10px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
            """
        )
        finish_button.clicked.connect(self.finish.emit)
        self.main_layout.addWidget(finish_button)

        self.setLayout(self.main_layout)

    def set_ticket_info(self, ticket_info):
        self.name_label.setText(f"NAME: {ticket_info['name']}")
        self.movie_label.setText(f"MOVIE: {ticket_info['movie']}")
        self.time_label.setText(f"TIME: {ticket_info['time']}")
        self.price_label.setText(f"PRICE: {ticket_info['price']}")
        self.seat_label.setText(f"SEATS: {', '.join(ticket_info['seats'])}")
