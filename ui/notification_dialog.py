from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class NotificationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Powiadomienie")
        self.setFixedSize(500, 250)

        main_layout = QVBoxLayout()

        message_text = (
            "Nie wszyscy pracownicy nie hospitowani w terminach podanych w zarządzeniu wewnętrznym zostali wybrani"
        )
        message_label = QLabel(message_text)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setFont(QFont("Arial", 12))
        message_label.setWordWrap(True)

        button_layout = QHBoxLayout()

        continue_button = QPushButton("Kontynuuj")
        back_button = QPushButton("Cofnij")

        continue_button.clicked.connect(self.accept)
        back_button.clicked.connect(self.reject)

        button_layout.addWidget(continue_button)
        button_layout.addWidget(back_button)

        main_layout.addWidget(message_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

