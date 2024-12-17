import datetime
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
from PyQt5 import QtWidgets
import requests

from api import APIClient


class MovieSelectionWindow(QWidget):
    goto_seat_booking = pyqtSignal(dict)  
    goto_history = pyqtSignal()
    goto_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT - Movie Selection")
        self.setStyleSheet("background-color: #1e1e2d; color: white;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        
        title_label = QLabel("MOVAIT")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #ff44ff;")
        self.main_layout.addWidget(title_label)

        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)

        buy_button = QPushButton("BUY")
        buy_button.setStyleSheet(self.style_button("red"))
        buy_button.clicked.connect(self.buy_tickets)
        buttons_layout.addWidget(buy_button)

        history_button = QPushButton("USER HISTORY")
        history_button.setStyleSheet(self.style_button("blue"))
        history_button.clicked.connect(self.goto_history.emit)
        buttons_layout.addWidget(history_button)

        logout_button = QPushButton("LOG OUT")
        logout_button.setStyleSheet(self.style_button("green"))
        logout_button.clicked.connect(self.goto_login.emit)
        buttons_layout.addWidget(logout_button)

        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)

        self.selected_movie = None
        self.movies = []
        self.movie_buttons = []

    def style_button(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            border-radius: 30px;
        }}
        QPushButton:hover {{
            background-color: {self.lighten_color(color)};
        }}
        """

    def lighten_color(self, color):
        colors = {
            "red": "#ff6666",
            "blue": "#6699ff",
        }
        return colors.get(color, color)

    def load_movies(self):
        api_client = APIClient()
        try:
            response = api_client.get("/movies")
            if response.status_code == 200:
                movies = response.json()
                self.display_movies(movies)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load movies.")
        except requests.RequestException as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Could not connect to server: {e}"
            )

    def display_movies(self, movies):
        
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.movies = movies
        self.movie_buttons = []

        for movie in self.movies:
            time_str = movie.get("time", "")
            try:
                parsed_time = datetime.datetime.fromisoformat(time_str)
                formatted_time = parsed_time.strftime("%B %d, %Y, %I:%M %p")
            except ValueError:
                formatted_time = time_str  

            movie_button = QPushButton(f"{movie['title']}   {formatted_time}")
            movie_button.setFont(QFont("Calibri", 18, QFont.Bold))
            movie_button.setStyleSheet(
                """
                QPushButton {
                    background-color: yellow;
                    color: black;
                    font-size: 22px;
                    padding: 10px;
                    border: 1px solid black;
                }
                QPushButton:hover {
                    background-color: #ffcc00;
                }
                """
            )
            movie_button.clicked.connect(lambda checked, m=movie: self.select_movie(m))
            self.scroll_layout.addWidget(movie_button)
            self.movie_buttons.append(movie_button)

    def select_movie(self, movie):
        self.selected_movie = movie
        
        for button, m in zip(self.movie_buttons, self.movies):
            if m["id"] == movie["id"]:
                button.setStyleSheet(
                    button.styleSheet() + "background-color: green; color: white;"
                )
            else:
                button.setStyleSheet(
                    button.styleSheet()
                    .replace("background-color: green;", "background-color: yellow;")
                    .replace("color: white;", "color: black;")
                )

    def buy_tickets(self):
        if self.selected_movie:
            self.goto_seat_booking.emit(self.selected_movie)
        else:
            QtWidgets.QMessageBox.warning(
                self, "No Selection", "Please select a movie."
            )
