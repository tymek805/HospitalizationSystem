from PyQt6.QtWidgets import (
    QWidget, QApplication
)

from db.database_manager import UserType
from ui.main_componenets import MainLayout
from ui.ui_dean import DeanController
from ui.ui_inpsected import InspectedController
from ui.ui_inspection_team_member import InspectionTMController
from ui.ui_zjk_member import ZJKMemberController


class MainWindow(QWidget):

    def __init__(self, database_manager, logout_action):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 900, 450)

        self.content_layout: MainLayout
        self.db_manager = database_manager
        self.logout_action = logout_action
        self.user_role = UserType[self.db_manager.get_user_role()]
        self.init_ui()
        self.center()

    def init_ui(self):
        main_layout = MainLayout(self.db_manager, self.user_role, self.logout_action)
        self.content_layout = main_layout.content_layout

        if self.user_role == UserType.INSPECTED:
            self.user_controller = InspectedController(self.content_layout, self.db_manager)
        elif self.user_role == UserType.INSPECTION_TEAM_MEMBER:
            self.user_controller = InspectionTMController(self.content_layout, self.db_manager)
        elif self.user_role == UserType.ZJK_MEMBER:
            self.user_controller = ZJKMemberController(self.content_layout, self.db_manager)
        elif self.user_role == UserType.DEAN:
            self.user_controller = DeanController(self.content_layout, self.db_manager)
        # elif self.user_role == UserType.HEAD_OF_DEPARTMENT:
        #     pass
        else:
            print("No action found for this UserType")

        self.setLayout(main_layout)

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
