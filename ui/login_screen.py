from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QDialog, QApplication
)


class LoginDialog(QDialog):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager

        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

        self.center()

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
            self.accept()
        else:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowe dane logowania.")

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
