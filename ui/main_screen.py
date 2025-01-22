from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy
)

from db.database_manager import UserType
from ui.protocols_screen import protocols_screen_1


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
        content_frame = QFrame()
        self.content_layout = QVBoxLayout()
        content_frame.setLayout(self.content_layout)

        self.main_screen()

        main_layout.addLayout(self.header_layout())
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setStyleSheet("color: black;")
        main_layout.addWidget(h_line)
        main_layout.addWidget(content_frame)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def main_screen(self):
        self.clear_content()

        actions_label = QLabel("Dostępne akcje:")
        actions_label.setFont(QFont("Arial", 14))
        self.content_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_actions()
        self.content_layout.setSpacing(20)

    def protocols_screen_1(self):
        self.clear_content()
        container = QWidget()
        container_layout = QHBoxLayout()

        actions_label = QLabel("Dostępne protokoły:")
        actions_label.setFont(QFont("Arial", 14))
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        back_button = QPushButton("Powrót")
        back_button.clicked.connect(self.main_screen)
        container_layout.addWidget(actions_label)
        container_layout.addSpacerItem(spacer)
        container_layout.addWidget(back_button)
        container.setLayout(container_layout)
        self.content_layout.addWidget(container)

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

    def add_actions(self):
        if self.user_role == UserType.INSPECTED:
            self.action_button("Protokoły hospitacji", self.protocols_screen_1)
        elif self.user_role == UserType.INSPECTION_TEAM_MEMBER:
            self.action_button("Protokoły hospitacji", self.protocols_screen_1)
        # elif self.user_role == UserType.ZJK_MEMBER:
        #     self.action_button("Zarządzanie wykazem osób proponowanych do hospitacji", layout)
        else:
            print("No action found for this UserType")


    def action_button(self, text, content):
        button = QPushButton(text)
        button.setStyleSheet("padding: 10px;")
        button.clicked.connect(content)
        self.content_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
