from PyQt6.QtWidgets import QSpacerItem

from ui.main_componenets import *

from ui.protocols import Protocols


class InspectionTMController(UserController):
    def __init__(self, content_layout, db_manager):
        super().__init__(content_layout)
        self.db_manager = db_manager
        self.main_screen()

    def main_screen(self):
        self.clear_content()
        container = self.main_container()
        self.action_button("Protokoły hospitacji", self.protocols_screen, container.layout())
        container.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.content_layout.addWidget(container)

    def protocols_screen(self):
        prot = Protocols(self, self.db_manager.get_all_protocols(self.db_manager.logged_user))
        prot.protocols_screen_1()
