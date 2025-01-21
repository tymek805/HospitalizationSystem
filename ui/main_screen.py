from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame
)


class MainWindow(QWidget):
    def __init__(self, database_manager, user):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 900, 450)

        self.database_manager = database_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Content section
        content_frame = QFrame()
        content_layout = QVBoxLayout()

        actions_label = QLabel("Dostępne akcje")
        actions_label.setFont(QFont("Arial", 12))
        protocols_button = QPushButton("Protokoły hospitacji")
        protocols_button.setFixedWidth(300)

        content_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(protocols_button, alignment=Qt.AlignmentFlag.AlignLeft)

        content_frame.setLayout(content_layout)
        content_frame.setStyleSheet("border: 1px solid black; padding: 10px;")

        # Add widgets to the main layout
        main_layout.addLayout(self.header_layout())
        # main_layout.addSpacing(20)
        main_layout.addWidget(content_frame)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def header_layout(self):
        layout = QHBoxLayout()

        header_label = QLabel("Zalogowany jako: Hospitowany")
        header_label.setFont(QFont("Arial", 16))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(header_label)

        user_info_layout = QHBoxLayout()
        user_label = QLabel("Adam Nowak")
        logout_button = QPushButton("Wyloguj")
        user_info_layout.addWidget(user_label)
        user_info_layout.addWidget(logout_button)
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addLayout(user_info_layout)
        return layout
