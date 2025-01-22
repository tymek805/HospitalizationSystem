from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy, QTextEdit, QScrollArea
)

from db.database_manager import UserType
# from ui.protocols_screen import protocols_screen_1
from ui.main_componenets import MainLayout
from ui.ui_inpsected import InspectedController


class MainWindow(QWidget):

    def __init__(self, database_manager):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 900, 450)

        self.db_manager = database_manager
        self.user_role = UserType[self.db_manager.get_user_role()]
        self.init_ui()
        self.center()

        self.content_layout: MainLayout

    def init_ui(self):
        main_layout = MainLayout(self.db_manager, self.user_role)
        self.content_layout = main_layout.content_layout

        # self.main_screen()
        if self.user_role == UserType.INSPECTED:
            self.user_controller = InspectedController(self.content_layout, self.db_manager)
        # elif self.user_role == UserType.INSPECTION_TEAM_MEMBER:
        #     self.action_button("Protokoły hospitacji", self.protocols_screen_1, layout)
        # elif self.user_role == UserType.ZJK_MEMBER:
        #     self.action_button("Zarządzanie wykazem osób proponowanych do hospitacji", layout)
        else:
            print("No action found for this UserType")

        self.setLayout(main_layout)

    def main_screen(self):
        self.clear_content()

        container = QWidget()
        container_layout = QVBoxLayout()

        actions_label = QLabel("Dostępne akcje:")
        actions_label.setFont(QFont("Arial", 14))
        container_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.add_actions(container_layout)
        container_layout.setSpacing(20)
        container.setLayout(container_layout)
        container_layout.addStretch()
        self.content_layout.addWidget(container)
        # self.content_layout.setSpacing(20)

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
