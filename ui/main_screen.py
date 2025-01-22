from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QApplication
)

from db.database_manager import UserType


class MainWindow(QWidget):

    def __init__(self, database_manager):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 900, 450)

        self.db_manager = database_manager
        self.user_role = UserType[self.db_manager.get_user_role()]
        self.init_ui()
        self.center()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Content section
        content_frame = QFrame()
        content_layout = QVBoxLayout()

        actions_label = QLabel("Dostępne akcje:")
        actions_label.setFont(QFont("Arial", 14))
        content_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_actions(content_layout)
        content_layout.setSpacing(20)
        content_frame.setLayout(content_layout)

        # Add widgets to the main layout
        main_layout.addLayout(self.header_layout())
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setStyleSheet("color: black;")
        main_layout.addWidget(h_line)
        main_layout.addWidget(content_frame)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def header_layout(self):
        layout = QHBoxLayout()

        header_label = QLabel(f"Zalogowany jako: {self.user_role.value}")
        header_label.setFont(QFont("Arial", 16))
        header_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(header_label)

        user_info_layout = QHBoxLayout()

        user_label = QLabel(self.db_manager.get_user_fullname())
        user_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        logout_button = QPushButton("Wyloguj")
        logout_button.setStyleSheet("padding: 10px;")

        user_info_layout.addWidget(user_label)
        user_info_layout.addWidget(logout_button)
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(user_info_layout)
        layout.setContentsMargins(5, 10, 5, 10)
        return layout

    def add_actions(self, layout):
        if self.user_role == UserType.INSPECTED:
            self.action_button("Protokoły hospitacji", layout)
        elif self.user_role == UserType.INSPECTION_TEAM_MEMBER:
            self.action_button("Protokoły hospitacji", layout)
        elif self.user_role == UserType.ZJK_MEMBER:
            self.action_button("Zarządzanie wykazem osób proponowanych do hospitacji", layout)
        else:
            print("No action found for this UserType")


    def action_button(self, text, layout):
        button = QPushButton(text)
        button.setStyleSheet("border: 1px solid black; padding: 10px;")
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
