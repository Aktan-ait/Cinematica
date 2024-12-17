import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginWindow
from register import RegistrationWindow
from movie_selection import MovieSelectionWindow
from seat_booking import SeatBookingWindow
from movie_history import MovieHistoryWindow
from ticket import TicketWindow
from admin_panel import AdminPanel  
from session import UserSession  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOVAIT Cinema App")
        self.setGeometry(600, 300, 800, 600)

        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        
        self.login_window = LoginWindow()
        self.register_window = RegistrationWindow()
        self.movie_selection_window = MovieSelectionWindow()
        self.seat_booking_window = SeatBookingWindow()
        self.movie_history_window = MovieHistoryWindow()
        self.ticket_window = TicketWindow()
        self.admin_panel = AdminPanel()  

        
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.register_window)
        self.stack.addWidget(self.movie_selection_window)
        self.stack.addWidget(self.seat_booking_window)
        self.stack.addWidget(self.movie_history_window)
        self.stack.addWidget(self.ticket_window)
        self.stack.addWidget(self.admin_panel)  

        
        self.login_window.goto_signup.connect(self.show_register)
        self.login_window.login_success.connect(
            self.show_next_screen
        )  
        self.register_window.registration_success.connect(self.show_login)
        self.movie_selection_window.goto_seat_booking.connect(self.show_seat_booking)
        self.movie_selection_window.goto_history.connect(self.show_movie_history)
        self.movie_selection_window.goto_login.connect(self.show_login)
        self.seat_booking_window.booking_confirmed.connect(self.show_ticket)
        self.seat_booking_window.back.connect(self.show_movie_selection)
        self.ticket_window.finish.connect(self.show_movie_selection)
        self.movie_history_window.back_to_menu.connect(self.show_movie_selection)
        self.admin_panel.logout.connect(self.show_login)  

        
        self.setStyleSheet("background-color: #1E1E2D;color: white;")

        
        self.stack.setCurrentWidget(self.login_window)

    def show_next_screen(self):
        user_session = UserSession()
        if user_session.is_admin:
            self.show_admin_panel()
        else:
            self.show_movie_selection()

    def show_register(self):
        self.stack.setCurrentWidget(self.register_window)

    def show_login(self):
        user_session = UserSession()
        user_session.clear_user()  
        self.stack.setCurrentWidget(self.login_window)

    def show_movie_selection(self):
        self.movie_selection_window.load_movies()
        self.stack.setCurrentWidget(self.movie_selection_window)

    def show_admin_panel(self):
        self.admin_panel.load_movies()
        self.stack.setCurrentWidget(self.admin_panel)

    def show_seat_booking(self, movie):
        self.seat_booking_window.set_movie(movie)
        self.stack.setCurrentWidget(self.seat_booking_window)

    def show_ticket(self, ticket_info):
        self.ticket_window.set_ticket_info(ticket_info)
        self.stack.setCurrentWidget(self.ticket_window)

    def show_movie_history(self):
        self.movie_history_window.load_purchase_history()
        self.stack.setCurrentWidget(self.movie_history_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
