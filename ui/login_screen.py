from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QDialog
)

from ui.main_screen import MainWindow


class LoginDialog(QDialog):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager

        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Zaloguj")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Wprowadź nazwę użytkownika")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wprowadź hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Zaloguj")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Błąd", "Proszę wprowadzić nazwę użytkownika i hasło.")
            return

        user = self.database_manager.login(username, password)
        if user:
            self.open_dashboard(user)
        else:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowe dane logowania.")

    def open_dashboard(self, user):
        self.dashboard = MainWindow(self.database_manager, user)
        self.dashboard.show()
        self.accept()
