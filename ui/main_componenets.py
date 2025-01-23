from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QSizePolicy, QScrollArea
)


class MainLayout(QVBoxLayout):
    def __init__(self, db_manager, user_role, logout_action):
        super().__init__()
        self.db_manager = db_manager
        self.user_role = user_role
        self.logout_action = logout_action

        content_frame = QFrame()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.content_layout = QVBoxLayout()
        content_frame.setLayout(self.content_layout)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setWidget(content_frame)

        self.addLayout(self.header_layout())
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setStyleSheet("color: black;")
        self.addWidget(h_line)

        self.addWidget(scroll_area)
        # main_layout.addStretch()

    # def logout(self):

    def header_layout(self):
        layout = QHBoxLayout()

        header_label = QLabel(f"Zalogowany jako: {self.user_role.value}")
        header_label.setFont(QFont("Arial", 16))
        header_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(header_label)

        user_info_layout = QHBoxLayout()

        user_label = QLabel(self.db_manager.get_fullname(self.db_manager.logged_user))
        user_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        logout_button = QPushButton("Wyloguj")
        logout_button.clicked.connect(self.logout_action)
        logout_button.setStyleSheet("padding: 10px;")

        user_info_layout.addWidget(user_label)
        user_info_layout.addWidget(logout_button)
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(user_info_layout)
        layout.setContentsMargins(5, 10, 5, 10)
        return layout

class UserController:
    def __init__(self, content_layout):
        self.content_layout = content_layout

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    @staticmethod
    def action_button(text, content, layout, alignment=Qt.AlignmentFlag.AlignTop):
        button = QPushButton(text)
        button.setStyleSheet("padding: 10px;")
        button.clicked.connect(content)
        layout.addWidget(button, alignment=alignment)

    def main_container(self) -> QWidget:
        container = QWidget()
        container_layout = QVBoxLayout()

        actions_label = QLabel("Dostępne akcje:")
        actions_label.setFont(QFont("Arial", 14))
        container_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignTop)

        container_layout.setSpacing(20)
        container.setLayout(container_layout)
        # container_layout.addStretch()
        return container
        # self.content_layout.setSpacing(20)

    def main_screen(self):
        self.clear_content()
        container = self.main_container()
        self.content_layout.addWidget(container)